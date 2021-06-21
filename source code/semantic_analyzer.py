

from re import match as match
from copy import deepcopy as deepcopy
from os.path import getsize as getsize
import re

ARITH_OPS = ["Addition Operator", "Subtraction Operator", "Multiplication Operator",
             "Division Operator", "Modulo Operator", "Max Operator", "Min Operator"]
BOOL_OPS_1 = "NOT Operator"
BOOL_OPS_2 = ["AND Operator", "OR Operator", "XOR Operator"]
BOOL_OPS_INF = ["Infinite Arity AND Operator", "Infinite Arity OR Operator"]
COMP_OPS = ["Equality Operator", "Inequality Operator"]
COMP_OPS_2 = ["Max Operator", "Min Operator"]
LITERALS = ["NUMBR Literal", "NUMBAR Literal",
            "YARN Literal", "TROOF Literal", "NOOB Type"]

# GIMMEH User input regexs
NUMBR_Literal_regex = "^-?[0-9]{1,}$"
NUMBAR_Literal_regex = "^-?[0-9]*\.[0-9]{1,}$"
TROOF_Literal_regex = "^WIN$|^FAIL$"


def get_symbol_idx(identifier, symbol_table):
    if symbol_table:
        for idx in range(len(symbol_table)):
            if identifier in symbol_table[idx].keys():
                return idx
        return None
    else:
        return None


def translate_bool_inf(symbol_table, lexeme_types, lexemes, index):
    bool_op_inf = lexeme_types[index]
    operands = []
    if lexeme_types[index+1] == "TROOF Literal":
        operands.append(parse_TROOF(lexemes[index+1]))
        index = index+3

    elif lexeme_types[index+1] == BOOL_OPS_1 or lexeme_types[index+1] in BOOL_OPS_2:
        result = translate_bool(
            symbol_table, lexeme_types[index+1:], lexemes[index+1:], 0)

        if result[0] == None:
            return result

        else:
            operands.append(result[0])
            index = index+result[1]+3

    elif lexeme_types[index+1] in COMP_OPS:

        result = translate_comp_expr(
            symbol_table, lexeme_types[index+1:], lexemes[index+1:], 0)
        if result[0] == None:
            return result

        else:
            operands.append(result[0])
            index = index+result[1]+3

    elif lexeme_types[index+1] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+1], symbol_table)

        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                result = parse_TROOF(symbol_table[var_idx][lexemes[index+1]])
                operands.append(result)
                index = index+3

            else:
                return None, lexemes[index+1]+" is not TROOF Type"

        else:
            return None, lexemes[index+1]+" is an undeclared variable"

    else:
        return None, lexemes[index+1]+" is an invalid operator in ALL OF and ANY OF expressions"

    if len(lexemes) > 2:
        while index < len(lexemes):
            if lexeme_types[index] == "TROOF Literal":
                result = parse_TROOF(lexemes[index])
                operands.append(result)
                index = index+2

            elif lexeme_types[index] == BOOL_OPS_1 or lexeme_types[index] in BOOL_OPS_2:
                result = translate_bool(
                    symbol_table, lexeme_types[index:], lexemes[index:], 0)

                if result[0] == None:
                    return result

                else:
                    operands.append(result[0])
                    index = index+result[1]+2

            elif lexeme_types[index] in COMP_OPS:
                result = translate_comp_expr(
                    symbol_table, lexeme_types[index:], lexemes[index:], 0)
                if result[0] == None:
                    return result

                else:
                    operands.append(result[0])
                    index = index+result[1]+2

            elif lexeme_types[index] == "Variable Identifier":
                var_idx = get_symbol_idx(lexemes[index], symbol_table)

                if var_idx != None:
                    if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                        result = parse_TROOF(
                            symbol_table[var_idx][lexemes[index]])
                        operands.append(result)
                        index = index+2

                    else:
                        return None, lexemes[index]+" is not TROOF Type"

                else:
                    return None, lexemes[index]+" is an undeclared variable"

            else:
                return None, lexemes[index]+" is an invalid operator in ALL OF and ANY OF expressions"

    return parse_bool_inf(bool_op_inf, operands), index


def parse_bool_inf(bool_op_inf, operands):
    if bool_op_inf == "Infinite Arity AND Operator":
        return all(operands)
    elif bool_op_inf == "Infinite Arity OR Operator":
        return any(operands)


