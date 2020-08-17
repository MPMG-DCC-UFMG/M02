from validacao import *
import pandas as pd 
import numpy as np
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

def verifica_target_coluna(df, coluna, target, limiar=0.70):
    lista_valores = list(set(df[coluna].values))
    #print(coluna)
    
    aux = 0
    for v in lista_valores:
        if target == 'titulo':
            if validar_titulo(str(v)):
                aux+=1
        if target == 'cpfoucnpj':
            if validar_cpf(str(v)) or validar_cnpj(str(v)):
                aux+=1
        if target == 'email':
            if validar_email(str(v)):
                aux+=1
        if target == 'titulo':
            if validar_titulo(str(v)):
                aux+=1
        if target == 'nit':
            #print("aaa")
            if validar_nit(str(v)):
                aux+=1
        if target == 'rg':
            if validar_rg(str(v)):
                aux+=1

    #print(coluna,aux)
    if aux/(len(lista_valores)) > limiar:
        return True
    return False

def find_target_columns_by_bd(bd_path , removed_columns, target, consider_header=True):
    columns = []
    df = pd.read_csv(bd_path)
    #print(df.columns)
    for c in df.columns:
        if c in removed_columns:
            #return columns
            continue
            
        if target == 'cpfoucnpj':
            if "cpf" in c or "cnpj" in c:
                columns.append(c)

            if not ("cpf" in c or "cnpj" in c) and verifica_target_coluna(df,c,'cpfoucnpj'):
                columns.append(c)
                
        if target == 'email':       
            if ("mail" in c) or ("e-mail" in c):
                #print('ok')
                columns.append(c)

            if not (("mail" in c) or ("e-mail" in c)) and verifica_target_coluna(df,c, 'email'):
                columns.append(c)
                
        if target == 'titulo': 
            if ("titulo" in c):# or ("eleitor" in c):
            #    #print('ok')
                columns.append(c)

            #if not (("mail" in c) or ("e-mail" in c)) and verifica_email_coluna(df,c):
            if not (("titulo" in c)) and verifica_target_coluna(df,c,'titulo'):
            #if verifica_target_coluna(df,c, 'titulo'):
                columns.append(c)

        if target == 'rg': 
            #if ("identidade" in c):# or ("eleitor" in c):
                #print('ok')
            #    columns.append(c)

            #if not (("mail" in c) or ("e-mail" in c)) and verifica_email_coluna(df,c):
            #if not (("titulo" in c)) and verifica_target_coluna(df,c,'rg'):
            
            if verifica_target_coluna(df,c,'rg'):
            #if verifica_target_coluna(df,c, 'titulo'):
                columns.append(c)
        
        if target == 'nit': 
            #if ("identidade" in c):# or ("eleitor" in c):
                #print('ok')
            #    columns.append(c)

            #if not (("mail" in c) or ("e-mail" in c)) and verifica_email_coluna(df,c):
            #if not (("titulo" in c)) and verifica_target_coluna(df,c,'rg'):
            
            if verifica_target_coluna(df,c,'nit'):
            #if verifica_target_coluna(df,c, 'titulo'):
                columns.append(c)
        
    #print(columns)
    return(columns)

from collections import Counter

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
    
def find_target_by_bd(target, mypath, removed_columns, onlybds):
    target_by_bd = []
    set_target_columns = []
    for idx, bd in enumerate(onlybds):
        print(idx)
        aux = find_target_columns_by_bd(f"{mypath}/{bd}", removed_columns, target)
        print(aux)
        target_by_bd.append(aux)
        set_target_columns += aux
    return target_by_bd, set_target_columns
    