import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextBoxHorizontal
import json
import os
import time
import sys
sys.setrecursionlimit(1500)

def segementarPDF(PDF, dir_output):
    if not os.path.exists(PDF):
        print("Arquivo não existe: '{}'.".format(PDF))
        print("Por favor, informar o caminho completo: {} --pdf <arquivo>".format(sys.argv[0]))
        exit(2)
    processarPDF(PDF, dir_output)


def processarPDF(PDF, dir_output):
    f = PDF

    start_time = time.time()
    print("Processando arquivo '" + f + "'")
    metadados = obterMetadados(f)
    data = dict()
    for k,v in metadados.items():
        data[k] = v

    elementos, cod_page = obterElementosOrdenados(f)
    #segmentos = obterSegmentos(elementos)
    data["segmentos"] = obterSegmentos(elementos, cod_page)

    with open(dir_output + f + ".json", 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print("Processado - %.2f segundos" % (time.time() - start_time))

def segementarDIR(dir_input, dir_output):

    if not os.path.exists(dir_input):
        print("Caminho não existe: '{}'.".format(dir_input))
        print("Por favor, informar o caminho completo com a entrada dos dados: {} --dir <caminho>".format(sys.argv[0]))
        exit(2)

    if not os.path.exists(dir_output):
        print("Caminho não existe: '{}'.".format(dir_output))
        print("Por favor, informar o caminho completo para a saída dos dados: {} -o <caminho>".format(sys.argv[0]))
        exit(2)

    start_time = time.time()
    files = os.listdir(dir_input)
    for f in files:
        if f.endswith(".pdf"):
            if (not os.path.exists(dir_output + f + ".json")):
                print("Processando arquivo '" + f + "'")
                metadados = obterMetadados(dir_input + "/" + f)
                data = dict()
                for k,v in metadados.items():
                    data[k] = v
                elementos, cod_page = obterElementosOrdenados(dir_input + "/" + f)
                #segmentos = obterSegmentos(elementos)
                data["segmentos"] = obterSegmentos(elementos, cod_page)

                with open(dir_output + f + ".json", 'w') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)
                print("Processado - %.2f segundos" % (time.time() - start_time))
            else:
                print("Arquivo já processado: ", f)
    print("Total: %.2f segundos" % (time.time() - start_time))


def obterElementosOrdenados(PDF, log=False):
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
        alturaDaPagina = page.bbox[3]
        
        duasColunas = []
        umaColuna = []
        
        page_e = []
        for elemento in page:
            if isinstance(elemento, LTTextBoxHorizontal):
                page_e.append(elemento)
        
        # Verifica se a página possui colunas mistas (parte com duas colunas e parte com uma)
        if n_colunas == 2:
            limit_y1 = False
            # Verifica se há dois formatos diferentes na mesma página
            for elemento in page_e:
                texto = elemento.get_text()
                if texto.startswith("ESTADO DE MINAS GERAIS \n"):
                    x0, x1 = elemento.bbox[0],elemento.bbox[2]
                    # Elemento posicionado no meio da página
                    if x0 < meioDaPagina and x1> meioDaPagina:
                        limit_y1 = alturaDaPagina - elemento.bbox[1]
                        break
            # O formato da página é de somente duas páginas
            if limit_y1 is False:
                duasColunas = page_e
            # Há uma parte em 2-colunas e outra parte em 1-coluna
            else:
                n_colunas = 1
                for elemento in page_e:
                    if (alturaDaPagina - elemento.bbox[1]) < limit_y1:
                        duasColunas.append(elemento)
                    else:
                        umaColuna.append(elemento)
            
            # Processa os elementos em duas colunas
            coluna1 = dict()
            coluna2 = dict()
            for elemento in duasColunas:
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
                if x0 <= meioDaPagina:
                    #if y1 in coluna1:
                    #    raise NameError('Conflito entre objetos sobrepostos com coordenadas iguais.')

                    while y1 in coluna1:
                        y1 += 0.0000000001
                    coluna1[y1] = elemento
                # Coluna à direita
                else:
                    #if y1 in coluna2:
                    #    raise NameError('Conflito entre objetos sobrepostos com coordenadas iguais.')

                    while y1 in coluna2:
                        y1 += 0.0000000001
                    coluna2[y1] = elemento

            # Gera uma lista ordenada dos elementos por coluna seguido pela coordenada Y.
            t_elementos = [v for (k,v) in sorted(coluna1.items())]
            for (k,v) in sorted(coluna2.items()):
                t_elementos.append(v)
            
            # Insere os elementos restantes do formato de uma coluna em ordem
            for e in umaColuna:
                t_elementos.append(e)
                
        # Formato uma-coluna
        else:
            for e in page_e:
                t_elementos.append(e)
        
        if primeira_pagina:
            t_elementos = filtrarInformacao(t_elementos, log)
            primeira_pagina = False
        else:
            t_elementos = descartarSentencas(t_elementos, log)
        
        for e in t_elementos:
            elementos.append(e)
            texto = e.get_text()
            if "Código Identificador:" in texto:
                COD_IDENTIFICADOR = (texto[texto.index("Código Identificador:")+len("Código Identificador:"):]).strip()
                cod_page[COD_IDENTIFICADOR] = page_count
        
    return elementos,cod_page
    


