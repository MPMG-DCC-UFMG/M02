
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def set_atributes_packages():
	#print("Python version:",python_version())
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)
	sns.set()
	fig_size = plt.rcParams["figure.figsize"]
	fig_size[0] = 6
	fig_size[1] = 4
	plt.rcParams["figure.figsize"] = fig_size
	print("matplotlib: ",plt.rcParams.get('figure.figsize'))

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.0f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

class Analises(object):
	"""docstring for Analises"""
	def __init__(self, finder):
		set_atributes_packages()
		self.mypath = finder.mypath
		self.onlybds = finder.onlybds
		self.annoted_atributes = finder.annoted_atributes
		self.all_atributes = finder.all_atributes
		

	def busca_total_e_nans_por_classe(self, df, classe, total_e_nans_por_classe):
	    
	    consider_set = self.annoted_atributes[classe]
	    
	    columns = [c for c in df.columns if c in consider_set]
	    if columns == []:
	        return
	    
	    total = df[columns].shape[0] * df[columns].shape[1]
	    #print(df[columns].shape)
	    nans = df[columns].isnull().sum().sum()

	    total_e_nans_por_classe[classe][0]+=total
	    total_e_nans_por_classe[classe][1]+=nans


	    #display(df[columns].head())
	

	def analise_nans_por_classe(self):

		total_e_nans_por_classe = {
		    'nome': [0,0],
		    'endereco': [0,0],
		    'cpf_cnpj': [0,0],
		    'titulo': [0,0],
		    'nis': [0,0],
		    'email': [0,0],
		}

		labels = [a for a in total_e_nans_por_classe.keys()]


		for i in range(len(self.onlybds)):
		    #print(i)
		    #print(onlybds[i])
		    df = pd.read_csv(f"{self.mypath}/{self.onlybds[i]}")

		    for classe in ['nome' ,'endereco' ,'cpf_cnpj' ,'titulo' ,'nis' ,'email']:
		        self.busca_total_e_nans_por_classe(df, classe, total_e_nans_por_classe)

		#total_e_nans_por_classe

		np.sum([total_e_nans_por_classe[a][0] for a in labels]) , \
		np.sum([total_e_nans_por_classe[a][1] for a in labels]) , \
		np.sum([total_e_nans_por_classe[a][1] for a in labels]) / np.sum([total_e_nans_por_classe[a][0] for a in labels])


		x = [total_e_nans_por_classe[a][1] for a in labels]
		fig_size = plt.rcParams["figure.figsize"]
		fig_size[0] = 8
		fig_size[1] = 8
		plt.rcParams["figure.figsize"] = fig_size
		print(plt.rcParams.get('figure.figsize'))

		plt.pie(x, labels=labels,  shadow=True, autopct=make_autopct(x),)
		plt.savefig('img/nans_por_classe.png')
		#

		# Agora tanto colunas a remover quanto selecionados serão uma lista de conjuntos
def mostra_dfs_sem_removidos(onlybds, colunas_a_remover):
    for i in range(len(onlybds)):
        print(i)
        #print(onlybds[i])
        df = pd.read_csv(f"bds_stage/{onlybds[i]}")
        #print(df.columns)
        columns = [c for c in df.columns if c not in colunas_a_remover]
        display(df[columns].head())
#mostra_dfs_sem_removidos(onlybds, colunas_a_remover)

def mostra_dfs_so_selecionados(onlybds, selecionados):
    for i in range(len(onlybds)):
        #print(onlybds[i])
        df = pd.read_csv(f"bds_stage/{onlybds[i]}")
        #print(df.columns)
        columns = [c for c in df.columns if c in selecionados[i]]
        if columns == []:
            continue
        
        print(i)
        display(df[columns].head())
#mostra_dfs_sem_removidos(onlybds, colunas_a_remover)

def plot_headers_qnt(set_target):
    aux = Counter(set_target)
    label = [x for x in aux.keys()]
    qnt = [aux[x] for x in label]

    index = np.arange(len(label))
    plt.bar(index, qnt)
    plt.xlabel('Header', fontsize=10)
    plt.ylabel('Qnt', fontsize=10)
    plt.xticks(index, label, fontsize=8, rotation=90)
    #plt.title('Market Share for Each Genre 1995-2017')
    plt.show()