import sys,os
import string
from enum import Enum

##############################################################
#                                                            #
#                     Class definitions                      #
#                                                            #
##############################################################

# For Error and warning printing
class ShellColors:
    GRN    = '\033[92m'
    WRN    = '\033[95m'
    ERR    = '\033[91m'
    END    = '\033[0m'
    BLD    = '\033[1m'
    UNDRLN = '\033[4m'

# Token ids
class TokenType(Enum):
    ID_TK = 0
    NUMBER_TK = 1
    # Arithmetic Operators
    PLUS_TK = 2
    MINUS_TK = 3
    TIMES_TK = 4
    SLASH_TK = 5
    # Punctuation marks
    COMMA_TK = 8
    COLON_TK = 9
    SEMICOLON_TK = 10
    # Relational operators
    EQUAL_TK = 11
    LESS_TK = 12
    GREATER_TK = 13
    NOT_EQUAL_TK = 14
    GREATER_THAN_OR_EQUAL = 15
    LESS_THAN_OR_EQUAL = 16
    # Value Assignment
    ASSIGN_TK = 17
    # Brackets
    LEFT_PARENTHESIS_TK = 18
    RIGHT_PARENTHESIS_TK = 19
    LEFT_BRACKET_TK = 20
    RIGHT_BRACKET_TK = 21
    LEFT_BRACE_TK = 22
    RIGHT_BRACE_TK= 23
    # Comments
    ONE_LINE_TK = 24
    OPEN_COMMENT_TK = 25
    CLOSE_COMMENT_TK = 26
    # Bound Words
    PROGRAM_TK = 27
    DECLARE_TK = 28
    IF_TK = 29
    ELSE_TK = 30
    WHILE_TK = 31
    DOUBLEWHILE_TK = 32
    LOOP_TK = 33
    EXIT_TK = 34
    FORCASE_TK = 35
    INCASE_TK = 36
    WHEN_TK = 37
    DEFAULT_TK = 38
    NOT_TK = 39
    AND_TK =40
    OR_TK = 41
    FUNCTION_TK = 42
    PROCEDURE_TK = 43
    CALL_TK = 44
    RETURN_TK = 45
    IN_TK = 46
    INOUT_TK = 47
    INPUT_TK = 48
    PRINT_TK = 49
    #End Of File
    EOF_TK =50

# Lexical analyzer return values to the syntax analyzer
class Token():

    def __init__(self,tk_type,tk_value):
        self.__tk_type = tk_type
        self.__tk_value = tk_value

    def get_tk_type(self):
        return self.__tk_type
    
    def set_tk_type(self, tk_type):
        self.__tk_type=tk_type

    def get_tk_value(self):
        return self.__tk_value

    def set_tk_value(self, tk_value):
        self.__tk_value=tk_value

    def __str__(self):
        return '('+str(self.__tk_type) +','+ str(self.__tk_value) + ')'

##############################################################
#                                                            #
#         Global declarations and definitions                #
#                                                            #
##############################################################

lineno = -1 #Current line number
charno = -1 #Current Character number from the start of the line
token = Token(None,None) 
infile = ''


tokens = {
    '+':            TokenType.PLUS_TK,
    '-':            TokenType.MINUS_TK,
    '*':            TokenType.TIMES_TK,
    '/':            TokenType.SLASH_TK,
    ',':            TokenType.COMMA_TK,
    ':':            TokenType.COLON_TK,
    ';':            TokenType.SEMICOLON_TK,
    '<':            TokenType.LESS_TK,
    '>':            TokenType.GREATER_TK,
    '<=':           TokenType.LESS_THAN_OR_EQUAL,
    '>=':           TokenType.GREATER_THAN_OR_EQUAL,
    '=':            TokenType.EQUAL_TK,
    '<>':           TokenType.NOT_EQUAL_TK,
    ':=':           TokenType.ASSIGN_TK,
    '(':            TokenType.LEFT_PARENTHESIS_TK,
    ')':            TokenType.RIGHT_PARENTHESIS_TK,
    '[':            TokenType.LEFT_BRACKET_TK,
    ']':            TokenType.RIGHT_BRACKET_TK,
    '{':            TokenType.LEFT_BRACE_TK,
    '}':            TokenType.RIGHT_BRACE_TK,
    '//':           TokenType.ONE_LINE_TK,
    '/*':           TokenType.OPEN_COMMENT_TK,
    '*/':           TokenType.CLOSE_COMMENT_TK,
    'program':      TokenType.PROGRAM_TK,
    'declare':      TokenType.DECLARE_TK,
    'if':           TokenType.IF_TK,
    'else':         TokenType.ELSE_TK,
    'while':        TokenType.WHILE_TK,
    'doublewhile':  TokenType.DOUBLEWHILE_TK,
    'loop':         TokenType.LOOP_TK,
    'exit':         TokenType.EXIT_TK,
    'forcase':      TokenType.FORCASE_TK,
    'incase':       TokenType.INCASE_TK,
    'when':         TokenType.WHEN_TK,
    'default':      TokenType.DEFAULT_TK,
    'not':          TokenType.NOT_TK,
    'and':          TokenType.AND_TK,
    'or':           TokenType.OR_TK,
    'function':     TokenType.FUNCTION_TK,
    'procedure':    TokenType.PROCEDURE_TK,
    'call':         TokenType.CALL_TK,
    'return':       TokenType.RETURN_TK,
    'in':           TokenType.IN_TK,
    'inout':        TokenType.INOUT_TK,
    'input':        TokenType.INPUT_TK,
    'print':        TokenType.PRINT_TK,
}

# Open files.
def open_files(input_file):
    global infile,lineno,charno
    lineno=1
    charno=0
    infile = open(input_file,"r+")

