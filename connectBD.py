from os import path, devnull, listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import csv

class Connection(object):

	#TODO
#	def __init__(self):
#		print("TODO: class Connection - init")

	def readFilesDB(self, path_bd):
		print("Reading the database files...")
		dict_bd_df = dict()
		tables = [f for f in listdir(path_bd) if isfile(join(path_bd, f)) and not f.endswith('.tar.gz') and not f.endswith('.tmp')]
		for table in tables:
			try:
				dict_bd_df[table] = pd.read_csv(f"{path_bd}/{table}",dtype=str)
			except:
				print("Cannot read file: {}/{}".format(path,table))
				print("Please, inform the properly path of the data: python3.6 {} --train --path <pathname>".format(sys.argv[0]))
				exit(2)
		print("Valid tables (databases): {}.".format(len(dict_bd_df)))
		return dict_bd_df

	# TODO: get data from the database
	def getColumnDB(self, pathname, table, column):
		dict_bd_df = dict()
		try:
			df = pd.read_csv(f"bds_stage/{table}",dtype=str)
		except:
			print("Cannot read file: bds_stage/{}".format(table))
			exit(2)
		
		dict_bd_df = dict()
		# Filtering columns
		dict_bd_df[table] = df[[column]]
		return dict_bd_df
