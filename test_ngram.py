import unittest
from corpus import *
from lm import LanguageModel

class TestCorpus(unittest.TestCase):
	def test_punctuation_remove_string(self):
		result = tokenize("[to john], Hey come (here)")
		self.assertEqual(result, ["[to","john]",",","hey","come","here"])
	
	def test_contraction_string(self):
		result = tokenize("I'd say you'd do it, won't you?")
		self.assertEqual(result, ["i","would","say","you","would","do","it",",","will","not","you","?"])
	
	def test_punctuation_capitalization(self):
		result = detokenize(["to","john",".","hey","come","here"])
		self.assertEqual(result, "To john. Hey come here")

	def test_ngram(self):
		result = LanguageModel(2).get_ngrams(["hello", "world","lmao"])
		self.assertEqual(result, [(None, 'hello'), ('hello', 'world'), ('world', 'lmao'), ('lmao', None)])


if __name__ == "__main__":
	unittest.main()