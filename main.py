import sys
import os
import argparse
import classification
import random
import json

def main():

	#To replicate the experimental results
	random.seed(1608637542)

	parser = argparse.ArgumentParser(description='Determining the semantic class of data entries.')

	# test args
	parser.add_argument("-i", metavar="<input file>",type=str,help="Filename of the trained model. By default, it loads the last model version at the 'model/' directory.", default="")
	parser.add_argument("--db", metavar="<database>",type=str,help='Name of the database.')
	parser.add_argument("-c", metavar="<column>",type=str,help='Column name.')

	# train args
	parser.add_argument("--train",help='Train data.', default=False, action='store_true')
	parser.add_argument("--path", metavar="<pathname>",type=str,help='Path of the entire data (default: bds_stage/).', default="bds_stage/")
	parser.add_argument("--threshold", metavar="float value",type=float,help='Threshold value of the matching phase (default=0.7).', default=0.7)
	parser.add_argument("-o", metavar="<output path>",type=str,help="Pathname to write the trained model. By default, it writes at the 'model/' directory.", default="")

	args = parser.parse_args()

	# Prediction case: semantic value for a specific database.column
	if getattr(args, "db") is not None:
		if getattr(args, "c") is not None:
			db = getattr(args, "db")
			column = getattr(args, "c")

			filename = getattr(args, "i")
			if filename is not "":
				if os.path.exists(filename):
					try:
						f = open(filename)
						f.close()
					except IOError:
						print("File '{}' is not accessible. Please check filesystem permissions.".format(filename))
						exit(2)
				else:
					print("File does not exist: '{}'.".format(filename))
					print("Please, inform the properly pathname of the trained data: {} --db <database> -c <column> -i <inputfile>".format(sys.argv[0]))
					exit(2)
			else:
				path = "model/"
				try:
					files = os.listdir(path)
					paths = [os.path.join(path, basename) for basename in files if basename.endswith(".joblib")]
				except:
					print("No such file or directory: 'model/'")
					print("Please, inform the properly pathname of the trained data: {} --db <database> -c <column> -i <inputfile>".format(sys.argv[0]))
					exit(2)

				if len(paths) == 0:
					print("No trained data was found at {}.".format(path))
					print("Please, train the data first: python3.6 {} --train".format(sys.argv[0]))
					exit(2)
				else:
					filename = max(paths, key=os.path.getctime)
			threshold = getattr(args, "threshold")
			pathname = getattr(args, "path")
			result = classification.test_data(pathname, db, column, filename, threshold)
			print(json.dumps(result, indent = 4))
		else:
			print("Please, inform the column name.")
			print("Usage: {} --db <database> -c <column>".format(sys.argv[0]))
	# Trainning case: generate a trained model.
	elif getattr(args, "train"):
		pathname = getattr(args, "path")
		if os.path.isdir(pathname):
			try:
				os.listdir(pathname)
			except:
				print("Directory '{}' is not accessible. Please check filesystem permissions.".format(pathname))
				exit(2)
		else:
			print("No such directory: '{}'".format(pathname))
			print("Please, inform the properly path of the data: python3.6 {} --train --path <pathname>".format(sys.argv[0]))
			exit(2)

		path_out = getattr(args, "o")
		if path_out is "":
			path_out = "model/"
		try:
			os.listdir(path_out)
		except:
			print("Directory '{}' is not accessible. Please check filesystem permissions.".format(path_out))
			exit(2)

		threshold = getattr(args, "threshold")
		classification.train_data(pathname, threshold, path_out)
	else:
		print("Usage:")
		print("\t(1) Determine the semantic class: python3.6 {} --db <database> -c <column>".format(sys.argv[0]))
		print("\t(2) Train the entire data: python3.6 {} --train".format(sys.argv[0]))
		print("For more options, type 'python3.6 {} --help'".format(sys.argv[0]))

if __name__ == "__main__":
    main()
