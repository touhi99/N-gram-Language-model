import string
import re

def tokenize(text):
	text = text.replace('--', ' ')
	text = clean_regex(text)
	punctuation_table = dict((ord(char), None) for char in string.punctuation) 
	text = text.translate(punctuation_table)
	tokens = text.split()
	tokens = [word for word in tokens if word.isalpha()]
	tokens = [word.lower() for word in tokens]
	return tokens

def clean_regex(text):
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

#implement later 
def detokenize(tokens):
	tokens = list(filter(None.__ne__, tokens))
	text = ' '.join(tokens)
	return text


#tokenizer = tokenize("Thou art a cobbler, I've art thou?")
#print(tokenizer)
#detokenizer = detokenize(tokenizer)
#print(detokenizer)