# In[2]:



from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
import re

def obterSegmentos(elementos, cod_page):
    resto = []
    segmentos = []
    
    data = dict()
    
    indice = 0
    # Loop para cada entidade
    while indice < len(elementos):
        
        elemento = elementos[indice]
        texto = elemento.get_text()
        if texto.startswith("ESTADO DE MINAS GERAIS \n"):
            ENTIDADE = re.sub('\s{2,}', ' ', (texto[texto.index("\n"):]).strip())
            if ENTIDADE == "":
                indice += 1
                if indice < len(elementos):
                    ENTIDADE = re.sub('\s{2,}', ' ', elementos[indice].get_text().strip())
            
            # Loop para cada matéria
            indice += 1
            while indice < len(elementos):
                # Obtendo título/subtítulo
                texto = elementos[indice].get_text().strip()
                
                while (indice + 1) < len(elementos):
                    if texto.strip() != "":
                        break
                    else:
                        indice += 1
                        texto = elementos[indice].get_text().strip()
                
                if indice < len(elementos):
                    if "\n" in texto:
                        TITULO = re.sub('\s{2,}', ' ', (texto[0:texto.index("\n")]).strip())
                        SUBTITULO = re.sub('\s{2,}', ' ', (texto[texto.index("\n"):]).strip().replace("\n", " "))
                    else:
                        TITULO = re.sub('\s{2,}', ' ', texto.strip())
                        SUBTITULO = ""
                    

                # Obtendo conteúdo da matéria e o identificador
                indice += 1
                if indice < len(elementos):
                    texto = elementos[indice].get_text().strip()
                    MATERIA = ""
                    while (indice+1) < len(elementos) and "Publicado por: " not in texto and "Código Identificador:" not in texto:
                        #MATERIA += texto #+ "\n"
                        #here
                        texto = re.sub(' \n  \n', '$$$', texto.strip()) + "\n"
                        texto = re.sub('\n', ' ', texto)
                        texto = re.sub('\$\$\$', '\n', texto)
#                        if not texto.endswith(". \n"):
 #                           texto = re.sub('\.\s\n', '. \n', texto.strip())
                            #texto = texto.strip()
                        #else:
                        #    texto = re.sub('\s{2,}', ' ', texto.strip())
                        
                        #elif texto.endswith(". \n"):
                        #    texto = texto.strip()
                        MATERIA += "\n" + texto + "\n"
                        indice += 1
                        texto = elementos[indice].get_text()
                    #akki
                    if "Publicado por: " in texto and "Código Identificador:" in texto:
                        #print("#", texto,"#")
                        #print("$", re.sub('\s{2,}', ' ', MATERIA.strip()), "$")
                        #print("---")
                        PUBLICADOR = (texto[len("Publicado por: \n"):texto.index("Código Identificador:")]).strip()
                        COD_IDENTIFICADOR = (texto[texto.index("Código Identificador:")+len("Código Identificador:"):]).strip()
                        
                        if ENTIDADE not in data:
                            data[ENTIDADE] = []
                            
                        texto = MATERIA
                        MATERIA = ""
                        index_start = 0
                        for match in re.finditer(r'[a-z][\,\s,\\n]+[\n][a-z]', texto):
                            MATERIA += texto[index_start:match.start()+1] + " " + texto[match.end()-1]
                            index_start = match.end()
                        
                        MATERIA += texto[index_start:len(texto)]
                    
                        data[ENTIDADE].append({
                        #"titulo": TITULO,
                        #"subtitulo": SUBTITULO,
                        #"materia": MATERIA,
                        "materia": TITULO + "\n" + SUBTITULO + "\n" + MATERIA,
                        "page": cod_page[COD_IDENTIFICADOR],
                        "publicador": PUBLICADOR,
                        "id": COD_IDENTIFICADOR
                        })
                # Apontando para o início da próxima matéria
                while (indice+1) < len(elementos):
                    indice += 1
                    texto = elementos[indice].get_text().strip()
                    if texto != "":
                        break
                
                # Se há uma nova entidade, então passa ao loop entidade
                if indice < len(elementos):
                    texto = elementos[indice].get_text()
                    if texto.startswith("ESTADO DE MINAS GERAIS \n"):
                        #print("BREAK")
                        indice -= 1
                        break
                
        indice += 1
    
    return data