def translate_bool(symbol_table, lexeme_types, lexemes, index):
    bool_op = lexeme_types[index]
    left, right = None, None

    if bool_op == BOOL_OPS_1:
        if lexeme_types[index+1] == "TROOF Literal":
            print(lexemes[index+1])
            return not parse_TROOF(lexemes[index+1]), index+1

        elif lexeme_types[index+1] == "Variable Identifier":
            var_idx = get_symbol_idx(lexemes[index+1], symbol_table)

            if var_idx != None:
                if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                    return not parse_TROOF(symbol_table[var_idx][lexemes[index+1]]), index+1

                else:
                    return None, lexemes[index+1]+" is not TROOF Type"

            else:
                return None, lexemes[index+1]+" is an undeclared variable"

        elif lexeme_types[index+1] == BOOL_OPS_1 or lexeme_types[index+1] in BOOL_OPS_2:
            result, index = translate_bool(
                symbol_table, lexeme_types, lexemes, index+1)
            return not result, index

        else:
            return None, lexemes[index+1]+" is not TROOF Type"

    elif lexeme_types[index+1] == "TROOF Literal":
        # print("left", lexemes[index+1])
        left, index = parse_TROOF(lexemes[index+1]), index+1

    elif lexeme_types[index+1] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+1], symbol_table)

        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                left, index = parse_TROOF(
                    symbol_table[var_idx][lexemes[index+1]]), index+1

            else:
                return None, lexemes[index+1]+" is not TROOF Type"

        else:
            return None, lexemes[index+1]+" is an undeclared variable"

    elif lexeme_types[index+1] == BOOL_OPS_1 or lexeme_types[index+1] in BOOL_OPS_2:
        left, index = translate_bool(
            symbol_table, lexeme_types, lexemes, index+1)
        # print("left",left)
        if left == None:
            return left, index

    else:
        return None, lexemes[index+1]+" is an invalid operator in TROOF expressions"

    if lexeme_types[index+2] == "TROOF Literal":
        # print("right", lexemes[index+2])
        right, index = parse_TROOF(lexemes[index+2]), index+2
        # print("right",right)

    elif lexeme_types[index+2] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+2], symbol_table)

        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                right, index = parse_TROOF(
                    symbol_table[var_idx][lexemes[index+2]]), index+2

            else:
                return None, lexemes[index+2]+" is not TROOF Type"

        else:
            return None, lexemes[index+2]+" is an undeclared variable"

    elif lexeme_types[index+2] == BOOL_OPS_1 or lexeme_types[index+2] in BOOL_OPS_2:
        right, index = translate_bool(
            symbol_table, lexeme_types, lexemes, index+2)
        # print(index)
        if right == None:
            return right, index

    else:
        return None, lexemes[index+2]+" is an invalid operator in TROOF expressions"

    # left,right = parse_TROOF(left),parse_TROOF(right)

    # print(len(lexemes),index)

    return parse_bool(bool_op, left, right), index


def translate_to_TROOF(bool):
    if bool:
        return "WIN"
    else:
        return "FAIL"


def parse_TROOF(operand):
    return operand == "WIN"


def parse_bool(lexeme_type, Op1, Op2):
    if lexeme_type == "AND Operator":
        return Op1 and Op2
    elif lexeme_type == "OR Operator":
        return Op1 or Op2
    elif lexeme_type == "XOR Operator":
        return Op1 ^ Op2


