from os import path, devnull, listdir
from os.path import isfile, join
from pyhive import hive
from thrift import Thrift
import pandas as pd
import numpy as np
import csv

class Connection(object):

	def __init__(self):
		print("Class Connection - init")
		self.query=None
		self.read_conn=None


	def getHiveConnection(self):	
		print("class Connection - getHiveConnection")
		self.config_db = {
			'host':'xx.xx.x.xx',
            'port':'xxxxx',
            'username':'xxxxxxxx',
            'password':'xxxxxxxx',
            'auth':'xxxxxxxx',
            'database':'xxxxxxxx'
        }
		objHive = hive(**self.config_db)
		return objHive


	def executeQueryDB(self, query):
		with self.read_conn.cursor() as read_cur:
			read_cur.execute(query)
			result_query = read_cur.fetchall()
		self.read_conn.close()
		print (result_query)


	def getTableDB(self, path_db):
		print("class Connection - getTableDB - ", path_db)
		self.read_conn = self.getHiveConnection()
		self.query = 'SHOW TABLES'
		self.executeQueryDB(self.query)


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
	def getColumnDB(self, table, column):
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