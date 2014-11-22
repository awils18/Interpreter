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

    def match(self, *args, **kwargs):
        for expected_token in args:
            if self.input_token.value == expected_token:
                if self.debug:
                    print("MATCHED '%s' from %s" % (self.input_token.value,kwargs['func']))
                self.consume_token()
            else:
                self.parse_error(kwargs['func'])

    def match_type(self, expected_type, func):
        if self.input_token.type == expected_type:
            if self.debug:
                print("MATCHED '%s' from %s" % (self.input_token.value,func))
            self.consume_token()
        else:
            self.parse_error(func)

    def fLambda(self):
        self.match('(','lambda')
        self.params()
        self.expression()
        self.match(')')

    def params(self):
        self.match('(')
        self.match_type('ID')
        self.params()
        self.match(')')

    def params_list(self):
        if self.input_token.type == 'ID':
            self.match_type('ID')
            self.params_list()
        elif self.input_token.value == ')':
            pass
        else:
            self.parse_error('params_list')

    def expression(self):
        if self.input_token.type == 'ID':
            self.match_type('ID')
        elif self.input_token.value == '(':
            self.match('(')
            self.operator()
            self.expression()
            self.expression()
            self.match(')')

    def operator(self):
        if self.input_token.value in ['+','-','*','/']:
            self.match(self.input_token.value)
        else:
            self.parse_error('operator')

    def application(self):
        pass

    def head(self):
        pass

    def tail(self):
        pass


    





file = sys.argv[1]
print("PARSING FOR " + file)
p = Parser(file)



