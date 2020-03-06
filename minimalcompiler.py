# ALEXANDROS ALEXIOU 2929 cse52929
# ATHANASIOS KROKOS 3012  cse53012
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
    GREEN  = '\033[92m'
    RED    = '\033[91m'
    END    = '\033[0m'
    BOLD   = '\033[1m'

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
    GREATER_THAN_OR_EQUAL_TK = 15
    LESS_THAN_OR_EQUAL_TK = 16
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
    THEN_TK = 50
    #End Of File
    EOF_TK =51

# Lexical analyzer return values to the syntax analyzer
class Token():

    def __init__(self,tk_type,tk_value,tk_lineno,tk_charno):
        self.__tk_type = tk_type    # token type
        self.__tk_value = tk_value  # token string value
        self.__tk_lineno= tk_lineno # token line number
        self.__tk_charno= tk_charno # token character number from the start of the line

    def get_tk_type(self):
        return self.__tk_type
    
    def set_tk_type(self, tk_type):
        self.__tk_type=tk_type

    def get_tk_value(self):
        return self.__tk_value

    def set_tk_value(self, tk_value):
        self.__tk_value=tk_value
    
    def get_tk_lineno(self):
        return self.__tk_lineno

    def set_tk_lineno(self, tk_lineno):
        self.__tk_lineno=tk_lineno
    
    def get_tk_charno(self):
        return self.__tk_charno

    def set_tk_charno(self, tk_charno):
        self.__tk_charno=tk_charno

    # Tostring for debugging purposes
    def __str__(self):
        return '('+str(self.__tk_type) +','+ str(self.__tk_value) + ')'

class Quad():
    # eg. 100: +,a,b,c
    def __init__(self,label,op,var1,var2,res):
        self.__label = label    # eg. 100,101
        self.__op = op  # +,-,*,/
        self.__var1= var1 # variable name or constant
        self.__var2= var2 # variable name or constant
        self.__res= res   # variable name
    
    def get_label(self):
        return self.__label
    
    def set_label(self, label):
        self.__label=label

    def get_op(self):
        return self.__op

    def set_op(self, op):
        self.__op=op
    
    def get_var1(self):
        return self.__var1

    def set_var1(self, var1):
        self.__var1=var1

    def get_var2(self):
        return self.__var2

    def set_var1(self, var2):
        self.__var2=var2
    
    def get_res(self):
        return self.__res

    def set_res(self, res):
        self.__res=res

    # Tostring for debugging purposes
    def __str__(self):
        return '(' + str(self.__label) + ': ' + str(self.__op)+ ', ' + \
            str(self.__var1) + ', ' + str(self.__var2) + ', ' + str(self.__res) + ')'

##############################################################
#                                                            #
#                  Global declarations                       #
#                                                            #
##############################################################
lineno = -1 #Current line number
charno = -1 #Current Character number from the start of the line
token = Token(None,None,None,None) #Each token returned from the lexical analyzer will be stored here
infile = ''
mainprogram_name=''
#Dictionary to store bound words and token values
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
    '<=':           TokenType.LESS_THAN_OR_EQUAL_TK,
    '>=':           TokenType.GREATER_THAN_OR_EQUAL_TK,
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
    'then':         TokenType.THEN_TK
}

##############################################################
#                                                            #
#             Files related definitions                      #
#                                                            #
##############################################################
# Open files.
def open_files(input_file):
    global infile,lineno,charno
    lineno=1
    charno=0
    infile =  open(input_file,  'r', encoding='utf-8')

# Close files.
def close_files():
    global infile
    infile.close()

##############################################################
#                                                            #
#          Error printing related definitions                #
#                                                            #
##############################################################
def error_line_message(lineno, charno, *args):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']', ShellColors.BOLD + '%s:%d:%d:' %(infile.name, lineno, charno) + ShellColors.END, *args)
    # character pointer
    infile.seek(0)
    for i, line in enumerate(infile):
        if i == lineno-1:
            print(line.replace('\t', ' ').replace('\n', ' '))
            print(ShellColors.GREEN + ' ' * (charno-1) + '^' + ShellColors.END)
    close_files()
    sys.exit(1)

