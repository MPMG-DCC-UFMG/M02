#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
import re


# In[2]:


# Retorna os elementos do pdf desde que sejam LTTextBoxHorizontal ordenados levando em conta que estão 
# em quatro colunas
def obterElementosOrdenados4col(PDF, log=False):
    primeira_pagina = True
    # Formato inicial é de duas colunas textuais. Ao final, torna-se de uma coluna.
    # n_colunas = 2
    n_colunas = 4
    
    elementos = []
    cod_page = dict()
    
    temp = extract_pages(PDF, laparams=LAParams(char_margin=4.0))
    
    page_count = 0;
    
    for page in temp:#extract_pages(PDF, laparams=LAParams(char_margin=4.0)):
        page_count = page_count + 1
        t_elementos = []
#       meioDaPagina = page.bbox[2]/2
        
        #Limites fixos retirados a partir de um diário oficial de 4 colunas       
        umQuartoDaPag = 244
        meioDaPagina = 430
        tresQuartosDaPag = 612
    
        alturaDaPagina = page.bbox[3]
        
        quatroColunas = []
#         duasColunas = []
#         umaColuna = []
        
        #filtra LTTextBoxHorizontal
        page_e = []
        for elemento in page:
            if isinstance(elemento, LTTextBoxHorizontal):
                #print(elemento.bbox, elemento.get_text())
                page_e.append(elemento)
        
        # Verifica se a página possui colunas mistas (parte com duas colunas e parte com uma)
        if n_colunas == 4:
            limit_y1 = False
            
            # Processa os elementos em quatro colunas
            coluna1 = dict()
            coluna2 = dict()
            coluna3 = dict()
            coluna4 = dict()
            
            for elemento in page_e:
                quatroColunas.append(elemento)
            
            #Identifica em que coluna o elemento está e o insere no dict dela indexando pela posição vertical
            for elemento in quatroColunas:
                # Caso for uma estrutura que possa conter texto
                x0 = False

                # Pega o posicionamento do primeiro dos seus filhos, uma vez que quadros externos se sobrepõem
                # bbox (x0, y0, x1, y1) tuple containing the coordinates of the left, bottom, right, and top of the object respectively.
                for obj in elemento._objs:
                    if isinstance(obj, LTTextLineHorizontal):
                        x0 = obj.bbox[0] # left
                        y1 = alturaDaPagina - obj.bbox[1] # top
                        break

                # Quando não há filhos pega o posicionamento do próprio elemento
                if x0 is False:
                    x0 = elemento.bbox[0] # left
                    y1 = alturaDaPagina - elemento.bbox[1] # top

                # Coluna à esquerda
                if x0 <= umQuartoDaPag:
                    #if y1 in coluna1:
                    #    raise NameError('Conflito entre objetos sobrepostos com coordenadas iguais.')

                    while y1 in coluna1:
                        y1 += 0.0000000001
                    coluna1[y1] = elemento
                # Coluna à direita
                elif (x0 >= umQuartoDaPag and  x0 <= meioDaPagina):
                    #if y1 in coluna2:
                    #    raise NameError('Conflito entre objetos sobrepostos com coordenadas iguais.')

                    while y1 in coluna2:
                        y1 += 0.0000000001
                    coluna2[y1] = elemento
                    
                elif (x0 >= meioDaPagina and  x0 <= tresQuartosDaPag):
                
                    while y1 in coluna3:
                        y1 += 0.0000000001
                    coluna3[y1] = elemento
                
                else:
                    while y1 in coluna4:
                        y1 += 0.0000000001
                    coluna4[y1] = elemento
                    
#             print(coluna1.items())
            # Gera uma lista ordenada dos elementos por coluna seguido pela coordenada Y.
            t_elementos = [v for (k,v) in sorted(coluna1.items())]
            for (k,v) in sorted(coluna2.items()):
                t_elementos.append(v)
            for (k,v) in sorted(coluna3.items()):
                t_elementos.append(v)
            for (k,v) in sorted(coluna4.items()):
                t_elementos.append(v)
            
                
        
#         if primeira_pagina:
#             t_elementos = filtrarInformacao(t_elementos, log)
#             primeira_pagina = False
#         else:
#             t_elementos = descartarSentencas(t_elementos, log)
        ident = 0
        for e in t_elementos:
            elementos.append(e)
            texto = e.get_text()
            cod_page[ident] = page_count
            ident = ident + 1 
            #if "Código Identificador:" in texto:
#             for identificador in identificadorList:
#                 if identificador in texto:
#                     COD_IDENTIFICADOR = (texto[texto.index(identificador)+len(identificador):]).strip()
#                     cod_page[COD_IDENTIFICADOR] = page_count
                    #print(COD_IDENTIFICADOR)
    print(cod_page)
    return elementos,cod_page


# In[3]:


# PDF = "./2pgs_09_04_2020_DO.pdf"


# In[4]:


PDF = "./diariobh2.pdf"


# In[5]:


elem, cod = obterElementosOrdenados4col(PDF)


# In[6]:


# Elementos retirados com obterElementosOrdenados4col(PDF)
for el in elem:
    print(el.get_text())


# In[7]:


iniciadoresComuns = [
'BELOTUR',
'Fundação Municipal de Cultura',
'CDPCM',
'Secretaria Municipal Adjunta de Recursos Humanos',
'BEPREM',
'Corregedoria-Geral do município',
'Secretaria Municipal Adjunta de Arrecadações',
'Secretaria Municipal Adjunta de Gestão Administrativa',
'Hospital Municipal Odilon Behrens',
'BHTRANS',
'SLU',
'Fundação Zoo-Botânica',
'COMAM',
'PRODABEL',
'Fundação de Parques Municipais e Zoobotânica',
'SUDECAP',
'COMPUR',
'COMUSA',
'URBEL']


