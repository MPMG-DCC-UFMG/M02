
from sklearn import svm, ensemble
import numpy as np
#from xsklearn.ensemble import Broof, Bert
#from xsklearn.neighbors import LazyNNRF
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


base_estimators = {
	'svm': svm.SVC(),
	'svmrbf': svm.SVC(),
	'lsvm': svm.LinearSVC(),
	'rf': ensemble.RandomForestClassifier(),
	#'broof': Broof(),
	#'bert': Bert(),
	'nb': MultinomialNB(),
	'knn': KNeighborsClassifier(),
	#'cd': LazyNNRF(),
	'lr': LogisticRegression()
}

default_params = {
	'svm': 	{'kernel': 'linear', 'C': 1, 'verbose': False, 'probability': False,
			 'degree': 3, 'shrinking': True, 
			 'decision_function_shape': None, 'random_state': None, 
			 'tol': 0.001, 'cache_size': 25000, 'coef0': 0.0, 'gamma': 'auto', 
			 'class_weight': None,'random_state':1608637542},#,'max_iter':-1},
#			 'max_iter':1000000},
	'svmrbf': 	{'kernel': 'rbf', 'C': 1, 'verbose': False, 'probability': False,
			 'degree': 3, 'shrinking': True, 'max_iter': -1, 
			 'decision_function_shape': None, 'random_state': None, 
			 'tol': 0.001, 'cache_size': 1000, 'coef0': 0.0, 'gamma': 'auto', 
			 'class_weight': None},
	'lsvm': {'loss': 'squared_hinge', 'C': 1, 'verbose': False, 'intercept_scaling': 1,
			 'fit_intercept': True, 'max_iter': 1000, 'penalty': 'l2',
			 'multi_class': 'ovr', 'random_state': None, 'dual': False, 
			 'tol': 0.001, 'class_weight': None},
	'rf':  	{'warm_start': False, 'oob_score': False, 'n_jobs': 1, 'verbose': 0,
			 'max_leaf_nodes': None, 'bootstrap': True, 'min_samples_leaf': 1,
			 'n_estimators': 200, 'min_samples_split': 2,
			 'min_weight_fraction_leaf': 0.0, 'criterion': 'gini', 
			 'random_state': None, 'max_features': 'auto', 'max_depth': None, 
			 'class_weight': None},
#	'broof':{'warm_start': False, 'n_jobs': 1, 'verbose': 0, 'n_iterations': 200,
#			 'max_leaf_nodes': None, 'learning_rate': 1, 'n_trees': 10, 
#			 'min_samples_leaf': 1, 'min_samples_split': 2, 
#			 'min_weight_fraction_leaf': 0.0, 'criterion': 'gini', 
#			 'random_state': None, 'max_features': 'auto', 'max_depth': None, 
#			 'class_weight': None},
#	'bert': {'warm_start': False, 'n_jobs': 1, 'verbose': 0, 'n_iterations': 200,
#			 'max_leaf_nodes': None, 'learning_rate': 1, 'n_trees': 8, 
#			 'min_samples_leaf': 1, 'min_samples_split': 2, 
#			 'min_weight_fraction_leaf': 0.0, 'criterion': 'entropy', 
#			 'random_state': None, 'max_features': 'auto', 'max_depth': None, 
#			 'class_weight': None},
	'nb': 	{'alpha':1.0, 'fit_prior':True, 'class_prior': None},
	'knn': 	{'n_neighbors': 30, 'weights': 'uniform', 'algorithm': 'auto', 'leaf_size': 30,#30, 
			 'p':2, 'metric':'minkowski', 'metric_params':None, 'n_jobs': -1},
#	'lazyrf':	{'warm_start': False, 'n_neighbors': 200, 'n_gpus': 0, 'n_jobs': 1,
#			 'verbose': 0, 'max_leaf_nodes': None, 'bootstrap': True,
#			 'oob_score': False, 'min_samples_leaf': 1, 'n_estimators': 200, 
#			 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 
#			 'criterion': 'gini', 'random_state': None, 'max_features': 'auto',
#			 'max_depth': None, 'class_weight': None},
	'lr':{'penalty': 'l2', 'dual': False, 'tol': 0.0001, 'C': 1.0, 'fit_intercept': True, 
			 'intercept_scaling': 1, 'class_weight': None, 'random_state': None, 'solver': 'warn', 
			 'max_iter': 100, 'multi_class': 'warn', 'verbose': 0, 'warm_start': False, 'n_jobs': -1, 'l1_ratio':None},
		}

default_tuning_params = {
	'svm': 	[{'C': 2.0 ** np.arange(-5, 15, 2)}],
	'svmrbf': 	[{'C': 2.0 ** np.arange(-5, 15, 2)}],
	'lsvm': [{'C': 2.0 ** np.arange(-5, 9, 2)}],
	'rf': [{'criterion': ['entropy', 'gini'], 'n_estimators': [100,200], 'max_features': ['sqrt', 'log2', 0.08, 0.15, 0.30]}],
	#'broof': [{'n_trees': [5], 'n_iterations': [50], 'max_features': [0.08]}],
	#'bert': [{'n_trees': [8], 'n_iterations': [200]}],
	'nb': [{'alpha': [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]}],
	#'knn': [{'weights':['uniform','distance'],'n_neighbors': [3,5,10,20,30]}], #,200,500
	'knn': [{'weights':['uniform','distance'],'n_neighbors': [10, 25, 50, 75, 100]}],#, 200, 500]}], #,200,500  cosine, euclidean, manhattan ????
	#'knn': [{'weights':['uniform','distance'],'n_neighbors': [25,30,35]}], #,200,500
	#'lazyrf': [{'n_neighbors': [30, 100, 200, 500], 'criterion': ['gini'], 'n_estimators': [100], 'max_features': ['sqrt']}],
	'lr': [{'penalty' : ['l1', 'l2'], 'C' : np.logspace(-4, 4, 12), 'solver' : ['liblinear']}]
	}







