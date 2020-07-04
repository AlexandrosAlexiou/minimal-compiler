#!/usr/bin/env python3
import os
import sys
from symbol_table import *
from quad import Quad
from token import *
from structures import tokens

##############################################################
#                                                            #
#                     Global variables                       #
#                                                            #
##############################################################
lineno = 1  # Current line number
charno = 0  # Current Character number from the start of the line
token = Token()  # Each token returned from the lexical analyzer will be stored here
infile = ''  # input file pointer
int_file = ''  # intermediate code file
c_code_file = ''  # intermediate code to C equivalent file
asm_code_file = ''  # assembly final code file
main_program_name = ''  # main program name to generate halt quad
main_program_start_label = ''  # used to generate the jump to main in the assembly file
quads_list = list()  # Program equivalent in quadruples.
actual_pars = list()  # subprogram parameters for error checking
scopes = list()  # Program current scopes
nextlabel = 0  # next quad label that is going to be created
variables_to_declare = list()  # all variable names used c equivalent file to declare all the variables of the program.
next_tmpvar = 1  # Temporary variables. eg. T_1 ... T_2 etc.
halt_label = -1
main_program_framelength = -1
subprogram_exists = False  # flag to check if the equivalent C file can be generated
inside_function = list()  # If last element is true then we are currently inside a function
has_return_stat = list()  # and if last element is true then we have return stat
procedure_id_list = list()  # holds all procedure id's to check for errors
enteredMain = False


##############################################################
#                                                            #
#                   Error printing                           #
#                                                            #
##############################################################
def error_line_message(lineno, charno, *args):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']',
          ShellColors.BOLD + '%s:%d:%d:' % (infile.name, lineno, charno) + ShellColors.END, *args)
    # character pointer reset
    infile.seek(0)
    for i, line in enumerate(infile):
        if i == lineno - 1:
            print(line.replace('\t', ' ').replace('\n', ' '))  # \t and \n count as 1 character
            print(ShellColors.GREEN + ' ' * (charno - 2) + '^' + ShellColors.END)
    close_files()
    sys.exit(1)


def error_file_not_found(infile):
    print(
        '[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']' + ' File:' + ShellColors.GREEN + ' ' + infile + ' ' + ShellColors.END + 'does not exist.')
    sys.exit(1)


def error(*args):
    print('[' + ShellColors.RED + 'ERROR' + ShellColors.END + ']', *args)
    sys.exit(1)


def warning(*args):
    print(ShellColors.WARNING + '[' + 'Warning' + ']' + ShellColors.END,
          ShellColors.UNDERLINED + infile.name + ShellColors.END + ': ' + str(*args))
    print('\n')


##############################################################
#                                                            #
#                        I/O files                           #
#                                                            #
##############################################################
def open_files(input_filename, intermediate_code_filepath, c_equivalent_filepath, asm_code_filepath):
    global infile, int_file, c_code_file, asm_code_file
    infile = open(input_filename, 'r', encoding='utf-8')
    int_file = open(intermediate_code_filepath, 'w', encoding='utf-8')
    c_code_file = open(c_equivalent_filepath, 'w', encoding='utf-8')
    asm_code_file = open(asm_code_filepath, 'w', encoding='utf8')


def close_files():
    infile.close()
    int_file.close()
    c_code_file.close()


##############################################################
#                                                            #
#                    Intermediate Code                       #
#                                                            #
##############################################################
def generate_intermediate_code_file():
    for quad in quads_list:
        int_file.write(quad.quad_to_file())


def generate_c_code_file():
    c_code_file.write('#include <stdio.h>\n\n')
    for quad in quads_list:
        if quad.get_op() == 'begin_block':
            if quad.get_x() == main_program_name:
                if variables_to_declare:
                    buffer = '\n\tint '
                    for var in variables_to_declare:
                        has_declares = True
                        buffer += var + ', '
                    buffer = buffer[:-2] + ';'
                    c_code_file.write('int main(void)\n{' + buffer + '\n')
                else:
                    c_code_file.write('int main(void)\n{' + '\n')
        elif quad.get_op() == 'end_block':
            c_code_file.write('\tL_' + str(quad.get_label()) + ':{}\n}\n')
        elif quad.get_op() == 'halt':
            c_code_file.write('\tL_' + str(quad.get_label()) + ': ' + 'return 0;\n')
        elif quad.get_op() in ('=', '>', '<', '>=', '<=', '<>'):
            c_operator = quad.get_op()
            if c_operator == '=':
                c_operator = '=='
            elif c_operator == '<>':
                c_operator = '!='
            c_code_file.write(
                '\tL_' + str(quad.get_label()) + ': ' + 'if(' + str(quad.get_x()) + c_operator + ' ' + str(
                    quad.get_y()) + ') goto L_' + str(quad.get_z()) + ';\n')
        elif quad.get_op() in ('+', '-', '/', '*'):
            c_code_file.write(
                '\tL_' + str(quad.get_label()) + ': ' + str(quad.get_z()) + '=' + str(quad.get_x()) + ' ' + str(
                    quad.get_op()) + ' ' + str(quad.get_y()) + ';\n')
        elif quad.get_op() == ':=':
            c_code_file.write(
                '\tL_' + str(quad.get_label()) + ': ' + str(quad.get_z()) + '=' + str(quad.get_x()) + ';\n')
        elif quad.get_op() == 'jump':
            c_code_file.write('\tL_' + str(quad.get_label()) + ': ' + 'goto L_' + str(quad.get_z()) + ';\n')
        elif quad.get_op() == 'out':
            c_code_file.write('\tL_' + str(quad.get_label()) + ': ' + 'printf("%d\\n", ' + str(quad.get_x()) + ');\n')
        elif quad.get_op() == 'inp':
            c_code_file.write('\tL_' + str(quad.get_label()) + ': ' + 'scanf("%d", ' + '&' + str(quad.get_x()) + ');\n')
        elif quad.get_op() == 'retv':
            c_code_file.write('\tL_' + str(quad.get_label()) + ': ' + 'return (' + str(quad.get_x()) + ');\n')


