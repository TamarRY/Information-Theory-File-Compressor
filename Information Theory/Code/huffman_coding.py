import os
import heapq
from datetime import datetime
from struct import pack

from heap_node import HeapNode


class HuffmanCoding:
	def __init__(self, file_extension_encode, file_extension_decode):
		self.file_extension_encode = file_extension_encode
		self.file_extension_decode = file_extension_decode
		self.heap = []
		self.codes = {}
		self.map_reverse = {}


	def frequency_dictionary(self, text):
		
		"""
		Creating a dictionary containing the frequencies of each character
		using Huffman coding 
		"""
		frequency = {}
		for ch in text:
			if ch not in frequency:
				frequency[ch] = 0
			frequency[ch] += 1

		return frequency
		

	def heap_creation(self, frequency):
		
		"""
		 use HeapNode class to create the binary tree
		"""
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node) #Push the value of the node onto the heap, maintaining the heap invariant


	def trees_merge(self):
		"""
		Choosing the 2 smallest frequency trees, combining them into a new tree with a new parent node with the frequency of
		both of its children until you have no more trees to merge
		"""

		while len(self.heap) > 1:
			node1 = heapq.heappop(self.heap) #Pop and return the smallest item from the heap, maintaining the heap invariant
			node2 = heapq.heappop(self.heap)

			tree_merged = HeapNode(None, node1.frequency + node2.frequency)
			tree_merged.left = node1
			tree_merged.right = node2

			heapq.heappush(self.heap, tree_merged)


	def codes_symbol_creation(self, root, current_code):
		"""
		New code for each symbol at root node:
		for each right arc, add a 1 to the end of the code
		for each right arc, add a 1 to the end of the code
		"""
		if root is None:
			return

		if root.character is not None:
			self.codes[root.character] = current_code
			self.map_reverse[current_code] = root.character
			return

		self.codes_symbol_creation(root.left, current_code + "0")
		self.codes_symbol_creation(root.right, current_code + "1")

	def codes_of_symbols(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.codes_symbol_creation(root, current_code)


	def pad_bits(self, encoded_text):
		"""
		Padding the accumulated bits to 8 '0'  bits if needed
		"""
		pad_with_zeros = 8 - len(encoded_text) % 8
		for i in range(pad_with_zeros):
			encoded_text += "0"

		padded = "{0:08b}".format(pad_with_zeros)
		encoded_text = padded + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		"""
		Output of the binary file
		"""
		byte_array = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			byte_array.append(int(byte, 2))
		return byte_array

	#Compression 

	def encode(self, file_input_path, file_output_path):
		filename, file_extension = os.path.splitext(file_input_path)

		with open(file_input_path, 'rb') as file, open(file_output_path, 'wb') as output:

			print(datetime.now(), ": Start huffman")

			text = file.read()
			text = text.rstrip()

			print(datetime.now(), ": Create frequency")

			frequency = self.frequency_dictionary(text)
			self.heap_creation(frequency)
			self.trees_merge()
			self.codes_of_symbols()

			print(datetime.now(), ": Start encode")

			encoded_text = []
			for character in text:
				encoded_text.append(self.codes[character])
			encoded_text = ''.join(encoded_text)

			print(datetime.now(), ": Padding encoded")

			padded_encoded_text = self.pad_bits(encoded_text)

			print(datetime.now(), ": Get byte array")

			byte_array = self.get_byte_array(padded_encoded_text)

			print(datetime.now(), ": Write file")

			output.write(bytes(byte_array))

			print(datetime.now(), ": Finish huffman")	

	#Starting decompression


	def padding_delete(self, padded_encoded_text):

		# To decode properly, we need to remove the padding added in the compression

		padded = padded_encoded_text[:8]
		pad_with_zeros = int(padded, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1*pad_with_zeros]

		return encoded_text
 
	
	def decode_text(self, encoded_text):

		# Read bit by bit from the compressed text 
		
		code = ""
		decoded_text = []

		for bit in encoded_text:
			code += bit
			if code in self.map_reverse:
				character = self.map_reverse[code]

				decoded_text.append(chr(character))
				code = ""

		return "".join(decoded_text)

	# Decompression
	# Use the read bit to traverse the Huffman coding tree (0 for left and 1 for right), starting from the root node

	def decode(self, file_input_path, file_output_path):
		filename, file_extension = os.path.splitext(file_input_path)

		print(datetime.now(), ": Start decode huffman")

		with open(file_input_path, 'rb') as file, open(file_output_path, 'wb') as output:
			list_bits = []

			print(datetime.now(), ": Read file")

			byte_file = file.read(1)
			while len(byte_file) > 0:
				byte_file = ord(byte_file)
				bits = bin(byte_file)[2:].rjust(8, '0')
				list_bits.append(bits)
				byte_file = file.read(1)
			bit_string = ''.join(list_bits)

			print(datetime.now(), ": Remove padding")

			encoded_text = self.padding_delete(bit_string)

			print(datetime.now(), ": Decoding")

			decompressed_text = self.decode_text(encoded_text)

			print(datetime.now(), ": Writing decoded")

			for element in decompressed_text:
				output.write(pack('B', ord(element)))

			print(datetime.now(), ": Finish huffman")
