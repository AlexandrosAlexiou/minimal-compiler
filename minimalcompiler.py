#!/usr/bin/env python3
import sys
import os
import string
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
class TokenType():
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
    # eg. 100: -,a,b,c => c := a - b
    def __init__(self, label, op, x, y, z):
        self.__label = label    # eg. 100,101
        self.__op = op          # +,-,*,/
        self.__x= x       # variable name or constant
        self.__y= y       # variable name or constant
        self.__z= z         # variable name
    
    def get_label(self):
        return self.__label
    
    def set_label(self, label):
        self.__label = label

    def get_op(self):
        return self.__op

    def set_op(self, op):
        self.__op = op
    
    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y):
        self.__y = y
    
    def get_z(self):
        return self.__z

    def set_z(self, z):
        self.__z=z

    # tostring for debugging purposes
    def __str__(self):
        return '(' + str(self.__label) + ': ' + str(self.__op)+ ', ' + str(self.__x) + ', ' + str(self.__y) + ', ' + str(self.__z) + ')'

    # tostring for intermediate code file generation
    def quad_to_file(self):
        return str(self.__label) + ': ' + str(self.__op)+ ', ' + str(self.__x) + ', ' + str(self.__y) + ', ' + str(self.__z) + '\n'


class Scope():
    def __init__(self, nestingLevel = 0, previous_scope = None):
        self.__entities_list = list()
        self.__nesting_level = nestingLevel
        self.__current_offset = 12
        self.__previous_scope = previous_scope

    def get_entities_list(self):
        return self.__entities_list

    def add_Entity(self, Entity):
        self.__entities_list.append(Entity)

    def get_nesting_level(self):
        return self.__nesting_level

    def get_current_offset(self):
        current = self.__current_offset
        self.__current_offset += 4  # this is the next offset
        return current

    def get_previous_scope(self):
        return self.__previous_scope

    # tostring for debugging purposes
    def __str__(self):
        return '( ' + str(self.__nesting_level) + ', ' + self.__previous_scope.__str__() + ' )'


class  Argument():
    def __init__(self, parMode, nextArgument):
        self.__parMode = parMode
        self.__nextArgument = nextArgument
    
    def get_parMode(self):
        return self.__parMode

    def set_parMode(self, parMode):
        self.__parMode = parMode

    def get_nextArgument(self):
        return self.__nextArgument

    def set_nextArgument(self, nextArgument):
        self.__nextArgument = nextArgument
    
    # tostring for debugging purposes
    def __str__(self):
        return '( ' + self.__parMode + ', ' + self.__nextArgument.__str__() + ' )'


class Entity():
    # Entity type can be Variable or Function or Parameter or TemporaryVariable 
    def __init__(self, name, entityType): 
        self.__name = name
        self.__entityType = entityType
        self.__nextEntity = None

    def get_name(self):
        return self.__name

    def get_entityType(self):
        return self.__entityType

    def get_nextEntity(self):
        return self.__nextEntity

    # tostring for debugging purposes
    def __str__(self):
        return  '( ' + ' Entity name: ' + self.__name + ',EntityType: ' + self.__entityType + ' )'


class Variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, 'Variable')
        self.__offset = __offset

    def get_offset(self):
        return self.__offset

    def set_offset(self, offset):
        self.__offset = offset

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '( ' +'Variable offset: ' + str(self.__offset) + ' )'


class Function(Entity):
    def __init__(self, name, startQuad=-1):
        super().__init__(name, 'Function')
        self.__startQuad = startQuad
        self.__arguments_list = list()
        self.__framelength =  -1

    def get_startQuad(self):
        return self.__startQuad
    
    def set_start_quad(self, start_quad):
        self.start_quad = start_quad

    def get_arguments_list(self):
        return self.__arguments_list

    def add_argument_in_list(self, argument):
        self.__arguments_list.append(argument)

    def get_framelength(self):
        return self.__framelength

    def set_framelen(self, framelength):
        self.__framelength = framelength

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '( startQuad: ' + str(self.__startQuad) + ', framelen: ' + str(self.__framelength) + ' )'


