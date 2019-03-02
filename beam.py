import heapq
 
class Beam(object):
	"""
	A class to represent a Beam data structure

	...
	Attributes
	----------

	heap: list
		list containing probability, token and setence completetion boolean information

	beam_width: int
		size of beam
	"""
	#For comparison of prefixes, the tuple (prefix_probability, complete_sentence) is used.
	#This is so that if two prefixes have equal probabilities then a complete sentence is preferred over an incomplete one since (0.5, False) < (0.5, True)
	def __init__(self, beam_width):
		"""
		Initiate the beam

		Parameters
		----------
		beam_width: int
			size of beam
		"""
		self.heap = list()
		self.beam_width = beam_width

	def add(self, prob, complete, prefix):
		"""
		Add item to the heap queue. Also pop from heap if beam size is greate than max defined

		Parameters
		----------
		prob: float
			Probability value of current sentence in the beam
		complete: boolean
			if the sentence is completed or not
		prefix:
			last n-1 token in the current sentence
		"""

		heapq.heappush(self.heap, (prob, complete, prefix))
		if len(self.heap) > self.beam_width:
			heapq.heappop(self.heap)

	def __iter__(self):
		"""
		Iterate over the heap structure
		"""
		return iter(self.heap)

