class Node():
    
    def __init__(self, tok_type, tok_value):
        self.tok_type = tok_type
        self.tok_value = tok_value
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self, depth):
        
        for child in self.children:
            str = ""
            for i in range (depth):
                str += "\t" 
            str += child.tok_value
            print(str)
            if child is not None:
                child.print_tree(depth+1)
            
            
# head = Node("Head", "Head")
# lambdaFunction = Node("Lambda Function", "Lambda Function")
# lparen = Node("Paren", "(")
# lambdaNode = Node("Lambda", "Lambda")
# idNode = Node("ID", "X")
# exprNode = Node("Expression Function", "Expresson Funciton")
# applicationNode = Node ("Application Function", "Application Function")
# rparen = Node("Paren", ")")

# head.add_child(lambdaFunction)
# lambdaFunction.add_child(lparen)
# lambdaFunction.add_child(lambdaNode)
# lambdaFunction.add_child(lparen)
# lambdaFunction.add_child(idNode)
# lambdaFunction.add_child(rparen)
# lambdaFunction.add_child(exprNode)
# lambdaFunction.add_child(rparen)
# exprNode.add_child(applicationNode)

# head.print_tree(0)


    
    