def error_file_not_found():
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']'+ ' File:'+ShellColors.GREEN +' '+ sys.argv[1] + ' '+ShellColors.END+'not found.')
    sys.exit(1)

def error(*args):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']', *args)
    sys.exit(1)

##############################################################
#                                                            #
#                   Lexical analyzer                         #
#                                                            #
##############################################################
def lex():
    
    global lineno,charno,infile
    character = infile.read(1)
    charno+=1
    
    # File is allowed to have empty lines tabs and spaces at the start
    while (character is ' ' or character is "\n" or character is "\t"):
        if character is "\n":
            lineno += 1
            charno=0
        character = infile.read(1)
        charno+=1

    while True:
        buffer = character
        #print(buffer)
        if character.isalpha():
            character = infile.read(1)
            charno+=1
            while character.isalpha() or character.isdigit():
                buffer+=character
                character = infile.read(1)
                charno+=1
            infile.seek(infile.tell() - 1)
            charno-=1
            if buffer in tokens.keys():
                retval = Token(tokens[buffer],buffer,lineno,charno)
            else:
                retval = Token(TokenType.ID_TK,buffer,lineno,charno)
            return retval
        elif character.isnumeric():
            while character.isnumeric():
                character = infile.read(1)
                charno+=1
                if character.isnumeric():
                    buffer+= character
                else:
                    if character.isalpha():
                        error_line_message(lineno,charno-1,'Variable names should begin with alphabetic character.')
            infile.seek(infile.tell() - 1)
            charno-=1
            '''character = infile.read(1)
            print("NEXT CHAR IS:"+character+"end")'''
            if int(buffer) > 32767 or int(buffer) < -32767:
                error_line_message(lineno,charno,'Integer value should be between [-32767,32767].')
            return Token(TokenType.NUMBER_TK,buffer,lineno,charno)
        elif character is '+':
           return Token(TokenType.PLUS_TK,buffer,lineno,charno)
        elif character is '-':
            return Token(TokenType.MINUS_TK,buffer,lineno,charno)
        elif character is '*':
            character =infile.read(1)
            charno+=1
            if character == '/':
                error_line_message(lineno,charno,'Expected "/*" to open comments before "*/" .')
            else :
                return Token(TokenType.TIMES_TK,buffer,lineno,charno)
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
                return Token(TokenType.SLASH_TK,buffer,lineno,charno)                                    
        elif character is '(':
           return Token(TokenType.LEFT_PARENTHESIS_TK,buffer,lineno,charno)
        elif character is ')':
            return Token(TokenType.RIGHT_PARENTHESIS_TK,buffer,lineno,charno)
        elif character is '[':
            return Token(TokenType.LEFT_BRACKET_TK,buffer,lineno,charno)
        elif character is ']':
            return Token(TokenType.RIGHT_BRACKET_TK,buffer,lineno,charno)
        elif character is '{':
            return Token(TokenType.LEFT_BRACE_TK,buffer,lineno,charno)
        elif character is '}':
            return Token(TokenType.RIGHT_BRACE_TK,buffer,lineno,charno)
        elif character is '<':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.LESS_THAN_OR_EQUAL_TK,buffer,lineno,charno)
            elif character is '>':
                buffer+=character
                return Token(TokenType.NOT_EQUAL_TK,buffer,lineno,charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.LESS_TK,buffer,lineno,charno)
        elif character is '>':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.GREATER_THAN_OR_EQUAL_TK,buffer,lineno,charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.GREATER_TK,buffer,lineno,charno)
        elif character is '=':
            return Token(TokenType.EQUAL_TK,buffer,lineno,charno)
        elif character is ',':
            return Token(TokenType.COMMA_TK,buffer,lineno,charno)
        elif character is ';':
            return Token(TokenType.SEMICOLON_TK,buffer,lineno,charno)
        elif character is ':':
            character = infile.read(1)
            if character is '=':
                buffer+=character
                return Token(TokenType.ASSIGN_TK,buffer,lineno,charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.COLON_TK,buffer,lineno,charno)
        elif character is '':
            return Token(TokenType.EOF_TK,'EOF',lineno,0)
        else:
            error_line_message(lineno,charno,'Invalid character.')

