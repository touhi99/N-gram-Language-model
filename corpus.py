import string
import re

def tokenize(text):
	"""
	Tokenize text based on several parameters using Reg expression 
	(punctuation, capitalization, contraction etc)

	Parameters
	----------
	text: string
		Takes each lines from the train data

	Return
	------
	list
		Tokenized string in a list form
	"""

	text = text.replace('--', ' ')
	text = clean_regex(text)
	#punctuation_table = dict((ord(char), None) for char in string.punctuation) 
	#text = text.translate(punctuation_table)

	# remove certain punctuation chars
	text = re.sub("[()]", "", text)
	# collapse multiples of certain chars
	text = re.sub('([.-])+', r'\1', text)

	if text[-1] in ".,!?":
		text = text[:-1]+" "+text[-1]
	# pad sentence punctuation chars with whitespace
	text = re.sub('([^0-9])([.,!?])([^0-9])', r'\1 \2 \3', text)
	tokens = text.split()
	#tokens = [word for word in tokens if word.isalpha()]
	tokens = [word.lower() for word in tokens]
	return tokens

def clean_regex(text):
	"""
	Clean contraction from the text

	Parameters
	----------
	text: string
		Text lines of string

	Return
	------
	string
		Cleaned contraction
	"""
	text = re.sub(r"i'm", "i am", text)
	text = re.sub(r"he's", "he is", text)
	text = re.sub(r"she's", "she is", text)
	text = re.sub(r"that's", "that is", text)
	text = re.sub(r"what's", "what is", text)
	text = re.sub(r"where's", "where is", text)
	text = re.sub(r"\'ll", " will", text)
	text = re.sub(r"\'ve", " have", text)
	text = re.sub(r"\'re", " are", text)
	text = re.sub(r"\'d", " would", text)
	text = re.sub(r"won't", "will not", text)
	text = re.sub(r"can't", "can not", text)
	return text

def detokenize(tokens):
	"""
	Detokenize list of tokens based on parameters using regex (punctuation, capitalization,
	padding etc)

	Parameters
	----------
	tokens: list
		list of tokens generated

	Return
	------
	string
		As a form of text
	"""
	tokens = list(filter(None.__ne__, tokens))
	text = ' '.join(tokens)
	# correct whitespace padding around punctuation
	text = re.sub('\\s+([.,!?])\\s*', r'\1 ', text)
	# capitalize first letter
	text = text.capitalize()
	# capitalize letters following terminated sentences
	text = re.sub('([.!?]\\s+[a-z])', lambda c: c.group(1).upper(), text)
	return text


#tokenizer = tokenize("[will], not you.")
#print(tokenizer)
#detokenizer = detokenize(["to","john",".","hey","come","here"])
#print(detokenizer)