from struct import pack, unpack
from rijndael import rijndael

try:
    from hashlib import sha256
except ImportError: # Python < 2.5
    try:
        from Crypto.Hash import SHA256
        sha256 = SHA256.new
    except ImportError:
        print "Update to python 2.5+, or install PyCrypto."
        raise ImportError, "No SHA256"

try:
    from os import urandom
except ImportError: # Python < 2.3, or incompatible os
    # os.urandom is far greater than randomrandint. I recomend you change
    # this and make it work with your operating systems random.
    from random import randint
    urandom = lambda s : '%s' % randint(0, s**s)

class PyPPP(object):
    __version__ = 3.1 # PPP Specification
    character_set = ['!', '#', '%', '+', '2', '3', '4', '5', '6', '7',
                     '8', '9', ':', '=', '?', '@', 'A', 'B', 'C', 'D',
                     'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                     'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                     'w', 'x', 'y', 'z']
    code_length = 4
    
    columns_on_card = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    lines_per_card = 10
    row_per_card = 7
    amount_per_card = 70
    
    def __init__(self, key=''):
        if key:
            self.key = key
            self.rijndael = rijndael(self.key.decode('hex'), block_size = 16)
    
    def generate_random_sequence_key(self):
        self.key = sha256(urandom(256)).hexdigest()
        self.rijndael = rijndael(self.key.decode('hex'), block_size = 16)
    
    def retrieve_passcode(self, count):
        if not hasattr(self, 'rijndael'):
            self.rijndael = rijndael(self.key.decode('hex'), block_size = 16)
        
        # Pack the count into a 128-bit block (1> 0x01x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00)
        block_128bit = pack('<2Q', (count & 0xFFFFFFFF), (count << 128) & 0xFFFFFFFF)
        
        # Feed the 128-bit block to rijndael
        block = self.rijndael.encrypt(block_128bit)
        
        # Swap the endian
        block = block[::-1]
        
        # Convert the block into a number
        num = 0
        for x in block:
            num = num * 256
            num = num + ord(x)
        
        passcode = []
        character_set_len = len(self.character_set)
        
        # Perform the long division
        for i in range(self.code_length):
            passcode.append(self.character_set[num%character_set_len])
            num = num/character_set_len
        
        return ''.join(passcode) # Join the passcode into a string seperated by '' (nothing)
    
    def retrieve_passcodes(self, first, last):
        passcodes = []
        for num in range(last-first+1):
            passcodes.append(self.retrieve_passcode(num+first))
        return passcodes
    
    def retrieve_card(self, card):
        #total = self.lines_per_card * self.row_per_card
        last = (self.amount_per_card * card) - 1
        first = last - self.amount_per_card + 1
        return self.retrieve_passcodes(first, last)
    
    def get_sequence_info(self, count):
        card = ((count)/self.amount_per_card) + 1
        num_on_card = (count % self.amount_per_card)
        column = num_on_card % self.row_per_card
        row = (num_on_card/self.row_per_card) + 1
        return {
            'card': card,
            'column': self.columns_on_card[column],
            'row': row,
        }