class Parameter(Entity):
    def __init__(self, name, parMode, offset = -1):
        super().__init__(name, 'Parameter')
        self.__parMode = parMode
        self.__offset = offset

    def get_parMode(self):
        return self.__parMode

    def set_parMode(self, parMode):
        self.__parMode = parMode

    def get_offset(self):
        return self.__offset
    
    def set_offset(self, offset):
        self.__offset = offset
    
    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '( Parameter mode: ' + self.__parMode + ', offset: ' + str(self.__offset) + ' )'


class TemporaryVariable(Entity):
    def __init__(self, name, offset = -1):
        super().__init__(name, 'Tempvar')
        self.__offset = offset

    def get_offset(self):
        return self.__offset

    def set_offset(self, offset):
        self.__offset = offset

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '(Temporary Variable offset: ' + str(self.__offset) + ')'


##############################################################
#                                                            #
#                     Global variables                       #
#                                                            #
##############################################################
lineno = 1 #Current line number
charno = 0 #Current Character number from the start of the line
token = Token(None,None,None,None) #Each token returned from the lexical analyzer will be stored here
infile = '' # input file pointer
intfile = '' # intermediate code file
mainprogram_name = '' # main program name to generate halt quad
quads_list= list() # Program equivalent in quadruples.
scopes = list() # Program current scopes
nextlabel = 0  # next quad label that is going to be created
tmpvars = dict() # Temporary variable names used in intermediate code generation.
next_tmpvar = 1  # Temporary variables. eg. T_1 ... T_2 etc.
halt_label = -1
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
#                  Open/Close I/O files                      #
#                                                            #
##############################################################
# Open files.
def open_files(input_filename,intermediate_code_filename):
    global infile,intfile
    infile = open(input_filename,  'r', encoding='utf-8')
    intfile= open(intermediate_code_filename,  'w', encoding='utf-8')


# Close files.
def close_files():
    global infile,intfile
    infile.close()
    intfile.close()


# Generate a file containing the intermediate code
def generate_intermediate_code_file():
    for quad in quads_list:
        intfile.write(quad.quad_to_file())

        
##############################################################
#                                                            #
#                   Error printing                           #
#                                                            #
##############################################################
def error_line_message(lineno, charno, *args):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']', ShellColors.BOLD + '%s:%d:%d:' %(infile.name, lineno, charno) + ShellColors.END, *args)
    # character pointer reset
    infile.seek(0)
    for i, line in enumerate(infile):
        if i == lineno-1:
            print(line.replace('\t', ' ').replace('\n', ' ')) # \t and \n count as 1 character
            print(ShellColors.GREEN + ' ' * charno + '^' + ShellColors.END)
    close_files()
    sys.exit(1)


def error_file_not_found(infile):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']'+ ' File:'+ShellColors.GREEN +' '+ infile + ' '+ShellColors.END+'does not exist.')
    sys.exit(1)


def error(*args):
    print('[' + ShellColors.RED + 'FATAL ERROR' + ShellColors.END + ']', *args)
    sys.exit(1)

            
##############################################################
#                                                            #
#                   Lexical analyzer                         #
#                                                            #
##############################################################
def lex():
    global lineno,charno,infile
    while(True):
        character = infile.read(1)
        charno+=1
        # File is allowed to have empty lines tabs and spaces at the start
        while (character is ' ' or character is "\n" or character is "\t"):
            if character is "\n":
                lineno += 1
                charno=0
            character = infile.read(1)
            charno+=1
        buffer = character
        #print(buffer)
        if character.isalpha():
            character = infile.read(1)
            charno+=1
            while character.isalpha() or character.isdigit():
                buffer+=character
                character = infile.read(1)
                charno+=1
            if buffer in tokens.keys():
                retval = Token(tokens[buffer],buffer,lineno,charno)
            else:
                retval = Token(TokenType.ID_TK,buffer,lineno,charno)
            infile.seek(infile.tell() - 1)
            charno-=1
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
            if int(buffer) > 32767 or int(buffer) < -32767:
                error_line_message(lineno,charno,'Integer value should be between [-32767,32767].')
            infile.seek(infile.tell() - 1)
            charno-=1
            return Token(TokenType.NUMBER_TK,buffer,lineno,charno)
        elif character is '+':
            return Token(TokenType.PLUS_TK,buffer,lineno,charno)
        elif character is '-':
            return Token(TokenType.MINUS_TK,buffer,lineno,charno)
        elif character is '*':
            character =infile.read(1)
            charno+=1
            if character is '/':
                error_line_message(lineno,charno,'Expected "/*" to open comments before "*/" .')
            else :
                infile.seek(infile.tell() - 1)
                charno-=1
                return Token(TokenType.TIMES_TK,buffer,lineno,charno)
        elif character is '/':
            character = infile.read(1)
            comments_charno=charno
            comments_line=lineno
            charno+=1
            if character is '*':
                while(True):
                    character = infile.read(1)
                    if not character:
                        error_line_message(comments_line,comments_charno,'Comments opened. Expected  "*/"  but EOF reached.')
                    if character is '*':
                        character = infile.read(1)
                        if character is '/':
                            break
                    elif character is '\n':
                        lineno += 1
                        charno=0
            elif character is '/':
                while(character is not '\n'):
                    character=infile.read(1)
                lineno+=1
                charno=0                       
            else:
                infile.seek(infile.tell() - 1)
                charno-=1
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
#               Intermediate code functions                  #
#                                                            #
##############################################################
def nextquad():
    return nextlabel


