from ASTparser import *

class Evaluator():
    
    env = {}
    mArray = ['','']
    
    # Return true if x is a function (Lx.x)
    def isFunc(x):
        if x[1] == 'L' and x[2].isalpha() and x[3] == '.':
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
    def evalFunc(M):
        if M.isdigit():
            return M
        elif M.isalpha():
            return env[M]
        elif isFunc(M):
            return M[2]
        else:
            
            seperateApplication(M)
            v = evalFunc(mArray[1])
            f = evalFunc(mArray[0])
            env[f] = v
            return v
        
    def processTree(node, depth):
        
        nodeArray = []
        for child in node.children:
            if child is not None:
                if child.type == "func":
                    nodeArray.append(processTree(child, depth+1))
                else:
                    nodeArray.append(child.value)
        
        return evalTree(''.join(nodeArray))
                 
                 

    

parser = ASTParser("testlambda.txt")
for tree in parser.expression_trees:
    processTree(tree, 0)
    
    
    