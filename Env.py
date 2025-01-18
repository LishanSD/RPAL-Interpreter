import logging

from Node import ASTNode


class Environment:
    logger = logging.getLogger(__name__)

    # Initialize the environment with an index and empty variables dictionary.
    def __init__(self, index):
        self.index = index
        self.vars = {}
        self.parent = None

    # Method to set variable bindings in the environment.
    def set_parameters(self, parent_environment, key, value):
        self.vars[key] = value
        if isinstance(key, ASTNode) and isinstance(value, ASTNode):
            pass
        else:
            pass
        self.parent = parent_environment
        
    # Get the index of the environment.
    def get_index(self):
        return self.index

    # Get the value associated with a variable key.
    def get_value(self, key):
        if key in self.vars.keys():
            value = self.vars[key]
            self.logger.info("found in cur env id {}".format(self.index))
            if isinstance(value, ASTNode):
                self.logger.info("value: {}".format(value.value))
            return value
        else:
            self.logger.info("not found in cur env")
            return None
