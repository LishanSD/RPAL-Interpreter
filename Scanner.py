from enum import Enum

# Identify the reservered keywords
RESERVED_KEYWORDS = ['fn','where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq','gr','ge','ls','le','ne','or','@','not','&','true','false','nil','dummy','and','|']


PUNCTION = ['(', ')', ';', ',']

# Token class
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Class for the token type which defines the different types of tokens that can be identified
class Type(Enum):
    RESERVED_KEYWORD = 'RESERVED_KEYWORD'
    ID = 'ID'
    COMMENT = 'COMMENT'
    INT = 'INT'
    COMMA = 'COMMA'
    PLUS = 'PLUS'  # +
    MINUS = 'MINUS'  # -
    MUL = 'MUL'  # *
    DIV = 'DIV'  # /
    GREATER_THAN = 'GREATER_THAN'  # >
    LESSER_THAN = 'LESSER_THAN'  # <
    AMPERSAND_OPERATOR = 'AMPERSAND_OPERATOR'  # &
    DOT_OPERATOR = 'DOT_OPERATOR'  # .
    AT_OPERATOR = 'AT_OPERATOR'  # @
    SEMICOLON = 'SEMICOLON'  # ;
    EQUAL = 'EQUAL'  # =
    CURL = 'CURL'  # ~
    SQUARE_OPEN_BRACKET = 'SQUARE_OPEN_BRACKET'  # [
    SQUARE_CLOSE_BRACKET = 'SQUARE_CLOSE_BRACKET'  # ]
    DOLLAR = 'DOLLAR'  # $
    EXCLAMATION_MARK = 'EXCLAMATION_MARK'
    HASH_TAG = 'HASH_TAG'
    MODULUS = 'MODULUS'
    CARROT = 'CARROT'
    CURLY_OPEN_BRACKET = 'CURLY_OPEN_BRACKET'
    CURLY_CLOSE_BRACKET = 'CURLY_CLOSE_BRACKET'
    BACK_TICK = 'BACK_TICK'
    DOUBLE_QUOTE = 'DOUBLE_QUOTE'
    QUESTION_MARK = 'QUESTION_MARK'
    PUNCTION = 'PUNCTION'
    OR_OPERATOR = 'OR_OPERATOR'
    STRING = 'STRING'
    TERNARY_OPERATOR = 'TERNARY_OPERATOR'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    LESSER_THAN_OR_EQUAL = 'LESSER_THAN_OR_EQUAL'
    POWER = 'POWER'
    EOF = 'EOF'


# State Class, maintains the current state of the tokenizer
class State:
    def __init__(self): 
        self.current_char = None
        self.column_num = None
        self.line_num = 0


