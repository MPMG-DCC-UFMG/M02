

# importando pacotes
from packages import *
from joblib import dump, load
import json

class MPMGFinder(object):
	"""docstring for Finder"""
	def __init__(self, args):
		self.args = args
		#set_atributes_packages()
		self.mypath = args.mypath
		self.classe = {}
		self.classe['nome'] = 0
		self.classe['endereco'] = 1
		
		self.classe['cpf_cnpj'] = 2
		self.classe['email'] = 3
		self.classe['titulo'] = 4
		self.classe['nis'] = 5

		self.classe["naoconsiderar"] = 6

		self.finded = {}
		
		
	def set_onlybds(self):
		self.onlybds = [f for f in listdir(self.mypath) if isfile(join(self.mypath, f)) and f != '.tar.gz' and f != '.tmp']
		print(len(self.onlybds))

	def set_annoted_atributes(self):
		self.annoted_atributes = {}
		self.annoted_atributes["email"] = set_email 
		self.annoted_atributes["titulo"] = set_titulo_eleitor
		self.annoted_atributes["nis"] = set_nis 
		self.annoted_atributes["cpf_cnpj"] = set_cpf_cnpj 
		self.annoted_atributes["rg"] = set_rg 
		self.annoted_atributes["tel"] = set_telefone 
		self.annoted_atributes["endereco"] = set_endereco_logradouro_completos_edemais.union(\
											set_endereco_bairro).union(\
											#set_endereco_cep).union(\
											set_endereco_cidade).union(\
											set_endereco_uf)
		self.annoted_atributes["nome"] = set_nome.union(\
											set_nome_empresa).union(\
											set_nome_orgao_publico).union(\
											set_nome_pessoal)
		#print(self.annoted_atributes["nome"])
		# todos
		self.all_atributes = self.annoted_atributes["nome"].union(\
											self.annoted_atributes["endereco"]).union(\
											self.annoted_atributes["email"]).union(\
											self.annoted_atributes["titulo"]).union(\
											self.annoted_atributes["nis"]).union(\
											self.annoted_atributes["cpf_cnpj"])

	def set_classes_nao_consideradas(self):
		#self.a_remover = set()
		self.atributos_nao_considerados = set()
		for bd in self.onlybds:
			df = pd.read_csv(f"{self.mypath}/{bd}")
			for c in df.columns:
				if "data" in c:
					self.atributos_nao_considerados.add(c)
			
			result = df.applymap(valida_a_remover).sum() / df.notna().sum()
	   
			for c in result[result > 0.70].index:
				#nao remover ddd e cpf
				if 'ddd' in c or 'cpf' in c:
					continue
				self.atributos_nao_considerados.add(c)


	def set_distinct_atributes(self):
		self.distinct_atributes = []
		for bd in self.onlybds:
			#print(onlybds[i])
			df = pd.read_csv(f"{self.mypath}/{bd}",nrows=1)
			self.distinct_atributes += list(df.columns)
			del df
		self.distinct_atributes = list(sorted(list(set(self.distinct_atributes))))
		#print(len(set(self.distinct_atributes)))
		#print(self.distinct_atributes)

	def set_atributes_to_consider(self):
		#self.atributes_to_consider_in_validable_search = [a for a in set(self.distinct_atributes) if a not in self.atributos_nao_considerados]
		self.atributes_to_consider = list(sorted([a for a in set(self.distinct_atributes) if a not in self.atributos_nao_considerados]))
		#print(len(self.atributes_to_consider_in_validable_search))


	def get_set_of_atributes(self, df, classe, limiar=0.70):
		seta = set()
		
		if classe == 'cpf':
			func = validar_cpf
		if classe == 'cnpj':
			func = validar_cnpj
		if classe == 'email':
			func = validar_email
		if classe == 'titulo':
			func = validar_titulo
		if classe == 'nis':
			func = validar_nit
		
		for c in df.columns:
			if classe in c:
				seta.add(c)
			
		df_notna_sum = df.notna().sum()
		result = df.applymap(func).sum() / df_notna_sum
		for c in result[result > limiar].index:
			seta.add(c)
			#print(c)
		return seta

	def find_validable_class(self):
		self.cpf_cnpf_finded = set()
		self.nis_finded = set()
		self.email_finded = set()
		self.titulo_finded = set()

		for bd in self.onlybds:
			df = pd.read_csv(f"{self.mypath}/{bd}")
			columns = [x for x in df.columns if x not in self.atributos_nao_considerados]
			df = df[columns]
			df = df.applymap(str)
			
			
			#Um a mais
			self.cpf_cnpf_finded = set.union(self.cpf_cnpf_finded,self.get_set_of_atributes(df, 'cpf'))
			self.cpf_cnpf_finded = set.union(self.cpf_cnpf_finded,self.get_set_of_atributes(df, 'cnpj'))
				
			#Ta falando correio eletronico
			self.email_finded  = set.union(self.email_finded,self.get_set_of_atributes(df, 'email'))
			
			#ta ok
			self.titulo_finded = set.union(self.titulo_finded,self.get_set_of_atributes(df, 'titulo'))
			
			# Tem diferença tambem
			self.nis_finded  = set.union(self.nis_finded ,self.get_set_of_atributes(df, 'nis'))

		self.finded['cpf_cnpj'] = self.cpf_cnpf_finded 
		self.finded['email'] = self.email_finded 
		self.finded['titulo'] = self.titulo_finded 
		self.finded['nis'] = self.nis_finded 
		
		self.all_validable_finded = self.cpf_cnpf_finded.union(self.email_finded).union(self.titulo_finded).union(self.nis_finded)


	def validate_to_remove(self):
		tmp = copy.copy(self.atributos_nao_considerados)
		for a in tmp:
			if a in self.cpf_cnpf_finded or  a in self.nis_finded or a in self.email_finded or a in self.titulo_finded \
			or a in self.annoted_atributes["nome"] or a in self.annoted_atributes["endereco"]:
				print(a)
				#print(type(self.atributes_to_consider))
				self.atributes_to_consider.append(a)
				self.atributos_nao_considerados.remove(a)
   
	def set_y_true(self):
		self.y_true = np.zeros(len(self.atributes_to_consider),dtype=int)
		self.y_true[self.y_true == 0] = self.classe["naoconsiderar"]

		for a in self.annoted_atributes["cpf_cnpj"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['cpf_cnpj']
		for a in self.annoted_atributes["email"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['email']
		for a in self.annoted_atributes["titulo"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['titulo']
		for a in self.annoted_atributes["nis"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['nis']
		for a in self.annoted_atributes["nome"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['nome']
		self.annoted_atributes["endereco"].remove("agncia")
		for a in self.annoted_atributes["endereco"]:
			self.y_true[self.atributes_to_consider.index(a)] = self.classe['endereco']

	def get_set_of_docs(self,classe):
		docs = []
		for bd in self.onlybds:
			df = pd.read_csv(f"{self.mypath}/{bd}")
			if classe == "nome":
				colunas = [c for c in df.columns if c in self.annoted_atributes["nome"]]
			if classe == 'endereco':
				colunas = [c for c in df.columns if c in self.annoted_atributes["endereco"]]
			if classe == 'naoconsiderar':
				colunas = [c for c in df.columns if c in self.atributos_nao_considerados]                                                                    
			if colunas == []:
				continue        
			#if len(colunas) > 1:
			for c in colunas:
				#print(colunas)
				#print(df[c][df[c].notna()])
				#exit()
				docs += list(map(str,df[c][df[c].notna()].values))
			#break
		#print(len(docs))
		#print(docs[:10])
		#exit()
		return docs

	def set_classifyable_docs(self):
		self.df_names = pd.DataFrame(self.get_set_of_docs("nome"), columns=["data"])
		self.df_endereco = pd.DataFrame(self.get_set_of_docs("endereco"), columns=["data"])
		self.df_naoconsiderar = pd.DataFrame(self.get_set_of_docs("naoconsiderar"), columns=["data"])

		self.df_names = DataPreprocessor(self.df_names).pre_processing()
		self.df_endereco = DataPreprocessor(self.df_endereco).pre_processing()
		self.df_naoconsiderar =  DataPreprocessor(self.df_naoconsiderar).pre_processing()

	def set_X_and_y(self):
		X_raw = list(self.df_names.data) + list(self.df_endereco.data) + list(self.df_naoconsiderar.data) 
		self.y = np.asarray([self.classe["nome"] for x in range(self.df_names.shape[0])] + \
					   [self.classe["endereco"] for x in range(self.df_endereco.shape[0])] + 
					   [self.classe["naoconsiderar"] for x in range(self.df_naoconsiderar.shape[0])])
		print(Counter(self.y))

		self.vectorizer = TfidfVectorizer()
		self.vectorizer.fit(X_raw)
		self.X = self.vectorizer.transform(X_raw)
		
	def most_common(self,lst):
		return np.argmax(np.bincount(lst))
		#return np.argmax(np.bincount(lst+1))-1

	def build_model(self):

		skf = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
		micro_list = []
		macro_list = []

		for train_index, test_index in skf.split(self.X, self.y):
			print("TRAIN:", train_index, "TEST:", test_index)
			X_train, X_test = self.X[train_index], self.X[test_index]
			y_train, y_test = self.y[train_index], self.y[test_index]

			dist_atual = Counter(y_train)
			dist_desejavel = {
				self.classe["nome"]: dist_atual[self.classe["nome"]],
				self.classe["endereco"]: dist_atual[self.classe["endereco"]],
				self.classe["naoconsiderar"]: max(dist_atual[self.classe["nome"]],dist_atual[self.classe["endereco"]]),
			}
			print(dist_desejavel)

			rus = RandomUnderSampler(random_state=42,sampling_strategy=dist_desejavel)
			X_train, y_train = rus.fit_resample(X_train, y_train)
			
			#exit()
			info = {
				"name_class": "lsvm",
				"cv": 10,
				'n_jobs': -1,
				"max_iter": 1000000,
			}
			self.classifier = TraditionalClassifier(info)
			self.classifier.fit(X_train, y_train)

			dump(self.classifier, 'model/classifier.joblib') 

			y_pred = self.classifier.predict(X_test)

			micro = f1_score(y_true=y_test, y_pred=y_pred, average='micro')
			macro = f1_score(y_true=y_test, y_pred=y_pred, average='macro')
			print("F1-Score")
			print("\tMicro: ", micro)
			print("\tMacro: ", macro)
			
			micro_list.append(micro)
			macro_list.append(macro)
			
			break

	def y_predict(self):
		self.y_test = np.zeros(len(self.atributes_to_consider),dtype=int)
		self.y_test[self.y_test == 0] = self.classe["naoconsiderar"]

		#self.cpf_cnpf_finded or  a in self.nis_finded or a in self.email_finded or a in self.titulo_finded 

		for a in self.cpf_cnpf_finded:
			self.y_test[self.atributes_to_consider.index(a)] = self.classe["cpf_cnpj"]
		for a in self.email_finded:
			self.y_test[self.atributes_to_consider.index(a)] = self.classe["email"]
		for a in self.titulo_finded:
			self.y_test[self.atributes_to_consider.index(a)] = self.classe["titulo"]
		for a in self.nis_finded:
			self.y_test[self.atributes_to_consider.index(a)] = self.classe["nis"]

		self.nomes_header = []
		self.enderecos_header = []

		for bd in self.onlybds:
			df = pd.read_csv(f"{self.mypath}/{bd}")
			df = DataPreprocessor(df).pre_processing()
			#df = pre_processing(df)
			#df = df.applymap(vectorizer.transform)
			docs = []
			atributos_avaliados = []
			for c in df.columns:
				if c not in self.atributos_nao_considerados and c not in self.all_validable_finded:
					#print(list(set(df[c])))
					#exit()
					docs.append(self.vectorizer.transform(list(set(df[c]))))
					#docs += list(map(str,df[c][df[c].notna()].values))
					atributos_avaliados.append(c)
			#df.head()
			#predic = [self.most_common(self.classifier.predict(a)) for a in docs]
			#for d in docs:
			#	ppp = self.classifier.predict(d)
			#	print(ppp,self.most_common(ppp))
			#exit()
			predic = [self.most_common(self.classifier.predict(a)) for a in docs]


			for idx, a in enumerate(atributos_avaliados):
				idx_total = self.atributes_to_consider.index(a)
				if self.y_test[idx_total] == self.classe['naoconsiderar']:
					#self.y_test[idx_total] = predic[idx]
					if predic[idx] == self.classe['nome']:
						self.y_test[idx_total] = self.classe['nome']
						self.nomes_header.append(a)
					if predic[idx] == self.classe['endereco']:
						self.y_test[idx_total] = self.classe['endereco']
						self.enderecos_header.append(a)

		self.finded['endereco'] = self.enderecos_header
		self.finded['nome'] = self.nomes_header
		print(self.y_test[:20])

	def general_results(self):
		print("micro",round(f1_score(self.y_true, self.y_test, average="micro")*100,2))
		print("macro",round(f1_score(self.y_true, self.y_test, average="macro")*100,2))
		print("precision_score", round(precision_score(self.y_true, self.y_test, average="macro")*100,2))
		print("recall_score", round(recall_score(self.y_true, self.y_test, average="macro")*100,2))

	def resultado_micro_macro_binario(self, c):
		
		encontrados = self.finded[c]
		self.results[c]["atributos_encontrados"] = list(self.finded[c])
		todos_da_classe = self.annoted_atributes[c]
		print("###########################")
		print(c, len(encontrados), len(todos_da_classe))
		print("encontrados: ", len(encontrados))
		print("todos: ", len(todos_da_classe))
		y_test = np.zeros(len(self.atributes_to_consider),dtype=int)
		y_test[y_test == 0] = -1

		for a in encontrados:
			y_test[self.atributes_to_consider.index(a)] = self.classe[c]

		y_true_binary = copy.copy(self.y_true)
		y_true_binary[y_true_binary != self.classe[c]] = -1
		print("micro",round(f1_score(y_true_binary, y_test, average="micro")*100,2))
		print("macro",round(f1_score(y_true_binary, y_test, average="macro")*100,2))

		tp = multilabel_confusion_matrix(y_true_binary, y_test)[0][0][0]
		fp = multilabel_confusion_matrix(y_true_binary, y_test)[0][1][0]
		fn = multilabel_confusion_matrix(y_true_binary, y_test)[0][0][1]
		print(f"precision: {tp/(tp+fp)}")
		print(f"recall: {tp/(tp+fn)}")
		print(f"f1: {harmonic_mean([tp/(tp+fp),tp/(tp+fn)])}")

		self.results[c]['micro'] = f1_score(y_true_binary, y_test, average="micro")*100
		self.results[c]['macro'] = f1_score(y_true_binary, y_test, average="macro")*100
		self.results[c]['precision'] = tp/(tp+fp)
		self.results[c]['recall'] = tp/(tp+fn)
		self.results[c]['f1'] = harmonic_mean([tp/(tp+fp),tp/(tp+fn)])


	def results(self):
		inv_map = {v: k for k, v in self.classe.items()}

		data = {'y_true': self.y_true,
			'y_test': self.y_test
		}

		df = pd.DataFrame(data, columns=['y_true','y_test'])
		df = df.applymap(lambda x: inv_map[x])

		self.results = {}
		for x in self.classe.keys():
			if x != "naoconsiderar":
				self.results[x] = {}

		self.confusion_matrix = pd.crosstab(df['y_true'], df['y_test'], rownames=['True'], colnames=['Predicted'])
		#self.results['confusion_matrix'] = self.confusion_matrix.tolist()

		print(self.confusion_matrix)
		self.resultado_micro_macro_binario('endereco')
		self.resultado_micro_macro_binario('nome')

		self.resultado_micro_macro_binario('cpf_cnpj')
		self.resultado_micro_macro_binario('nis')
		self.resultado_micro_macro_binario('email')
		self.resultado_micro_macro_binario('cpf_cnpj')
		self.resultado_micro_macro_binario('titulo')

		print("Saving Json Results")
		with open("results.json", 'w') as outfile:
			json.dump(self.results, outfile, indent=4)
		
		

def main():
	gc.collect()
	args = arguments()

	finder = MPMGFinder(args)
	finder.set_onlybds()
	finder.set_annoted_atributes()
	finder.set_distinct_atributes()
	finder.set_classes_nao_consideradas()
	finder.set_atributes_to_consider()
	finder.find_validable_class()
	#finder.validate_to_remove()
	finder.set_y_true()
	finder.set_classifyable_docs()
	finder.set_X_and_y()
	finder.build_model()
	finder.y_predict()

	finder.general_results()
	finder.results()


	#analises = Analises(finder)
	#analises.analise_nans_por_classe()


if __name__ == '__main__':
	main()
