from os import path, devnull, listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import csv
import re
import validation
import connectBD
import select_attributes
import traditionalClassifiers
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
import re
import unicodedata
import inflect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, multilabel_confusion_matrix
import sys, os
from joblib import dump, load
from datetime import datetime

def train_data(pathname, threshold, path_out):
	validate = validation.Validation(threshold)

	bd = connectBD.Connection()

	bd.getTableDB(pathname)

	# Phase 1: filtering the data
	print("Phase 1: Filtering the data...")
	# dict[database][column] = DataFrame
	dict_bd_column_df = validate.filterData(bd.readFilesDB(pathname))

	# Phase 2: detecting pattern
	print("Phase 2: Detecting patterns...")
	y_true = list() # ground-truth classes
	y_pred = list() # predicted classes
	dict_bd_column_true = dict() # manual labeled
	dict_bd_column_pred = dict() # predicted by pattern

	# TODO: to remove - only for checking the results
	dict_bd_column_examples = dict() # examples

	# dict[column] = class
	column_class = select_attributes.getAnnotatedColumns()
	noClass_columns = set()

	for bd,column_df in dict_bd_column_df.items():
		dict_bd_column_true[bd] = dict()
		dict_bd_column_pred[bd] = dict()
		for column,df in column_df.items():
			if column not in column_class:
				noClass_columns.add(column)

			pred = validate.checkPattern(df,column)
			if pred is None:
				pred = "nenhuma"
			y_pred.append(pred)
			dict_bd_column_pred[bd][column] = pred

			if column in column_class:
				y_true.append(column_class[column])
				dict_bd_column_true[bd][column] = column_class[column]
			else:
				y_true.append("nenhuma")
				dict_bd_column_true[bd][column] = "nenhuma"
			
			# TODO: to remove - only for checking the results
			instances = ""
			n_instances = 1
			c = column
			if len(df.unique()) > 0:
				for value in df.unique():
					instances = instances + str(value) + "#"
					if n_instances == 5:
						break
					n_instances = n_instances + 1
			if bd not in dict_bd_column_examples:
				dict_bd_column_examples[bd] = dict()
			dict_bd_column_examples[bd][column] = instances

	# Results of the automatic pattern checking
	#print(classification_report(y_true, y_pred))

	# Phase 3: predicting classes
	print("Phase 3: Trainning the classifier...")
	# Selecting columns that need to be trained
	columns_SVM = set()
	for cl,d in dict(classification_report(y_true, y_pred, output_dict=True, zero_division=0)).items():
		if type(d) is dict:
			if d['f1-score'] < threshold and d['support'] != 0:
				columns_SVM.update(select_attributes.getAnnotatedColumn(cl))
		else:
			break

	columns_SVM.update(noClass_columns)

	# Assigning the class of the subclasses
	for c,cl in column_class.items():
		column_class[c] = cl if "_" not in cl else cl[:cl.index("_")]

	X, y, vectorizer = get_X_and_y(dict_bd_column_df, columns_SVM, column_class)
	
	classifier = build_model(X, y)

	y_pred, y_true = y_predict(vectorizer, classifier, dict_bd_column_df, columns_SVM, column_class)
	
	print("Saving Model and Vocabulary...")
	outputName = (path_out if path_out.endswith("/") else path_out + "/") + "classifier_" + datetime.now().strftime("%d%m%Y_%H%M%S") + ".joblib"
	dump([classifier, vectorizer.vocabulary_], outputName)
	print("Objects saved as '{}'.".format(outputName))

	#print(classification_report(y_true, y_pred))

	index = 0
	for bd,column_df in dict_bd_column_df.items():
		for c in column_df:
			if c in columns_SVM:
				# If it is not a false positive, then update it
				if dict_bd_column_pred[bd][c] is "nenhuma":
					dict_bd_column_pred[bd][c] = y_pred[index]
				index += 1

	y_true = list() # ground-truth classes
	y_pred = list() # predicted classes
	for bd,column_df in dict_bd_column_pred.items():
		for c in column_df:
			cl = dict_bd_column_pred[bd][c]
			y_pred.append(cl if "_" not in cl else cl[:cl.index("_")])
			cl = dict_bd_column_true[bd][c]
			y_true.append(cl if "_" not in cl else cl[:cl.index("_")])

	# TODO: to remove - only for checking the results
	f_write = open("output_checkingData.tsv", "w")
	f_write.write("column\tmanual\tpredita\tnum_DB\tinstances\n")
	for bd,column_df in dict_bd_column_pred.items():
		for c in column_df:
			f_write.write("{}\t{}\t{}\t{}\t{}\n".format(c,"nenhuma" if c not in column_class else column_class[c],dict_bd_column_pred[bd][c],bd,dict_bd_column_examples[bd][c]))
	f_write.close()

	print("Classification report:")
	print(classification_report(y_true, y_pred))

