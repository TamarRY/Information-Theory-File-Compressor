from datetime import datetime
from struct import *
import struct


class LZWAlgorithm(object):

    def __init__(self, file_extension_encode, file_extension_decode):
        self.file_extension_encode = file_extension_encode
        self.file_extension_decode = file_extension_decode

    def get_encoded_text(self, text):
        """
        Building and initializing the dictionary containing characters with their codes.
        Codes 0-255 represent single bytes from the input file.
        To begin, the dictionary contains only the first 256 entries (ascii characters).
        LZW identifies repeated sequences in the text and adds them to the dictionary.
        """
        n = 16
        size_max = pow(2, int(n))-1

        size_dict = 256
        dictionary = {chr(i): i for i in range(size_dict)}
        string = ""             
        encoded_text = []    

        for character in text:
            string_and_caracter = string + character  
            if string_and_caracter in dictionary:
                string = string_and_caracter
            else:
                encoded_text.append(str(dictionary[string]))
                if len(dictionary) <= size_max:
                    dictionary[string_and_caracter] = size_dict
                    size_dict += 1
                string = character

        if string in dictionary:
            encoded_text.append(str(dictionary[string]))
        
        return encoded_text

    def encode(self, file_input_path, file_output_path):

        print(datetime.now(), ": Start encode LZW")

        with open(file_input_path) as file, open(file_output_path, 'wb') as output:
            file = open(file_input_path)
            text = file.read()
            encoded_text = self.get_encoded_text(text)

            # Storing the compressed string into a file (byte-wise).
            
            print(datetime.now(), ": Start writing encoded text")

            for text in encoded_text:
                output.write(pack('>H', int(text)))

            print(datetime.now(), ": Finish encode LZW")


    def get_decoded_text(self, compressed_text):
        """
        Decoding by taking each code from the compressed file and translating it through
        the dictionary to find what character or characters it represents.
        """
        n = 10
        maximum_table_size = pow(2, int(n))
    
        encoded_text = []
        next_code = 256
        decoded_text = ""
        string = ""

        print(datetime.now(), ": Reading compressed file")

        while True:
            reading_compressed_text = compressed_text.read(2)
            if len(reading_compressed_text) != 2:
                break
            (data, ) = unpack('>H', reading_compressed_text)
            encoded_text.append(data)
       
        # Building and initializing the dictionary.
        size_dict = 256
        dictionary = dict([(x, chr(x)) for x in range(size_dict)])
        
        temp = []
        for code in encoded_text:

            if code not in dictionary:
                dictionary[code] = string + (string[0])
            temp.append(dictionary[code])

            if len(string) != 0:
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]
        decoded_text = "".join(temp)

        return decoded_text

    def decode(self, file_input_path, file_output_path):

        with open(file_input_path, 'rb') as file, open(file_output_path, 'w') as output:
        
            decoded_text = self.get_decoded_text(file)
            
            for element in decoded_text:
                output.write(element)

        