def translate_arith(symbol_table, lexeme_types, lexemes, index, is_numbar):
    arith = lexeme_types[index]
    left, right = None, None

    if lexeme_types[index+1] == "NUMBR Literal":
        left, index = int(lexemes[index+1]), index+1

    elif lexeme_types[index+1] == "NUMBAR Literal":
        left, index = float(lexemes[index+1]), index+1
        is_numbar = True

    elif lexeme_types[index+1] == "Variable Identifier":
        # print("VARIABLE!")
        var_idx = get_symbol_idx(lexemes[index+1], symbol_table)
        # print(var_idx)
        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "NUMBR Literal" or symbol_table[var_idx]["Data Type"] == "NUMBAR Literal":
                left, index = symbol_table[var_idx][lexemes[index+1]], index+1

            else:
                return None, lexemes[index+1]+" is neither NUMBR nor NUMBAR type", is_numbar

        else:
            return None, lexemes[index+1]+" is an undeclared variable", is_numbar

    elif lexeme_types[index+1] in ARITH_OPS:
        left, index, is_numbar = translate_arith(
            symbol_table, lexeme_types, lexemes, index+1, is_numbar)
        # print(index)
        if left == None:
            return left, index, is_numbar
    else:
        return None, lexemes[index+1]+" is neither NUMBR nor NUMBAR type", is_numbar

    if lexeme_types[index+2] == "NUMBR Literal":
        print("right", lexemes[index+2])
        right, index = int(lexemes[index+2]), index+2

    elif lexeme_types[index+2] == "NUMBAR Literal":
        right, index = float(lexemes[index+2]), index+2
        is_numbar = True

    elif lexeme_types[index+2] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+2], symbol_table)
        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "NUMBR Literal" or symbol_table[var_idx]["Data Type"] == "NUMBAR Literal":
                right, index = symbol_table[var_idx][lexemes[index+2]], index+2

            else:
                return None, lexemes[index+2]+" is neither NUMBR nor NUMBAR type", is_numbar

        else:
            return None, lexemes[index+2]+" is an undeclared variable", is_numbar

    elif lexeme_types[index+2] in ARITH_OPS:
        right, index, is_numbar = translate_arith(
            symbol_table, lexeme_types, lexemes, index+2, is_numbar)

        if right == None:
            return right, index, is_numbar
    else:
        return None, lexemes[index+2]+" is neither NUMBR nor NUMBAR type", is_numbar

    return parse_arith(arith, left, right), index, is_numbar


def parse_arith(lexeme_type, Op1, Op2):
    if lexeme_type == "Addition Operator":
        return Op1+Op2
    elif lexeme_type == "Subtraction Operator":
        return Op1-Op2
    elif lexeme_type == "Multiplication Operator":
        return Op1*Op2
    elif lexeme_type == "Division Operator":
        if Op2 == 0:
            return None, "Division by zero"
        else:
            return Op1/Op2
    elif lexeme_type == "Modulo Operator":
        if Op2 == 0:
            return None, "Modulo by zero"
        else:
            return Op1 % Op2
    elif lexeme_type == "Max Operator":
        return max(Op1, Op2)
    elif lexeme_type == "Min Operator":
        return min(Op1, Op2)


def translate_comp_expr(symbol_table, lexeme_types, lexemes, index):
    comp_op = lexeme_types[index]
    left, right = None, None

    if lexeme_types[index+1] in LITERALS:
        if lexeme_types[index+1] == "TROOF Literal":
            left, index = parse_TROOF(lexemes[index+1]), index+1

        elif lexeme_types[index+1] == "NUMBR Literal":
            left, index = int(lexemes[index+1]), index+1

        elif lexeme_types[index+1] == "NUMBAR Literal":
            left, index = float(lexemes[index+1]), index+1

        else:
            left, index = lexemes[index+1], index+1

    elif lexeme_types[index+1] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+1], symbol_table)

        if var_idx != None:
            if symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                left, index = parse_TROOF(
                    symbol_table[var_idx][lexemes[index+1]]), index+1

            else:
                left, index = symbol_table[var_idx][lexemes[index+1]], index+1

        else:
            return None, lexemes[index+1]+" is an undeclared variable"

    else:
        return None, lexemes[index+1]+" is an invalid operand"

    # print("left",left)

    if lexeme_types[index+2] in LITERALS:
        if lexeme_types[index+2] == "TROOF Literal":
            right, index = parse_TROOF(lexemes[index+2]), index+2

        elif lexeme_types[index+2] == "NUMBR Literal":
            right, index = int(lexemes[index+2]), index+2

        elif lexeme_types[index+2] == "NUMBAR Literal":
            right, index = float(lexemes[index+2]), index+2

        else:
            right, index = lexemes[index+2], index+2

    elif lexeme_types[index+2] == "Variable Identifier":
        var_idx = get_symbol_idx(lexemes[index+2], symbol_table)

        if var_idx != None:
            right, index = symbol_table[var_idx][lexemes[index+2]], index+2

        else:
            return None, lexemes[index+2]+" is an undeclared variable"

    elif lexeme_types[index+2] in COMP_OPS_2:
        comp2_result = translate_arith(
            symbol_table, lexeme_types, lexemes, index+2, False)
        if comp2_result[0] == None:
            return comp2_result
        else:
            right, index = comp2_result[0], comp2_result[1]

    else:
        return None, lexemes[index+2]+" is an invalid operand"

    # print("right",right)

    final = parse_comp_op(comp_op, left, right)
    # print("final", final)

    return final, index