##############################################################
#                                                            #
#                   Final code generation                    #
#                                                            #
##############################################################
# Load in register $t0 the address of a non-local variable 'v'.
def gnvlcode(v):
    entity_to_load = search_entity(v)
    current_nesting_level = scopes[-1].get_nesting_level()
    entity_nesting_level = get_entity_nesting_level(entity_to_load.get_name())
    asm_code_file.write('    lw    $t0, -4($sp)\n')
    access_link = current_nesting_level - entity_nesting_level - 1
    while access_link > 0:
        asm_code_file.write('    lw    $t0, -4($t0)\n')
        access_link -= 1
    asm_code_file.write('    addi    $t0, $t0, -%d\n' % entity_to_load.get_offset())


# Load entity 'v' from memory to register $t(r) r refers to the number of the temporary register. 
def loadvr(v, r):
    if str(v).isdigit():  # constant
        asm_code_file.write('    li    $t%s, %s\n' % (r, v))
    else:  # data
        entity_to_load = search_entity(v)
        current_nesting_level = scopes[-1].get_nesting_level()
        entity_nesting_level = get_entity_nesting_level(entity_to_load.get_name())
        if entity_to_load.get_entityType() == 'Variable' and entity_nesting_level == 0:
            asm_code_file.write('    lw    $t%s, -%d($s0)\n' % (r, entity_to_load.get_offset()))
        elif (entity_to_load.get_entityType() == 'Variable' and entity_nesting_level == current_nesting_level) or \
                (entity_to_load.get_entityType() == 'Parameter' and entity_nesting_level == current_nesting_level and entity_to_load.get_parMode() == 'in') or \
                (entity_to_load.get_entityType() == 'Tempvar'):
            asm_code_file.write('    lw    $t%s, -%d($sp)\n' % (r, entity_to_load.get_offset()))
        elif entity_to_load.get_entityType() == 'Parameter' and \
                entity_to_load.get_parMode() == 'inout' and \
                entity_nesting_level == current_nesting_level:
            asm_code_file.write('    lw    $t0, -%d($sp)\n' % entity_to_load.get_offset())
            asm_code_file.write('    lw    $t%s, 0($t0)\n' % r)
        elif (entity_to_load.get_entityType() == 'Variable' and entity_nesting_level < current_nesting_level) or \
                (entity_to_load.get_entityType() == 'Parameter' and entity_to_load.get_parMode() == 'in' and entity_nesting_level < current_nesting_level):
            gnvlcode(v)
            asm_code_file.write('    lw    $t%s, 0($t0)\n' % r)
        elif entity_to_load.get_entityType() == 'Parameter' and entity_to_load.get_parMode() == 'inout' \
                and entity_nesting_level < current_nesting_level:
            gnvlcode(v)
            asm_code_file.write('    lw    $t0, 0($t0)\n')
            asm_code_file.write('    lw    $t%s, 0($t0)\n' % r)
        else:
            error('loadvr is not used correctly.')


# Transfer contents of register $t{r} to memory for variable v.
def storerv(r, v):
    entity_to_store = search_entity(v)
    current_nesting_level = scopes[-1].get_nesting_level()
    entity_nesting_level = get_entity_nesting_level(entity_to_store.get_name())
    if entity_to_store.get_entityType() == 'Variable' and entity_nesting_level == 0:
        asm_code_file.write('    sw    $t%s, -%d($s0)\n' % (r, entity_to_store.get_offset()))
    elif (entity_to_store.get_entityType() == 'Variable' and entity_nesting_level == current_nesting_level) or \
            (entity_to_store.get_entityType() == 'Parameter' and entity_to_store.get_parMode() == 'in' and entity_nesting_level == current_nesting_level) or \
            (entity_to_store.get_entityType() == 'Tempvar'):
        asm_code_file.write('    sw    $t%s, -%d($sp)\n' % (r, entity_to_store.get_offset()))
    elif entity_to_store.get_entityType() == 'Parameter' and entity_to_store.get_parMode() == 'inout' and entity_nesting_level == current_nesting_level:
        asm_code_file.write('    lw    $t0, -%d($sp)\n' % entity_to_store.get_offset())
        asm_code_file.write('    sw    $t%s, 0($t0)\n' % r)
    elif (entity_to_store.get_entityType() == 'Variable' and entity_nesting_level < current_nesting_level) or \
            (entity_to_store.get_entityType() == 'Parameter' and entity_to_store.get_parMode() == 'in' and entity_nesting_level < current_nesting_level):
        gnvlcode(v)
        asm_code_file.write('    sw    $t%s, 0($t0)\n' % r)
    elif entity_to_store.get_entityType() == 'Parameter' and entity_to_store.get_parMode() == 'inout' and entity_nesting_level < current_nesting_level:
        gnvlcode(v)
        asm_code_file.write('    lw    $t0, 0($t0)\n')
        asm_code_file.write('    sw    $t%s, 0($t0)\n' % r)
    else:
        error('storerv is not used correctly.')


