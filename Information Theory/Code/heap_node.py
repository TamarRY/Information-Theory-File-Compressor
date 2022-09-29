from functools import total_ordering
"""
Needed in order to construct nodes for the binary tree representing the unique 
binary string designed by Huffman coding
"""

@total_ordering
class HeapNode:
	def __init__(self, character, frequency):
		self.character = character
		self.frequency = frequency
		self.left = None
		self.right = None

	def __lt__(self, other):
		return self.frequency < other.frequency

	def __eq__(self, other):
		if other is None:
			return False
		if not isinstance(other, HeapNode):
			return False
		return self.frequency == other.frequency
