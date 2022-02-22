import operator

def main():
    #Create instance of Decryptor class and call apropriate functions
    dec = Decryptor('cryptograms_list.txt')
    dec.init_cryptograms()
    dec.output()


class Cryptogram:

    def __init__(self, cipher):
        # Table of encrypted chars
        self.chars = []
        tmp = str(cipher).split(' ')

        for ch in tmp:
            self.chars.append(chr(int(ch, 2)))
            

    def get_char(self, index):
        if index < len(self.chars):
            return self.chars[index]
        else:
            return '*'


class Decryptor:

    def __init__(self, file_name):
        # List of cryptograms from file
        self.cryptograms_list = []

        # Input file
        self.file_name = file_name

        # Dict with letters and its frequency (for Polish language)
        self.letters_freq = {
            'a': 89, 'i': 82, 'o': 78, 'e': 77, 'z': 56, 'n': 55, 'r': 47, 'w': 47, 's': 43, 't': 40, 'c': 40, 'y': 38,
            'k': 35, 'd': 33, 'p': 31, 'm': 28, 'u': 25, 'j': 23, 'l': 21, 'b': 15, 'g': 14, 'h': 11, 'f': 3, 'q': 1,
            'v': 1, 'x': 1, ' ': 100, ',': 16, '.': 10, '-': 10, '"': 10, '!': 10, '?': 10, ':': 10, ';': 10, '(': 10,
            ')': 10
        }

        # Big letters
        for i in range(65, 91):
            self.letters_freq[chr(i)] = 10

        # Numbers
        for i in range(48, 58):
            self.letters_freq[chr(i)] = 10

    # From every line in cryptograms_list.txt file we create new cryptogram
    def init_cryptograms(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                self.cryptograms_list.append(Cryptogram(line))

    # Main function for searching key
    def find_key(self):
        
        #Found key
        key = []

        # Length of the longest cryptogram
        longest = 0

        for crypt in self.cryptograms_list:
            if len(crypt.chars) > longest:
                longest = len(crypt.chars)

        for i in range(0, longest):
            # Dict with signs which could be key
            possible_key = {}

            # Cryptograms which length is smaller than current i
            matching_cryptograms = []   

            # Looking for cryptograms which length is bigger than i
            for crypt in self.cryptograms_list:
                if i < len(crypt.chars):
                    matching_cryptograms.append(crypt)

            for crypt in matching_cryptograms:
                for possible, frequency in self.letters_freq.items():

                    # Tuple of XOR chars of cryptogram with letters in alphabet and frequency of letter
                    tmp = (ord(crypt.get_char(i)) ^ ord(possible), frequency)

                    # Put into dict frequency of XOR result
                    if tmp[0] not in possible_key.keys():
                        possible_key[tmp[0]] = tmp[1]
                    else:
                        possible_key[tmp[0]] = possible_key.get(tmp[0]) + frequency

            # Sort possible keys to make searching easier
            tmp_sorted = sorted(possible_key.items(), key=operator.itemgetter(1), reverse=True)
            possible_key = dict(tmp_sorted)
            # We assume firstly that space is the best key
            best_possible = ord(' ')
            # Best counter tells us for how many cryptograms we got letter from language
            best_counter = 0

            for possible in possible_key.keys():
                counter = 0

                for crypt in matching_cryptograms:
                    # Check if XOR returns char from alphabet
                    if (chr(ord(crypt.get_char(i)) ^ possible)) in self.letters_freq.keys():
                        counter += 1

                # The best key is that which gives a sign from alphabet the most often. 
                if counter > best_counter:
                    best_counter = counter
                    best_possible = possible

            # Then we append our best option to key
            key.append(best_possible)
        return key

    # Write decrypted messages to files
    def output(self):
        key = self.find_key()
        with open('output.txt', 'w') as file:
            for crypt in self.cryptograms_list:
                for i in range(0, len(crypt.chars)):
                    file.write(chr(ord(crypt.get_char(i)) ^ key[i]))
                file.write('\n')
        #Our message to test decryptor        
        with open('result.txt', 'w') as result_file:
            with open('to_decrypt.txt', 'r') as to_decrypt:
                crypto = Cryptogram(to_decrypt.read())
            for i in range(0, len(crypto.chars)):
                result_file.write(chr(ord(crypto.get_char(i)) ^ key[i]))
            result_file.write('\n')
                




if __name__ == '__main__':
    main()