iniciadoresNegrito = [
'GABINETE DO PREFEITO',
'SECRETARIA MUNICIPAL DE GOVERNO',
'SECRETARIA MUNICIPAL DE PLANEJAMENTO, ORÇAMENTO E INFORMAÇÃO',
'PROCURADORIA-GERAL DO MUNICÍPIO',
'CONTROLADORIA-GERAL DO MUNICÍPIO',
'SECRETARIA MUNICIPAL DE FINANÇAS',
'SECRETARIA MUNICIPAL DE POLÍTICAS SOCIAIS',
'SECRETARIA MUNICIPAL DE EDUCAÇÃO',
'SECRETARIA MUNICIPAL DE SAÚDE',
'SECRETARIA MUNICIPAL DE POLÍTICAS URBANAS',
'SECRETARIA MUNICIPAL DO MEIO AMBIENTE',
'SECRETARIA MUNICIPAL DE ASSUNTOS INSTITUCIONAIS E COMUNICAÇÃO SOCIAL',
'SECRETARIA MUNICIPAL DE PLANEJAMENTO, ORÇAMENTO E GESTÃO',
'SECRETARIA MUNICIPAL DE FAZENDA',
'SECRETARIA MUNICIPAL DE DESENVOLVIMENTO ECONÔMICO',
'SECRETARIA MUNICIPAL DE OBRAS E INFRAESTRUTURA',
'SECRETARIA MUNICIPAL DE POLÍTICA URBANA',
'SECRETARIA MUNICIPAL DE SEGURANÇA E PREVENÇÃO',
'SECRETARIA MUNICIPAL DE ASSISTÊNCIA SOCIAL, SEGURANÇA ALIMENTAR E CIDADANIA',
'SECRETARIA MUNICIPAL DE CULTURA',
'SECRETARIA MUNICIPAL DE ESPORTES E LAZER',
'CONTROLADORIA-GERAL DO MUNICÍPIO'
]


# In[8]:


# Exibe inicializadores definidos acima ao longo do texto
def obterSegmentos4col(elementos, cod_page):
    resto = []
    segmentos = []
    
    data = dict()
    
    indice = 0
    # Loop para cada entidade
    while indice < len(elementos):
        
        elemento = elementos[indice]
        texto = elemento.get_text()
        texto = texto.strip()
        texto = texto.replace('\n', ' ').replace('\r',' ').replace('  ', ' ')
        
        if(texto in iniciadoresNegrito):
            print("|#TITULO| -", texto)
            
        elif(texto in iniciadoresComuns):
            print("  |#SUB| -", texto)
            
        else:
            print("       ", texto)
        
        indice += 1
    
    return data


# In[9]:


elem, cod = obterElementosOrdenados4col(PDF)
seg = obterSegmentos4col(elem, cod)


# In[10]:


# retorna a coordenada de todos os elementos (não é necessário mas é bom para debugar)
def obterCoordenadasElementosOrdenados(PDF):
    primeira_pagina = True
    # Formato inicial é de duas colunas textuais. Ao final, torna-se de uma coluna.
    n_colunas = 2
    elementos = []
    cod_page = dict()
    temp = extract_pages(PDF, laparams=LAParams(char_margin=4.0))
    
    page_count = 0;
    for page in temp:#extract_pages(PDF, laparams=LAParams(char_margin=4.0)):
        page_count = page_count + 1
        t_elementos = []
        meioDaPagina = page.bbox[2]/2
        print(meioDaPagina)
        alturaDaPagina = page.bbox[3]
        
        duasColunas = []
        umaColuna = []
        
        bbox_elements = []
        texts = []
        
        page_e = []
        for elemento in page:
            if isinstance(elemento, LTTextBoxHorizontal):
                if(elemento.get_text().strip() != ""):
                    bbox_elements.append(elemento.bbox)
                    texts.append(elemento.get_text())
                    page_e.append(elemento)
                    #print(elemento.bbox, elemento.get_text())
#         print(bbox_elements)
#         print(texts)    
        for i in range(len(bbox_elements)):
            x00, y00, x01, y01 = bbox_elements[i]
            quantColunas = 1
            colisoes = []
            colisoest = []
            colisocond = []
            
            for j in range(len(bbox_elements)):
                if(i != j):
                    x10, y10, x11, y11 = bbox_elements[j]
                    cond1 = y00 >= y10 and y00 <= y11
                    cond2 = y01 >= y10 and y01 <= y11
                    cond3 = y00 <= y10 and y01 >= y10
                    if(cond1 or cond2 or cond3):
                        colunaDiferente = True
                        for colisao in colisoes:
                            x20, y20, x21, y21 = colisao
                            cond1 = x10 >= x20 and x10 <= x21
                            cond2 = x11 >= x20 and x11 <= x21
                            cond3 = x10 <= x20 and x11 >= x20
                            if(cond1 or cond2 or cond3):
                                colunaDiferente = False
                                break
                            colisocond.append((x10,x11,x20,x21))
                        if(colunaDiferente):
                            quantColunas = quantColunas + 1
                        colisoes.append(bbox_elements[j])
                        colisoest.append(texts[j])
#             print(colisoest)
#             print(colisoes)
#             print(colisocond)
            print(bbox_elements[i], texts[i])
#             print(texts[i],"ncols = " ,  quantColunas)
    
#             for x00, y00, x01, y01 in range(len(bbox_elements)):
#             print(x00, y00, x01, y01)


# In[11]:


obterCoordenadasElementosOrdenados(PDF)

