from ASTparser import *

class Evaluator():
    
    env = {}
    mArray = ['','']
    
    # Return true if x is a function (Lx.x)
    def isFunc(self, x):
        print x
        if x[1].type == "Lambda":
            return True
        return False
    
    # Seperate the str into (M1 M2)
    # Access in the mArray[] = {M1, M2}
    def seperateApplication(x):
        str1 = ''
        str2 = ''
        
        # Is the first str being processed
        isFirst = True
        
        for n in range(1, len(x)-1):
            if x[n] == ' ':
                pass
            elif x[n] != ')':
                if isFirst:
                    str1 += x[n]
                else:
                    str2 += x[n]
            else:
                if isFirst:
                    isFirst = False
                    str1 += x[n]
                else:
                    str2 += x[n]
        mArray[0] = str1
        mArray[1] = str2
    
    # Evaluate the expression the Lambda function M and return reduction
    def evalNodeArray(self, M):
        for child in M:
            print child.value        
        if M[0].type in ["number", "id"]:
            return Node(M[0].type, M[0].value)
        elif M[1].value == "lambda":
            return Node(M[3].type, M[3].value)
        elif M[1].value == "head" and M[2].value == "tail":
            v = self.evalNodeArray(M[2])
            f = self.evalNodeArray(M[1])
            env[f] = v
            return Node("number", v)
        else:
            print "FUCKs"

    def processTree(self, node):
        
        nodeArray = []
        for child in node.children:
            if child.type == "func":
                nodeArray.append(self.processTree(child))
            else:
                nodeArray.append(child)
        
      
        return self.evalNodeArray(nodeArray)
                 
                 

    

parser = ASTParser("testlambda.txt")
evaluator = Evaluator()
for tree in parser.expression_trees:
    evaluator.processTree(tree)
    
    
    