# Generate a file containing the final code in assembly targeting the MIPS32 architecture
def generate_asm_code_file(quad, name):
    global enteredMain
    if str(quad.get_label()) == '0':
        asm_code_file.write('# This file was automatically generated by: Minimal++ Compiler\n\n')
        asm_code_file.write('    j    Lmain\n')
    relational_operators = ['=', '<>', '<', '<=', '>', '>=']
    asm_relational_operators_instructions = ['beq', 'bne', 'blt', 'ble', 'bgt', 'bge']
    arithmetic_operators = ['+', '-', '/', '*']
    asm_arithmetic_operators_instructions = ['add', 'sub', 'div', 'mul']
    if name == main_program_name and not enteredMain:
        # Write Lmain once and mark the start of the main block
        asm_code_file.write('\nLmain:\n')
        enteredMain = True
    else:
        asm_code_file.write('\nL_' + str(quad.get_label()) + ':\n')
    if quad.get_op() == 'jump':
        asm_code_file.write('    j    L_%d\n' % quad.get_z())
    elif quad.get_op() in relational_operators:
        loadvr(quad.get_x(), '1')
        loadvr(quad.get_y(), '2')
        asm_code_file.write('   %s    $t1, $t2, L_%s\n'
                            % (asm_relational_operators_instructions[relational_operators.index(quad.get_op())],
                               quad.get_z()))
    elif quad.get_op() in arithmetic_operators:
        loadvr(quad.get_x(), '1')
        loadvr(quad.get_y(), '2')
        asm_code_file.write('   %s    $t1, $t1, $t2\n'
                            % (asm_arithmetic_operators_instructions[arithmetic_operators.index(quad.get_op())]))
        storerv('1', quad.get_z())
    elif quad.get_op() == ':=':
        loadvr(quad.get_x(), '1')
        storerv('1', quad.get_z())
    elif quad.get_op() == 'halt':
        asm_code_file.write('    li    $v0, 10\n')
        asm_code_file.write('    syscall\n')
    elif quad.get_op() == 'out':
        loadvr(quad.get_x(), '9')
        asm_code_file.write('    li    $v0, 1\n')
        asm_code_file.write('    move  $a0, $t9\n')
        asm_code_file.write('    syscall\n')
        # print new line after integer out
        asm_code_file.write('    addi    $a0, $0, 0xA\n')  # ascii code for LF
        asm_code_file.write(
            '    addi    $v0, $0, 0xB\n')  # syscall 11 prints the lower 8 bits of $a0 as an ascii character
        asm_code_file.write('    syscall\n')
    elif quad.get_op() == 'inp':
        asm_code_file.write('    li    $v0, 5\n')
        asm_code_file.write('    syscall\n')
        asm_code_file.write('    move $t0, $v0\n')
        # print new line after integer out
        asm_code_file.write('    addi    $a0, $0, 0xA\n')  # ascii code for LF
        asm_code_file.write(
            '    addi    $v0, $0, 0xB\n')  # syscall 11 prints the lower 8 bits of $a0 as an ascii character
        asm_code_file.write('    syscall\n')
        storerv('0', quad.get_x())
    elif quad.get_op() == 'retv':
        loadvr(quad.get_x(), '1')
        asm_code_file.write('    lw    $t0, -8($sp)\n')
        asm_code_file.write('    sw    $t1, 0($t0)\n')
    elif quad.get_op() == 'par':
        if name != main_program_name:
            caller, caller_nesting_level = search_entity_by_type(name, 'Function')
            framelength = caller.get_framelength()
        else:
            caller_nesting_level = 0
            framelength = main_program_framelength
        if not actual_pars:
            asm_code_file.write('    addi    $fp, $sp, %d\n' % framelength)
        actual_pars.append(quad)
        parameter_offset = 12 + 4 * actual_pars.index(quad)
        if quad.get_y() == 'CV':
            loadvr(quad.get_x(), '0')
            asm_code_file.write('    sw    $t0, -%d($fp)\n' % parameter_offset)
        elif quad.get_y() == 'REF':
            variable = search_entity(quad.get_x())
            variable_nesting_level = get_entity_nesting_level(quad.get_x())
            if caller_nesting_level == variable_nesting_level:
                if variable.get_entityType() == 'Variable' or \
                        (variable.get_entityType() == 'Parameter' and variable.get_parMode() == 'in'):
                    asm_code_file.write('    addi    $t0, $sp, -%d\n' % variable.get_offset())
                    asm_code_file.write('    sw    $t0, -%d($fp)\n' % parameter_offset)
                elif variable.get_entityType() == 'Parameter' and variable.get_parMode() == 'inout':
                    asm_code_file.write('    lw    $t0, -%d($sp)\n' % variable.get_offset())
                    asm_code_file.write('    sw    $t0, -%d($fp)\n' % parameter_offset)
            else:
                if variable.get_entityType() == 'Variable' or \
                        (variable.get_entityType() == 'Parameter' and variable.get_parMode() == 'in'):
                    gnvlcode(quad.get_x())
                    asm_code_file.write('    sw    $t0, -%d($fp)\n' % parameter_offset)
                elif variable.get_entityType() == 'Parameter' and variable.get_parMode() == 'inout':
                    gnvlcode(quad.get_x())
                    asm_code_file.write('    lw    $t0, 0($t0)\n')
                    asm_code_file.write('    sw    $t0, -%d($fp)\n' % parameter_offset)
        elif quad.get_y() == 'RET':
            variable = search_entity(quad.get_x())
            variable_nesting_level = get_entity_nesting_level(quad.get_x())
            asm_code_file.write('    addi    $t0, $sp, -%d\n' % variable.get_offset())
            asm_code_file.write('    sw    $t0, -8($fp)\n')
    elif quad.get_op() == 'call':
        if name != main_program_name:
            caller = search_entity(name)
            caller_nesting_level = get_entity_nesting_level(name)
            framelength = caller.get_framelength()
        else:
            caller_nesting_level = 0
            framelength = main_program_framelength
        to_call = search_entity(quad.get_x())
        to_call_nesting_level = get_entity_nesting_level(quad.get_x())
        if actual_pars:
            if actual_pars[-1].get_y() == 'RET':
                actual_pars.pop()
        if len(to_call.get_arguments_list()) != len(actual_pars):
            # print(len(to_call.get_arguments_list()), len(actual_pars))
            error('Subprogram \'%s\' parameters number is not matching definition' % to_call.get_name())
        for argument in to_call.get_arguments_list():
            quad = actual_pars.pop(0)
            if argument.get_parMode() != quad.get_y():
                expected_mode = 'inout' if quad.get_x() == 'CV' else 'in'
                error('Subprogram: \'%s\'. Expected parameter \'%s\' mode to be \'%s\''
                      % (to_call.get_name(), quad.get_x(), expected_mode))
        if caller_nesting_level == to_call_nesting_level:
            asm_code_file.write('    lw    $t0, -4($sp)\n')
            asm_code_file.write('    sw    $t0, -4($fp)\n')
        else:
            asm_code_file.write('    sw    $sp, -4($fp)\n')
        asm_code_file.write('    addi    $sp, $sp, %d\n' % framelength)
        asm_code_file.write('    jal     L_%d\n' % to_call.get_startQuad())
        asm_code_file.write('    addi    $sp, $sp, -%d\n' % framelength)
    elif quad.get_op() == 'begin_block':
        asm_code_file.write('    sw    $ra, 0($sp)\n')
        if name == main_program_name:
            asm_code_file.write('    addi  $sp, $sp, %d\n' % main_program_framelength)
            asm_code_file.write('    move  $s0, $sp\n')
    elif quad.get_op() == 'end_block':
        if name == main_program_name:
            asm_code_file.write('    j    L_%d\n' % halt_label)
        else:
            asm_code_file.write('    lw    $ra, 0($sp)\n')
            asm_code_file.write('    jr    $ra\n')


