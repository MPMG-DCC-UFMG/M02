import sys
import os
import argparse
import segmentacao
import random

def main():

	#Para replicar os resultados
	random.seed(1608637542)

	parser = argparse.ArgumentParser(description='Segmentação dos Diários Oficiais dos Municípios Mineiros.')
	parser.add_argument("-o", metavar="<diretório>",type=str, help="Caminho do diretório par guardar as saídas no formato .json.", default="MPMG_segmentos/")
	parser.add_argument("--pdf", metavar="<arquivo>",type=str, help="Nome do arquivo do diário oficial em formato PDF.")
	parser.add_argument("--dir", help="Caminho do diretório contendos os arquivos dos diário oficiais em formato PDF.", default="amostra_AMM/")
	
	args = parser.parse_args()
	dir_output = getattr(args, "o")
	if dir_output[-1] != "/":
		dir_output += "/"

	if getattr(args, "pdf") is not None:
		segmentacao.segementarPDF(getattr(args, "pdf"), dir_output)
	else:
		dir_input = getattr(args, "dir")
		if dir_input[-1] != "/":
			dir_input += "/"
		segmentacao.segementarDIR(dir_input, dir_output)

if __name__ == "__main__":
    main()
