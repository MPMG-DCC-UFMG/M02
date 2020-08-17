from platform import python_version
from collections import Counter
import pandas as pd
import csv
from os import path
from os import listdir
from os.path import isfile, join
import copy
import re
import numpy as np
from collections import Counter


from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, multilabel_confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from traditionalClassifiers import *
from sklearn.metrics import f1_score
from scipy.stats import t as qt
from imblearn.under_sampling import RandomUnderSampler


import importlib


import sys
import gc
from atributos import *
import argparse
from analises import *
from validacao import *
import random
from datapreprocessor import *

from statistics import harmonic_mean


def arguments():
	#python3 saci.py -d example -t "pulp fiction"
	parser = argparse.ArgumentParser(description='MPMG.')
	parser.add_argument("--mypath", type=str, help='Path of BD', default="bds_stage/") #required=True)
	args = parser.parse_args()

	random.seed(1608637542)
	print(args)
	return args