def genquad(op=None, x = '_', y = '_', z = '_'):
    global nextlabel
    label = nextlabel
    nextlabel += 1
    newquad  = Quad(label, op, x, y, z)
    quads_list.append(newquad)


def newtemp():
    global tmpvars, next_tmpvar
    key = 'T_'+str(next_tmpvar)
    tmpvars[key] = None
    next_tmpvar += 1
    return key


def emptylist():
    return list()


def makelist(label):
    new_list = list()
    new_list.append(label)
    return new_list


def merge(list1, list2):
    return list1 + list2


def backpatch(label_list, z):
    global quads_list
    for quad in quads_list:
        if quad.get_label() in label_list:
            quad.set_z(z)


##############################################################
#                                                            #
#           Syntax analyzer related functions                #
#                                                            #
##############################################################
def program():
    global token, lineno, charno,  mainprogram_name
    if token.get_tk_type() is TokenType.PROGRAM_TK:
        token = lex()
        if token.get_tk_type() is TokenType.ID_TK:
            mainprogram_name = name = token.get_tk_value()
            token = lex()
            if token.get_tk_type() is TokenType.LEFT_BRACE_TK:
                token = lex()
                block(name)
                if token.get_tk_type() is not TokenType.RIGHT_BRACE_TK:
                     error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
                token=lex()
            else:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())
        else:
           error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected program name but found \'%s\' instead.' % token.get_tk_value())
    else:
       error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \'program\' keyword but found \'%s\' instead.' % token.get_tk_value())
    

def block(name):
    declarations()
    subprograms()
    genquad('begin_block', name)
    statements() 
    if name is mainprogram_name:
        halt_label = nextquad()
        genquad('halt')
    genquad('end_block', name)


def declarations():
    global token
    while token.get_tk_type() is TokenType.DECLARE_TK:
        token = lex()
        varlist() 
        if token.get_tk_type() is not TokenType.SEMICOLON_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \';\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()


def varlist():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        token = lex()
        while token.get_tk_type() is TokenType.COMMA_TK:
            token = lex()
            if token.get_tk_type() is not TokenType.ID_TK:
               error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected variable declaration but found \'%s\' instead' % token.get_tk_value())
            token = lex()


def subprograms():
    global token
    while token.get_tk_type() is TokenType.FUNCTION_TK or token.get_tk_type() is TokenType.PROCEDURE_TK:
        token = lex()
        if token.get_tk_type() is TokenType.ID_TK:
            name = token.get_tk_value()
            token = lex()
            funcbody(name)
        else:
             error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected subprogram name but found \'%s\' instead.' % token.get_tk_value())


def funcbody(name):
    global token
    formalpars(name)
    if token.get_tk_type() is TokenType.LEFT_BRACE_TK:
        token = lex()
        block(name)
        if token.get_tk_type() is not TokenType.RIGHT_BRACE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())  
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected subprogram block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())


def formalpars(func_name):
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token=lex()
        formalparlist(func_name)
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token=lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value()) 


