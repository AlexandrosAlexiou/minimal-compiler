class Quad:
    # eg. 100: -,a,b,c => c := a - b
    def __init__(self, label, op, x, y, z):
        self.__label = label  # eg. 100,101
        self.__op = op  # +,-,*,/
        self.__x = x  # variable name or constant
        self.__y = y  # variable name or constant
        self.__z = z  # variable name

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
        self.__z = z

    # tostring for debugging purposes
    def __str__(self):
        return '(' + str(self.__label) + ': ' + str(self.__op) + ', ' + str(self.__x) + ', ' + str(
            self.__y) + ', ' + str(self.__z) + ')'

    # tostring for intermediate code file generation
    def quad_to_file(self):
        return str(self.__label) + ': ' + str(self.__op) + ', ' + str(self.__x) + ', ' + str(self.__y) + ', ' + str(
            self.__z) + '\n'