##############################################################
#                                                            #
#                   Lexical analyzer                         #
#                                                            #
##############################################################
def lex():
    global lineno, charno, infile
    while True:
        character = infile.read(1)
        charno += 1
        # File is allowed to have empty lines tabs and spaces at the start
        while character == ' ' or character == "\n" or character == "\t":
            if character == "\n":
                lineno += 1
                charno = 0
            character = infile.read(1)
            charno += 1
        buffer = character
        # print(buffer)
        if character.isalpha():
            character = infile.read(1)
            charno += 1
            while character.isalpha() or character.isdigit():
                buffer += character
                character = infile.read(1)
                charno += 1
            if buffer in tokens.keys():
                retval = Token(tokens[buffer], buffer, lineno, charno)
            else:
                retval = Token(TokenType.ID_TK, buffer, lineno, charno)
            infile.seek(infile.tell() - 1)
            charno -= 1
            return retval
        elif character.isnumeric():
            while character.isnumeric():
                character = infile.read(1)
                charno += 1
                if character.isnumeric():
                    buffer += character
                else:
                    if character.isalpha():
                        error_line_message(lineno, charno - 1, 'Variable names should begin with alphabetic character.')
            if int(buffer) > 32767 or int(buffer) < -32767:
                error_line_message(lineno, charno, 'Integer value should be between [-32767,32767].')
            infile.seek(infile.tell() - 1)
            charno -= 1
            return Token(TokenType.NUMBER_TK, buffer, lineno, charno)
        elif character == '+':
            return Token(TokenType.PLUS_TK, buffer, lineno, charno)
        elif character == '-':
            return Token(TokenType.MINUS_TK, buffer, lineno, charno)
        elif character == '*':
            character = infile.read(1)
            charno += 1
            if character == '/':
                error_line_message(lineno, charno, 'Expected "/*" to open comments before "*/" .')
            else:
                infile.seek(infile.tell() - 1)
                charno -= 1
                return Token(TokenType.TIMES_TK, buffer, lineno, charno)
        elif character == '/':
            character = infile.read(1)
            comments_charno = charno
            comments_line = lineno
            charno += 1
            if character == '*':
                while (True):
                    character = infile.read(1)
                    if not character:
                        error_line_message(comments_line, comments_charno,
                                           'Comments opened. Expected  "*/"  but EOF reached.')
                    if character == '*':
                        character = infile.read(1)
                        if character == '/':
                            break
                    elif character == '\n':
                        lineno += 1
                        charno = 0
            elif character == '/':
                while (character != '\n'):
                    character = infile.read(1)
                lineno += 1
                charno = 0
            else:
                infile.seek(infile.tell() - 1)
                charno -= 1
                return Token(TokenType.SLASH_TK, buffer, lineno, charno)
        elif character == '(':
            return Token(TokenType.LEFT_PARENTHESIS_TK, buffer, lineno, charno)
        elif character == ')':
            return Token(TokenType.RIGHT_PARENTHESIS_TK, buffer, lineno, charno)
        elif character == '[':
            return Token(TokenType.LEFT_BRACKET_TK, buffer, lineno, charno)
        elif character == ']':
            return Token(TokenType.RIGHT_BRACKET_TK, buffer, lineno, charno)
        elif character == '{':
            return Token(TokenType.LEFT_BRACE_TK, buffer, lineno, charno)
        elif character == '}':
            return Token(TokenType.RIGHT_BRACE_TK, buffer, lineno, charno)
        elif character == '<':
            character = infile.read(1)
            if character == '=':
                buffer += character
                return Token(TokenType.LESS_THAN_OR_EQUAL_TK, buffer, lineno, charno)
            elif character == '>':
                buffer += character
                return Token(TokenType.NOT_EQUAL_TK, buffer, lineno, charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.LESS_TK, buffer, lineno, charno)
        elif character == '>':
            character = infile.read(1)
            if character == '=':
                buffer += character
                return Token(TokenType.GREATER_THAN_OR_EQUAL_TK, buffer, lineno, charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.GREATER_TK, buffer, lineno, charno)
        elif character == '=':
            return Token(TokenType.EQUAL_TK, buffer, lineno, charno)
        elif character == ',':
            return Token(TokenType.COMMA_TK, buffer, lineno, charno)
        elif character == ';':
            return Token(TokenType.SEMICOLON_TK, buffer, lineno, charno)
        elif character == ':':
            character = infile.read(1)
            if character == '=':
                buffer += character
                return Token(TokenType.ASSIGN_TK, buffer, lineno, charno)
            else:
                infile.seek(infile.tell() - 1)
                return Token(TokenType.COLON_TK, buffer, lineno, charno)
        elif character == '':
            return Token(TokenType.EOF_TK, 'EOF', lineno, 0)
        else:
            error_line_message(lineno, charno, 'Invalid character.')


