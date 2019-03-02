"""N-gram Language Model.

Usage:
  main.py train [--n <n>] [--path <path>]
  main.py generate [--lines <n>] 
  main.py perplexity [--path <path>]
  main.py common [--number <n>]
  main.py --help

Options:
  --n <n>     		Number of n-gram
  --path <path>     Train/Test file path
  --lines <n>		No. of lines to be generated
  --number <n>		No. of n-gram to show
  --help     		Show this screen


"""

'''
@Author: Touhidul Alam
'''

from lm import LanguageModel
from corpus import *
import pickle
from docopt import docopt
import click

def readFile(filename):
	"""
	Read a file, return file data as tokenized in list form

	Parameters
	----------
	filename: path
		File location

	Returns
	-------
	list
		tokenized data in a nested list form
	"""
	data = []
	file = open(filename)
	for line in file:
		data.append(tokenize(line))
	return data

def loadPickle():
	"""
	Load saved model after training and get the saved object information

	TODO: Static file saved for now

	Return
	------
	Object
		Language model object saved from training
	"""
	f = open('trained_model_ngram.pkl','rb')
	lm = pickle.load(f)
	f.close()
	return lm

def main(args):
	"""
	Main function of the program operates based on the argument provided.

	Train
		- Ask for ngram
		- Ask for training file path
		- Train language model
		- Save the trained model

	Generate
		- Load the saved model from pickle file
		- Ask for a beam search (y/n)
			- Ask Beam length
		- Print one generated sentence in terminal
		- Ask for number of sentences to be generated on file
		- Save the input number of sentences in a file (Default: new_shakespeare.txt)

	Perplexity
		- Load Pickle file
		- Ask the test set file path
		- Print perplexity value

	Common
		- Load pickle
		- Ask number of most common ngram
		- Print the most common ngram with their occurence number.

	"""
	if args['train']:
		if not args['--n']:
			ngram = input("Please enter n for n-gram (Default: 3)-\n")
			if not ngram:
				ngram=3
		else:
			ngram=args['--n']
		lm = LanguageModel(int(ngram))

		if not args['--path']:
			path = input("Please enter path of the file-\n")
		else:
			path = args['--path']
		lm.train(readFile(path))
		print("N-gram training completed")
		print("Saving the model")
		f = open('trained_model_ngram.pkl','wb')
		pickle.dump(lm, f)
		f.close()
		print("Model saved")

	if args['generate']:
		lm = loadPickle()

		if click.confirm('Do you want to generate with Beam search?', default=True):
			lm.beam_flag = True
			beam_size =input("Enter beam size (Default: 20)-\n")
			if not beam_size:
				lm.beam_width = beam_size
		else:
			lm.beam_flag = False
		print("Generating one sentence in terminal...")
		print(detokenize(lm.generate()))
		if not args['--lines']:
			noOfText =input("Enter number of generated text you want to save (Default: 10)-\n")
			if not noOfText:
				noOfText=10
		else:
			noOfText = args['--lines']
		generated = []
		for g in range(0, int(noOfText)):
			generated.append(detokenize(lm.generate()))

		with open('new_shakespeare.txt', 'w') as f:
			for g in generated:
				f.write("%s\n" % g)
		print("Sentence file generated in current folder")

	if args['perplexity']:
		lm = loadPickle()
		if not args['--path']:
			path = input("Please enter path of the test file-\n")
		else:
			path = args['--path']
		print("Perplexity for {}-gram is {}".format(lm.ngram,lm.perplexity(readFile(path))))

	if args['common']:
		lm = loadPickle()
		if args['--number']:
			number = args['--number']
		else:
			number = 5
		lm.count_common_ngram(int(number))


if __name__ == '__main__':
	argument = docopt(__doc__)
	main(argument)