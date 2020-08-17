import pandas as pd 
import re
import unicodedata
import inflect
import numpy as np

class DataPreprocessor(object):
	"""docstring for DataPreprocessor"""
	def __init__(self, df):
		self.df = df
		p = inflect.engine()
		replace_patterns = [
			(r'[\(\)\"\/\.\-\~\º\'\;\,]'," "),
			('s.a', 'sa'),
			('s/a', 'sa')]
		for i in range(1,21):
			for pre, pos in [('(\D)','(\D)'), ('^','(\D)'), ('(\D)','$')]:
				pattern = pre + '\d'*i + pos
				replace = ' p' + p.number_to_words(i) + 'd '
				replace_patterns.append((pattern, replace))
		replace_patterns += [('\d+', 'parsedd')]
		#replace_patterns

		self.compiled_replace_patterns = [(re.compile(p[0]), p[1]) for p in replace_patterns]



	def pre_processing(self):
		#self.df = self.df.replace(np.nan, '', regex=True)
		self.df = self.df.applymap(str)
		self.df = self.df.applymap(str.lower)
		self.df = self.df.applymap(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore'))

		for pattern, replace in self.compiled_replace_patterns:
			self.df = self.df.applymap(lambda x: re.sub(pattern, replace,x).rstrip() )
		
		self.df = self.df.applymap(lambda x: re.sub(r" +", r" ", x).rstrip() )
		return self.df