##############################################################
#                                                            #
#               Intermediate code functions                  #
#                                                            #
##############################################################
def nextquad():
    return nextlabel


def genquad(op=None, x='_', y='_', z='_'):
    global nextlabel
    label = nextlabel
    nextlabel += 1
    newquad = Quad(label, op, x, y, z)
    quads_list.append(newquad)


def newtemp():
    global variables_to_declare, next_tmpvar
    tempvar = 'T_' + str(next_tmpvar)
    variables_to_declare.append(tempvar)
    offset = scopes[-1].get_current_offset_and_advance()
    scopes[-1].add_Entity(TemporaryVariable(tempvar, offset))
    next_tmpvar += 1
    return tempvar


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
#                   Symbol table functions                   #
#                                                            #
##############################################################
def is_declared(name, entity_type, nesting_level):
    scope = scopes[nesting_level]
    for i in range(len(scope.get_entities_list())):
        entity1 = scope.get_entities_list()[i]
        if entity1.get_name() == name and entity1.get_entityType() == entity_type:
            return True
    return False


def variable_is_parameter(name, nesting_level):
    for i in range(len(scopes[nesting_level].get_entities_list())):
        if scopes[nesting_level].get_entities_list()[i].get_entityType() == "Parameter" and \
                scopes[nesting_level].get_entities_list()[i].get_name() == name:
            return True
    return False


def search_entity(entity_name):
    if not scopes:
        return
    current_scope = scopes[-1]
    while current_scope is not None:  # search until global scope
        for entity in current_scope.get_entities_list():
            if entity.get_name() == entity_name:
                return entity
        current_scope = current_scope.get_enclosing_scope()


def get_entity_nesting_level(entity_name):
    if not scopes:
        return
    current_scope = scopes[-1]
    while current_scope is not None:  # search until global scope
        for entity in current_scope.get_entities_list():
            if entity.get_name() == entity_name:
                return current_scope.get_nesting_level()
        current_scope = current_scope.get_enclosing_scope()


def search_entity_by_type(entity_name, entity_type):
    if not scopes:
        return
    current_scope = scopes[-1]
    while current_scope is not None:  # search until global scope
        for entity in current_scope.get_entities_list():
            if entity.get_name() == entity_name and entity.get_entityType() == entity_type:
                return entity, current_scope.get_nesting_level()
        current_scope = current_scope.get_enclosing_scope()


def add_new_scope():
    if not scopes:  # if scopes list is empty then add the main scope
        current_scope = Scope()
        scopes.append(current_scope)
        return
    enclosing_scope = scopes[-1]
    current_scope = Scope(enclosing_scope.get_nesting_level() + 1, enclosing_scope)
    scopes.append(current_scope)


def add_function_entity(name):
    nesting_level = scopes[-1].get_enclosing_scope().get_nesting_level()
    if is_declared(name, "Function", nesting_level):
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Redefinition of \'%s\' inside the same scope. Minimal++ does not support function overloading.' % name)
    scopes[-2].add_Entity(Function(name))


def update_function_startQuad(name):
    global main_program_name, main_program_start_label
    startQuad = nextquad()
    if name == main_program_name:
        main_program_start_label = startQuad
        return startQuad
    scopes[-2].get_entities_list()[-1].set_start_quad(startQuad)
    return startQuad


def update_function_framelength(name, framelength):
    global main_program_framelength, main_program_name
    if name is main_program_name:
        main_program_framelength = framelength
        return
    scopes[-2].get_entities_list()[-1].set_framelength(framelength)


