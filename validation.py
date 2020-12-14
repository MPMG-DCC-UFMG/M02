from os import path, devnull, listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import csv
import re
import select_attributes

list_states = ["acre", "ac", "alagoas", "al", "amapá", "ap", "amazonas", "am", "bahia", "ba", "ceará", "ce", "espírito santo", "es", "goiás", "go", "maranhão", "ma", "mato grosso", "mt", "mato grosso do sul", "ms", "minas gerais", "mg", "pará", "pa", "paraíba", "pb", "paraná", "pr", "pernambuco", "pe", "piauí", "pi", "rio de janeiro", "rj", "rio grande do norte", "rn", "rio grande do sul", "rs", "rondônia", "ro", "roraima", "rr", "santa catarina", "sc", "são paulo", "sp", "sergipe", "se", "tocantins", "to", "distrito federal", "df"]

class Validation(object):

	def __init__(self, threshold):
		self.threshold = threshold
		# Automatic select non-listed validated methods
		self.methods = [func for func in dir(Validation) if callable(getattr(Validation, func)) and func.startswith("validate_")]

	def isInvalid(self, df, c):
		if pd.notna(df).sum()/len(df) < self.threshold:
			return True
		if list(df.values).count("")/pd.notna(df).sum() >= self.threshold:
			return True

		invalidated = 0
		for value in df:
			value = str(value).strip()
			if re.fullmatch('^\d{1,5}$', value):
				invalidated = invalidated + 1

		if invalidated/pd.notna(df).sum() >= self.threshold:
			return True

		return False

	def filterData(self, dict_bd_df, verbose=True):
		new_dict_bd_df = dict()
		count_invalid = 0
		for bd, df in dict_bd_df.items():
			df = df.replace(to_replace=r'^#EMPTY$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^\|\|$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^\|\s\|$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'\.00$', value='', regex=True)
			df = df.replace(to_replace=r'\s\s+', value=' ', regex=True)
			df = df.replace(to_replace=r'^\s$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^\|$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^0$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^-1$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^Sem informação$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^NULO$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^$', value=np.nan, regex=True)
			df = df.replace(to_replace=r'^\.$', value=np.nan, regex=True)

			new_dict_bd_df[bd] = dict()
			for c in df.columns:
				if self.isInvalid(df[c], c):
					count_invalid += 1
					continue
				new_dict_bd_df[bd][c] = df[c]

		if verbose:
			print("Discarding null values...")
			print("Discarding empty entries...")
			print("Discarding numbers with less than 5 digits...")
		
		count_all = 0
		for d,df in dict_bd_df.items():
			count_all += len(df.columns)
		
		if verbose:
			print("Invalid columns (attributes): {} out of {} ({:.2f}%)".format(count_invalid,count_all,count_invalid/count_all*100))

		return new_dict_bd_df

	def checkPattern(self, df, column):
		r = None
		# for each validated function
		for f in self.methods:
			# calling the function
			if getattr(Validation, f)(self, df, column):
				# getting the semantic class name
				r = f[f.index("_")+1:]
				break
		return r

	# signature: validate_[NAME_CLASS](self, df, column)

	def validate_corRaca(self, df, column):
		options = set(df.dropna().unique())
		# IBGE: 5 options (brancos, pardos, pretos, amarelos e indígenas)
		if len(options) >1 and len(options) <=6:
			options = [x.lower() for x in options]
			if "branca" in options or "parda" in options or "preta" in options or "branco" in options or "pardo" in options or "preto" in options:
				return True
		return False

	def validate_genero(self, df, column):
		options = set(df.dropna().unique())
		if len(options) >=1 and len(options) <=3:
			options = [x.lower() for x in options]
			if "feminino" in options or "masculino" in options:
				return True
			elif "f" in options and "m" in options:
				return True
			elif ("sexo" in column or "genero" in column) and ("feminino" in options or "masculino" in options or "f" in options or "m" in options):
				return True
		return False

	# Note: not validating "ttuloeleitor" because this column is invalid.
	# For instance, the following examples are wrong: 68109502, 439880302, 446594802, 924152002 and 770794402.
	def validate_tituloEleitor(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			value = str(value).strip()

			try:
				value = int(value)
			except:
				continue

			titulo = str(value)

			# coder: Washington
			if int(titulo) == 0:
				continue

			#Se tiver só números iguais
			if len(set(titulo)) == 1:
				continue

			#0000 0000 XX00 o X demarca a regiao.
			if len(titulo) < 6:
				continue

			# Completa quantidade de digitos
			while len(titulo) < 12:
				titulo = "0"+titulo

			# Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
			inteiros = list(map(int, titulo))
			novo = inteiros[:8]

			#prod = [2, 3, 4, 5, 6, 7, 8, 9]
			prod = list(range(2,10))
			#print(prod)

			dv1 = sum([x*y for (x, y) in zip(novo, prod)]) % 11
			if dv1 == 10:
				dv1 = 0

			#prod = [7, 8, 9]
			prod = list(range(7,10))

			dv2 = sum([x*y for (x, y) in zip(inteiros[8:10]+[dv1], prod)]) % 11
			if dv2 == 10:
				dv2 = 0

			if dv1 == inteiros[-2] and dv2 == inteiros[-1]:
				validated = validated+1

		if validated/size >= self.threshold:
			return True

		return False

	def validate_nis(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			nit = str(value).strip()

			if not (re.fullmatch('^\d{3}\.?\d{5}\.?\d{2}-?\d{1}$', nit)):
				continue

			nit = ''.join(re.findall('\d', str(nit)))

			# Se for zero ja retorna
			if int(nit) == 0 or int(nit) < 100000:
				continue

			#Se tiver só números iguais
			if len(set(nit)) == 1:
				continue

			inteiros = list(map(int, nit))
			novo = inteiros[:10]
			real = inteiros[10]

			prod = list(reversed(range(2,4)))+list(reversed(range(2,10)))

			dv1 = 11-sum([x*y for (x, y) in zip(novo, prod)]) % 11

			if dv1 == 10 or dv1 == 11:
				dv1 = 0

			if dv1 == real:
				validated = validated + 1

		if validated/size >= self.threshold:
			return True

		return False

	def validate_cnsCartorio(self, df, column):
		# CNS = Cadastro Nacional de Serventias Públicas e Privadas do Brasil
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			value = str(value).strip()
			# mask: xx.xxx-x
			if len(value) == 8:
				if re.fullmatch('^\d{2}.\d{3}-\d{1}$', str(value)):
					validated = validated + 1

		if validated/size >= self.threshold:
			return True
		return False

	def validate_dataTempo(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		# datetime
		for value in df:
			value = str(value).strip()
			# mask: date ^(0?[1-9]|[12][0-9]|3[01])(-|\/)((0?[1-9])|(1[0-2]))(-|\/)(\d{2}|\d{4})$
			# 1-1-12 - 01/01/1999
			if len(value) >=6 and len(value) <= 10:
				if re.fullmatch('^(0?[1-9]|[12][0-9]|3[01])(-|\/)((0?[1-9])|(1[0-2]))(-|\/)(\d{2}|\d{4})$', str(value)):
					validated = validated + 1
			# mask: time ^((0|1)?[0-9]|[2][0-3]):([0-5][0-9])(:([0-5][0-9]))?$
			# 1:00 - 23:59:59
			if len(value) >=4 and len(value) <= 8:
				if re.fullmatch('^(0?[1-9]|[12][0-9]|3[01])(-|\/)((0?[1-9])|(1[0-2]))(-|\/)(\d{2}|\d{4})$', str(value)):
					validated = validated + 1
			# mask: datetime ^(0?[1-9]|[12][0-9]|3[01])(-|\/)((0?[1-9])|(1[0-2]))(-|\/)(\d{2}|\d{4})\s((0|1)?[0-9]|[2][0-3]):([0-5][0-9])(:([0-5][0-9]))?$
			#1-1-12 1:00 - 01/01/1999 23:59:59
			if len(value) >=11 and len(value) <= 20:
				if re.fullmatch('^(0?[1-9]|[12][0-9]|3[01])(-|\/)((0?[1-9])|(1[0-2]))(-|\/)(\d{2}|\d{4})\s((0|1)?[0-9]|[2][0-3]):([0-5][0-9])(:([0-5][0-9]))?$', str(value)):
					validated = validated + 1

		if validated/size >= self.threshold:
			return True

		# checking month
		if "mes" == column or column.startswith("mes_"):
			# integer values
			months = set()
			for x in df:
				try:
					value = int(value)
				except:
					continue
				months.add(value)
			
			if len(months) > 0:
				if min(months) >= 1 and max(months) <= 12:
					return True

			# string
			validated = 0
			for x in df:
				if str(x).lower() in ['janeiro', 'fevereiro', 'março', 'maro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro', 'jan', 'fev', 'mar', 'abr', 'maio', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']:
					validated = validated + 1

			if validated/size >= self.threshold:
				return True
	
		# checking year
		if "ano" == column or column.startswith("ano_"):
			# integer values
			validated = 0
			for value in df:
				try:
					value = int(value)
				except:
					continue
				if value >= 1900 and value <= 2099:
					validated = validated + 1

			if validated/size >= self.threshold:
				return True
			
		# checking month-year
		if "mes" == column or column.startswith("mes_") or "ano" == column or column.startswith("ano_"):
			# mask jan/19 dez-2020
			validated = 0
			for value in df:
				value = str(value).strip().lower()
				if len(value) >=6 or len(value) <= 9:
					if re.fullmatch('^(jan|fev|mar|abr|mai|maio|jun|jul|ago|set|out|nov|dez)(\/|-)(19|20)(\d{2})?$', value):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True

			# mask 19/jan 2020-dez
			validated = 0
			for value in df:
				value = str(value).strip().lower()
				if len(value) >=6 or len(value) <= 9:
					if re.fullmatch('^(19|20)(\d{2})?(\/|-)(jan|fev|mar|abr|mai|maio|jun|jul|ago|set|out|nov|dez)$', value):
						validated = validated + 1

			

			if validated/size >= self.threshold:
				return True

		# Special case: month with year
		if ("ano" in column and "mes" in column) or column.startswith("anoems") or column.startswith("anoms") or ("mes" in column and "refer" in column):
			# case 1: mask = YearMonth 2020/1 201406
			validated = 0
			for value in df:
				value = str(value).strip()
				if len(value) ==6 or len(value) ==7:
					if re.fullmatch('^(19|20)\d{2}(-|\/)?(0[1-9]|1[0-2])$', value):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True

			# case 2: mask = MonthYear 07-2014 062016
			validated = 0
			for value in df:
				value = str(value).strip()
				if len(value) ==6 or len(value) ==7:
					if re.fullmatch('^(0[1-9]|1[0-2])(-|\/)?(19|20)\d{2}$', value):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True

			# case 3: mask = Month/Year abr/16
			validated = 0
			for value in df:
				value = str(value).strip()
				if len(value) ==6 or len(value) ==7:
					if re.fullmatch('^(jan|fev|mar|abr|mai|maio|jun|jul|ago|set|out|nov|dez)(\/|-)\d{2}$', value):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True

		# special cases without format
		if column.startswith("dta_") or column.startswith("data_") or column.startswith("dt_"):
			# mask yearMonthDay - 20170927
			validated = 0
			for value in df:
				value = str(value).strip()
				if len(value) ==8:
					if re.fullmatch('^(19|20)\d{2}(0[1-9]|1[0-2])((0[1-9])|((1|2)[0-9]))$', value):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True

		return False

	def validate_endereco_cep(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		if "cep" in column:
			validated = 0
			for value in df:
				value = str(value).strip()
				# mask: 00000-000
				if len(value) ==8 or len(value) == 9:
					if re.fullmatch('^0?\d{5}-?\d{3}$', str(value)):
						validated = validated + 1

			if validated/size >= self.threshold:
				return True
		return False

	def _validate_cnpj(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		# mask: 04.034.872/0001-21
		# String
		validated = 0
		for value in df:
			value = str(value).strip()
			if re.fullmatch('^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', str(value)):
				validated = validated+1

			if validated/size >= self.threshold:
				return True

		# Number
		validated = 0
		for value in df:
			try:
				value = str(int(float(value)))
			except:
				continue

			if int(value) <= 0:
				continue
			#coder: washington
			if len(set(value)) == 1:
				continue

			if len(value) < 3:
				continue

			while len(value) < 14:
				value = "0" + value

			inteiros = list(map(int, value))
			novo = inteiros[:12]

			prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

			while len(novo) < 14:
				r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
				if r > 1:
					f = 11 - r
				else:
					f = 0
				novo.append(f)
				prod.insert(0, 6)
			if novo == inteiros:
				validated = validated+1

		if validated/size >= self.threshold:
			return True
			
		return False

	# TODO
	def _validate_empty(self, df, column):
		not_null = pd.notna(df).sum()
		if len(df) == 0:
			return True
		if not_null/len(df) < self.threshold:
			return True
		return False

	def validate_metadado(self, df, column):
		if "metadata" in column or "meta_data" in column:
			return True
		return False

	def validate_email(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			value = str(value).strip()
			if re.fullmatch('^[a-zA-Z0-9._-]+@([a-zA-Z0-9]+\.)+[a-zA-Za-zA-Z]{1,3}(\.[a-zA-Za-zA-Z]{1,3})?$', str(value)):
				validated = validated+1
		if validated/size >= self.threshold:
			return True
		return False

	def validate_cpfCnpj(self, df, column):	
		return self._validate_cpf(df, column) or self._validate_cnpj(df, column)

	def _validate_cpf(self, df, column):
		size = pd.notna(df).sum()

		if size == 0:
			return False

		# mask: ***.016.001-**
		# mask: 000.123.001-78
		# String
		validated = 0
		for value in df:
			value = str(value).strip()
			if re.fullmatch('^(\d{3}.\d{3}.\d{3}-\d{2}|\*\*\*.\d{3}.\d{3}-\*\*)$', str(value)):
				validated = validated+1

			if validated/size >= self.threshold:
				return True
		
		# number
		validated = 0
		for value in df:
			try:
				value = str(int(float(value)))
			except:
				continue

			if int(value) <= 0:
				continue

			#coder: washington
			if len(set(value)) == 1:
				continue

			if len(value) < 3:
				continue

			while len(value) < 11:
				value = "0" + value

			
			inteiros = list(map(int, value))
			novo = inteiros[:9]

			while len(novo) < 11:
				r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11
				if r > 1:
					f = 11 - r
				else:
					f = 0
				novo.append(f)
			if novo == inteiros:
				validated = validated+1

		if size > 0:
			if validated/size >= self.threshold:
				return True
			
		return False

	#TODO
	def validate_monetaria(self, df, column):
		df_t = df.dropna().unique()
		size = len(df_t)
		if size == 0:
			return False

		# mask xxx,xx
		validated = 0
		for value in df_t:
			value = str(value).strip()
			# mask: 345235,78
			if re.fullmatch('^\d+\,\d{2}$', value):
				validated = validated+1

		if validated/size >= self.threshold:
			return True

		# mask R$ xx.xxx,xx
		validated = 0
		for value in df_t:
			value = str(value).strip()
			# mask: R$ 1.225.423.452.345.235,78
			# mask: 1.225.423.452.345.235,78
			# mask: R$ 345235,78
			# mask: 345235,78
			if re.fullmatch('^((R|r)\$\s?)?\d+(\.\d{3})*?\,\d{2}$', str(value)):
				validated = validated+1

		if validated/size >= self.threshold:
			return True

		# special case: excess decimal places (702,00000 13547,78852 10000,00000 17358,05000 73,00000)
		if column.startswith("valor"):
			validated = 0
			for value in df_t:
				value = str(value).strip()
				if re.fullmatch('^\d+,\d{2}0+$', str(value)):
					validated = validated+1

			if validated/size >= self.threshold:
				return True
		
		return False

	def validate_telefone(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			value = str(value).strip()
			if re.fullmatch('^(\(?0?(\d{2}|xx)?\d{2}\)?\s?)?(\d{4,5}-\d{4})$', str(value)):
				validated = validated+1

		if validated/size >= self.threshold:
			return True
		
		if "telefone" in column or "tel_" in column or "_tel" in column or "fax_" in column or "tel" is column or "tel1" in column:
			df_t = df.dropna().unique()
			size = len(df_t)
			validated = 0
			for value in df_t:
				value = str(value).strip()
				if re.fullmatch('^(\(?0?(\d{2}|xx)?\d{2}\)?\s?)?(\d{4,5}-?\d{4})$', str(value)):
					validated = validated+1

			if validated/size >= self.threshold:
				return True

		if "ddd" == column or "ddd_" in column or "_ddd" in column:
			df_t = df.dropna().unique()
			size = len(df_t)
			validated = 0
			for value in df_t:
				value = str(value).strip()
				if re.fullmatch('^(\(?0?(\d{2}|xx)?\d{2}\)?)?$', str(value)):
					validated = validated+1

			if validated/size >= self.threshold:
				return True

		return False

	def _validate_endereco_logradouro(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			if str(value).strip().lower().startswith(("av. ", "avenida ", "rua ", "r. ", "rodovia ", "via ", "vila ", "vale ")):
				validated = validated + 1

		if validated/size >= self.threshold:
			return True
		return False		

	def validate_endereco_uf(self, df, column):
		size = pd.notna(df).sum()
		if size == 0:
			return False

		validated = 0
		for value in df:
			value = str(value).strip()
			if len(value) <= 19:
				if value.lower() in list_states:
					validated = validated + 1

		if validated/size >= self.threshold:
			return True
		return False

def t_cpf(value):
	try:
		value = str(int(float(value)))
	except:
		return

	if int(value) <= 0:
		return

	#coder: washington
	if len(set(value)) == 1:
		return

	if len(value) < 3:
		return

	while len(value) < 11:
		value = "0" + value
	
	inteiros = list(map(int, value))
	novo = inteiros[:9]

	while len(novo) < 11:
		r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11
		if r > 1:
			f = 11 - r
		else:
			f = 0
		novo.append(f)
	if novo == inteiros:
		print("SIM")
