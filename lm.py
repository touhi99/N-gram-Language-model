from itertools import islice
import functools
import operator
import random


class LanguageModel:
	def __init__(self, n):
		self.ngram = n
		self.vocabulary = set()
		self.count = {}
		self.smoothing_alpha = 0.5

	def train(self, token_sequences):
		self.vocabulary = set(functools.reduce(operator.concat, token_sequences))
		self.vocabulary.add(None)

		for item in token_sequences:
			for subitem in self.get_ngrams(item):
				if subitem[:self.ngram-1] not in self.count:
					self.count[subitem[:self.ngram-1]] = {subitem[self.ngram-1:][0]: 1}
				else:
					if subitem[self.ngram-1:][0] in self.count[subitem[:self.ngram-1]]:
						self.count[subitem[:self.ngram-1]][subitem[self.ngram-1:][0]] += 1
					else:
						self.count[subitem[:self.ngram-1]][subitem[self.ngram-1:][0]] = 1
	def normalize(self, word_counts):
		prob_dict = {}
		total = sum(word_counts.values())
		for key, value in word_counts.items():
			prob_dict[key] = value/total
		return prob_dict

	def p_next(self, tokens):
		tokens = tokens[-(self.ngram-1):]
		return self.normalize(self.count[tuple(tokens)])
		'''
		prob_dict = {}
		total = sum(self.count[tuple(tokens)].values())
		#sorted disabled
		for key, value in (self.count[tuple(tokens)].items()):
			#prob = (value + self.smoothing_alpha) / (total + ( len(self.vocabulary)*self.smoothing_alpha) )
			prob = value / total
			prob_dict[key] = prob
		return prob_dict
		'''

	def generate(self, num=1):
		#tokens = token = [None]* (self.ngram-1)
		tokens = [None]* (self.ngram-1)
		while 1:
			tokens.append(self.sample(self.p_next(tokens)))
			#token = tokens[-(self.ngram-1):]
			if tokens[-1:]==[None]:
				break
		return tokens	

	def sample(self, distribution):
		print(distribution)
		rand = random.random()
		total = 0
		for k, v in distribution.items():
			total += v
			if rand <= total:
				return k


	def window(self, seq, n):
	    it = iter(seq)
	    result = tuple(islice(it, n))
	    if len(result) == n:
	        yield result
	    for elem in it:
	        result = result[1:] + (elem,)
	        yield result

	def get_ngrams(self, token):
		n = self.ngram
		sequence = []
		if not token:
			return sequence
		token = [None]*(n-1) + token + [None]*(n-1)
		result = self.window(token, n)
		for r in result:
			sequence.append(r)
		return sequence