def add_parameter_entity(name, parMode):
    nesting_level = scopes[-1].get_nesting_level()
    parameter_offset = scopes[-1].get_current_offset_and_advance()
    if is_declared(name, "Parameter", nesting_level):
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(), 'Redefinition of \'%s\'.' % name)
    scopes[-1].add_Entity(Parameter(name, parMode, parameter_offset))


def add_function_argument(parMode):
    if parMode == 'in':
        new_argument = Argument('CV')
    else:
        new_argument = Argument('REF')
    scopes[-2].get_entities_list()[-1].add_argument_in_list(new_argument)
    if len(scopes[-2].get_entities_list()[-1].get_arguments_list()) >= 2:
        scopes[-2].get_entities_list()[-1].get_arguments_list()[-2].set_nextArgument(new_argument)


def add_variable_entity(name):
    nesting_level = scopes[-1].get_nesting_level()
    variable_offset = scopes[-1].get_current_offset_and_advance()
    if is_declared(name, "Variable", nesting_level):
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(), 'Redeclaration of \'%s\'.' % name)
    if variable_is_parameter(name, nesting_level):
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Variable \'%s\' is a subprogram parameter therefore it cannot be redeclared.' % name)
    scopes[-1].add_Entity(Variable(name, variable_offset))


# Print current scope and its enclosing ones.
def print_scopes():
    print(ShellColors.BOLD + ShellColors.UNDERLINED + 'main scope' + ShellColors.END)
    for scope in scopes:
        level = scope.get_nesting_level() + 1
        print('     ' * level + str(scope))
        for entity in scope.get_entities_list():
            print('     ' * level + str(entity))
            if isinstance(entity, Function):
                for argument in entity.get_arguments_list():
                    print('     ' * level + '      ' + str(argument))
    print('-' * 100 + '\n')


##############################################################
#                                                            #
#                  Syntax analyzer functions                 #
#                                                            #
##############################################################
def program():
    global token, lineno, charno, main_program_name
    if token.get_tk_type() is TokenType.PROGRAM_TK:
        token = lex()
        if token.get_tk_type() is TokenType.ID_TK:
            main_program_name = name = token.get_tk_value()
            token = lex()
            if token.get_tk_type() is TokenType.LEFT_BRACE_TK:
                add_new_scope()
                token = lex()
                block(name)
                if token.get_tk_type() is not TokenType.RIGHT_BRACE_TK:
                    error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                       'Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
                token = lex()
            else:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected program name but found \'%s\' instead.' % token.get_tk_value())
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'program\' keyword but found \'%s\' instead.' % token.get_tk_value())


##############################################################
######################## Main block ##########################
##############################################################
def block(name):
    global scopes, main_program_name, halt_label
    # print_scopes()
    declarations()
    subprograms()
    startQuad = update_function_startQuad(name)
    genquad('begin_block', name)
    statements()
    if name == main_program_name:
        halt_label = nextquad()
        genquad('halt')
    genquad('end_block', name)
    update_function_framelength(name, scopes[-1].get_current_offset())
    print_scopes()
    for quad in quads_list[startQuad:]:
        generate_asm_code_file(quad, name)
    scopes.pop()


##############################################################
##############################################################
##############################################################

def declarations():
    global token
    while token.get_tk_type() is TokenType.DECLARE_TK:
        token = lex()
        varlist()
        if token.get_tk_type() is not TokenType.SEMICOLON_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \';\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()


def varlist():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        add_variable_entity(token.get_tk_value())
        variables_to_declare.append(token.get_tk_value())
        token = lex()
        while token.get_tk_type() is TokenType.COMMA_TK:
            token = lex()
            if token.get_tk_type() is not TokenType.ID_TK:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected variable declaration but found \'%s\' instead.' % token.get_tk_value())
            add_variable_entity(token.get_tk_value())
            variables_to_declare.append(token.get_tk_value())
            token = lex()


def subprograms():
    global token, subprogram_exists, inside_function, has_return_stat
    while token.get_tk_type() is TokenType.FUNCTION_TK or token.get_tk_type() is TokenType.PROCEDURE_TK:
        subprogram_exists = True
        is_procedure = False
        if token.get_tk_type() is TokenType.PROCEDURE_TK:
            is_procedure = True
        if token.get_tk_type() is TokenType.FUNCTION_TK:
            inside_function.append(True)
        else:
            inside_function.append(False)
        has_return_stat.append(False)
        token = lex()
        add_new_scope()
        if token.get_tk_type() is TokenType.ID_TK:
            if is_procedure:
                procedure_id_list.append(token.get_tk_value())
            name = token.get_tk_value()
            token = lex()
            add_function_entity(name)
            funcbody(name)
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected subprogram name but found \'%s\' instead.' % token.get_tk_value())
        if inside_function.pop():
            if not has_return_stat.pop():
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected return statement in function body but found \'%s\' instead.' % token.get_tk_value())
        else:
            has_return_stat.pop()


def funcbody(name):
    global token
    formalpars(name)
    if token.get_tk_type() is TokenType.LEFT_BRACE_TK:
        token = lex()
        block(name)
        if token.get_tk_type() is not TokenType.RIGHT_BRACE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected block end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected subprogram block start (\'{\') but found \'%s\' instead.' % token.get_tk_value())


def formalpars(func_name):
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        formalparlist(func_name)
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value())


