import scipy
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import json
import numpy as np
from sklearn import svm
import sys
import traditionalClassifiers
from joblib import dump, load
from datetime import datetime
import time

import warnings
warnings.filterwarnings("ignore")

def train_data(jsonFile, annotationFile, path_out):
	print("Criando o modelo...")
	
	X, y, vectorizer, X_values, X_ids, labeled_idx = get_data(jsonFile, annotationFile)
	X, y = X[labeled_idx], y[labeled_idx]

	classifier = svm.SVC(kernel='linear', C=1, random_state=42)
	classifier.fit(X, y)
	
	print("Salvando o modelo e Vocabulário...")
	outputName = (path_out if path_out.endswith("/") else path_out + "/") + "classifier_" + datetime.now().strftime("%d%m%Y_%H%M%S") + ".joblib"
	dump([classifier, vectorizer.vocabulary_], outputName)
	print("Salvos como'{}'.".format(outputName))

	segmento = "A licitação foi essa"
	X = vectorizer.transform([segmento]).toarray()
	print(classifier.predict(X))

	print("loading")

	
	segmento = "kiu assum biu"
	X = vectorizer.transform([segmento]).toarray()
	print(classifier.predict(X))
	print("Fim")

def loadClassifier(path_model):
	classifier, vocabulary_ = load(path_model)
	pt_stopwords = nltk.corpus.stopwords.words('portuguese')
	vectorizer = CountVectorizer(analyzer='word', stop_words= pt_stopwords, vocabulary=vocabulary_)
	return classifier, vectorizer

def predict(classifier, vectorizer, segmento):
	X = vectorizer.transform([segmento]).toarray()
	return classifier.predict(X)


def predictFile(classifier, vectorizer, fileName, dir_output):
	start_time = time.time()
	print("Processando arquivo '" + fileName + "'")

	if (not os.path.exists(dir_output + fileName[fileName.rfind("/")+1:] + ".csv")):
		fWrite = open(dir_output + fileName[fileName.rfind("/")+1:] + ".csv", 'w')
		
		fRead = open(fileName)
		data = json.load(fRead)
		fRead.close()
		for key, value in data["segmentos"].items():
			for v in value:
				X = vectorizer.transform([v["materia"]]).toarray()
				c = classifier.predict(X)
				fWrite.write(v["id"] + "," + c[0] + "\n")
		fWrite.close()	
		print("Processado - %.2f segundos" % (time.time() - start_time))
	else:
                print("Arquivo já processado: ", fileName)

def evaluate(jsonFile, annotationFile):
	X, y, vectorizer, X_values, X_ids, labeled_idx = get_data(jsonFile, annotationFile)

	X, y = X[labeled_idx], y[labeled_idx]

	clf = svm.SVC(kernel='linear', C=1, random_state=42)
	scores = cross_val_score(clf, X, y, cv=5)

	print("Classification Report (5-folds):")

	print("Accuracy\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='f1_macro')
	print("F1_macro %0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='f1_weighted')
	print("F1_weighted %0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='precision_macro')
	print("Precision_macro\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='recall_macro')
	print("Recall_macro\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))


def data_process(corpus, labels):
    pt_stopwords = nltk.corpus.stopwords.words('portuguese')
    vectorizer = CountVectorizer(analyzer='word', stop_words= pt_stopwords)
    countVector = vectorizer.fit_transform(corpus)
    vectorizer2 = TfidfTransformer(norm='l2', use_idf=False)

    X = scipy.sparse.csr_matrix.todense(vectorizer2.fit_transform(countVector))
    y = np.array(labels) 

    return X, y, vectorizer

def get_data(jsonFile, annotationFile):
    labels = dict()
    file = open(annotationFile, "r")
    for line in file:
        line = line.strip().split("\t")
        labels[line[0]] = line[1]

    file.close()

    X_ids = list()
    X = list()
    y = list()

    labeled_idx = list()
    idx = 0

    with open(jsonFile, 'r') as openfile:
        json_object = json.load(openfile)
    
    for segment in json_object["segments"]:
        ID = segment["id"]
        if len(segment["materia"]) > 60000:
            continue
        X_ids.append(ID)
        X.append(segment["materia"])
        if ID in labels:
            y.append(labels[ID])
            labeled_idx.append(idx)
        else:
            y.append(None)
        idx += 1

    y = np.array(y)
    X_values = np.array(X)
    X_ids = np.array(X_ids)
    
    X, y, vectorizer = data_process(X_values, y)
    
    return X, y, vectorizer, X_values, X_ids, labeled_idx


