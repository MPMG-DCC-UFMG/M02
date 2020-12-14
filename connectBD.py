from os import path, devnull, listdir
from os.path import isfile, join
from pyhive import hive
import pandas as pd
import numpy as np
import csv

class Connection(object):

	def __init__(self):
		print("Class Connection - init...")
		self.read_conn = None

	def openHiveConnection(self, database):
		print("class Connection - openHiveConnection...")
		try:
			self.config_db = {'host':'*****', 'port':'*****', 'username':'*****', 'password':'*****', 'auth':'*****'}
			self.config_db.update({'database': database})
			#print("self.config_db", self.config_db)
			self.read_conn = hive.connect(**self.config_db)
			if self.read_conn is None:
					print("Hive connection failed!")
					exit(2)
			else:
					print ("Hive connection is working. DB = ", database)
		except:
			print("Hive connection failed!")
			exit(2)

	def closeHiveConnectin(self):
		print("class Connection - closeHiveConnectin...")
		try:
			self.read_conn.close()
		except:
			print("Hive connection coould not close correctly...")
			exit(2)

	def executeQueryDB(self, query):
		print("class Connection - executeQueryDB...")
		with self.read_conn.cursor() as read_cur:
			read_cur.execute(query)
			result_query = read_cur.fetchall()
		return result_query

	def showTablesQuery(self):
		return 'SHOW TABLES'

	def selectColumnQuery(self, table_name, column_name):
		return 'SELECT ' + str(column_name) + ' FROM ' + str(table_name)

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

	def getColumnsDB(self, pathname, table, columns):
		try:
				df = pd.read_csv(f"{pathname}{table}",dtype=str)
		except:
				print("Cannot read file: {}{}".format(pathname,table))
				exit(2)

		for c in columns:
				if c not in df:
						print("Column/attribute '{}' not found at table '{}'".format(c,table))
						exit(2)

		dict_tab_df = dict()
		dict_tab_df[table] = dict()
		if len(columns) != 0:
				dict_tab_df[table] = df[columns]
		else:
				dict_tab_df[table] = df

		return dict_tab_df

	def getColumnsDB2(self, database, table, columns):
		#print("getColumnDB2 - database name..: ", database)
		self.openHiveConnection(database)

		#print(self.executeQueryDB(self.showTablesQuery())) #test
		tableColumns = self.executeQueryDB('SHOW COLUMNS FROM ' + str(table))
		dfColumns = pd.DataFrame(tableColumns, dtype=str, columns=['Columns'])
		columnList = dfColumns['Columns'].values.tolist()

		if len(columns)!=0:
			
			if len(set(columnList).intersection(set(columns))) <= 0:
				print("Column/attribute '{}' not found at table '{}'".format(columns[0],table))
				exit(2)
	
			columnList=None
			columnList=columns	
	
		dict_tab_df = dict()
		dict_tab_df[table] = dict()		
		dict_columns = dict()
		
		for col in columnList: 
			query_result = self.executeQueryDB('SELECT ' + str(col) + ' FROM ' + str(table))
			dfCol = pd.DataFrame(query_result, dtype=str, columns=[str(col)])
			dict_columns[col]=list(dfCol[col])
				
				
		df_merge_col = pd.DataFrame(dict_columns, dtype=str)

		dict_tab_df[table] = df_merge_col
		return dict_tab_df
