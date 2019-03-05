from itertools import islice
import functools
import operator
import random, collections
import math
from beam import *
import numpy as np
import heapq
import pprint
import time

"""
Terminology:
SOS - Start of tokens
EOS - End of tokens
UNK - Unknown tokens

"""
class LanguageModel:
	"""
	A class used to represent Language model

	...
	Attributes
	----------

	ngram : int
		Value of n in n-gram
	vocabulary : set
		Unique tokens in the training data
	count : dictionary
		N-gram representation with word count in key-value
	beam_flag : boolean
		If a beam search is set or unset
	beam_width : int
		Size fo the beam
	smoothing_alpha : float
		Smoothing hyperparameters
	"""
	def __init__(self, n):
		"""
		Initiate the Language Model

		Parameters
		----------
		n : int
			Value of n in n-gram
		"""
		self.ngram = n
		self.vocabulary = set()
		self.count = {}
		self.beam_flag = False
		self.beam_width = 20
		self.smoothing_alpha = 0.001

	def train(self, token_sequences):
		"""
		Train the Language model from given texts

		Add tokens in n-gram form to the dictionary , additionally add unique tokens to vocabulary.
		Add 'None' as Start/End of token and '<UNK>' as Out-of-vocabulary token

		Paramters
		---------

		token_sequences: list
			A nested list containing all the tokens from the training data
		"""
		print("Training started...")
		start_time = time.time()
		self.vocabulary = set(flatten(token_sequences))
		self.vocabulary.add(None)
		#self.vocabulary.add('<UNK>')
		#print(len(self.vocabulary))
		#print("--- %s seconds ---" % (time.time() - start_time))
		for item in token_sequences:
			for subitem in self.get_ngrams(item):
				if subitem[:self.ngram-1] not in self.count:
					self.count[subitem[:self.ngram-1]] = {subitem[self.ngram-1:][0]: 1}
				else:
					if subitem[self.ngram-1:][0] in self.count[subitem[:self.ngram-1]]:
						self.count[subitem[:self.ngram-1]][subitem[self.ngram-1:][0]] += 1
					else:
						self.count[subitem[:self.ngram-1]][subitem[self.ngram-1:][0]] = 1
			if len(self.count) % 1000 == 0:
				print("Training {} tokens".format(len(self.count)))

		#self.count[('<UNK>',)] = {'<UNK>': random.random()}
		print(len(self.count))
		print(len(self.vocabulary))
	
	def normalize(self, word_counts):
		"""
		Normalize the probablility distribution based on counts
		Smoothen based on alpha-smoothing

		TODO: perpelxity flag condition

		Parameters
		----------
		word_counts: dictionary
			containing word and their count as key-value pair
		perplexity_flag: int
			flag to check if the function is called for generation or from perplexity checking

		Returns
		-------
		dictionary
			key-value pair as probability distribution.
		"""
		prob_dict = {}
		total = sum(word_counts.values())
		for key, value in word_counts.items():
			prob_dict[key] = (value+self.smoothing_alpha)/(total+len(self.vocabulary)*self.smoothing_alpha )
			#prob_dict[key] = value/total
		
		return prob_dict

	def p_next(self, tokens):
		"""
		Function returns the most probable next token from the last n-1 gram

		For unigram, it choose a random token and count its probability distribution
		For n-gram n>1, it calculates probability distribution of last n-1 gram 

		Parameters
		----------
		tokens: list
			A list of token

		Returns
		-------
		dictionary
			Containing key as the word, and value as the probability for the given ngram/token

		"""

		tokens = tokens[-(self.ngram-1):]
		if self.ngram!=1:
			return self.normalize(self.count[tuple(tokens)])
		else:
			rand_pair = random.choice( list(self.count[()].items()))
			rand_prob = rand_pair[1] / len(self.vocabulary)
			return {rand_pair[0]:rand_prob}

	def generate(self):
		"""
		Function generates sentences based on trained model

		If it uses beam search, most probable sentence is extracted from beam
		If it doesn't use beam, it keeps generating most probable token until it find None as EOS token

		Returns
		-------
		list
			A sentences token in the form of list
		"""

		tokens = [None]* (self.ngram-1)
		if self.beam_flag:
			tokens.extend(self.beam_search(tokens, self.beam_width)[0])
		else:
			while 1:
				tokens.append(self.sample(self.p_next(tokens))[0])
				if tokens[-1:]==[None]:
					break
		return tokens	

	def sample(self, distribution):
		"""
		Sample takes a word with distribution of probability and returns the probable word and value

		If beam search is off, it chooses a random choice of probability from the value
		If beam search is on, it chooses top-k number of the key-value and add them in beam list

		Parameters
		----------
		distribution: dictionary
			Key-value pair containing word and their probability

		Returns
		-------
		tuple
			If beam search is off containing a (key,value)
		Or
		list
			If beam search on, containing list of tuples as (key, value)
		"""

		#print(distribution)
		beam_list = set()
		counter = 0
		k = np.random.choice(list(distribution.keys()), 1, list(distribution.values()))[0]
		v = distribution[k]
		if not self.beam_flag:
			return (k, v)
		else:
			#return distribution.items()
			# we take at max 5 word for our case
			while counter <= 5:
				beam_list.add((k, v))
				k = np.random.choice(list(distribution.keys()), 1, list(distribution.values()))[0]
				v = distribution[k]
				if len(beam_list) == self.beam_width:
					break
				counter+=1
			#print( list(beam_list))

			return list(beam_list)
			
			

	def perplexity(self, data):
		"""
		Perplexity is computed from the test set data

		If ngram is matched in the training data, it adds the probability distribution on perplexity
		If ngram is not matched, <UNK> is considered and a random probability distribution is added on perplexity

		Parameters
		----------
		data: list
			Test set tokens in a form of nested list

		Returns
		-------
		float
			Calculated perplexity value
		"""

		perplexity = 0
		num = 0
		for item in data:
			for subitem in self.get_ngrams(item):
				num+= 1
				perplexity += math.log(self.ngram_probability(subitem[:self.ngram-1], subitem[self.ngram-1:][0]), 2)
		print(perplexity)
		perplexity = math.pow(2, -1*(perplexity/num))
		return perplexity

	def ngram_probability(self, ngram, word):
		"""
		Probability counting for perplexity. For simplicity different function is created to calculate.

		Parameters
		----------
		ngram: tuple
			tuple to match with the count dictionary keys
		word: string
			word to match up with the specific ngram

		Returns
		-------
		float
			probability of the specific (ngram, word)
		"""
		if ngram in self.count:
			if word in self.count[ngram]:
				count = self.count[ngram][word]
				total = sum(self.count[ngram].values())
			else:
				count = 1
				total = sum(self.count[ngram].values())+1
			prob = (count+self.smoothing_alpha)/ (total+ (len(self.vocabulary)*self.smoothing_alpha))
		else:
			count = 0
			total = 1
			prob = random.random() / len(self.vocabulary)
		return prob


	def get_ngrams(self, token):
		"""
		Gives n-gram from a list of tokens.

		None is padded as SOS/EOS tokens and window function slices through list of tokens and give
		n-grams

		Parameters
		----------
		token : list
			List of sentence token

		Returns
		-------
		list
			Sequence or tuples in a form of n-gram from the token list
		"""
		sequence = []
		if not token:
			return sequence
		if self.ngram!=1:
			token = [None]*(self.ngram-1) + token + [None]*(self.ngram-1)
		else:
			token = token + [None]
		result = window(token, self.ngram)
		for r in result:
			sequence.append(r)
		return sequence

	def beam_search(self, tokens, beam_width=10, clip_len=15):
		"""
		Search and return the most probable sentence from the current beam

		Parameters
		----------
		tokens: list
			List of initial token 
		beam_width: int
			Beam size. Default value is 10
		clip_len: int
			Clip length to check the most possible lowest value of beam size

		Returns
		-------
		tuple
			Most probable sentence with its probability, not including the SOS token. 
		"""
		prev_beam = Beam(beam_width)
		prev_beam.add(1.0, False, tokens)
		while True:
			curr_beam = Beam(beam_width)
			#Add complete sentences that do not yet have the best probability to the current beam, the rest prepare to add more words to them.
			for (prefix_prob, complete, prefix) in prev_beam:
				if complete == True:
					 if len(prefix) >= clip_len:
					 	curr_beam.add(prefix_prob, True, prefix)
				else:
				#Get probability of each possible next word for the incomplete prefix.
					for next_word, next_prob in self.sample(self.p_next(prefix)):
						if next_word == None: #if next word is the end token then mark prefix as complete and leave out the end token
							if len(prefix) >= clip_len:
								curr_beam.add(prefix_prob*next_prob, True, prefix)
						else: #if next word is a non-end token then mark prefix as incomplete
							curr_beam.add(prefix_prob*next_prob, False, prefix+[next_word])

			(best_prob, best_complete, best_prefix) = max(curr_beam)

			if best_complete == True and len(best_prefix) >= clip_len: #if most probable prefix is a complete sentence or has a length that exceeds the clip length (ignoring the start token) then return it
				return (best_prefix[1:], best_prob) #return best sentence without the start token and together with its probability
			prev_beam = curr_beam

	def count_common_ngram(self, count = 5):
		"""
		Count the most common ngram from trained data
		Excluding token with EOS/SOS and <UNK> from vocabulary.

		Parameters
		----------
		count : int
			Number of top ngram to show. Default is 5
		"""

		temp_dict = {}
		for k, v in self.count.items():
			if None not in k and '<UNK>' not in k:
				for k2, v2 in v.items():
					if k2!=None and k2!='<UNK>':
						temp_dict[k + (k2,)] = v2
		sorted_d = sorted(temp_dict.items(), key=operator.itemgetter(1))[-count:]
		pprint.pprint(sorted_d)


def window(seq, ngram):
	"""
	Function returns iterating each element as sliding window

	Parameters
	----------
	seq: list
		List of tokens in sequence
	ngram: int
		Value of n in ngram
	Returns
	-------
	generators
		tuples as size of n-gram iterating over whole sequence

	"""
	it = iter(seq)
	result = tuple(islice(it, ngram))
	if len(result) == ngram:
		yield result
	for elem in it:
		result = result[1:] + (elem,)
		yield result

def flatten(container):
	"""
	Recursively flatten a nested list to 1-D list

	Parameters
	----------
	container: list
		Containing a nested list of tokens

	Returns
	-------
	geenrators
		a single form of list from the nested list
	"""
	for i in container:
		if isinstance(i, (list,tuple)):
			for j in flatten(i):
				yield j
		else:
			yield i