class Tokenizer:
    def __init__(self, text): # Initializes the tokenizer with the given text and sets the initial state
        self.text = text
        self.pos = 0
        self.state = State()

        self.state.current_char = self.text[self.pos]
        self.state.line_num = 1
        self.state.column_num = 1

    # Raises an exception for handling errors during tokenization
    def error(self):
        raise Exception('Error!')

    # Moves the current position to the next character and updates the state
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.state.current_char = None  # Indicates end of input
        else:
            self.state.current_char = self.text[self.pos]
            self.state.column_num += 1

    # Skips over whitespace characters, including updating line and column numbers for newlines
    def skip_space(self):
        while self.state.current_char is not None and self.state.current_char.isspace():
            if self.state.current_char == '\n':
                self.state.line_num += 1
                self.state.column_num = 0
            self.advance()

    # Reads a sequence of digits and returns it as an integer token
    def integer(self):
        result = ''
        while self.state.current_char is not None :
            if self.state.current_char.isdigit():
                result += self.state.current_char
                self.advance()
            elif self.state.current_char.isalpha():
                self.error()
            else: break


        return int(result)

    # Reads a sequence of alphanumeric characters and underscores to identify an identifier token
    def identifier(self):
        result = ''
        while self.state.current_char is not None and (
                self.state.current_char.isalpha() or self.state.current_char.isdigit() or self.state.current_char == '_'):
            result += self.state.current_char
            self.advance()
        return result

    # Reads characters until the end of the line to identify a comment token
    def comment(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != '\n':
            result += self.state.current_char
            self.advance()
        return result

    # Reads characters within single quotes to identify a string token
    def string(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != "'":
            result += self.state.current_char
            self.advance()
        self.advance()
        return result

    # Main method to get the next token from the input text
    def next_token(self):
        while self.state.current_char is not None:

            # skip whitespaces
            if self.state.current_char.isspace():
                self.skip_space()
                continue

            # tokenize digits
            elif self.state.current_char.isdigit():
                return Token(Type.INT, self.integer())

            # tokenize identifier
            elif self.state.current_char.isalpha():
                return Token(Type.ID, self.identifier())


            # read comment or punctuation
            elif self.state.current_char == '/':
                if self.text[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    return Token(Type.COMMENT, self.comment())

                else :
                    self.advance()
                    return Token(Type.DIV, '/')



            # tokenize string
            elif self.state.current_char == "'":
                self.advance()
                return Token(Type.STRING, self.string())


            # tokenize punctuation
            elif self.state.current_char in PUNCTION:
                token = Token(Type.PUNCTION, self.state.current_char)
                self.advance()
                return token

            # tokenize +, -, *, <, >, &, ., @, ;, =, ~, [, ], $, !, #, %, ^, {, }, `, ", ?, |
            elif self.state.current_char == '+':
                self.advance()
                return Token(Type.PLUS, '+')

            elif self.state.current_char == '-':
                self.advance()
                return Token(Type.MINUS, '-')

            elif self.state.current_char == '*':
                self.advance()
                return Token(Type.MUL, '*')

            elif self.state.current_char == '<':
                self.advance()
                return Token(Type.GREATER_THAN, '<')

            elif self.state.current_char == '>':
                self.advance()
                return Token(Type.LESSER_THAN, '>')

            elif self.state.current_char == '&':
                self.advance()
                return Token(Type.AMPERSAND_OPERATOR, '&')

            elif self.state.current_char == '.':
                self.advance()
                return Token(Type.DOT_OPERATOR, '.')

            elif self.state.current_char == '@':
                self.advance()
                return Token(Type.AT_OPERATOR, '@')

            elif self.state.current_char == ';':
                self.advance()
                return Token(Type.SEMICOLON, ';')

            elif self.state.current_char == '=':
                self.advance()
                return Token(Type.EQUAL, '=')

            elif self.state.current_char == '~':
                self.advance()
                return Token(Type.CURL, '~')

            elif self.state.current_char == '[':
                self.advance()
                return Token(Type.SQUARE_OPEN_BRACKET, '[')

            elif self.state.current_char == ']':
                self.advance()
                return Token(Type.SQUARE_CLOSE_BRACKET, ']')

            elif self.state.current_char == '$':
                self.advance()
                return Token(Type.DOLLAR, '$')

            elif self.state.current_char == '!':
                self.advance()
                return Token(Type.EXCLAMATION_MARK, '!')

            elif self.state.current_char == '#':
                self.advance()
                return Token(Type.HASH_TAG, '#')

            elif self.state.current_char == '%':
                self.advance()
                return Token(Type.MODULUS, '%')

            elif self.state.current_char == '^':
                self.advance()
                return Token(Type.CARROT, '^')

            elif self.state.current_char == '{':
                self.advance()
                return Token(Type.CURLY_OPEN_BRACKET, '{')

            elif self.state.current_char == '}':
                self.advance()
                return Token(Type.CURLY_CLOSE_BRACKET, '}')

            elif self.state.current_char == '`':
                self.advance()
                return Token(Type.BACK_TICK, '`')

            elif self.state.current_char == '\"':
                self.advance()
                return Token(Type.DOUBLE_QUOTE, '\"')

            elif self.state.current_char == '?':
                self.advance()
                return Token(Type.QUESTION_MARK, '?')

            elif self.state.current_char == '|':
                self.advance()
                return Token(Type.OR_OPERATOR, '|')

            self.error()

        return Token(Type.EOF, None)


# Processes the list of tokens to apply further transformations and filtering
class Screener:
    def __init__(self,tokens):  #  Initializes the screener with a list of tokens
        self.text = None
        self.tokens=tokens

    # erges specific sequences of tokens into single tokens
    def merge(self ):
        tokens=self.tokens

        for i in range(len(tokens)):
            # merge ternanary operator
            if i < len(tokens) and tokens[i].type == Type.MINUS and tokens[i + 1].type == Type.LESSER_THAN:
                tokens[i].value = '->'
                tokens[i].type = Type.TERNARY_OPERATOR
                tokens.pop(i + 1)

            # merge greater than or equal
            if i < len(tokens) and tokens[i].type == Type.GREATER_THAN and tokens[i + 1].type == Type.EQUAL:
                tokens[i].value = '>='
                tokens[i].type = Type.GREATER_THAN_OR_EQUAL
                tokens.pop(i + 1)

            # merge lesser than or equal
            if i < len(tokens) and tokens[i].type == Type.LESSER_THAN and tokens[i + 1].type == Type.EQUAL:
                tokens[i].value = '<='
                tokens[i].type = Type.LESSER_THAN_OR_EQUAL
                tokens.pop(i + 1)

            if i < len(tokens) and tokens[i].type == Type.MUL and tokens[i + 1].type == Type.MUL:
                tokens[i].value = '**'
                tokens[i].type = Type.POWER
                tokens.pop(i + 1)



        self.tokens=tokens

    # Identifies tokens that match reserved keywords and updates their type to RESERVED_KEYWORD

    def screen_reserved(self):
        tokens=self.tokens
        for i in range(len(tokens)):
            if tokens[i].value in RESERVED_KEYWORDS:
                tokens[i].type=Type.RESERVED_KEYWORD
        self.tokens=tokens

    # Removes all comment tokens from the list of tokens
    def remove_comments(self):
        tokens = self.tokens
        tokens_to_be_Poped=[]
        for (i , token) in enumerate(tokens):
            if tokens[i].type == Type.COMMENT:
                tokens_to_be_Poped.append(i)
        for i in tokens_to_be_Poped:
            tokens.pop(i)
        self.tokens = tokens

    # Runs the merging, comment removal, and reserved keyword identification in sequence and returns the processed list of tokens
    def screen(self):
        self.merge()
        self.remove_comments()
        self.screen_reserved()
        return self.tokens