##############################################################
#                                                            #
#           Syntax analyzer related functions                #
#                                                            #
##############################################################
def program():
    global token, lineno,charno
    if token.get_tk_type() == TokenType.PROGRAM_TK:
        token = lex()
        if token.get_tk_type() == TokenType.ID_TK:
            token = lex()
            if token.get_tk_type()== TokenType.LEFT_BRACE_TK:
                token = lex()
                block()
                if token.get_tk_type() != TokenType.RIGHT_BRACE_TK:
                    error('Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
                token=lex()
            else:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())
        else:
           error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected program name but found \'%s\' instead.' % token.get_tk_value())
    else:
        error('Expected \'program\' keyword but found \'%s\' instead.' % token.get_tk_value())
    

def block():
    declarations()
    subprograms() 
    statements() 

def declarations():
    global token
    if token.get_tk_type()== TokenType.DECLARE_TK:
        token = lex()
        varlist() 
        if token.get_tk_type() != TokenType.SEMICOLON_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \';\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()

def varlist():
    global token
    if token.get_tk_type() == TokenType.ID_TK:
        token = lex()
        while token.get_tk_type() == TokenType.COMMA_TK:
            token = lex()
            if token.get_tk_type() != TokenType.ID_TK:
               error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected variable declaration but found \'%s\' instead' % token.get_tk_value())
            token = lex()

def subprograms():
    global token
    while token.get_tk_type()==TokenType.FUNCTION_TK or token.get_tk_type()==TokenType.PROCEDURE_TK:
        token = lex()
        if token.get_tk_type()==TokenType.ID_TK:
            token = lex()
            funcbody()
        else:
             error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected subprogram name but found \'%s\' instead.' % token.get_tk_value())

def funcbody():
    global token
    formalpars()
    if token.get_tk_type()==TokenType.LEFT_BRACE_TK:
        token = lex()
        block()
        if token.get_tk_type() != TokenType.RIGHT_BRACE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())  
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected subprogram block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())

def formalpars():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token=lex()
        formalparlist()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token=lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value()) 

def formalparlist():
    global token
    formalparitem()
    while token.get_tk_type() == TokenType.COMMA_TK:
        token = lex()
        if token.get_tk_type() != TokenType.IN_TK and token.get_tk_type() != TokenType.INOUT_TK:
           error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected formal parameter declaration but found \'%s\' instead'% token.get_tk_value())
        formalparitem()

def formalparitem():
    global token
    if token.get_tk_type() == TokenType.IN_TK or token.get_tk_type() == TokenType.INOUT_TK:
        token = lex()
        if token.get_tk_type() != TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected formal parameter name but found \'%s\' instead'% token.get_tk_value()) 
        token = lex()

def statements():
    global token
    if token.get_tk_type() == TokenType.LEFT_BRACE_TK:
        token = lex()
        statement()
        while token.get_tk_type() == TokenType.SEMICOLON_TK:
            token = lex()
            statement()
        if token.get_tk_type()!= TokenType.RIGHT_BRACE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected statements end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        statement()

def statement():
    global token
    if token.get_tk_type() == TokenType.ID_TK:
        token = lex()
        assignment_stat()
    elif token.get_tk_type() == TokenType.IF_TK:
        token = lex()
        if_stat()
    elif token.get_tk_type() == TokenType.WHILE_TK:
        token = lex()
        while_stat()
    elif token.get_tk_type() == TokenType.DOUBLEWHILE_TK:
        token = lex()
        doublewhile_stat()
    elif token.get_tk_type() == TokenType.LOOP_TK:
        token = lex()
        loop_stat()
    elif token.get_tk_type() == TokenType.EXIT_TK:
        token = lex()
        #exit_stat() ???
    elif token.get_tk_type() == TokenType.FORCASE_TK:
        token = lex()
        forcase_stat()
    elif token.get_tk_type() == TokenType.INCASE_TK:
        token = lex()
        incase_stat()
    elif token.get_tk_type() == TokenType.RETURN_TK:
        token = lex()
        return_stat()
    elif token.get_tk_type() == TokenType.CALL_TK:
        token = lex()
        call_stat()
    elif token.get_tk_type() == TokenType.PRINT_TK:
        token = lex()
        print_stat()
    elif token.get_tk_type() == TokenType.INPUT_TK:
        token = lex()
        input_stat()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected statement but found \'%s\' instead' % token.get_tk_value())
    
