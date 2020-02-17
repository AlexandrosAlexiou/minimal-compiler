import sys
import string


class lex_output():
    token_numberid = -2
    token=""

#Bound words (Desmeumenes Lekseis)
program_tk=0
declare_tk=1
if_tk=2
else_tk=3
while_tk=4
doublewhile_tk=5
loop_tk=6
exit_tk=7
forcase_tk=8
incase_tk=9
default_tk=10
not_tk=11
and_tk=12
or_tk=13
function_tk=14
procedure_tk=15
call_tk=16
return_tk=17
in_tk=18
inout_tk=19
input_tk=20
print_tk=21

bound_words_array =['program_tk','declare_tk',
        'if_tk','else_tk',
        'while_tk','doublewhile_tk','loop_tk','exit_tk',
        'forcase_tk','incase_tk','incase_tk','default_tk'
        'not_tk','and_tk','or_tk',
        'function_tk','procedure_tk','call_tk','return_tk','in_tk','inout_tk',
        'input_tk','print_tk']

#Tokens (Lektikes monades)
id_tk = 22  # variable
digit_tk = 23  # pshfio
plus_tk = 24  # +
minus_tk = 25  # -
multi_tk = 26  # *
division_tk = 27  # /
equal_tk = 28  # =
smaller_tk = 29  # <
different_tk = 30  # <>
greater_than_tk = 31  # >
greater_than_or_equal_tk =32  # >=
smaller_than_or_equal_tk = 33 # <=
assign_tk = 34  # :=
double_colon_tk = 35  # :
open_comment_tk = 36  # \*
close_comment_tk = 37  # *\
comma_tk = 38  # ,
semicolon_tk = 39  # ;
open_brackets1_tk = 40  # (
close_brackets1_tk = 41  # )
open_brackets2_tk = 42  # [
close_brackets2_tk = 43  # ]
eof_tk = 44  # eof_tk
white_character_tk = 45 
error_tk = -1  # error




def main():
    lex_return_values=lex_output()
    compile_target=open(sys.argv[1], "r+")

if __name__=="__main__":
    main()

