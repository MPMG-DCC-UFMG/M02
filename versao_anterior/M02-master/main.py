import sys
import os
import argparse
import classification
import segmentacao
import random
#import json

def main():

	#Para replicar os resultados
	random.seed(1608637542)

	parser = argparse.ArgumentParser(description='Segmentação dos Diários Oficiais dos Municípios Mineiros.')

	parser.add_argument("-o", metavar="<diretório>",type=str, help="Caminho do diretório par guardar as saídas no formato .json.", default="MPMG_segmentos/")
	parser.add_argument("--pdf", metavar="<arquivo>",type=str, help="Nome do arquivo do diário oficial em formato PDF.")
	parser.add_argument("--dir", help="Caminho do diretório contendos os arquivos dos diário oficiais em formato PDF.", default="amostra_AMM/")
	parser.add_argument("--labels", metavar="<arquivo>", help="Arquivo com as anotações realizadas pelo no serviço web da aplicação (PRISMA).", default="annotation.tsv")
	parser.add_argument("--json", metavar="<arquivo>", help="Arquivo em JSON contendo os segmentos que foram avaliados pelo no serviço web da aplicação (PRISMA).", default="sample.json")
	parser.add_argument("--test", help="Avaliação da classificação semântica (validação cruzada).", action='store_true')
	
	args = parser.parse_args()
	dir_output = getattr(args, "o")
	if dir_output[-1] != "/":
		dir_output += "/"

	if getattr(args, "pdf") is not None:
		segmentacao.segementarPDF(getattr(args, "pdf"), dir_output)

	elif getattr(args, "test"):
		classification.evaluate(getattr(args, "json"),getattr(args, "labels"))

	else:
		dir_input = getattr(args, "dir")
		if dir_input[-1] != "/":
			dir_input += "/"
		segmentacao.segementarDIR(dir_input, dir_output)


if __name__ == "__main__":
    main()
