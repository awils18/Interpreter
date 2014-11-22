import sys
from tokenizer import *

class Parser():

    def __init__(self, file):
        self.debug = False
        self.tokenizer = Tokenizer(file)
        self.input_token = None
        self.consume_token()
        self.statement_count = 0
        self.statement_tokens = []

    def consume_token(self):
        self.input_token = self.tokenizer.next_token()
        while self.input_token.type == 'meta':
            self.match_type('meta','consume_token')

    def parse_error(self,func):
        if self.debug:
            print('PARSING ERROR AT %s -- UNEXPECTED TOKEN "%s"' % (func,self.input_token.value))
            print('TYPE == %s' % self.input_token.type)
        else:
            print('PARSING ERROR -- UNEXPECTED TOKEN "%s"' % self.input_token.value)
            print('TYPE == %s' % self.input_token.type)
        sys.exit(1)

    def match(self, *args, **kwargs):
        for expected_token in args:
            if self.input_token.value == expected_token:
                if self.debug:
                    print("MATCHED '%s' from %s" % (self.input_token.value,kwargs['func']))
                self.statement_tokens.append(self.input_token)
                self.consume_token()
            else:
                self.parse_error(kwargs['func'])

    def match_type(self, expected_type, func):
        if self.input_token.type == expected_type:
            if self.debug:
                print("MATCHED '%s' from %s" % (self.input_token.value,func))
            if self.input_token.type != 'meta':
                self.statement_tokens.append(self.input_token)
            self.consume_token()
        else:
            self.parse_error(func)

    def output_statement(self):
        for t in self.statement_tokens:
            print(t.value + ' ', end='')
        print()
        self.statement_tokens = []

    def lambda_list(self):
        if self.debug:
            print("EXPLORING lambda_list")
        if self.input_token.value == '(':
            self.statement_count += 1
            print('PARSING Statement #%s:' % self.statement_count)
            self.lambda_expression()
            self.output_statement()
            print('-------- SUCCESS! --------\n')
            self.lambda_list()
        elif self.input_token.value == '$$':
            pass
        else:
            self.parse_error('lambda_list')

    def lambda_expression(self):
        if self.debug:
            print("EXPLORING lambda_expression")
        self.match('(', func='lambda_expression')
        self.lambda_expression_tail()

    def lambda_expression_tail(self):
        if self.debug:
            print("EXPLORING lambda_expression_tail")
        if self.input_token.value == 'lambda':
            self.match('lambda', func='lambda_expression_tail')
            self.params()
            self.expression()
            self.match(')', func='lambda_expression_tail')
        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            self.head()
            self.tail()
            self.match(')', func='lambda_expression_tail')

    def lambda_func(self):
        if self.debug:
            print("EXPLORING lambda_func")
        self.match('(','lambda', func='lambda_func')
        self.params()
        self.expression()
        self.match(')',func='lambda_func')

    def params(self):
        if self.debug:
            print("EXPLORING params")
        self.match('(', func='params')
        self.match_type('ID', 'params')
        self.params_list()
        self.match(')', func='params')

    def params_list(self):
        if self.debug:
            print("EXPLORING params_list")
        if self.input_token.type == 'ID':
            self.match_type('ID', func='params_list')
            self.params_list()
        elif self.input_token.value == ')':
            pass
        else:
            self.parse_error('params_list')

    def expression(self):
        if self.debug:
            print("EXPLORING expression")
        if self.input_token.type == 'ID':
            self.match_type('ID', 'expression')
        elif self.input_token.type == 'number':
            self.match_type('number', 'expression')
        elif self.input_token.value == '(':
            self.match('(', func='expression')
            self.expression_tail()

    def expression_tail(self):
        if self.debug:
            print("EXPLORING expression_tail")
        if self.input_token.value in ['+','-','*','/']:
            self.operator()
            self.expression()
            self.expression()
            self.match(')', func='expression_tail')
        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            self.head()
            self.tail()
            self.match(')', func='expression_tail')
        else:
            self.parse_error('expression_tail')

    def operator(self):
        if self.debug:
            print("EXPLORING operator")
        if self.input_token.value in ['+','-','*','/']:
            self.match(self.input_token.value, func='operator')
        else:
            self.parse_error('operator')

    def application(self):
        if self.debug:
            print("EXPLORING application")
        self.match('(', func='application')
        self.head()
        self.tail()
        self.match(')', func='fLambda')

    def head(self):
        if self.debug:
            print("EXPLORING head")
        if self.input_token.value == '(':
            self.match('(', func='fLambda')
            self.application_head()
        elif self.input_token.type == 'ID':
            self.match_type('ID','head')
        else:
            self.parse_error('head')

    def application_head(self):
        if self.debug:
            print("EXPLORING application_head")
        if self.input_token.value == 'lambda':
            self.match('lambda', func='application_head')
            self.params()
            self.expression()
            self.match(')', func='application_head')
        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            self.head()
            self.tail()
            self.match(')', func='application_head')
        else:
            self.parse_error('application_head')

    def tail(self):
        if self.debug:
            print("EXPLORING tail")
        if self.input_token.type == 'ID':
            self.match_type('ID', 'tail')
        elif self.input_token.type == 'number':
            self.match_type('number', 'tail')
        elif self.input_token.value == '(':
            self.match('(', func='tail')
            self.application_tail()
        else:
            self.parse_error('tail')

    def application_tail(self):
        if self.debug:
            print("EXPLORING application_tail")
        if self.input_token.value in ['+','-','*','/']:
            self.operator()
            self.expression()
            self.expression()
            self.match(')', func='application_tail')
        elif self.input_token.value == 'lambda':
            self.match('lambda', func='application_tail')
            self.params()
            self.expression()
            self.match(')', func='application_tail')
        else:
            self.parse_error('application_tail')

file = sys.argv[1]
p = Parser(file)
p.lambda_list()

# t = Tokenizer(file)
# token = t.next_token()
# while token.value != '$$':
#     print(token.value + ":" + token.type)
#     token = t.next_token()