# In[3]:


def descartarSentencas(elementos, log=False):
    # Descarta sentenças em que todos os elementos da lista estejam presentes em um bloco.
    # Ex. descarte todos os blocos em que haja três fragmentos seguintes: descartar.append(("parte 1", "parte 2", "parte 3))
    descartar = list()
    descartar.append(["www.diariomunicipal.com.br/amm-mg"])
    descartar.append("Minas Gerais Diário Oficial dos Municípios Mineiros de ANO".split(" "))
    
    elementos_filtrados = []
    indice = 0
    while indice < len(elementos):
        #if isinstance(elementos[indice], LTTextBoxHorizontal):
        texto = elementos[indice].get_text()
        flag = False
        # Conteúdo pré-definido a ser removido (e.g., cabeçalho/rodapé)
        for t_list in descartar:
            flag = True
            for e in t_list:
                if e not in texto:
                    flag = False
                    break
            if flag:
                break

        if not flag:
            elementos_filtrados.append(elementos[indice])
        elif log:
            print("Sentença Removida: '", texto, "'")
                        
        indice += 1
        
    return elementos_filtrados

def filtrarInformacao(elementos, log=False):
    # Filtra conteúdos iniciados pelo elemento 0 (início do filtro) e finalizados pelo elemento 1 (fim do filtro).
    # Ex.: filtrar.append(("início", "fim"))
    filtrar = []
    filtrar.append(("Expediente: \nAssociação Mineira de Municípios", "O Diário Oficial dos Municípios do Estado de Minas Gerais"))
    
    elementos_filtrados = []
    indice = 0
    while indice < len(elementos):
        #if isinstance(elementos[indice], LTTextBoxHorizontal):
        texto = elementos[indice].get_text()
        # Filtrando conteúdo com início e fim pré-definido
        for (inicio, fim) in filtrar:
            if inicio in texto:
                if log:
                    print("FILTRO ATIVADO")

                if fim in texto:
                    if log:
                        print(texto)
                    indice += 1

                while (fim not in texto and indice < len(elementos)):
                    if isinstance(elementos[indice], LTTextBoxHorizontal):
                        texto = elementos[indice].get_text()
                        if log:
                            print(texto)
                    indice += 1
                if log:
                    print("FILTRO DESATIVADO")

        if indice < len(elementos):
            if isinstance(elementos[indice], LTTextBoxHorizontal):
                elementos_filtrados.append(elementos[indice])
                        
        indice += 1
        
    return descartarSentencas(elementos_filtrados, log)

def obterMetadados(PDF, log=False):
    ret = dict()
    ret["origem"]   = PDF
    ret["diario"]   = ""
    ret["numero"]   = ""
    ret["data"] = ""

    page = next(extract_pages(PDF, page_numbers=[0], maxpages=1))
    for elemento in page:
        if isinstance(elemento, LTTextBoxHorizontal):
                texto = elemento.get_text()
                if re.match("Minas Gerais(.*?)ANO (.*?)\d+", texto):
                    if "Diário Oficial dos Municípios Mineiros" in texto:
                        ret["diario"] = "Diário Oficial dos Municípios Mineiros"

                    match = re.search("ANO (.*?)\d+", texto)
                    if match:
                        ret["numero"] = re.findall(r'\d+', match.group())[-1]

                    match = re.search("\d+\d\sde\s(Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)\sde\s\d\d\d\d", texto)
                    if match:
                        ret["data"] = match.group()
                    break

    return ret

