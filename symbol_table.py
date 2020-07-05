# This file holds the classes needed to implement the Symbol Table functionality.

from colors import ShellColors


class Scope:
    def __init__(self, nestinglevel=0, enclosing_scope=None):
        self.__entities_list = list()
        self.__nesting_level = nestinglevel
        self.__current_offset = 12
        self.__enclosing_scope = enclosing_scope

    def get_entities_list(self):
        return self.__entities_list

    def add_Entity(self, Entity):
        self.__entities_list.append(Entity)

    def get_nesting_level(self):
        return self.__nesting_level

    def get_current_offset(self):
        return self.__current_offset

    def get_current_offset_and_advance(self):
        current = self.__current_offset
        self.__current_offset += 4  # this is the next offset
        return current

    def get_enclosing_scope(self):
        return self.__enclosing_scope

    # tostring for debugging purposes
    def __str__(self):
        return '( ' + ShellColors.RED + 'Nesting Level: ' + ShellColors.END + str(
            self.__nesting_level) + ': Enclosing Scope: ' + self.__enclosing_scope.__str__() + ' )'


class Argument:
    def __init__(self, parMode, nextArgument=None):
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
        return '( ' + ShellColors.LIGHT_GRAY + 'Argument Parmode: ' + ShellColors.END + self.__parMode + '-->' \
               + ShellColors.LIGHT_GRAY + 'NextArgument: ' + ShellColors.END + self.__nextArgument.__str__() + ' )'


class Entity:
    # Entity type can be Variable or Function or Parameter or TemporaryVariable
    def __init__(self, name, entityType):
        self.__name = name
        self.__entityType = entityType

    def get_name(self):
        return self.__name

    def get_entityType(self):
        return self.__entityType

    # tostring for debugging purposes
    def __str__(self):
        return '( ' + ShellColors.YELLOW + ' Entity name: ' \
               + ShellColors.END + self.__name + ',  EntityType: ' + self.__entityType + ' )'


class Variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, 'Variable')
        self.__offset = offset

    def get_offset(self):
        return self.__offset

    def set_offset(self, offset):
        self.__offset = offset

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '    ( ' + 'Variable offset: ' + str(self.__offset) + ' )'


class Function(Entity):
    def __init__(self, name, startQuad=-1):
        super().__init__(name, 'Function')
        self.__startQuad = startQuad
        self.__arguments_list = list()
        self.__framelength = -1

    def get_startQuad(self):
        return self.__startQuad

    def set_start_quad(self, start_quad):
        self.__startQuad = start_quad

    def get_arguments_list(self):
        return self.__arguments_list

    def add_argument_in_list(self, argument):
        self.__arguments_list.append(argument)

    def get_framelength(self):
        return self.__framelength

    def set_framelength(self, framelength):
        self.__framelength = framelength

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '    ( startQuad: ' + str(self.__startQuad) + ', framelen: ' + str(
            self.__framelength) + ' )'


class Parameter(Entity):
    def __init__(self, name, parMode, offset=-1):
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
        return super().__str__() + '    ( Parameter mode: ' + self.__parMode + ', offset: ' + str(self.__offset) + ' )'


class TemporaryVariable(Entity):
    def __init__(self, name, offset=-1):
        super().__init__(name, 'Tempvar')
        self.__offset = offset

    def get_offset(self):
        return self.__offset

    def set_offset(self, offset):
        self.__offset = offset

    # tostring for debugging purposes
    def __str__(self):
        return super().__str__() + '    ( Temporary Variable offset: ' + str(self.__offset) + ' )'
