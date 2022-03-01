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

import warnings
warnings.filterwarnings("ignore")

def evaluate(jsonFile, annotationFile):

	if not os.path.exists(jsonFile):
		print("Arquivo não existe: '{}'.".format(jsonFile))
		print("Por favor, informar o caminho completo: {} --json <arquivo>".format(sys.argv[0]))
		exit(2)

	if not os.path.exists(annotationFile):
		print("Arquivo não existe: '{}'.".format(annotationFile))
		print("Por favor, informar o caminho completo: {} --labels <arquivo>".format(sys.argv[0]))
		exit(2)

	X, y, X_values, X_ids, labeled_idx = get_data(jsonFile, annotationFile)

	X, y = X[labeled_idx], y[labeled_idx]

	clf = svm.SVC(kernel='linear', C=1, random_state=42)
	scores = cross_val_score(clf, X, y, cv=5)

	print("Classification report (5-folds):")

	print("accuracy\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='f1_macro')
	print("f1_macro %0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='f1_weighted')
	print("f1_weighted %0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='precision_macro')
	print("precision_macro\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))

	scores = cross_val_score(clf, X, y, cv=5, scoring='recall_macro')
	print("recall_macro\t%0.2f\t%0.2f" % (scores.mean(), scores.std()))


def data_process(corpus, labels):
    pt_stopwords = nltk.corpus.stopwords.words('portuguese')
    vectorizer = CountVectorizer(analyzer='word', stop_words= pt_stopwords)
    countVector = vectorizer.fit_transform(corpus)
    vectorizer2 = TfidfTransformer(norm='l2', use_idf=False)

    X = scipy.sparse.csr_matrix.todense(vectorizer2.fit_transform(countVector))
    y = np.array(labels) 

    return X, y

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
    
    X, y = data_process(X_values, y)
    
    return X, y, X_values, X_ids, labeled_idx