def formalparlist(func_name):
    global token
    formalparitem(func_name)
    while token.get_tk_type() is TokenType.COMMA_TK:
        token = lex()
        if token.get_tk_type() is not TokenType.IN_TK and token.get_tk_type() is not TokenType.INOUT_TK:
           error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected formal parameter declaration but found \'%s\' instead'% token.get_tk_value())
        formalparitem(func_name)


def formalparitem(func_name):
    global token
    if token.get_tk_type() is TokenType.IN_TK or token.get_tk_type() is TokenType.INOUT_TK:
        token = lex()
        if token.get_tk_type() is not TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected formal parameter name but found \'%s\' instead'% token.get_tk_value()) 
        token = lex()


def statements():
    global token
    if token.get_tk_type() is TokenType.LEFT_BRACE_TK:
        token = lex()
        statement()
        while token.get_tk_type() is TokenType.SEMICOLON_TK:
            token = lex()
            statement()
        if token.get_tk_type() is not TokenType.RIGHT_BRACE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),'Expected statements end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        statement()


def statement():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        lhand = token.get_tk_value()
        token = lex()
        rhand = assignment_stat()
        genquad(':=', rhand,'_', lhand)
    elif token.get_tk_type() is TokenType.IF_TK:
        token = lex()
        if_stat()
    elif token.get_tk_type() is TokenType.WHILE_TK:
        token = lex()
        while_stat()
    elif token.get_tk_type() is TokenType.DOUBLEWHILE_TK:
        token = lex()
        doublewhile_stat()
    elif token.get_tk_type() is TokenType.LOOP_TK:
        token = lex()
        loop_stat()
    elif token.get_tk_type() is TokenType.EXIT_TK:
        exit_list = makelist(nextquad())
        genquad('jump')
        token = lex()
        #exit_stat() ???
    elif token.get_tk_type() is TokenType.FORCASE_TK:
        token = lex()
        forcase_stat()
    elif token.get_tk_type() is TokenType.INCASE_TK:
        token = lex()
        incase_stat()
    elif token.get_tk_type() is TokenType.RETURN_TK:
        token = lex()
        return_stat()
    elif token.get_tk_type() is TokenType.CALL_TK:
        token = lex()
        call_stat()
    elif token.get_tk_type() is TokenType.PRINT_TK:
        token = lex()
        print_stat()
    elif token.get_tk_type() is TokenType.INPUT_TK:
        token = lex()
        input_stat()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected statement but found \'%s\' instead' % token.get_tk_value())


def assignment_stat():
    global token
    if token.get_tk_type() is TokenType.ASSIGN_TK:
        token=lex()
        return expression()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':=\' but found \'%s\' instead' % token.get_tk_value())


def if_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        (b_true,b_false) = condition() 
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
           error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' after if condition but found \'%s\' instead' % token.get_tk_value())
        token = lex()
        if token.get_tk_type() is TokenType.THEN_TK:
            token = lex()
            backpatch(b_true, nextquad())
            statements()
            if_list = makelist(nextquad())
            genquad('jump')
            backpatch(b_false, nextquad())
            elsepart()
            backpatch(if_list, nextquad())
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'then\' after if condition but found \'%s\' instead' % token.get_tk_value())
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after if token but found \'%s\' instead' % token.get_tk_value())        


def elsepart():
    global token
    if token.get_tk_type() is TokenType.ELSE_TK:
        token = lex()
        statements()


def while_stat():
    global token
    b_quad = nextquad()
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        (b_true, b_false) = condition()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        backpatch(b_true, nextquad())
        statements()
        genquad('jump','_','_',b_quad)
        backpatch(b_false, nextquad())
    else:
         error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after \'while\' but found \'%s\' instead'% token.get_tk_value())


def doublewhile_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token =lex()
        condition()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        statements()
        if token.get_tk_type() is not TokenType.ELSE_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'else\' inside doublewhile but found \'%s\' instead' % token.get_tk_type())
        token = lex()
        statements()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after \'doublewhile\' but found \'%s\' instead'% token.get_tk_value())


def loop_stat():
    statements()