def formalparlist(func_name):
    global token
    formalparitem(func_name)
    while token.get_tk_type() is TokenType.COMMA_TK:
        token = lex()
        if token.get_tk_type() is not TokenType.IN_TK and token.get_tk_type() is not TokenType.INOUT_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected formal parameter declaration but found \'%s\' instead.' % token.get_tk_value())
        formalparitem(func_name)


def formalparitem(func_name):
    global token
    if token.get_tk_type() is TokenType.IN_TK or token.get_tk_type() is TokenType.INOUT_TK:
        parMode = token.get_tk_value()
        token = lex()
        if token.get_tk_type() is not TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected formal parameter name but found \'%s\' instead.' % token.get_tk_value())
        parameter_name = token.get_tk_value()
        add_function_argument(parMode)
        add_parameter_entity(parameter_name, parMode)
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
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected statements end (\'}\') but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        statement()


def statement():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        target = token.get_tk_value()
        if search_entity(target) is None:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(), 'Undefined variable id \'%s\'.' % target)
        token = lex()
        value = assignment_stat()
        genquad(':=', value, '_', target)
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
        # exit_stat() ???
    elif token.get_tk_type() is TokenType.FORCASE_TK:
        token = lex()
        forcase_stat()
    elif token.get_tk_type() is TokenType.INCASE_TK:
        token = lex()
        incase_stat()
    elif token.get_tk_type() is TokenType.RETURN_TK:
        global inside_function, has_return_stat
        if not inside_function or not inside_function[-1]:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Encountered \'return\' statement outside of function body')
        else:
            has_return_stat[-1] = True
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
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected statement but found \'%s\' instead.' % token.get_tk_value())


def assignment_stat():
    global token
    if token.get_tk_type() is TokenType.ASSIGN_TK:
        token = lex()
        return expression()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \':=\' but found \'%s\' instead.' % token.get_tk_value())


def if_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        (b_true, b_false) = condition()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' after if condition but found \'%s\' instead.' % token.get_tk_value())
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
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \'then\' after if condition but found \'%s\' instead.' % token.get_tk_value())
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' after if token but found \'%s\' instead.' % token.get_tk_value())


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
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_type())
        token = lex()
        backpatch(b_true, nextquad())
        statements()
        genquad('jump', '_', '_', b_quad)
        backpatch(b_false, nextquad())
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' after \'while\' but found \'%s\' instead.' % token.get_tk_value())


def doublewhile_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        condition()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_type())
        token = lex()
        statements()
        if token.get_tk_type() is not TokenType.ELSE_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \'else\' inside doublewhile but found \'%s\' instead.' % token.get_tk_type())
        token = lex()
        statements()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' after \'doublewhile\' but found \'%s\' instead' % token.get_tk_value())


def loop_stat():
    statements()


def forcase_stat():
    global token
    s_quad = nextquad()
    # exit_list = emptylist()
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
                    # tmp_list = makelist(nextquad())
                    genquad('jump', '_', '_', s_quad)
                    # exit_list =merge(exit_list,tmp_list)
                    backpatch(b_false, nextquad())
                else:
                    error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                       'Expected \':\' but found \'%s\' instead.' % token.get_tk_value())
            else:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value())
    if token.get_tk_type() is TokenType.DEFAULT_TK:
        token = lex()
        if token.get_tk_type() is TokenType.COLON_TK:
            token = lex()
            statements()
            # backpatch(exit_list, nextquad())
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \':\' after \'default\' but found \'%s\' instead.' % token.get_tk_value())

    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'default:\' declaration but found \'%s\' instead.' % token.get_tk_value())


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
                    error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                       'Expected \':\' but found \'%s\' instead.' % token.get_tk_value())
            else:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value())


def return_stat():
    global token
    exp = expression()
    genquad('retv', exp)


def call_stat():
    global token
    if token.get_tk_type() is TokenType.ID_TK:
        procedure_id = token.get_tk_value()
        if procedure_id not in procedure_id_list:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Calling undefined procedure \'%s\'.' % procedure_id)
        if search_entity(procedure_id) is None:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Undefined procedure \'%s\'.' % procedure_id)
        token = lex()
        actualpars()
        genquad('call', procedure_id)
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected function or procedure id but found \'%s\' instead.' % token.get_tk_value())


def print_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        exp = expression()
        genquad('out', exp)
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' but found \'%s\' instead.' % token.get_tk_value())


def input_stat():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        if token.get_tk_type() is not TokenType.ID_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected variable id but found \'%s\' instead.' % token.get_tk_value())
        id_name = token.get_tk_value()
        if search_entity(id_name) is None:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(), 'Undefined variable id \'%s\'.' % id_name)
        genquad('inp', id_name)
        token = lex()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' but found \'%s\' instead' % token.get_tk_value())


def condition():
    global token
    (b_true, b_false) = boolterm()
    while token.get_tk_type() is TokenType.OR_TK:
        backpatch(b_false, nextquad())
        token = lex()
        (b2_true, b2_false) = boolterm()
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
        q_false = merge(q_false, r2_false)
        q_true = r2_true
    return (q_true, q_false)


