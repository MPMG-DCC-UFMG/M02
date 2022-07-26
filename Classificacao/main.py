import sys
import os
import argparse
import classification
import random
import json
import glob

def main():

	#Para replicar os resultados
	random.seed(1608637542)

	parser = argparse.ArgumentParser(description='Classificação dos Diários Oficiais dos Municípios Mineiros.')
	parser.add_argument("--test", help="Avaliação da classificação semântica (validação cruzada).", action='store_true')
	parser.add_argument("--annotation", metavar="<arquivo>", help="Arquivo com as anotações realizadas pelo no serviço web da aplicação (PRISMA).", default="annotation.tsv")
	parser.add_argument("--json", metavar="<arquivo>", help="Arquivo em JSON contendo os segmentos que foram avaliados pelo no serviço web da aplicação (PRISMA).", default="sample.json")
	parser.add_argument("--train",help='Treina o modelo preditivo.', default=False, action='store_true')
	parser.add_argument("--dir_model", metavar="<diretório>",type=str, help="Caminho do diretório com os arquivos em formato .json.", default="models/")
	
	parser.add_argument("--dir_output", metavar="<diretório>",type=str, help="Caminho do diretório para guardar as saídas no formato .csv.", default="MPMG_resultados/")
	parser.add_argument("--dir_input", metavar="<diretório>",type=str, help="Caminho do diretório com os arquivos em formato .json.", default="MPMG_segmentos/")
	parser.add_argument("--model", metavar="<arquivo>",type=str, help="Caminho do arquivo com o modelo preditivo.", default=False)
	parser.add_argument("--segmento", metavar="Texto com o conteúdo do segmento",type=str, help="Texto do segmento a ser classificado.", default=False)
	
	args = parser.parse_args()
	
	if getattr(args, "test") or getattr(args, "train"):
		jsonFile = getattr(args, "json")
		annotationFile = getattr(args, "annotation")
		
		if not os.path.exists(jsonFile):
			print("O arquivo não existe: '{}'.".format(jsonFile))
			print("Por favor, informar o caminho completo: {} --json <arquivo>".format(sys.argv[0]))
			exit(2)

		if not os.path.exists(annotationFile):
			print("O arquivo não existe: '{}'.".format(annotationFile))
			print("Por favor, informar o caminho completo: {} --annotation <arquivo>".format(sys.argv[0]))
			exit(2)
	
		if getattr(args, "test"):
			classification.evaluate(jsonFile, annotationFile)

		if getattr(args, "train"):
			dir_model = getattr(args, "dir_model")
			if not os.path.exists(dir_model):
				print("O diretório para guardar os modelos não existe: '{}'.".format(dir_model))
				print("Por favor, informar o caminho completo: {} --dir_model <diretório>".format(sys.argv[0]))
				exit(2)
			classification.train_data(jsonFile, annotationFile, dir_model)
	else:
		model = getattr(args, "model")
		dir_model = getattr(args, "dir_model")
		if dir_model[-1] != "/":
			dir_model += "/"
		model = getattr(args, "model")
		if model:
			if not os.path.exists(model):
				print("O arquivo não existe: '{}'.".format(model))
				print("Por favor, informar o caminho completo: {} --model <arquivo>".format(sys.argv[0]))
				exit(2)
		elif not os.path.exists(dir_model):
			print("Não existe a pasta com os modelos preditivos: '{}'.".format(dir_model))
			print("Por favor, treinar o modelo: {} --train".format(sys.argv[0]))
			exit(2)
		else:
			# Getting the latest predictive model
			models = glob.glob(dir_model+ "*.joblib")
			if len(models) < 1:
				print("Não há nenhum modelo preditivo criado.")
				print("Por favor, treinar o modelo: {} --train".format(sys.argv[0]))
				exit(2)
			model = max(models, key=os.path.getctime)
		
		print("Usando o modelo preditivo '{}'".format(model))
		classifier, vectorizer = classification.loadClassifier(model)
		
		if getattr(args, "segmento"):
			print(classification.predict(classifier, vectorizer, getattr(args, "segmento"))[0])
		else:
			dir_input  = getattr(args, "dir_input")
			dir_output = getattr(args, "dir_output")

			if not os.path.exists(dir_input):
				print("O diretório de entrada com os JSONs a serem classificados não existe: '{}'.".format(dir_input))
				print("Por favor, informar o caminho completo: {} --dir_input <diretório>".format(sys.argv[0]))
				exit(2)

			if not os.path.exists(dir_output):
				print("O diretório para guardar os resultados não existe: '{}'.".format(dir_output))
				print("Por favor, informar o caminho completo: {} --dir_output <diretório>".format(sys.argv[0]))
				exit(2)
				
			files = glob.glob(dir_input + "*.json")
			for f in files:
				classification.predictFile(classifier, vectorizer, f, dir_output)

if __name__ == "__main__":
    main()
