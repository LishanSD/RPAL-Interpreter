import math
import sys

import Node

from Env import Environment
from controlStructure import LambdaExpression, Beta, Tau


class CSEMachine :
    results = []
    def __init__(self , controlStructures ,file):
        self.mapEnvironments={}
        self.currentEnvIndex=0
        self.maxEnvIndex=0

        self.currentEnvStack=[]
        self.file=file

        # Initialize the root environment.
        env=Environment(self.currentEnvIndex)
        self.mapEnvironments[self.currentEnvIndex]=env
        self.currentEnvStack.append(env)


        self.controlStructures = controlStructures
        self.stack = []
        self.control = []
        self.stack.append(env)
        self.control.append(env)
        self.control.extend(controlStructures[0])


    def binaryOperation(self ,operation, random1,random2):

        binary_operation=operation.type
        if isinstance(random2 , Node.ASTNode) and isinstance(random1 ,Node.ASTNode):
            type1=random1.type
            type2=random2.type
            val1=random1.value
            val2=random2.value
        
        # Perform different binary operations based on the operator.
        if binary_operation == "+":
            result = Node.ASTNode("Type.INT")
            result.value = str(int(val1) + int(val2))
            return result

        elif binary_operation == "-":
            result=Node.ASTNode( "Type.INT")
            result.value=str(int(val1) -int(val2))
            return result

        elif binary_operation == "*":
            result= Node.ASTNode(  "Type.INT" )
            result.value=str(int(val1 )* int(val2))
            return result
        elif binary_operation == "/":

            result=Node.ASTNode("Type.INT")
            result.value=str(val1 // val2)

            return result
        elif binary_operation == "**":
            result = Node.ASTNode("Type.INT")
            result.value = str( math.pow(int(val2) ,int(val1)))
            return result


        elif binary_operation == "&":
            result=""
            if val1 == "true" and val2 == "true":
                result = Node.ASTNode("true")
                result.value = "true"
            else:
                result = Node.ASTNode("false")
                result.value = "false"
            return result

        elif binary_operation == "or":
            result=""
            if val1 == "true" and val2 == "true":
                result = Node.ASTNode("true")
                result.value = "true"
            elif  val1 == "false" and val2 == "true":
                result = Node.ASTNode("true")
                result.value = "true"

            elif  val1 == "true" and val2 == "false":
                result = Node.ASTNode("true")
                result.value = "true"

            else:
                result = Node.ASTNode("false")
                result.value = "false"
            return result


        elif binary_operation == "aug":
            
            if isinstance(random1, list):
                if isinstance(random2, list):
                    # add all elements of random2 to random1
                    t1 = random1
                    t2 = random2
                    t2Size = len(t2)
                    for i in range(t2Size):
                        t1.append(t2[i])
                    return t1
                else:
                    if isinstance(random2, Node.ASTNode):
                        # add random2 to a new tuple and return the new tuple
                        t1 = random1
                        t1.append(random2)
                        return t1
                    else:
                        exit(-1)
            elif random1.value == "nil":
                if isinstance(random2, list):
                    return random2
                else:
                    if isinstance(random2, Node.ASTNode):
                        # add random2 to a new tuple and return the new tuple
                        t = []
                        t.append(random2)
                        return t
                    else:
                        exit(-1)
            else:
                exit(-1)
        elif binary_operation == "gr" or  binary_operation == ">" :

            if float(val1) > float(val2):
                result = Node.ASTNode("true")

                result.value = "true"
            else :
                result = Node.ASTNode("false")

                result.value = "false"
            return  result

        elif binary_operation == "ge" or  binary_operation == ">=":

            if int(val1) >= int(val2):
                result = Node.ASTNode("true")

                result.value = "true"
            else:
                result = Node.ASTNode("false")

                result.value = "false"
            return  result

        elif binary_operation == "ls" or  binary_operation == "<":

            if int(val1) < int(val2):
                result = Node.ASTNode("true")

                result.value = "true"
            else:
                result = Node.ASTNode("false")

                result.value = "false"
            return  result

        elif binary_operation == "le" or  binary_operation == "<=":

            if int(val1) <= int(val2):
                result = Node.ASTNode("true")

                result.value = "true"
            else:
                result = Node.ASTNode("false")

                result.value = "false"
            return  result




        elif binary_operation == "ne":

            result = None

            if random1.type == "Type.STRING" and random2.type == "Type.STRING":

                if val1 != val2:

                    result = Node.ASTNode("true")

                    result.value = "true"

                else:

                    result = Node.ASTNode("false")

                    result.value = "false"

                return result

            else:

                if (int(val1) != int(val2)):

                    result = Node.ASTNode("true")

                    result.value = "true"

                else:

                    result = Node.ASTNode("false")

                    result.value = "false"

            #print(result.type)

            return result





        elif binary_operation == "eq":
            result=None
            if random1.type == "Type.STRING" and random2.type == "Type.STRING":
                if val1 == val2:
                    result = Node.ASTNode("true")
                    result.value = "true"
                else:
                    result = Node.ASTNode("false")
                    result.value = "false"
                return result
            else :

                if  (int(val1) == int(val2)):

                    result=Node.ASTNode("true")
                    result.value="true"
                else:
                    result=Node.ASTNode("false")
                    result.value="false"
            #print(result.type)
            return result

        else:
            print("no matching binary operator found:", binary_operation)

        print("Unreachable code !! Something wrong happened!!")
        return None

    def unaryOperation(self, operation, rand):
        unop_type=operation.type
        type1=rand.type
        val1=rand.value
        if unop_type == "not":
            if type1 != "true" and type1 != "false":
                print("Wrong type: true/false expected for operand: type1:", type1)
                exit(-1)
            if val1 == "true":
                result=Node.ASTNode("false")
                result.value="false"

                return result
            else:
                result = Node.ASTNode("true")
                result.value = "true"

                return result
        if unop_type == "neg":
            if type1 != "Type.INT":
                print("Wrong type: INT expected for operand: type1:", type1)
                exit(-1)

            result=Node.ASTNode("Type.INT")
            result.value= str(-int(val1))
            return result

        print("no matching unary operator found:", unop_type)
        return None

    # Print an object
    def Print(self ,obj):

        if isinstance( obj , Node.ASTNode):
            string = obj.value
            if isinstance(obj.value,str):



                if "\\n" in string:
                    string=string.replace("\\n","\n")
                if "\\t" in string:
                    string=string.replace("\\t","\t")

            print(string ,end="")

        if isinstance(obj ,list):
            print("(",end="")
            for index ,i in enumerate(obj) :
                self.Print(i)
                if index < len(obj)-1:
                    print(",",end=" " )
            print(")",end="\n")


    def executeCSEMachine(self):

        count = 0;
        while len(self.control)>0:
            controlTop=self.control[-1]
            stackTop=self.stack[-1]


            if isinstance(controlTop, LambdaExpression):
                lambdha=self.control.pop(-1)
                lambdha.environmentIndex=self.currentEnvIndex
                self.stack.append(lambdha)

            elif isinstance(controlTop, Node.ASTNode):
                node=controlTop
                if node.type=="gamma":
                    if isinstance(stackTop, LambdaExpression):
                        self.control.pop()  # remove gamma
                        self.stack.pop()  # remove lambda

                        rand = self.stack[-1] # get rand from stack
                        self.stack.pop()  # remove rand from stack

                        lambdaStack = stackTop
                        k = lambdaStack.lambdaIndex
                        environmentIdLambda = lambdaStack.environmentIndex
                        tokenStackLambdaList = None
                        tokenStackLambda = None




                        if isinstance(lambdaStack.item, Node.ASTNode):
                            tokenStackLambda = lambdaStack.item  # the variable of lambda of stack
                        else:
                            # a list of Tokens
                            if isinstance(lambdaStack.item, list):
                                tokenStackLambdaList = lambdaStack.item
                            else:
                                print("tokenStackLambdaList is not a list, some error")
                        
                        self.maxEnvIndex += 1
                        self.currentEnvIndex = self.maxEnvIndex
                        env = Environment(self.currentEnvIndex)

                        if tokenStackLambdaList is None:
                            env.set_parameters(self.mapEnvironments.get(environmentIdLambda), tokenStackLambda.value, rand)
                        else:
                            cnt = 0
                            for item in tokenStackLambdaList:
                                env.set_parameters(self.mapEnvironments.get(environmentIdLambda), item.value,
                                                   rand[cnt])
                                cnt += 1

                        self.control.append(env)
                        self.control.extend(self.controlStructures[k]) # k is from stack
                        self.stack.append(env)
                        # maintain environment variables
                        self.currentEnvStack.append(env)
                        self.mapEnvironments[self.currentEnvIndex] = env


                    elif isinstance( stackTop, Node.ASTNode):
                        if stackTop.type == "Y*":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            lambdaY=self.stack[-1]
                            self.stack.pop(-1)
                            self.stack.append(Eta(lambdaY.environmentIndex,lambdaY.lambdaIndex,lambdaY.item))
                        elif stackTop.value == "Print":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            rand =self.stack.pop(-1)
                            self.Print(rand)
                            self.stack.append(Node.ASTNode("dummy"))

                        elif stackTop.value == "Conc":
                            self.stack.pop(-1)
                            stackTop =self.stack[-1]
                            str1 = stackTop.value
                            self.stack.pop(-1)
                            #print("in conc: stackTop:", self.stack[-1].value)
                            str2 = self.stack[-1].value
                            self.stack.pop(-1)  # remove str2
                            #print("in conc: str1:", str1, "| str2:", str2)
                            str_result =  str2 +str1
                            result=Node.ASTNode("Type.STRING")
                            result.value= str_result
                            self.stack.append(result)  # push result into stack

                            self.control.pop(-1)  # remove gamma from control
                            # if controlTop.type != Type.GAMMA:
                            #     #print("GAMMA expected, error !!! controlTop:", controlTop.name)
                            self.control.pop(-1)  # remove gamma from control
                            # controlTop = control[-1]

                        elif stackTop.value=="Stem":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.value) == 0:
                                sys.exit(0)
                            # if len(str1.value) == 1:
                            #     value = ""
                            else:
                                value = str1.value[0]
                            result = Node.ASTNode("Type.STRING")
                            result.value = value
                            self.stack.append(result)
                            # self.stack.append(value)

                        elif stackTop.value=="Stern":
                            #print("Stern")
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.value) == 0:
                                sys.exit(0)
                            if len(str1.value)==1:
                                value=''
                                # print("******************",str1.value[1:] , "******************",str1.value)

                            else:

                                # print("******************",str1.value[1:] , "******************",str1.value)
                                value=str1.value[1:]
                            result = Node.ASTNode("Type.STRING")
                            result.value = value
                            self.stack.append(result)
                            # self.stack.append(value)

                        elif stackTop.value== "Null":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            stackTop=self.stack[-1]
                            self.stack.pop(-1)


                            if isinstance(stackTop , Node.ASTNode):
                                if stackTop.type== 'nil':
                                    result=Node("true")
                                    result.value="true"
                                    self.stack.append(result)

                            elif isinstance(stackTop ,list):
                                if len(stackTop) == 0 :
                                    result = Node.ASTNode("true")
                                    result.value = "true"
                                    self.stack.append(result)
                                else:
                                    result = Node.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)

                        elif stackTop.value =="ItoS":
                            self.control.pop(-1)
                            self.stack.pop(-1)

                            stackTop= self.stack.pop(-1)
                            result=Node.ASTNode("Type.STRING")
                            result.value=str(stackTop.value)
                            print("ItoS")
                            print(result.value)
                            self.stack.append(result)

                        elif stackTop.value == "Isinteger":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop , Node.ASTNode):
                                if stackTop.type=="Type.INT":
                                    result=Node.ASTNode("true")
                                    result.value="true"
                                    self.stack.append(result)
                                else:
                                    result = Node.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)
                            else :
                                sys.exit(0)


                        elif stackTop.value == "Istruthvalue":

                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, Node.ASTNode):

                                if stackTop.type == "true" or stackTop.type=="false":

                                    result = Node.ASTNode("true")

                                    result.value = "true"

                                    self.stack.append(result)

                            else:
                                result = Node.ASTNode("false")

                                result.value = "false"

                                self.stack.append(result)

                        elif stackTop.value== "Isstring" :
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, Node.ASTNode):
                                if stackTop.type == "Type.STRING":
                                    result = Node.ASTNode("true")
                                    result.value = "true"
                                    self.stack.append(result)
                                else:
                                    result = Node.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)
                            else:
                                sys.exit(0)

                        elif stackTop.value=="Istuple":
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if isinstance(stackTop,list):
                                result = Node.ASTNode("true")
                                result.value = "true"
                                self.stack.append(result)

                            else:
                                result = Node.ASTNode("false")
                                result.value = "false"
                                self.stack.append(result)


                        elif stackTop.value=="Isdummy":
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if stackTop.value=="dummy":
                                result = Node.ASTNode("true")
                                result.value = "true"
                                self.stack.append(result)
                            else:
                                result = Node.ASTNode("false")
                                result.value = "false"
                                self.stack.append(result)


                        elif stackTop.value =="Order":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            rand=self.stack.pop(-1)
                            if isinstance(rand,Node.ASTNode):
                                node = Node.ASTNode("Type.INT")
                                node.value="0"

                                self.stack.append(node)
                            elif isinstance(rand, list):
                                node=Node.ASTNode("Type.INT")
                                node.value=(len(rand))
                                self.stack.append(node)
                            else:
                                #print("Order: rand is not a tuple or nil!!")
                                exit(-1)

                        elif stackTop.type=="Type.INT":
                            self.control.pop(-1)

                        elif stackTop.type=="Type.STRING":
                            self.control.pop(-1)

                    elif isinstance(stackTop, list):
                        self.control.pop(-1)
                        self.stack.pop(-1)
                        index=int(self.stack[-1].value)
                        self.stack.pop(-1)

                        self.stack.append(stackTop[index-1])


                    elif isinstance(stackTop,Eta):
                        self.control.append(Node.ASTNode( "gamma"))
                        eta = stackTop
                        lambdaStack = LambdaExpression(eta.environmentId, eta.id, eta.token)
                        self.stack.append(lambdaStack)


                elif node.type in ["-", "+" , "*", "/","or","&","**" ,"aug" ,"gr",">=","ge",">","ls","<","<=","eq","ne","le" ]:
                    operation=self.control.pop(-1)
                    rand=self.stack.pop(-1)
                    ran2=self.stack.pop(-1)
                    val=self.binaryOperation(operation,rand,ran2 )
                    self.stack.append(val)


                elif node.type=="neg":
                    operation = self.control.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOperation(operation, rand)
                    self.stack.append(val)

                elif node.type=="not":
                    operation = self.control.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOperation(operation, rand)
                    self.stack.append(val)

                elif node.type=="Y*":
                    
                    Ystar=self.control.pop(-1)
                    self.stack.append(Ystar)

                elif node.type=="Type.INT":

                    Ystar = self.control.pop(-1)
                    self.stack.append(Ystar)


                else :
                
                    self.control.pop()
                    currentEnv = self.currentEnvStack[-1]
                    type_ = controlTop.type
                    control_value=controlTop.value

                    if controlTop.type == "Type.ID":
                        
                        stackVal = currentEnv.get_value(controlTop.value)


                        if stackVal is None:
                            currentEnv = currentEnv.parent
                            while currentEnv is not None:
                                stackVal = currentEnv.get_value(controlTop.value)
                                if stackVal is not None:
                                    break
                                currentEnv = currentEnv.parent


                        if stackVal is not None:
                            self.stack.append(stackVal)
                            if isinstance(stackVal, Node.ASTNode):
                                pass

                        if stackVal is None:
                            # if not found in the env tree, check if it was a special function
                            # it may be a special function name which was not redefined
                            if control_value in ["Print", "Conc", "Stern", "Stem", "Order", "Isinteger", "Istruthvalue",
                                         "Isstring", "Isinteger",
                                         "Istuple", "Isfunction", "Isdummy", "ItoS", "Null"]:
                                
                                self.stack.append(controlTop)
                            else:
                                sys.exit(-1)
                    else:
                        self.stack.append(controlTop)



            elif isinstance(controlTop , Tau):
                n = self.control[-1].n

                self.control.pop()
                tuple = []

                while n > 0:
                    tuple.append(self.stack.pop())
                    stackTop = self.stack[-1] if self.stack else None
                    n -= 1
                self.stack.append(tuple)
            elif isinstance(controlTop, Beta):
                if stackTop.type == "true":
                    self.control.pop(-1)  # remove beta
                    self.control.pop(-1)  # remove else
                    self.control.extend(self.controlStructures[self.control.pop(-1).index])
                    self.stack.pop(-1)
                elif stackTop.type == "false":
                    self.control.pop(-1)
                    controlTop = self.control[-1]
                    self.control.pop(-1)  # remove else
                    self.control.pop(-1)  # remove then
                    self.control.extend( self.controlStructures[controlTop.index])  # insert else back
                    self.stack.pop(-1)
            elif isinstance(controlTop, Environment):
                self.control.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.append(stackTop)
                self.currentEnvStack.pop()


            count+=1
            if (count>500):
                break



class Eta :
    def __init__ (self, environmentId,id ,token):
        self.environmentId=environmentId
        self.id=id
        self.token=token
