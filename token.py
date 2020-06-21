class TokenType:
    def __init__(self):
        pass

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
    RIGHT_BRACE_TK = 23
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
    AND_TK = 40
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
    # End Of File
    EOF_TK = 51


# Lexical analyzer return values to the syntax analyzer
class Token:
    def __init__(self, tk_type=None, tk_value=None, tk_lineno=None, tk_charno=None):
        self.__tk_type = tk_type  # token type
        self.__tk_value = tk_value  # token string value
        self.__tk_lineno = tk_lineno  # token line number
        self.__tk_charno = tk_charno  # token character number from the start of the line

    def get_tk_type(self):
        return self.__tk_type

    def set_tk_type(self, tk_type):
        self.__tk_type = tk_type

    def get_tk_value(self):
        return self.__tk_value

    def set_tk_value(self, tk_value):
        self.__tk_value = tk_value

    def get_tk_lineno(self):
        return self.__tk_lineno

    def set_tk_lineno(self, tk_lineno):
        self.__tk_lineno = tk_lineno

    def get_tk_charno(self):
        return self.__tk_charno

    def set_tk_charno(self, tk_charno):
        self.__tk_charno = tk_charno

    # Tostring for debugging purposes
    def __str__(self):
        return '(' + str(self.__tk_type) + ',' + str(self.__tk_value) + ')'
