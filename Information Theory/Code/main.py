from LZW import LZWAlgorithm
from huffman_coding import HuffmanCoding

class CompressionManager(object):
    def __init__(self, input_path):
        self.input_path = input_path
        self.compressions_list = []

    def add_compression(self, compression):
        self.compressions_list.append(compression)

    def run(self):
        encode_output_path = './Output/encode'
        decode_output_path = './Output/decode'

        for i in range(len(self.compressions_list)):
            output_path = f'{encode_output_path}_{i}.{self.compressions_list[i].file_extension_encode}'
            self.compressions_list[i].encode(self.input_path, output_path)
            self.input_path = output_path

        self.compressions_list = self.compressions_list[::-1]

        for i in range(len(self.compressions_list)):
            output_path = f'{decode_output_path}_{i}.{self.compressions_list[i].file_extension_decode}'
            self.compressions_list[i].decode(self.input_path, output_path)
            self.input_path = output_path
        print(f'Final output path: {self.input_path}')

def main():
    compression_manager = CompressionManager('./Input/dickens.txt')
    compression_manager.add_compression(LZWAlgorithm(file_extension_encode='bin', file_extension_decode='txt'))
    compression_manager.add_compression(HuffmanCoding(file_extension_encode='zip', file_extension_decode='bin'))
    compression_manager.run()

if __name__ == "__main__":
    main()


