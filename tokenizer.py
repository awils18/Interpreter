#!/usr/bin/env python

import sys

class Token():

    def __init__(self, value):
        self.type_dict = {
            self.isLambda: "lambda",
            self.isIdentifier: "ID",
            self.isNumber: "number",
            self.isSymbol: "symbol",
            self.isMeta: "meta"
        }
        if value == '$$':
            self.type = 'EOF'
        else:
            self.type = self.getType(value)
        #print('!' + value + '!' + self.type + '!')
        self.value = value

    def getType(self,token):
        # loop through all functions, return the corresponding number for the first function that returns True
        for func in [self.isLambda, self.isIdentifier, self.isNumber, self.isSymbol, self.isMeta]:
            if func(token):
                return self.type_dict[func]
        return None

    # <letter> --> a | b | ... | y | z | A | B | ... | Z | underscore
    def isLetter(self,c):
        return (ord('a') <= ord(c) <= ord('z')) or (ord('A') <= ord(c) <= ord('Z')) or c == '_'

    # <digit> --> 0 | 1 | ... | 9
    def isDigit(self,c):
        return 48 <= ord(c) <= 57

    # <number> --> <digit>+
    def isNumber(self, num):
        if num == "":
            return False
        for i in num:
            if not self.isDigit(i):
                return False
        return True

    # <identifier> --> <letter> (<letter> | <digit>)*
    def isIdentifier(self,token):
        if token == "":
            return False
        elif not self.isLetter(token[0]):
            return False
        for i in range(1,len(token)):
            if not self.isDigit(token[i]) and not self.isLetter(token[i]):
                return False
        return True

    def isLambda(self, t):
        return t == 'lambda'

    def isSymbol(self,token):
        return token in ['(',')','+','-','*','/']

    def isMeta(self, token):
        return token[:2] == "//" or token[0] == '#'

class Tokenizer():

    # create reverse list of lines so we can use pop() to remove lines from list and get them in order
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.lines = self.file.readlines()
        self.lines = [line.rstrip('\n') for line in self.lines]
        self.lines.reverse()
        self.current_line = ""
        self.current_index = 0  # keep track of the index after each token we read

    def next_token(self):

        while self.current_index >= len(self.current_line):
            if len(self.lines) == 0:
                return Token('$$')
            else:
                self.current_line = self.lines.pop()
            self.current_index = 0

        current_token = ""
        for i in range(self.current_index, len(self.current_line)): # read from current index until break or end of line (at most)
            char = self.current_line[i]
            if char in [' ','\t']: # skip whitespace
                self.current_index += 1
                return self.next_token()

            if i+1 == len(self.current_line):   # if we're at the last index, make next_char empty
                next_char = ""
            else:
                next_char = self.current_line[i+1]  # otherwise, get value of next char

            # if we reach comment, read until newline or just through entire rest of the list
            if char+next_char == '//' or char == '#':
                for j in range(i,len(self.current_line)):
                    if self.current_line[j] == '\n':
                        self.current_index = len(self.current_line)
                        return Token(current_token)
                    current_token += self.current_line[j]
                self.current_index = len(self.current_line)
                return Token(current_token)

            current_token += char # add character to current token

            if self.isSymbol(char) or self.isSymbol(next_char) or next_char in [' ','\n','\t']:
                self.current_index = i+1
                return Token(current_token)

    def isSymbol(self,token):
        return token in ['(',')','+','-','*','/']