def forcase_stat():
    global token
    s_quad = nextquad()
    #exit_list = emptylist()
    while token.get_tk_type() is TokenType.WHEN_TK:
        token = lex()
        if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
            token = lex()
            (b_true, b_false) = condition()
            if token.get_tk_type() is TokenType.RIGHT_PARENTHESIS_TK:
                token = lex()
                if token.get_tk_type() is TokenType.COLON_TK:
                    token = lex()
                    backpatch(b_true, nextquad())
                    statements()
                    #tmp_list = makelist(nextquad())
                    genquad('jump','_','_',s_quad)
                    #exit_list =merge(exit_list,tmp_list)
                    backpatch(b_false, nextquad())
                else:
                    error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':\' but found \'%s\' instead'% token.get_tk_value())
            else:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        else:
             error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())
    if token.get_tk_type() is TokenType.DEFAULT_TK:
        token = lex()
        if token.get_tk_type() is TokenType.COLON_TK:
            token = lex()
            statements()
            #backpatch(exit_list, nextquad())
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \':\' after \'default\' but found \'%s\' instead'% token.get_tk_value()) 
        
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'default:\' declaration but found \'%s\' instead'% token.get_tk_value())


def incase_stat():
    global token
    while token.get_tk_type() is TokenType.WHEN_TK:
        token = lex()
        if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
            token = lex()
            condition()
            if token.get_tk_type() is TokenType.RIGHT_PARENTHESIS_TK:
                token = lex()
                if token.get_tk_type() is TokenType.COLON_TK:
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
    exp = expression()
    genquad('retv', exp)


def call_stat():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        procedure_id = token.get_tk_value()
        token = lex()
        actualpars()
        genquad('call',procedure_id)
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected function or procedure id but found \'%s\' instead'% token.get_tk_value())


def print_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        exp = expression()
        genquad('out',exp)
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())


def input_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        if token.get_tk_type() is not TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected variable id but found \'%s\' instead'% token.get_tk_value())
        id_name = token.get_tk_value()
        genquad('inp',id_name)
        token = lex()
        if token.get_tk_type()  is not  TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' but found \'%s\' instead'% token.get_tk_value())


def condition():
    global token
    (b_true,b_false)= boolterm()
    while token.get_tk_type() is TokenType.OR_TK:
        backpatch(b_false, nextquad())
        token = lex()
        (b2_true, b2_false) =boolterm()
        b_true = merge(b_true, b2_true)
        b_false = b2_false
    return (b_true, b_false)


def boolterm():
    global token
    (q_true, q_false) = boolfactor()
    while token.get_tk_type() is TokenType.AND_TK:
        backpatch(q_true, nextquad())
        token = lex()
        (r2_true, r2_false) = boolfactor()
        q_false = merge (q_false, r2_false)
        q_true  = r2_true
    return (q_true, q_false)


def boolfactor():
    global token
    if token.get_tk_type() is TokenType.NOT_TK:
        token = lex()
        if token.get_tk_type() is TokenType.LEFT_BRACKET_TK:
            token = lex()
            ret = condition()
            ret = ret[::-1]
            if token.get_tk_type()  is not  TokenType.RIGHT_BRACKET_TK:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \']\' but found \'%s\' instead'% token.get_tk_value())
            token = lex()
        else:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'[\' after \'not\' but found \'%s\' instead'% token.get_tk_value())
    elif token.get_tk_type() is TokenType.LEFT_BRACKET_TK:
        token = lex()
        ret = condition()
        if token.get_tk_type() is not TokenType.RIGHT_BRACKET_TK:
                error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \']\' but found \'%s\' instead'% token.get_tk_value())
        token = lex()
    else:
        exp1 = expression()
        op   = relational_oper()
        exp2 = expression()
        r_true = makelist(nextquad())
        genquad(op , exp1, exp2)
        r_false = makelist(nextquad())
        genquad('jump')
        ret = (r_true, r_false)
    return ret


def relational_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.EQUAL_TK and token.get_tk_type() is not TokenType.LESS_THAN_OR_EQUAL_TK and token.get_tk_type() is not TokenType.LESS_TK and \
        token.get_tk_type() is not TokenType.GREATER_THAN_OR_EQUAL_TK and token.get_tk_type() is not TokenType.GREATER_TK and token.get_tk_type() is not TokenType.LESS_THAN_OR_EQUAL_TK and \
        token.get_tk_type() is not TokenType.NOT_EQUAL_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected relational operator but found \'%s\' instead'% token.get_tk_value())
    token = lex()
    return op


