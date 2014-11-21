import sys
from tokenizer import *

class Parser():

    def __init__(self, file):
        self.debug = False
        self.tokenizer = Tokenizer(file)
        self.input_token = None
        self.consume_token()

    def consume_token(self):
        self.input_token = self.tokenizer.next_token()

    def parse_error(self,func):
        if self.debug:
            print('PARSING ERROR AT %s -- UNEXPECTED TOKEN "%s"' % (func,self.input_token.value))
        else:
            print('PARSING ERROR -- UNEXPECTED TOKEN "%s"' % self.input_token.value)
        sys.exit(1)

    def match(self, expected_token, func):
        if self.input_token.value == expected_token:
            if self.debug:
                print("MATCHED '%s' from %s" % (self.input_token.value,func))
            self.consume_token()
        else:
            self.parse_error(func)

    def match_type(self, expected_type, func):
        if self.input_token.type == expected_type:
            if self.debug:
                print("MATCHED '%s' from %s" % (self.input_token.value,func))
            self.consume_token()
        else:
            self.parse_error(func)



file = sys.argv[1]
print("PARSING FOR " + file)
#p = Parser(file)
t = Tokenizer(file)
token = t.next_token()
while token.value != '$$':
    print(token.value + ':' + token.type)
    token = t.next_token()