def assignment_stat():
    global token
    if token.get_tk_type()==TokenType.ASSIGN_TK:
        token=lex()
        expression()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':=\' but found \'%s\' instead' % token.get_tk_value())

def if_stat():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        condition() 
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
           error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' after if condition but found \'%s\' instead' % token.get_tk_value())
        token = lex()
        if token.get_tk_type() == TokenType.THEN_TK:
            token = lex()
            statements()
            elsepart()
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'then\' after if condition but found \'%s\' instead' % token.get_tk_value())
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after if token but found \'%s\' instead' % token.get_tk_value())        

def elsepart():
    global token
    if token.get_tk_type() == TokenType.ELSE_TK:
        token = lex()
        statements()

def while_stat():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        condition()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        statements()
    else:
         error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after \'while\' but found \'%s\' instead'% token.get_tk_value())

def doublewhile_stat():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token =lex()
        condition()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        statements()
        if token.get_tk_type() != TokenType.ELSE_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'else\' inside doublewhile but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        statements()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after \'doublewhile\' but found \'%s\' instead'% token.get_tk_value())

def loop_stat():
    statements()

def forcase_stat():
    global token
    while token.get_tk_type()== TokenType.WHEN_TK:
        token = lex()
        if token.get_tk_type()== TokenType.LEFT_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.get_tk_type()== TokenType.RIGHT_PARENTHESIS_TK:
                token = lex()
                if token.get_tk_type()== TokenType.COLON_TK:
                    token = lex()
                    statements()
                else:
                    error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':\' but found \'%s\' instead'% token.get_tk_value())
            else:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        else:
             error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())
    if token.get_tk_type()== TokenType.DEFAULT_TK:
        token = lex()
        if token.get_tk_type()== TokenType.COLON_TK:
            token = lex()
            statements()
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':\' after \'default\' but found \'%s\' instead'% token.get_tk_value()) 
        
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'default:\' declaration but found \'%s\' instead'% token.get_tk_value())

def incase_stat():
    global token
    while token.get_tk_type()== TokenType.WHEN_TK:
        token = lex()
        if token.get_tk_type()== TokenType.LEFT_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.get_tk_type()== TokenType.RIGHT_PARENTHESIS_TK:
                token = lex()
                if token.get_tk_type()== TokenType.COLON_TK:
                    token = lex()
                    statements()
                else:
                    error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':\' but found \'%s\' instead'% token.get_tk_value())
            else:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        else:
             error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())

def return_stat():
    global token
    token = lex()
    expression()

def call_stat():
    global token
    if token.get_tk_type() == TokenType.ID_TK:
        token = lex()
        actualpars()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected function or procedure id but found \'%s\' instead'% token.get_tk_value())

def print_stat():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        expression()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())

def input_stat():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        if token.get_tk_type() != TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected variable id but found \'%s\' instead'% token.get_tk_value())
        token = lex()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())

def condition():
    global token
    boolterm()
    while token.get_tk_type() == TokenType.OR_TK:
        token = lex()
        boolterm()

def boolterm():
    global token
    boolfactor()
    while token.get_tk_type() == TokenType.AND_TK:
        token = lex()
        boolfactor()

def boolfactor():
    global token
    if token.get_tk_type() == TokenType.NOT_TK:
        token = lex()
        if token.get_tk_type() == TokenType.LEFT_BRACKET_TK:
            token = lex()
            condition()
            if token.get_tk_type() != TokenType.RIGHT_BRACKET_TK:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \']\' but found \'%s\' instead'% token.get_tk_value())
            token = lex()
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'[\' after \'not\' but found \'%s\' instead'% token.get_tk_value())
    elif token.get_tk_type() == TokenType.LEFT_BRACKET_TK:
        token = lex()
        condition()
        if token.get_tk_type() != TokenType.RIGHT_BRACKET_TK:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \']\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        expression()
        relational_oper()
        expression()