def boolfactor():
    global token
    if token.get_tk_type() is TokenType.NOT_TK:
        token = lex()
        if token.get_tk_type() is TokenType.LEFT_BRACKET_TK:
            token = lex()
            ret = condition()
            ret = ret[::-1]
            if token.get_tk_type() is not TokenType.RIGHT_BRACKET_TK:
                error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                                   'Expected \']\' but found \'%s\' instead.' % token.get_tk_value())
            token = lex()
        else:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \'[\' after \'not\' but found \'%s\' instead.' % token.get_tk_value())
    elif token.get_tk_type() is TokenType.LEFT_BRACKET_TK:
        token = lex()
        ret = condition()
        if token.get_tk_type() is not TokenType.RIGHT_BRACKET_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \']\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    else:
        exp1 = expression()
        op = relational_oper()
        exp2 = expression()
        r_true = makelist(nextquad())
        genquad(op, exp1, exp2)
        r_false = makelist(nextquad())
        genquad('jump')
        ret = (r_true, r_false)
    return ret


def relational_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.EQUAL_TK and \
            token.get_tk_type() is not TokenType.LESS_THAN_OR_EQUAL_TK and \
            token.get_tk_type() is not TokenType.LESS_TK and \
            token.get_tk_type() is not TokenType.GREATER_THAN_OR_EQUAL_TK and \
            token.get_tk_type() is not TokenType.GREATER_TK and \
            token.get_tk_type() is not TokenType.LESS_THAN_OR_EQUAL_TK and \
            token.get_tk_type() is not TokenType.NOT_EQUAL_TK:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected relational operator but found \'%s\' instead.' % token.get_tk_value())
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
    while token.get_tk_type() is TokenType.PLUS_TK or token.get_tk_type() is TokenType.MINUS_TK:
        oper = add_oper()
        term_2 = term()
        tmpvar = newtemp()
        genquad(oper, term_1, term_2, tmpvar)
        term_1 = tmpvar
    return term_1


def optional_sign():
    global token
    if token.get_tk_type() is TokenType.PLUS_TK or token.get_tk_type() is TokenType.MINUS_TK:
        return add_oper()


def term():
    global token
    factor_1 = factor()
    while token.get_tk_type() is TokenType.SLASH_TK or token.get_tk_type() is TokenType.TIMES_TK:
        m_oper = mul_oper()
        factor_2 = factor()
        tmpvar = newtemp()
        genquad(m_oper, factor_1, factor_2, tmpvar)
        factor_1 = tmpvar
    return factor_1


def factor():
    global token
    if token.get_tk_type() is TokenType.NUMBER_TK:
        ret = token.get_tk_value()
        token = lex()
    elif token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        ret = expression()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
    elif token.get_tk_type() is TokenType.ID_TK:
        ret = token.get_tk_value()
        ret_charno = token.get_tk_charno()
        ret_lineno = token.get_tk_lineno()
        entity = search_entity(ret)
        if entity is None:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(), 'Undefined id \'%s\'.' % ret)
        token = lex()
        tail = idtail()
        if tail is not None:
            if ret in procedure_id_list:
                error_line_message(ret_lineno, ret_charno,
                                   'Calling procedure \'%s\' with assignment. Procedures do not have \'return\' statement.' % ret)
            function_return = newtemp()
            genquad('par', function_return, 'RET')
            genquad('call', ret)
            ret = function_return
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected factor but found \'%s\' instead.' % token.get_tk_value())
    return ret


def idtail():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        return actualpars()


def add_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.PLUS_TK and token.get_tk_type() is not TokenType.MINUS_TK:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'+\' or \'-\' but found \'%s\' instead.' % token.get_tk_value())
    token = lex()
    return op


def mul_oper():
    global token
    op = token.get_tk_value()
    if token.get_tk_type() is not TokenType.TIMES_TK and token.get_tk_type() is not TokenType.SLASH_TK:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'*\' or \'/\' but found \'%s\' instead.' % token.get_tk_value())
    token = lex()
    return op


def actualpars():
    global token
    if token.get_tk_type() is TokenType.LEFT_PARENTHESIS_TK:
        token = lex()
        actualparlist()
        if token.get_tk_type() is not TokenType.RIGHT_PARENTHESIS_TK:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected \')\' but found \'%s\' instead.' % token.get_tk_value())
        token = lex()
        return True
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'(\' after procedure or function call  but found \'%s\' instead.' % token.get_tk_value())


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
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Expected variable id but found \'%s\' instead.' % token.get_tk_value())
        if search_entity(parameter_id) is None:
            error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                               'Undefined actual parameter entity \'%s\'.' % parameter_id)
        token = lex()
        genquad('par', parameter_id, 'REF')
    else:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected parameter type in or inout but found \'%s\' instead.' % token.get_tk_value())


##############################################################
#                                                            #
#                   main driver program                      #
#                                                            #
##############################################################
def main(input_filename):
    intermediate_code_filepath = input_filename[:-4] + '.int'
    c_equivalent_filepath = input_filename[:-4] + '.c'
    asm_code_filepath = input_filename[:-4] + '.asm'
    open_files(input_filename, intermediate_code_filepath, c_equivalent_filepath, asm_code_filepath)

    global token
    # Begin syntax analysis
    token = lex()
    program()
    if token.get_tk_type() is not TokenType.EOF_TK:
        error_line_message(token.get_tk_lineno(), token.get_tk_charno(),
                           'Expected \'EOF\' but found \'%s\' instead.' % token.get_tk_value())

    generate_intermediate_code_file()
    if not subprogram_exists:
        generate_c_code_file()
    else:
        warning("Subprogram declared. Intermediate code to C equivalent file generation aborted.")
        # close and delete the empty file
        global c_code_file
        c_code_file.close()
        os.remove(c_equivalent_filepath)

    # print quad equivalent code
    '''for Quad in quads_list:
        print(Quad)'''
    print("Main program framelength: %d" % main_program_framelength)
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
