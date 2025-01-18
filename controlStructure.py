import Node

# Define a class for Tau expression
class Tau:
    def __init__(self, n):
        self.n = n

# Define a class for Beta expression
class Beta:
    def __init__(self):
        pass

# Define a class for Control Structure
class ControlStructure:
    def __init__(self, index, delta):
        self.index = index
        self.delta = delta

# Define a class for Lambda Expression
class LambdaExpression:
    def __init__(self, environmentIndex, lambdaIndex, token):
        self.environmentIndex = environmentIndex
        self.lambdaIndex = lambdaIndex
        self.item = token

    def print_lambda_expression(self):
        if isinstance(self.item, Node.ASTNode):
            pass
        elif isinstance(self.item, list):
            lam_vars = ""
            for it in self.item:
                lam_vars += it.name + ','

# Define a class for Control Structure Generator
class ControlStructureGenerator:
    def __init__(self):
        self.current_index_delta = 0
        self.queue = []
        self.map_control_structs = {}
        self.current_delta=[]

    def generate_control_structures(self, root):
        delta = []
        self.current_delta = []
        self.pre_order_traversal(root, delta)
        
        ctrl_delta = ControlStructure(self.current_index_delta, delta)
        self.map_control_structs[0] = self.current_delta.copy()
        
        while len(self.queue)>0:
            self.current_delta = []
            index, node, delta_queue = self.queue[0]
            self.pre_order_traversal(node, delta_queue)
            ctrl_delta = ControlStructure(index, delta_queue)
            self.map_control_structs[index] = self.current_delta.copy()
            self.queue.pop(0)
        return self.map_control_structs

    # Perform pre-order traversal of the AST
    def pre_order_traversal(self, root ,delta):
        match root.type :
            case "lambda": # Lambda expression
                self.current_index_delta += 1
                lambda_exp = None
                if root.child.type ==',':
                    tau_list = []
                    child = root.child.child
                    while child is not None:
                        tau_list.append(child)
                        child = child.sibling
                    lambda_exp = LambdaExpression(0, self.current_index_delta, tau_list)
                else:
                    lambda_exp = LambdaExpression(0, self.current_index_delta, root.child)

                self.current_delta.append(lambda_exp)
                delta_lambda = []

                self.queue.append((self.current_index_delta, root.child.sibling, delta_lambda))
                return
            case "->": # Arrow expression
                delta2 = []
                savedcurrent_index_delta2 = self.current_index_delta + 1
                savedcurrent_index_delta3 = self.current_index_delta + 2
                self.current_index_delta += 2

                node2 = root.child.sibling

                node3 = root.child.sibling.sibling

                node2.sibling = None  # to avoid re-traversal
                """
                preOrderTraversal(node2, delta2)
                ctrlDelta2 = ControlStructure(savedcurrent_index_delta2, delta2)
                mapCtrlStructs[savedcurrent_index_delta2] = ctrlDelta2
                """
                self.queue.append((savedcurrent_index_delta2, node2, delta2))
                delta3 = []
                """
                preOrderTraversal(node3, delta3)
                ctrlDelta3 = ControlStructure(savedcurrent_index_delta3, delta3)
                mapCtrlStructs[savedcurrent_index_delta3] = ctrlDelta3
                """
                self.queue.append((savedcurrent_index_delta3, node3, delta3))
                self.current_delta.append( ControlStructure ( savedcurrent_index_delta2 , delta2))
                self.current_delta.append(ControlStructure ( savedcurrent_index_delta3 , delta3))
                beta = Beta()
                self.current_delta.append(beta)  # TODO: may create a problem: be careful!!!!!!!!!!!!!!!!
                # this is imp so that you don't traverse the sibling of the 1st child again
                # as you already did it above.
                root.child.sibling = None
                self.pre_order_traversal(root.child, delta)
                return
            case "gamma": # Gamma expression
                self.current_delta.append(root)
                self.pre_order_traversal(root.child, delta)
                if root.child.sibling is not None:
                    self.pre_order_traversal(root.child.sibling, delta)
                return

            case "tau": # Tau expression
                initial_length=len(self.current_delta)
                node = root.child
                next_node = node.sibling
                deltas_tau = []
                counter = 0
                while node is not None:
                    node.sibling = None
                    self.pre_order_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sibling
                    counter += 1

                tau = Tau(counter)
                temp=[]
                final_length=len(self.current_delta)
                counter=final_length-initial_length
                for i in range(counter):
                    temp.append(self.current_delta.pop())

                self.current_delta.append(tau)
                for i in range(counter):
                    self.current_delta.append(temp.pop())

                if root.sibling is not None:
                    self.pre_order_traversal(root.sibling, delta)
                return

            case _ :
                self.current_delta.append(root)
                if (root.child is not None):
                    self.pre_order_traversal(root.child, delta)
                    if (root.child.sibling is not None):
                        self.pre_order_traversal(root.child.sibling, delta)
                return
            