# parses LOLCODE comparison operation to

def parse_comp_op(operation, op1, op2):
    if operation == "Equality Operator":
        return op1 == op2
    elif operation == "Inequality Operator":
        return op1 != op2

# parses user input to corresponding LOLCODE data type and Python literal


def input_analyzer(input):
    if match(NUMBR_Literal_regex, input):
        return ("NUMBR Literal", int(match(NUMBR_Literal_regex, input).group(0)))
    elif match(NUMBAR_Literal_regex, input):
        return ("NUMBAR Literal", float(match(NUMBAR_Literal_regex, input).group(0)))
    elif match(TROOF_Literal_regex, input):
        return ("TROOF Literal", match(TROOF_Literal_regex, input).group(0))
    else:
        return ("YARN Literal", '"'+input+'"')

# evaluates value of IT variable to a TROOF value

def eval_IT(it_value, it_type):
    if it_type == "NOOB Type":
        return False
    elif it_type == "TROOF Literal" and it_value == "FAIL":
        return False
    elif it_value == 0:
        return False
    else:
        return True

# parses LOLCODE literals to Python literals

def parse_literal(literal, literal_type):
    if literal_type == "NUMBR Literal":
        return int(literal)
    elif literal_type == "NUMBAR Literal":
        return float(literal)
    elif literal_type == "TROOF Literal":
        return parse_TROOF(literal)
    elif literal_type == "YARN Literal":
        return literal[1:-1]
    else:
        return literal

# semantic analyzer main function