def test_data(table, column, filename, threshold):
	validate = validation.Validation(threshold)

	bd = connectBD.Connection()
	
	# dict[database][column] = DataFrame
	dict_bd_column_df = validate.filterData(bd.getColumnDB(table, column), verbose=False)

	dict_bd_column_df_pred = dict()
	for db in dict_bd_column_df:
		dict_bd_column_df_pred[db] = dict()

	# Test automatic detection
	flag_SVM = False
	for bd,column_df in dict_bd_column_df.items():
		for c in column_df:
			pred = validate.checkPattern(column_df[column], column)
			if pred is None:
				flag_SVM = True
			else:
				dict_bd_column_df_pred[db][c] = pred

	# SVM predict: if at least one column needs to be predict
	if flag_SVM:
		try:
			classifier, vocabulary_ = load(filename)
		except:
			print("Saved model not loaded (filename as '{}')".format(filename))
			print("Please, train the entire data: python3.6 {} --train".format(sys.argv[0]))
			exit(2)

		vectorizer = getVectorizer(dict_bd_column_df, vocabulary_)

		for bd,column_df in dict_bd_column_df.items():
			for c in column_df:
				if c not in dict_bd_column_df_pred[db]:
					df = pre_processing(column_df[c])
					doc = vectorizer.transform(list(set(df)))
					dict_bd_column_df_pred[db][c] = np.unique(classifier.predict(doc), return_counts=True)[0][0]

	return dict_bd_column_df_pred

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def get_X_and_y(dict_bd_column_df, columns_SVM, column_class):
	df = dict()
	for c in columns_SVM:
		df[c] = []
	
	X = []
	y = []
	for bd,column_df in dict_bd_column_df.items():
		for c in column_df:
			if c in columns_SVM:
				cl = "nenhuma"
				if c in column_class:
					cl = column_class[c]
				y = y + [cl,]*len(column_df[c])
				p_df = pre_processing(pd.DataFrame(column_df[c], columns=[c]))
				X = X + list(p_df[c])

	y = np.asarray(y)

	vectorizer = TfidfVectorizer()
	vectorizer.fit(X)
	X = vectorizer.transform(X)

	return X, y, vectorizer

#aki
def getVectorizer(dict_bd_column_df, vocabulary):
	X = []
	for bd,column_df in dict_bd_column_df.items():
		for c in column_df:
			p_df = pre_processing(pd.DataFrame(column_df[c], columns=[c]))
			X = X + list(p_df[c])

	vectorizer = TfidfVectorizer(vocabulary=vocabulary)
	vectorizer.fit(X)
	return vectorizer

def build_model(X, y):
	#t_init = time.time()
	skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
	#self.micro_in_train = []
	#self.macro_in_train = []

	classinfo = {
			"name_class": "lsvm",
			"cv": 10,
			'n_jobs': -1,
			"max_iter": 1000000,
		}
	classifier = traditionalClassifiers.TraditionalClassifier(classinfo)

	for train_index, test_index in skf.split(X, y):
		print("TRAIN:", train_index, "TEST:", test_index)
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]

		rus = RandomUnderSampler(random_state=42,sampling_strategy="majority")
		#rus = RandomUnderSampler(random_state=42)
		X_train, y_train = rus.fit_resample(X_train, y_train)

		
		classifier.fit(X_train, y_train)

		y_pred = classifier.predict(X_test)

		micro = f1_score(y_true=y_test, y_pred=y_pred, average='micro')
		macro = f1_score(y_true=y_test, y_pred=y_pred, average='macro')
		print("F1-Score")
		print("\tMicro: ", micro)
		print("\tMacro: ", macro)
		
		#self.micro_in_train.append(micro)
		#self.macro_in_train.append(macro)
		
		break
	#self.time_to_generate = time.time() - t_init

	return classifier

def y_predict(vectorizer, classifier, dict_bd_column_df, columns_SVM, column_class):
	y_pred = list()
	y_true = list()

	blockPrint()
	for bd,column_df in dict_bd_column_df.items():
		for c in column_df:
			if c in columns_SVM:
				cl = "nenhuma"
				if c in column_class:
					cl = column_class[c]

				df = pre_processing(column_df[c])
				doc = vectorizer.transform(list(set(df)))
				y_pred.append(np.unique(classifier.predict(doc), return_counts=True)[0][0])
				y_true.append(cl)

	enablePrint()

	return y_pred, y_true

def pre_processing(df):
	p = inflect.engine()
	replace_patterns = [
		(r'[\(\)\"\/\.\-\~\º\'\;\,]'," "),
		('s.a', 'sa'),
		('s/a', 'sa')]
	for i in range(1,21):
		for pre, pos in [('(\D)','(\D)'), ('^','(\D)'), ('(\D)','$')]:
			pattern = pre + '\d'*i + pos
			replace = ' p' + p.number_to_words(i) + 'd '
			replace_patterns.append((pattern, replace))
	replace_patterns += [('\d+', 'parsedd')]
	#replace_patterns

	compiled_replace_patterns = [(re.compile(p[0]), p[1]) for p in replace_patterns]

	if isinstance(df, pd.Series):
		df = df.map(str)
		df = df.map(str.lower)
		df = df.map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore'))

		for pattern, replace in compiled_replace_patterns:
			df = df.map(lambda x: re.sub(pattern, replace,x).rstrip() )
	
		df = df.map(lambda x: re.sub(r" +", r" ", x).rstrip())
	else:
		df = df.applymap(str)
		df = df.applymap(str.lower)
		df = df.applymap(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore'))

		for pattern, replace in compiled_replace_patterns:
			df = df.applymap(lambda x: re.sub(pattern, replace,x).rstrip() )
	
		df = df.applymap(lambda x: re.sub(r" +", r" ", x).rstrip())

	return df