from ASTparser import *

class Evaluator():
    
    env = {}
    
    # Evaluate the expression the Lambda function M and return reduction
    def evalNodeArray(self, M):
        
        '''print "##################"
        for child in M:
            print child.value
        print "####################"'''
        if len(M) == 0:
            return []
        if M[0].type in ["number", "ID"] and len(M) == 1:
            #print "In ID NUM 2"
            return [Node(M[0].type, M[0].value)]
        elif M[1].value == "lambda":
            return [Node(M[3].type, M[3].value)]
        elif M[1].value == "head" and M[2].value == "tail":
            v = self.evalNodeArray(M[2])
            f = self.evalNodeArray(M[1])
            env[f] = v
            return [Node("number", v)]
        elif M[1].type in ["number", "ID"] and M[2].type in ["number", "ID"]:
            v = self.evalNodeArray([M[2]])[0]
            f = self.evalNodeArray([M[1]])[0]
            self.env[f.value] = v.value
            return [Node("number", v.value)]         
        else:
           # print "FUCKs"
            return M

    def processTree(self, node):
        
        nodeArray = []
        for child in node.children:
            if child.type == "func":
                nodeArray.extend(self.processTree(child))
            else:
                nodeArray.append(child)
                
        return self.evalNodeArray(nodeArray)
                 
                 

    

parser = ASTParser("testlambda.txt")
evaluator = Evaluator()
for tree in parser.expression_trees:
    #for child in evaluator.env.keys():
        #print child
    print "EVAL: " 
    evaluation = evaluator.processTree(tree)[0]
    print evaluation.value

    
    
    
    