def relational_oper():
    global token
    if token.get_tk_type() != TokenType.EQUAL_TK and token.get_tk_type() != TokenType.LESS_THAN_OR_EQUAL_TK and token.get_tk_type() != TokenType.LESS_TK and \
        token.get_tk_type() != TokenType.GREATER_THAN_OR_EQUAL_TK and token.get_tk_type() != TokenType.GREATER_TK and token.get_tk_type() != TokenType.LESS_THAN_OR_EQUAL_TK and \
        token.get_tk_type() != TokenType.NOT_EQUAL_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected relational operator but found \'%s\' instead'% token.get_tk_value())
    token = lex()

def expression():
    global token
    optional_sign()
    term()
    while token.get_tk_type()==TokenType.PLUS_TK or token.get_tk_type()==TokenType.MINUS_TK :
        add_oper()
        term()
        
def optional_sign():
    global token
    if token.get_tk_type()== TokenType.PLUS_TK or token.get_tk_type()==TokenType.MINUS_TK :
        add_oper()
    
def term():
    global token 
    factor()
    while token.get_tk_type()==TokenType.SLASH_TK or token.get_tk_type()==TokenType.TIMES_TK:
        mul_oper()
        factor()
        
def factor(): 
    global token
    if token.get_tk_type() == TokenType.NUMBER_TK or token.get_tk_type() == TokenType.PLUS_TK or token.get_tk_type() == TokenType.MINUS_TK:
        token = lex()
    elif token.get_tk_type()==TokenType.LEFT_PARENTHESIS_TK:
        token=lex()
        expression()
        if token.get_tk_type()!=TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()

    elif token.get_tk_type()==TokenType.ID_TK:
        token=lex()
        idtail()
    else: 
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected factor but found \'%s\' instead' % token.get_tk_value())

def idtail():
   global token
   if token.get_tk_type()==TokenType.LEFT_PARENTHESIS_TK:
       actualpars() 

def add_oper():
    global token
    if token.get_tk_type()!= TokenType.PLUS_TK and token.get_tk_type()!= TokenType.MINUS_TK :
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'+\' or \'-\' but found \'%s\' instead' % token.get_tk_value())
    token=lex()

def mul_oper():
    global token
    if token.get_tk_type() != TokenType.TIMES_TK and token.get_tk_type() != TokenType.SLASH_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'*\' or \'/\' but found \'%s\' instead' % token.get_tk_value())
    token = lex()

def actualpars():
    global token
    if token.get_tk_type() == TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        actualparlist()
        if token.get_tk_type() != TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after procedure or function call  but found \'%s\' instead'% token.get_tk_value())

def actualparlist():
    global token
    if token.get_tk_type() == TokenType.IN_TK or token.get_tk_type() == TokenType.INOUT_TK:
        actualparitem()
        while token.get_tk_type() == TokenType.COMMA_TK:
            token = lex()
            actualparitem()

def actualparitem():
    global token
    if token.get_tk_type() == TokenType.IN_TK:
        token = lex()
        expression()
    elif token.get_tk_type() == TokenType.INOUT_TK:
        token = lex()
        if token.get_tk_type() != TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected variable id but found \'%s\' instead' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected parameter type in or inout but found \'%s\' instead' % token.get_tk_value())

##############################################################
#                                                            #
#                   main compiler program                    #
#                                                            #
##############################################################
def main(argv):
    open_files(argv)
    global token
    token = lex()
    #Begin syntax analysis
    program()
    if token.get_tk_type() != TokenType.EOF_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),
            'Expected \'EOF\' but found \'%s\' instead' % token.get_tk_value())
    '''# This is for lex debugging
    while True:
        token=lex()
        print(token)
        print('\n')
        if token.get_tk_type()==TokenType.EOF_TK:
            break'''
    '''while True:
        character = infile.read(1)
        print(character)
        print('\n')
        if character=='':
            break'''
    close_files()

if __name__=='__main__':

    # No arguments passed
    if len(sys.argv)==1:
        error(':no input files.')
        sys.exit(1)

    # File does not exist
    if os.path.exists(sys.argv[1])==False:
        error_file_not_found()
        sys.exit(1)

    # Call main function
    main(sys.argv[1])