def expression():
    global token
    op_sign = optional_sign()
    term_1 = term()
    if op_sign != None:
        signtmp = newtemp()
        genquad('-', 0, term_1, signtmp)
        term_1 = signtmp
    while token.get_tk_type() is TokenType.PLUS_TK or token.get_tk_type() is TokenType.MINUS_TK :
        oper = add_oper()
        term_2   = term()
        tmpvar   = newtemp()
        genquad(oper, term_1, term_2, tmpvar)
        term_1 = tmpvar
    return term_1


def optional_sign():
    global token
    if token.get_tk_type() is TokenType.PLUS_TK or token.get_tk_type() is TokenType.MINUS_TK :
        return add_oper()


def term():
    global token 
    factor_1 = factor()
    while token.get_tk_type() is TokenType.SLASH_TK or token.get_tk_type() is TokenType.TIMES_TK:
        m_oper = mul_oper()
        factor_2 = factor()
        tmpvar   = newtemp()
        genquad(m_oper, factor_1, factor_2, tmpvar)
        factor_1 = tmpvar
    return factor_1


def factor(): 
    global token
    if token.get_tk_type() is TokenType.NUMBER_TK :
        ret = token.get_tk_value()
        token = lex()
    elif token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token=lex()
        ret = expression()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()
    elif token.get_tk_type() is TokenType.ID_TK:
        ret = token.get_tk_value()
        token=lex()
        tail = idtail()
        if tail is not None:
            function_return = newtemp()
            genquad('par', function_return, 'RET')
            genquad('call', ret)
            ret = function_return
    else: 
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected factor but found \'%s\' instead' % token.get_tk_value())
    return ret


def idtail():
   global token
   if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        return actualpars() 


def add_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.PLUS_TK and token.get_tk_type() is not TokenType.MINUS_TK :
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'+\' or \'-\' but found \'%s\' instead' % token.get_tk_value())
    token=lex()
    return op


def mul_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.TIMES_TK and token.get_tk_type() is not TokenType.SLASH_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'*\' or \'/\' but found \'%s\' instead' % token.get_tk_value())
    token = lex()
    return op


def actualpars():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        actualparlist()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \')\' but found \'%s\' instead' % token.get_tk_value())
        token = lex()
        return True
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'(\' after procedure or function call  but found \'%s\' instead'% token.get_tk_value())


def actualparlist():
    global token
    if token.get_tk_type() is TokenType.IN_TK or token.get_tk_type() is TokenType.INOUT_TK:
        actualparitem()
        while token.get_tk_type() is TokenType.COMMA_TK:
            token = lex()
            actualparitem()


def actualparitem():
    global token
    if token.get_tk_type() is TokenType.IN_TK:
        token = lex()
        exp = expression()
        genquad('par', exp, 'CV')
    elif token.get_tk_type() is TokenType.INOUT_TK:
        token = lex()
        parameter_id = token.get_tk_value()
        if token.get_tk_type() is not TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected variable id but found \'%s\' instead' % token.get_tk_value())
        token = lex()
        genquad('par', parameter_id, 'REF')
    else:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected parameter type in or inout but found \'%s\' instead' % token.get_tk_value())


##############################################################
#                                                            #
#                   main compiler program                    #
#                                                            #
##############################################################
def main(input_filename):

    interm_filepath = input_filename[:-4] + '.int'
    c_equivalent_filepath = input_filename[:-4] + '.c'
    open_files(input_filename,interm_filepath)

    global token
    #Begin syntax analysis
    token = lex()
    program()
    if token.get_tk_type() is not TokenType.EOF_TK:
        error_line_message(token.get_tk_lineno(),token.get_tk_charno(),'Expected \'EOF\' but found \'%s\' instead' % token.get_tk_value())

    generate_intermediate_code_file()
    # print quad equivalent code
    for Quad in quads_list:
        print(Quad)
    close_files()


if __name__ == '__main__':

    # No arguments passed
    if len(sys.argv) == 1:
        error(':no input files.')
        sys.exit(1)

    # File does not exist
    if not os.path.exists(sys.argv[1]):
        error_file_not_found(sys.argv[1])
        sys.exit(1)

    # Call main function
    main(sys.argv[1])
