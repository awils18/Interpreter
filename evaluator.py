from ASTparser import *

class Evaluator():
    
    env = {}
    
    # Evaluate the expression the Lambda function M and return reduction
    def evalNodeArray(self, M):
        
        '''print "##################"
        for child in M:
            print child.value
        print "####################"'''
      
        
        # The case of an empty array
        if len(M) == 0:
            return []
        
        # The case of id, number, or op
        elif M[0].type in ["number", "ID", "operator"] and len(M) == 1:
            #print "In ID NUM 2"
            return [Node(M[0].type, M[0].value)]
    
        # The case of + 5 5) operations
        elif M[0].type == "operator":
            if M[1].type == "number" and M[2].type == "number":
                opstr = M[1].value + M[0].value +  M[2].value
                return [Node("number", eval(opstr))]
            return M
        
        # The case of (lambda (x) x)
        elif M[1].value == "lambda":
            return [Node(M[3].type, M[3].value)]
        
        # The case of lambda (x) expr) application
        elif M[0].value == "lambda" and M[4].type != "ID":
            v = self.evalNodeArray([M[4]])[0]
            f = self.evalNodeArray([M[2]])[0]
            self.env[f.value] = v.value
            return [Node("number", v.value)]
        
        # The case of (5 after an evaluation
        elif len(M) > 1 and M[0].value == "(" and M[1].type == "number":
            return [Node(M[1].type, M[1].value)]
        
        # The case of (head tail) application
        elif M[1].value == "head" and M[2].value == "tail":
            v = self.evalNodeArray([M[2]])[0]
            f = self.evalNodeArray([M[1]])[0]
            self.env[f.value] = v.value
            return [Node("number", v.value)]    
        
        # The case of (x 5) simple application
        elif len(M) > 2 and M[1].type in ["number", "ID"] and M[2].type in ["number", "ID"]:
            v = self.evalNodeArray([M[2]])[0]
            f = self.evalNodeArray([M[1]])[0]
            self.env[f.value] = v.value
            return [Node("number", v.value)]         
       
        # The case of meaningless characters to be appended
        else:
            return M
        
    def createTree(self, node):
        nodeArray = []
                
        #Loop through tree and build linear array
        for child in node.children:
            if child.type == "func":
                nodeArray.extend(self.createTree(child))
            else:
                nodeArray.append(child)  
                
        return nodeArray
    
    
    def processArgs(self, node):
        
        nodeArray = self.createTree(node)
        
        length = len(nodeArray)
        if nodeArray[length - 2].type == "number":
            num = nodeArray[length-2].value
            #print num
            #print nodeArray[4].value
            self.env[nodeArray[4].value] = num
            
            for i in range(5, len(nodeArray)):
                if(nodeArray[i].type == "ID"):
                    nodeArray[i].value = self.env[nodeArray[i].value]
                    nodeArray[i].type = "number"
            
        #self.processTree(nodeArray[1: (length-2)])
        #for child in node.children:
            #print child.value
            return self.processTree(node)
        else:
            return [Node("Func Decl", "Func Decl")]
                
                    
                    
    def processTree(self, node):
        
        nodeArray = []
        for child in node.children:
            if child is not None:
                if child.type == "func":
                    #print child.children
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
    #evaluation = evaluator.processTree(tree)[0]
    #print evaluation.value
    lists = evaluator.processArgs(tree)[0]
    print lists.value
    
    #for child in lists:
     #   print child.value

    
    
    
    