def semantic_analyzer(lexeme_tokens_in_line, symbol_table, is_o_rly, is_wtf, is_multi_comment):
    if not lexeme_tokens_in_line:
        return
    # print(lexeme_tokens_in_line)
    lexeme_types = [list(word.values())[0] for word in lexeme_tokens_in_line]
    lexemes = [list(word.keys())[0] for word in lexeme_tokens_in_line]

    if is_multi_comment:
        if "End of Multi-line Comment" in lexeme_types:
            end_idx = lexeme_types.index("End of Multi-line Comment")
            is_multi_comment.pop()
            if len(lexeme_types) > 1:
                return semantic_analyzer(lexeme_tokens_in_line[end_idx+1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

            return

        else:
            return

    if is_wtf[0] == 1:
        if is_wtf[1] == 0 and is_wtf[2] == 0:
            if lexeme_types[0] == "Case Declaration":
                if len(lexemes) > 1:
                    if len(lexemes) > 2:
                        if lexeme_types[2] != "Single Line Comment Declaration":
                            return "expected end of line, found "+lexemes[2]

                    case = parse_literal(lexemes[1], lexeme_types[1])
                    it_value = parse_literal(
                        is_wtf[3]["IT"], is_wtf[3]["Data Type"])
                    result = parse_comp_op("Equality Operator", case, it_value)
                    if result:
                        is_wtf[1] = 1
                    return

                else:
                    return "expected a case literal, found none"

            elif lexeme_types[0] == "End Condition Delimiter":
                is_wtf[0] = 0
                is_wtf[1] = 0
                is_wtf[2] = 0
                is_wtf[3] = None

            elif lexeme_types[0] == "Default Case Declaration":
                if len(lexemes) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return "expected end of line, found "+lexemes[1]

                is_wtf[1] = 1
                return

            else:
                return

        elif is_wtf[1] == 1 and is_wtf[2] == 0:
            if lexeme_types[0] == "Case Break":
                if len(lexeme_types) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return "expected end of line, found "+lexemes[1]

                    else:
                        is_wtf[2] = 1
                        return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

                is_wtf[2] = 1
                return

            elif lexeme_types[-1] == "Case Break":
                if len(lexeme_types) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return "expected end of line, found "+lexemes[1]

                    else:
                        is_wtf[2] = 1
                        return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

                is_wtf[2] = 1
                return

            elif lexeme_types[0] == "End Condition Delimiter":
                if len(lexeme_types) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return "expected end of line, found "+lexemes[1]

                    else:
                        is_wtf[0] = 0
                        is_wtf[1] = 0
                        is_wtf[2] = 0
                        is_wtf[3] = None

                        return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

                is_wtf[0] = 0
                is_wtf[1] = 0
                is_wtf[2] = 0
                is_wtf[3] = None

                return

        elif is_wtf[1] == 1 and is_wtf[2] == 1:
            if lexeme_types[0] == "End Condition Delimiter":
                if len(lexeme_types) > 1:
                    is_wtf[0] = 0
                    is_wtf[1] = 0
                    is_wtf[2] = 0
                    is_wtf[3] = None
                    return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

                is_wtf[0] = 0
                is_wtf[1] = 0
                is_wtf[2] = 0
                is_wtf[3] = None
                return

            else:
                return

    if is_o_rly[0] == 1:
        if is_o_rly[1] == 0 and is_o_rly[2] == 0:
            if lexeme_types[0] == "IF-Clause":
                if len(lexemes) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return 'expected end of line, found"'+lexemes[1]

                is_o_rly[1] = 1
                return

            else:
                return 'expected YA RLY, found"'+lexemes[0]

        elif is_o_rly[1] == 1 and is_o_rly[2] == 0:
            if lexeme_types[0] == "ELSE-Clause":
                if len(lexemes) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return 'expected end of line, found"'+lexemes[1]

                is_o_rly[2] = 1
                return

            elif lexeme_types[0] == "End Condition Delimiter":
                if len(lexemes) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return 'expected end of line, found"'+lexemes[1]

                for idx in range(len(is_o_rly)):
                    is_o_rly[idx] = 0

            elif is_o_rly[3] == 0:
                # print("skip YA RLY")
                return

        elif is_o_rly[1] == 1 and is_o_rly[2] == 1:
            if lexeme_types[0] == "End Condition Delimiter":
                if len(lexemes) > 1:
                    if lexeme_types[1] != "Single Line Comment Declaration":
                        return 'expected end of line, found"'+lexemes[1]

                    else:
                        return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

                for idx in range(len(is_o_rly)):
                    is_o_rly[idx] = 0
                return

            elif is_o_rly[3] == 1:
                # print("skip NO WAI")
                return

    if lexeme_types[0] == "Code Delimiter":
        if len(lexeme_types) > 1:
            return semantic_analyzer(lexeme_tokens_in_line[1:], symbol_table, is_o_rly, is_wtf, is_multi_comment)

        else:
            return

    elif lexeme_types[0] == "End of Code Delimiter":
        if len(lexeme_types) > 1:
            if lexeme_types[1] != "Single Line Comment Declaration":
                return "expected end of line, found"+lexeme_types[1]

        return

    elif lexeme_types[0] == "Variable Declaration":
        identifier = lexemes[1]
        token_idx = get_symbol_idx(identifier, symbol_table)
        # print("token idx", token_idx)
        if token_idx != None:
            if len(lexeme_tokens_in_line) > 2:
                if lexeme_types[3] == "NUMBR Literal":
                    symbol_table[token_idx][identifier] = int(lexemes[3])
                    symbol_table[token_idx]["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] == "NUMBAR Literal":
                    symbol_table[token_idx][identifier] = float(lexemes[3])
                    symbol_table[token_idx]["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] == "YARN Literal" or lexeme_types[3] == "TROOF Literal" or lexeme_types[3] == "NOOB Type":
                    symbol_table[token_idx][identifier] = lexemes[3]
                    symbol_table[token_idx]["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] in ARITH_OPS:
                    # print("LEXEMES!", lexemes[3:])
                    result = translate_arith(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0, False)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = result[0]

                        if result[2]:
                            symbol_table[token_idx]["Data Type"] = "NUMBAR Literal"
                        else:
                            symbol_table[token_idx]["Data Type"] = "NUMBR Literal"

                elif lexeme_types[3] in BOOL_OPS_2:
                    result = translate_bool(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] in BOOL_OPS_INF:
                    result = translate_bool_inf(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] in COMP_OPS:
                    result = translate_comp_expr(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] == "Variable Identifier":
                    var_idx = get_symbol_idx(lexemes[3], symbol_table)

                    if var_idx != None:
                        symbol_table[token_idx][identifier] = symbol_table[var_idx][lexemes[3]]
                        symbol_table[token_idx]["Data Type"] = symbol_table[var_idx]["Data Type"]

                    else:
                        return lexemes[3]+" is an undeclared variable"

            else:
                symbol_table[token_idx][identifier] = "NOOB"
                symbol_table[token_idx]["Data Type"] = "NOOB Type"

        else:
            symbol_token = {}
            if len(lexeme_tokens_in_line) > 2:
                if lexeme_types[3] == "NUMBR Literal":
                    symbol_token[identifier] = int(lexemes[3])
                    symbol_token["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] == "NUMBAR Literal":
                    symbol_token[identifier] = float(lexemes[3])
                    symbol_token["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] == "YARN Literal" or lexeme_types[3] == "TROOF Literal" or lexeme_types[3] == "NOOB Type":
                    symbol_token[identifier] = lexemes[3]
                    symbol_token["Data Type"] = lexeme_types[3]

                elif lexeme_types[3] in ARITH_OPS:
                    # print("LEXEMES!", lexemes[3:])
                    result = translate_arith(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0, False)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_token[identifier] = result[0]

                        if result[2]:
                            symbol_token["Data Type"] = "NUMBAR Literal"
                        else:
                            symbol_token["Data Type"] = "NUMBR Literal"

                elif lexeme_types[3] in BOOL_OPS_2:
                    print("BOOL OPSSS")
                    result = translate_bool(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    print(result)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_token[identifier] = translate_to_TROOF(
                            result[0])
                        symbol_token["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] in BOOL_OPS_INF:
                    result = translate_bool_inf(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_token[identifier] = translate_to_TROOF(
                            result[0])
                        symbol_token["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] in COMP_OPS:
                    result = translate_comp_expr(
                        symbol_table, lexeme_types[3:], lexemes[3:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_token[identifier] = translate_to_TROOF(
                            result[0])
                        symbol_token["Data Type"] = "TROOF Literal"

                elif lexeme_types[3] == "Variable Identifier":
                    var_idx = get_symbol_idx(lexemes[3], symbol_table)

                    if var_idx != None:
                        symbol_token[identifier] = symbol_table[var_idx][lexemes[3]]
                        symbol_token["Data Type"] = symbol_table[var_idx]["Data Type"]

                    else:
                        return lexemes[3]+" is an undeclared variable"

                elif lexeme_types[2] == "Single Line Comment Declaration":
                    symbol_token[identifier] = "NOOB"
                    symbol_token["Data Type"] = "NOOB Type"

            else:
                symbol_token[identifier] = "NOOB"
                symbol_token["Data Type"] = "NOOB Type"

            symbol_table.append(symbol_token)

    # variable start of expression
    elif lexeme_types[0] == "Variable Identifier" or lexeme_types[0] == "Implicit Variable":
        if len(lexeme_types) == 1:
            return "invalid keyword at the start of expression, found "+lexemes[0]

        identifier = lexemes[0]
        token_idx = get_symbol_idx(identifier, symbol_table)
        if token_idx != None:
            if lexeme_types[1] == "Assignment Operator":
                if lexeme_types[2] == "NUMBR Literal":
                    symbol_table[token_idx][identifier] = int(lexemes[2])
                    symbol_table[token_idx]["Data Type"] = lexeme_types[2]

                elif lexeme_types[2] == "NUMBAR Literal":
                    symbol_table[token_idx][identifier] = float(lexemes[2])
                    symbol_table[token_idx]["Data Type"] = lexeme_types[2]

                elif lexeme_types[2] == "YARN Literal" or lexeme_types[2] == "TROOF Literal" or lexeme_types[2] == "NOOB Type":
                    symbol_table[token_idx][identifier] = lexemes[2]
                    symbol_table[token_idx]["Data Type"] = lexeme_types[2]

                elif lexeme_types[2] in ARITH_OPS:
                    result = translate_arith(
                        symbol_table, lexeme_types[2:], lexemes[2:], 0, False)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = result[0]

                        if result[2]:
                            symbol_table[token_idx]["Data Type"] = "NUMBAR Literal"
                        else:
                            symbol_table[token_idx]["Data Type"] = "NUMBR Literal"

                elif lexeme_types[2] in BOOL_OPS_2:
                    result = translate_bool(
                        symbol_table, lexeme_types[2:], lexemes[2:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[2] in BOOL_OPS_INF:
                    result = translate_bool_inf(
                        symbol_table, lexeme_types[2:], lexemes[2:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[2] in COMP_OPS:
                    result = translate_comp_expr(
                        symbol_table, lexeme_types[2:], lexemes[2:], 0)
                    if result[0] == None:
                        return result[1]
                    else:
                        symbol_table[token_idx][identifier] = translate_to_TROOF(
                            result[0])
                        symbol_table[token_idx]["Data Type"] = "TROOF Literal"

                elif lexeme_types[2] == "Variable Identifier":
                    value_var_identifier = lexemes[2]
                    value_var_idx = get_symbol_idx(
                        value_var_identifier, symbol_table)

                    if value_var_idx != None:
                        symbol_table[token_idx][identifier] = symbol_table[value_var_idx][value_var_identifier]
                        symbol_table[token_idx]["Data Type"] = symbol_table[value_var_idx]["Data Type"]

                    else:
                        return value_var_identifier+" is an undeclared variable"

            elif lexeme_types[1] == "IT Assignment Operator":
                symbol_table[0]["IT"] = symbol_table[token_idx][identifier]
                symbol_table[0]["Data Type"] = symbol_table[token_idx]["Data Type"]

                if len(lexemes) > 2:
                    return semantic_analyzer(lexeme_tokens_in_line[2:], symbol_table, is_o_rly, is_wtf)

        else:
            return lexemes[0]+" is an undeclared variable"

    # VISIBLE start of expression
    elif lexeme_types[0] == "Printing Keyword":
        print_string = ""
        idx = 1
        while idx < len(lexeme_types):
            if lexeme_types[idx] == "YARN Literal":
                print_string = print_string + lexemes[idx][1:-1]
                idx = idx+1

            elif lexeme_types[idx] == "TROOF Literal":
                print_string = print_string + lexemes[idx]
                idx = idx+1

            elif lexeme_types[idx] == "NUMBR Literal" or lexeme_types[idx] == "NUMBAR Literal":
                print_string = print_string + str(lexemes[idx])
                idx = idx+1

            elif lexeme_types[idx] == "NOOB Type":
                return "Cannot implicitly cast NOOB to string"

            elif lexeme_types[idx] == "Variable Identifier" or lexeme_types[idx] == "Implicit Variable":
                var_identifier = lexemes[idx]
                var_idx = get_symbol_idx(var_identifier, symbol_table)

                if var_idx != None:
                    if symbol_table[var_idx]["Data Type"] == "YARN Literal":
                        print_string = print_string + \
                            symbol_table[var_idx][var_identifier][1:-1]
                        idx = idx+1

                    elif symbol_table[var_idx]["Data Type"] == "TROOF Literal":
                        print_string = print_string + \
                            symbol_table[var_idx][var_identifier]
                        idx = idx+1

                    elif symbol_table[var_idx]["Data Type"] == "NUMBR Literal" or symbol_table[var_idx]["Data Type"] == "NUMBAR Literal":
                        print_string = print_string + \
                            str(symbol_table[var_idx][var_identifier])
                        idx = idx+1

                    elif symbol_table[var_idx]["Data Type"] == "NOOB Type":
                        return "Cannot implicitly cast NOOB to string"

                else:
                    return var_identifier+" is an undeclared variable"

            elif lexeme_types[idx] in ARITH_OPS:
                result = translate_arith(
                    symbol_table, lexeme_types[idx:], lexemes[idx:], 0, False)
                if result[0] == None:
                    return result[1]
                else:
                    print_string = print_string+str(result[0])
                    idx = result[1]+idx+1

            elif lexeme_types[idx] in BOOL_OPS_2 or lexeme_types[idx] == BOOL_OPS_1:
                result = translate_bool(
                    symbol_table, lexeme_types[idx:], lexemes[idx:], 0)
                if result[0] == None:
                    return result[1]
                else:
                    print_string = print_string + \
                        str(translate_to_TROOF(result[0]))
                    idx = result[1]+idx+1

            elif lexeme_types[idx] in BOOL_OPS_INF:
                result = translate_bool_inf(
                    symbol_table, lexeme_types[idx:], lexemes[idx:], 0)
                if result[0] == None:
                    return result[1]
                else:
                    print_string = print_string + \
                        str(translate_to_TROOF(result[0]))
                    idx = result[1]+idx+1

            elif lexeme_types[idx] in COMP_OPS:
                result = translate_comp_expr(
                    symbol_table, lexeme_types[idx:], lexemes[idx:], 0)
                if result[0] == None:
                    return result[1]
                else:
                    print_string = print_string + \
                        str(translate_to_TROOF(result[0]))
                    idx = result[1]+idx+1

            elif lexeme_types[idx] == "Single Line Comment Declaration":
                break

            else:
                return "invalid type in VISIBLE statement, found "+lexemes[idx]

        # MAY BE IMPLEMENTED DIFFERENTLY WITH GUI
        print(print_string)
        file_output = open("./output.txt", "a")
        file_output.write(print_string+"\n")
        file_output.close()

    # GIMMEH start of expression
    elif lexeme_types[0] == "Input Keyword":
        # input_widget()
        var_identifier = lexemes[1]
        var_idx = get_symbol_idx(var_identifier, symbol_table)

        # print("INPUT!",var_idx)

        if var_idx != None:

            # data_type,user_input = input_analyzer(input())          # MAY BE IMPLEMENTED DIFFERENTLY WITH GUI

            if symbol_table[var_idx][var_identifier] == "NOOB":
                if getsize("./gimme.txt") == 0:
                    return 1, var_identifier+":"

                file_gimme = open("./gimme.txt", "r")
                data_type, user_input = input_analyzer(file_gimme.read())
                print(user_input, data_type)
                file_gimme.close()

                symbol_table[var_idx][var_identifier] = user_input
                symbol_table[var_idx]["Data Type"] = data_type

                file_gimme = open("./gimme.txt", "w")
                file_gimme.close()

            else:
                return

        else:
            return var_identifier+" is an undeclared variable"

    # ARITHMETIC start of expression
    elif lexeme_types[0] in ARITH_OPS:
        result = translate_arith(symbol_table, lexeme_types, lexemes, 0, False)
        if result[0] == None:
            return result[1]
        else:
            symbol_table[0]["IT"] = result[0]

            if result[2]:
                symbol_table[0]["Data Type"] = "NUMBAR Literal"
            else:
                symbol_table[0]["Data Type"] = "NUMBR Literal"

    # Unary and Binary BOOLEAN start of expression
    elif lexeme_types[0] in BOOL_OPS_2 or lexeme_types[0] == BOOL_OPS_1:
        result = translate_bool(symbol_table, lexeme_types, lexemes, 0)
        if result[0] == None:
            return result[1]
        else:
            symbol_table[0]["IT"] = translate_to_TROOF(result[0])
            symbol_table[0]["Data Type"] = "TROOF Literal"
            return

    elif lexeme_types[0] in BOOL_OPS_INF:
        result = translate_bool_inf(symbol_table, lexeme_types, lexemes, 0)
        if result[0] == None:
            return result[1]
        else:
            symbol_table[0]["IT"] = translate_to_TROOF(result[0])
            symbol_table[0]["Data Type"] = "TROOF Literal"

    elif lexeme_types[0] in COMP_OPS:
        result = translate_comp_expr(symbol_table, lexeme_types, lexemes, 0)
        if result[0] == None:
            return result[1]
        else:
            symbol_table[0]["IT"] = translate_to_TROOF(result[0])
            symbol_table[0]["Data Type"] = "TROOF Literal"

    elif lexeme_types[0] in LITERALS:
        if len(lexeme_types) == 1:
            symbol_table[0]["IT"] = lexemes[0]
            symbol_table[0]["Data Type"] = lexeme_types[0]
            return

        else:
            return "expected end of line, found "+lexemes[1]

    elif lexeme_types[0] == "Start of IF-Condition Delimiter":
        if len(lexeme_types) > 1:
            if lexeme_types[1] != "Single Line Comment Declaration":
                return 'expected end of line, found "'+lexemes[1]

        is_o_rly[0] = 1
        it_value = eval_IT(symbol_table[0]["IT"], symbol_table[0]["Data Type"])

        if it_value:
            is_o_rly[3] = 1

    elif lexeme_types[0] == "Start of Switch-Case Delimiter":
        if len(lexeme_types) > 1:
            if lexeme_types[1] != "Single Line Comment Declaration":
                return 'expected end of line, found "'+lexemes[1]

        is_wtf[0] = 1
        is_wtf[3] = deepcopy(symbol_table[0])

    elif lexeme_types[0] == "Single Line Comment Declaration":
        return

    elif lexeme_types[0] == "Start of Multi-line Comment":
        is_multi_comment.append(1)
        return

    else:
        return "invalid keyword at the start of expression, found "+lexemes[0]
# end of main function
