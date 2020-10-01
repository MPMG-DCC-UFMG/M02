from platform import python_version
from collections import Counter
import pandas as pd
import csv
from os import path, devnull, listdir
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
from datetime import datetime


def arguments():

	parser = argparse.ArgumentParser(description='MPMG.')
	parser.add_argument("--mypath", type=str, help='Path of BD', default="bds_stage/") #required=True)
	# O default sera somente realizar os teste nos datasets presentes no mypath
	parser.add_argument("--train", type=int, default=0) #required=True)
	parser.add_argument("--test", type=int, default=1) #required=True)
	parser.add_argument("--dovalidable", type=int, default=1) #required=True)
	parser.add_argument("--outputdir", type=str, default="model/") #required=True)
	parser.add_argument("--control",type=str,default=datetime.now().strftime("%d%m%Y_%H%M%S"))
	parser.add_argument("--treined",type=str,default="")
	args = parser.parse_args()

	random.seed(1608637542)
	print(args)
	return args

# Disable
def blockPrint():
    sys.stdout = open(devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
