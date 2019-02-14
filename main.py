from lm import LanguageModel
from corpus import *


def readFile():
	data = []
	file = open('../train_shakespeare.txt')
	for line in file:
		data.append(tokenize(line))
	return data

ngram =int(input("Enter n for n-gram:\n"))
lm = LanguageModel(ngram)
lm.train(readFile())
print(detokenize(lm.generate()))

noOfText =int(input("Enter number of generated text:\n"))
generated = []
for g in range(0, noOfText):
	generated.append(detokenize(lm.generate()))

#i=1
with open('new_shakespeare.txt', 'w') as f:
	for g in generated:
		f.write("%s\n" % g)