# Close files.
def close_files():
    global infile
    infile.close()

# Error messages printing beatifully
def error_line_message(lineno, charno, *args, **kwargs):
    print('[' + ShellColors.ERR + 'ERROR' + ShellColors.END + ']', ShellColors.BLD + '%s:%d:%d:' %
        (infile.name, lineno, charno) + ShellColors.END, *args,  **kwargs)
    currchar = infile.tell()
    # character pointer
    infile.seek(0)
    for index, line in enumerate(infile):
        if index == lineno-1:
            print(line.replace('\t', ' ').replace('\n', ' '))
            print(ShellColors.GRN + " " * (charno-1) + '^' + ShellColors.END)
    close_files()
    sys.exit()

##############################################################
#                                                            #
#                   Lexical analyzer                         #
#                                                            #
##############################################################
def lex():
    
    global lineno,charno
    character = infile.read(1)
    charno+=1

    # File is allowed to have empty lines tabs and spaces at the start
    while (character == ' ' or character == "\n" or character == "\t"):
        if character == "\n":
            lineno += 1
            charno=0
        character = infile.read(1)
        charno+=1
    
    while True:
        buffer = character
        if character.isalpha():

            character = infile.read(1)
            charno+=1

            while character.isalpha() or character.isnumeric():
                buffer+=character
                character = infile.read(1)
                charno+=1
                

            infile.seek(infile.tell() - 1)
            charno-=1

            if buffer in tokens.keys():
                retval = Token(tokens[buffer],buffer)
            else:
                retval = Token(TokenType.ID_TK,buffer)

            return retval
        elif character.isnumeric():

            while character.isnumeric():
               
                character = infile.read(1)
                charno+=1
                if character.isnumeric():
                    buffer+= character
                else:
                    if character.isalpha():
                        error_line_message(lineno,charno,'Variable names should begin with alphabetic character.')
                        close_files()
                        sys.exit(0)
                        
            infile.seek(infile.tell() - 1)
            charno-=1
           
            if int(buffer) > 32767 or int(buffer) < -32767:
                error_line_message(lineno,charno,'Integer value out of range [-32767,32767].')
                close_files()
                sys.exit(0)
            return Token(TokenType.NUMBER_TK,buffer)
        elif character is '+':
           return Token(TokenType.PLUS_TK,buffer)
        elif character is '-':
            return Token(TokenType.MINUS_TK,buffer)
        elif character is '*':
            character =infile.read(1)
            charno+=1
            if character == '/':
                error_line_message(lineno,charno,'Expected "/*" to open comments before "*/" .')
                close_files()
                sys.exit()
            else :
                return Token(TokenType.TIMES_TK,buffer)
        elif character is '/':
            character = infile.read(1)
            comments_charno=charno
            comments_line=lineno
            charno+=1
            if character is '*':
                while (1):
                    character = infile.read(1)
                    if not character:
                        error_line_message(comments_line,comments_charno,'Comments opened. Expected  "*/"  but EOF reached.')
                        close_files()
                        sys.exit()
                    if character is '*':
                        character = infile.read(1)
                        if character is '/':
                            
                            return lex()
                    elif character is '\n':
                        lineno += 1
                        charno=0
            elif character is '/':
                while(character is not '\n'):
                    character=infile.read(1)
                lineno+=1
                charno=0
                return lex()                        
            elif character is not '/':
                return Token(TokenType.SLASH_TK,buffer)                                    
        elif character is '(':
           return Token(TokenType.LEFT_PARENTHESIS_TK,buffer)
        elif character is ')':
            return Token(TokenType.RIGHT_PARENTHESIS_TK,buffer)
        elif character is '[':
            return Token(TokenType.LEFT_BRACKET_TK,buffer)
        elif character is ']':
            return Token(TokenType.RIGHT_BRACKET_TK,buffer)
        elif character is '{':
            return Token(TokenType.LEFT_BRACE_TK,buffer)
        elif character is '}':
            return Token(TokenType.RIGHT_BRACE_TK,buffer)
        elif character is '<':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.LESS_THAN_OR_EQUAL,buffer)
            elif character is '>':
                buffer+=character
                return Token(TokenType.NOT_EQUAL_TK,buffer)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.LESS_TK,buffer)
        elif character is '>':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.GREATER_THAN_OR_EQUAL,buffer)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.GREATER_TK,buffer)
        elif character is '=':
            return Token(TokenType.EQUAL_TK,buffer)
        elif character is ',':
            return Token(TokenType.COMMA_TK,buffer)
        elif character is ';':
            return Token(TokenType.SEMICOLON_TK,buffer)
        elif character is ':':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.ASSIGN_TK,buffer)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.COLON_TK,buffer)
        elif character is '':
            return Token(TokenType.EOF_TK,'EOF')
        else:
            error_line_message(lineno,charno,'Invalid character.')
            close_files()
            sys.exit()


##############################################################
#                                                            #
#                   main compiler program                    #
#                                                            #
##############################################################
def main(argv):
    open_files(argv)
    while True:
        global token
        token=lex()
        print(token)
        print('\n')
        if(token.get_tk_value()=='EOF'):
            sys.exit()
    close_files()

if __name__=='__main__':

    # No arguments passed
    if len(sys.argv)==1:
        print('[' + ShellColors.ERR + 'ERROR' + ShellColors.END + ']'+ ": no input files")
        sys.exit(1)

    # File does not exist
    if os.path.exists(sys.argv[1])==False:
        print('[' + ShellColors.ERR + 'ERROR' + ShellColors.END + ']'+ ShellColors.ERR +' '+ sys.argv[1] + ' '+ShellColors.END+ " File specified not found.")
        sys.exit(1)

    # Call main function
    main(sys.argv[1])
