import sys
from tokenizer import *

class Node():
    
    def __init__(self, tok_type, tok_value):
        self.type = tok_type
        self.value = tok_value
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self, depth):
        
        for child in self.children:
            str = ""
            for i in range (depth):
                str += "\t" 
            str += child.value
            print(str)
            if child is not None:
                child.print_tree(depth+1)

class ASTParser():

    def __init__(self, file):
        self.debug = False
        self.tokenizer = Tokenizer(file)
        self.input_token = None
        self.consume_token()
        self.expression_trees = []
        self.statement_count = 0
        self.lambda_list()

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

    def lambda_list(self):
        if self.debug:
            print("EXPLORING lambda_list")
        if self.input_token.value == '(':
            self.statement_count += 1

            lambda_expression_node = Node('func','lambda expression')
            self.lambda_expression(lambda_expression_node)
            self.expression_trees.append(lambda_expression_node)

            self.lambda_list()

        elif self.input_token.value == '$$':
            pass
        else:
            self.parse_error('lambda_list')

    def lambda_expression(self, parent_node):
        if self.debug:
            print("EXPLORING lambda_expression")
        parent_node.add_child(Node('Left Parenthesis', '('))
        self.match('(', func='lambda_expression')

        lambda_expression_tail_node = Node('func','lambda expression tail')
        self.lambda_expression_tail(lambda_expression_tail_node)
        parent_node.add_child(lambda_expression_tail_node)

    def lambda_expression_tail(self, parent_node):
        if self.debug:
            print("EXPLORING lambda_expression_tail")
        if self.input_token.value == 'lambda':
            parent_node.add_child(Node('Lambda', 'lambda'))
            self.match('lambda', func='lambda_expression_tail')

            parent_node.add_child(Node('Left Parenthesis','('))
            self.match('(', func='params')

            parent_node.add_child(Node('ID',self.input_token.value))
            self.match_type('ID', 'params')

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='params')

            expression_node = Node('func','expression')
            self.expression(expression_node)
            parent_node.add_child(expression_node)

            parent_node.add_child(Node('Right Parenthesis', ')'))
            self.match(')', func='lambda_expression_tail')

        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            head_node = Node('func','head')
            self.head(head_node)
            parent_node.add_child(head_node)

            tail_node = Node('func','tail')
            self.tail(tail_node)
            parent_node.add_child(tail_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='lambda_expression_tail')

    def lambda_func(self, parent_node):
        if self.debug:
            print("EXPLORING lambda_func")
        parent_node.add_child(Node('Left Parenthesis','('))
        self.match('(','lambda', func='lambda_func')

        params_node = Node('func','params')
        self.params(params_node)
        parent_node.add_child(params_node)

        expression_node = Node('func','expression')
        self.expression(expression_node)
        parent_node.add_child(expression_node)

        parent_node.add_child(Node('Right Parenthesis',')'))
        self.match(')',func='lambda_func')

    def params(self, parent_node):
        if self.debug:
            print("EXPLORING params")
        parent_node.add_child(Node('Left Parenthesis','('))
        self.match('(', func='params')

        parent_node.add_child(Node('ID',self.input_token.value))
        self.match_type('ID', 'params')

        #params_list_node = Node('func','params_list')
        #self.params_list(params_list_node)
        #parent_node.add_child(params_list_node)

        parent_node.add_child(Node('Right Parenthesis',')'))
        self.match(')', func='params')

    def params_list(self, parent_node):
        if self.debug:
            print("EXPLORING params_list")
        if self.input_token.type == 'ID':
            parent_node.add_child(Node('ID',self.input_token.value))
            self.match_type('ID', func='params_list')

            params_list_node = Node('func','params_list')
            self.params_list(params_list_node)
            parent_node.add_child(params_list_node)

        elif self.input_token.value == ')':
            pass
        else:
            self.parse_error('params_list')

    def expression(self, parent_node):
        if self.debug:
            print("EXPLORING expression")
        if self.input_token.type == 'ID':
            parent_node.add_child(Node('ID',self.input_token.value))
            self.match_type('ID', 'expression')

        elif self.input_token.type == 'number':
            parent_node.add_child(Node('number',self.input_token.value))
            self.match_type('number', 'expression')

        elif self.input_token.value == '(':
            parent_node.add_child(Node('Left Parenthesis','('))
            self.match('(', func='expression')

            expression_tail_node = Node('func','expression_tail')
            self.expression_tail(expression_tail_node)
            parent_node.add_child(expression_tail_node)

    def expression_tail(self, parent_node):
        if self.debug:
            print("EXPLORING expression_tail")
        if self.input_token.value in ['+','-','*','/']:
            operator_node = Node('func','operator')
            self.operator(operator_node)
            parent_node.add_child(operator_node)

            expression1_node = Node('func','expression')
            self.expression(expression1_node)
            parent_node.add_child(expression1_node)

            expression2_node = Node('func','expression')
            self.expression(expression2_node)
            parent_node.add_child(expression2_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='expression_tail')

        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            head_node = Node('func','head')
            self.head(head_node)
            parent_node.add_child(head_node)

            tail_node = Node('func','tail')
            self.tail(tail_node)
            parent_node.add_child(tail_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='expression_tail')

        else:
            self.parse_error('expression_tail')

    def operator(self, parent_node):
        if self.debug:
            print("EXPLORING operator")
        if self.input_token.value in ['+','-','*','/']:
            parent_node.add_child(Node('operator',self.input_token.value))
            self.match(self.input_token.value, func='operator')
        else:
            self.parse_error('operator')

    def application(self, parent_node):
        if self.debug:
            print("EXPLORING application")
        parent_node.add_child(Node('Left Parenthesis','('))
        self.match('(', func='application')

        head_node = Node('func','head')
        self.head(head_node)
        parent_node.add_child(head_node)

        tail_node = Node('func','tail')
        self.tail(tail_node)
        parent_node.add_child(tail_node)

        parent_node.add_child(Node('Right Parenthesis',')'))
        self.match(')', func='fLambda')

    def head(self, parent_node):
        if self.debug:
            print("EXPLORING head")
        if self.input_token.value == '(':
            parent_node.add_child(Node('Left Parenthesis','('))
            self.match('(', func='head')

            application_head_node = Node('func','application_head')
            self.application_head(application_head_node)
            parent_node.add_child(application_head_node)

        elif self.input_token.type == 'ID':
            parent_node.add_child(Node('ID',self.input_token.value))
            self.match_type('ID','head')
        else:
            self.parse_error('head')

    def application_head(self, parent_node):
        if self.debug:
            print("EXPLORING application_head")
        if self.input_token.value == 'lambda':
            parent_node.add_child(Node('Lambda','lambda'))
            self.match('lambda', func='application_head')

            params_node = Node('func','params')
            self.params(params_node)
            parent_node.add_child(params_node)

            expression_node = Node('func','expression')
            self.expression(expression_node)
            parent_node.add_child(expression_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='application_head')

        elif self.input_token.value == '(' or self.input_token.type == 'ID':
            head_node = Node('func','head')
            self.head(head_node)
            parent_node.add_child(head_node)

            tail_node = Node('func','tail')
            self.tail(tail_node)
            parent_node.add_child(tail_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='application_head')

        else:
            self.parse_error('application_head')

    def tail(self, parent_node):
        if self.debug:
            print("EXPLORING tail")
        if self.input_token.type == 'ID':
            parent_node.add_child(Node('ID',self.input_token.value))
            self.match_type('ID', 'tail')

        elif self.input_token.type == 'number':
            parent_node.add_child(Node('number',self.input_token.value))
            self.match_type('number', 'tail')

        elif self.input_token.value == '(':
            parent_node.add_child(Node('Left Parenthesis','('))
            self.match('(', func='tail')

            application_tail_node = Node('func','application_tail')
            self.application_tail(application_tail_node)
            parent_node.add_child(application_tail_node)

        else:
            self.parse_error('tail')

    def application_tail(self, parent_node):
        if self.debug:
            print("EXPLORING application_tail")
        if self.input_token.value in ['+','-','*','/']:
            operator_node = Node('func','operator')
            self.operator(operator_node)
            parent_node.add_child(operator_node)

            expression1_node = Node('func','expression')
            self.expression(expression1_node)
            parent_node.add_child(expression1_node)

            expression2_node = Node('func','expression')
            self.expression(expression2_node)
            parent_node.add_child(expression2_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='application_tail')

        elif self.input_token.value == 'lambda':
            parent_node.add_child(Node('Lambda','lambda'))
            self.match('lambda', func='application_tail')

            params_node = Node('func','params')
            self.params(params_node)
            parent_node.add_child(params_node)

            expression_node = Node('func','expression')
            self.expression(expression_node)
            parent_node.add_child(expression_node)

            parent_node.add_child(Node('Right Parenthesis',')'))
            self.match(')', func='application_tail')

        else:
            self.parse_error('application_tail')

#file = sys.argv[1]
p = ASTParser("testlambda.txt")
count = 1
for tree in p.expression_trees:
    print("AST Tree for Statement %s:" % count)
    tree.print_tree(0)
    print('========================================\n')
    count += 1

# t = Tokenizer(file)
# token = t.next_token()
# while token.value != '$$':
#     print(token.value + ":" + token.type)
#     token = t.next_token()





