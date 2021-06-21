import re
from semantic_analyzer import semantic_analyzer as semantic_analyzer
from semantic_analyzer import get_symbol_idx as get_symbol_idx
from os.path import getsize as getsize

FILE_INPUT_PATH = "./samp2.lol"
FILE_OUTPUT_PATH = "./output.txt"

# lexical analysis global variable/s
lexeme_table = []


# syntax analysis global variables/s
USED_HAI, USED_KTHXBYE, USED_VISIBLE, SINGLE_COMMENT_ON, MULTICOMMENT_ON, MULTICOMMENT_CLOSE, VISIBLE_ON, COMPARISON_ON, IS_SUCCESSFUL = False, False, False, False, False, False, False, False, False

INF_AND, INF_OR, MKAY_BOOL = False, False, False
START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED, COMPONENT_CNT = False, False, False, False, 0
START_SWITCH, SWITCH_CLOSED, COMPONENT_CNT2 = False, False, 0
START_GENERAL_IF, START_GENERAL_SWITCH = False, False
ARITH_OP, AN_OP, BOOL_OP, AN_OP2, COMP_OP, AN_OP3 = 0, 0, 0, 0, 0, 0

# semantics analysis global variable/s
symbol_table = [{"IT": "NOOB", "Data Type": "NOOB Type"}]

# ---------------------------------------------------------------------------------------------------------------------------------------

# Code Delimiter
HAI_regex = '^\s*HAI\s*$|^\s*HAI\s{1,}'
KTHXBYE_regex = '^\s*KTHXBYE\s*$|^\s*KTHXBYE\s{1,}'

# Variable Declaration
I_HAS_A_regex = '^\s*I HAS A\s*$|^\s*I HAS A\s{1,}'
ITZ_regex = '^\s*ITZ\s*$|^\s*ITZ\s{1,}'

IT_regex = '^\s*IT\s*$|^\s*IT\s{1,}'

# Comment
BTW_regex = '^\s*BTW\s*$|^\s*BTW\s{1,}'
OBTW_regex = '^\s*OBTW\s*$|^\s*OBTW\s{1,}'
TLDR_regex = '^\s*TLDR\s*$|^\s*TLDR\s{1,}'

# Value assignment
R_regex = "^\s*R\s*$|^\s*R\s{1,}"

# Arithmetic Operations
SUM_OF_regex = "^\s*SUM OF\s*$|^\s*SUM OF\s{1,}"
DIFF_OF_regex = "^\s*DIFF OF\s*$|^\s*DIFF OF\s{1,}"
PRODUKT_OF_regex = "^\s*PRODUKT OF\s*$|^\s*PRODUKT OF\s{1,}"
QUOSHUNT_OF_regex = "^\s*QUOSHUNT OF\s*$|^\s*QUOSHUNT OF\s{1,}"
MOD_OF_regex = "^\s*MOD OF\s*$|^\s*MOD OF\s{1,}"

# Logical Operations
BIGGR_OF_regex = "^\s*BIGGR OF\s*$|^\s*BIGGR OF\s{1,}"
SMALLR_OF_regex = "^\s*SMALLR\s*OF\s*$|^\s*SMALLR\s*OF\s{1,}"
BOTH_OF_regex = "^\s*BOTH OF\s*$|^\s*BOTH OF\s{1,}"
EITHER_OF_regex = "^\s*EITHER OF\s*$|^\s*EITHER OF\s{1,}"
WON_OF_regex = "^\s*WON OF\s$|^\s*WON OF\s{1,}"
NOT_regex = "^\s*NOT\s*$|^\s*NOT\s{1,}"
ANY_OF_regex = "^\s*ANY OF\s*$|^\s*ANY OF\s{1,}"
ALL_OF_regex = "^\s*ALL OF\s*$|^\s*ALL OF\s{1,}"
BOTH_SAEM_regex = "^\s*BOTH SAEM\s*$|^\s*BOTH SAEM\s{1,}"
DIFFRINT_regex = "^\s*DIFFRINT\s*$|^\s*DIFFRINT\s{1,}"

# Operand Separator
AN_regex = "^\s*AN\s*$|^\s*AN\s{1,}"

# String Concatenation
SMOOSH_regex = "^\s*SMOOSH\s*$|^\s*SMOOSH\s{1,}"

# User input/output
GIMMEH_regex = "^\s*GIMMEH\s*$|^\s*GIMMEH\s{1,}"
VISIBLE_regex = "^\s*VISIBLE\s*$|^\s*VISIBLE\s{1,}"

# Control Flow

# If-condition
O_RLY_regex = "^\s*O\sRLY\?\s*$|^\s*O\sRLY\?\s{1,}"
YA_RLY_regex = "^\s*YA\sRLY\s*$|^\s*YA\sRLY\s{1,}"
MEBBE_regex = "^\s*MEBBE\s*$|^\s*MEBBE\s{1,}"
NO_WAI_regex = "^\s*NO\sWAI\s*$|^\s*NO\sWAI\s{1,}"
OIC_regex = "\s*OIC\s*$|\s*OIC\s{1,}"

# switch-case
WTF_regex = "^\s*WTF\?\s*$|^\s*WTF\?\s{1,}"
OMG_regex = "^\s*OMG\s*$|^\s*OMG\s{1,}"
GTFO_regex = "^\s*GTFO\s*$|^\s*GTFO\s{1,}"
OMGWTF_regex = "^\s*OMGWTF\s*$|^\s*OMGWTF\s{1,}"
COMMA_regex = "^\s*\,\s*$|^\s*\,\s{1,}"

# Literals
NUMBR_Literal_regex = "^\s*-?[0-9]{1,}\s*$|^\s*-?[0-9]{1,}\s{1,}"
NUMBAR_Literal_regex = "^\s*-?[0-9]*\.[0-9]{1,}\s*$|^\s*-?[0-9]*\.[0-9]{1,}\s{1,}"
YARN_Literal_regex = '^\s*\"[^\"]*\"\s*$|^\s*\"[^\"]*\"\s{1,}'
TROOF_Literal_regex = "^\s*WIN\s*$|^\s*WIN\s{1,}|^\s*FAIL\s*$|^\s*FAIL\s{1,}"
Variable_regex = "^\s*[a-zA-z]{1,}[a-zA-Z0-9\_]*\s*|^\s*[a-zA-z]{1,}[a-zA-Z0-9\_]*\s{1,}"

# Comments
COMMENT_regex = "^\s*[^\s]{1,}\s*$|^\s*[^\s]{1,}\s{1,}"


def create_lexeme_dictionary():
    lexeme_dictionary = {}

    lexeme_dictionary["HAI"] = "Code Delimiter"
    lexeme_dictionary["KTHXBYE"] = "End of Code Delimiter"
    lexeme_dictionary["BTW"] = "Single Line Comment Declaration"
    lexeme_dictionary["OBTW"] = "Start of Multi-line Comment"
    lexeme_dictionary["TLDR"] = "End of Multi-line Comment"
    lexeme_dictionary["I HAS A"] = "Variable Declaration"
    lexeme_dictionary["ITZ"] = "Initialization Assignment Operator"
    lexeme_dictionary["R"] = "Assignment Operator"
    lexeme_dictionary["IT"] = "Implicit Variable"

    # arithmetic/mathematical operations
    lexeme_dictionary["SUM OF"] = "Addition Operator"
    lexeme_dictionary["DIFF OF"] = "Subtraction Operator"
    lexeme_dictionary["PRODUKT OF"] = "Multiplication Operator"
    lexeme_dictionary["QUOSHUNT OF"] = "Division Operator"
    lexeme_dictionary["MOD OF"] = "Modulo Operator"
    lexeme_dictionary["BIGGR OF"] = "Max Operator"
    lexeme_dictionary["SMALLR OF"] = "Min Operator"

    # logical operators
    lexeme_dictionary["BOTH OF"] = "AND Operator"
    lexeme_dictionary["EITHER OF"] = "OR Operator"
    lexeme_dictionary["WON OF"] = "XOR Operator"
    lexeme_dictionary["NOT"] = "NOT Operator"
    lexeme_dictionary["ALL OF"] = "Infinite Arity AND Operator"
    lexeme_dictionary["ANY OF"] = "Infinite Arity OR Operator"

    # comparison operators
    lexeme_dictionary["BOTH SAEM"] = "Equality Operator"
    lexeme_dictionary["DIFFRINT"] = "Inequality Operator"

    # operand separator
    lexeme_dictionary["AN"] = "Operand Separator"

    # Concatenation
    lexeme_dictionary["SMOOSH"] = "Concatenation Operator"
    lexeme_dictionary["MKAY"] = "End Delimiter"

    # Input Output
    lexeme_dictionary["GIMMEH"] = "Input Keyword"
    lexeme_dictionary["VISIBLE"] = "Printing Keyword"

    # Conditions
    lexeme_dictionary["O RLY?"] = "Start of IF-Condition Delimiter"
    lexeme_dictionary["YA RLY"] = "IF-Clause"
    lexeme_dictionary["NO WAI"] = "ELSE-Clause"

    lexeme_dictionary["WTF?"] = "Start of Switch-Case Delimiter"
    lexeme_dictionary["OMG"] = "Case Declaration"
    lexeme_dictionary["GTFO"] = "Case Break"
    lexeme_dictionary["OMGWTF"] = "Default Case Declaration"
    lexeme_dictionary["OIC"] = "End Condition Delimiter"

    # literals
    lexeme_dictionary["NUMBR"] = "NUMBR Literal"
    lexeme_dictionary["NUMBAR"] = "NUMBAR Literal"
    lexeme_dictionary["YARN"] = "YARN Literal"
    lexeme_dictionary["TROOF"] = "TROOF Literal"

    lexeme_dictionary["VARIABLE"] = "Variable Identifier"
    lexeme_dictionary["COMMA"] = "IT Assignment Operator"
    lexeme_dictionary["COMMENT"] = "Comment Identifier"

    return lexeme_dictionary


def get_type(line):
    if re.match(BTW_regex, line):
        return ("BTW",)
    elif re.match(OBTW_regex, line):
        return ("OBTW",)
    elif re.match(HAI_regex, line):
        return ("HAI",)
    elif re.match(KTHXBYE_regex, line):
        return ("KTHXBYE",)
    elif re.match(I_HAS_A_regex, line):
        return ("I HAS A",)
    elif re.match(ITZ_regex, line):
        return ("ITZ",)
    elif re.match(IT_regex, line):
        return ("IT",)
    elif re.match(R_regex, line):
        return ("R",)
    elif re.match(TLDR_regex, line):
        return ("TLDR",)
    elif re.match(SUM_OF_regex, line):
        return ("SUM OF",)
    elif re.match(DIFF_OF_regex, line):
        return ("DIFF OF",)
    elif re.match(PRODUKT_OF_regex, line):
        return ("PRODUKT OF",)
    elif re.match(QUOSHUNT_OF_regex, line):
        return ("QUOSHUNT OF",)
    elif re.match(MOD_OF_regex, line):
        return ("MOD OF",)
    elif re.match(BIGGR_OF_regex, line):
        return ("BIGGR OF",)
    elif re.match(SMALLR_OF_regex, line):
        return ("SMALLR OF",)
    elif re.match(BOTH_OF_regex, line):
        return ("BOTH OF",)
    elif re.match(EITHER_OF_regex, line):
        return ("EITHER OF",)
    elif re.match(WON_OF_regex, line):
        return ("WON OF",)
    elif re.match(NOT_regex, line):
        return ("NOT",)
    elif re.match(ANY_OF_regex, line):
        return ("ANY OF",)
    elif re.match(ALL_OF_regex, line):
        return ("ALL OF",)
    elif re.match(BOTH_SAEM_regex, line):
        return ("BOTH SAEM",)
    elif re.match(DIFFRINT_regex, line):
        return ("DIFFRINT",)
    elif re.match(AN_regex, line):
        return("AN",)
    elif re.match(SMOOSH_regex, line):
        return ("SMOOSH",)
    elif re.match(GIMMEH_regex, line):
        return ("GIMMEH",)
    elif re.match(VISIBLE_regex, line):
        return ("VISIBLE",)
    elif re.match(O_RLY_regex, line):
        return ("O RLY?",)
    elif re.match(YA_RLY_regex, line):
        return ("YA RLY",)
    elif re.match(NO_WAI_regex, line):
        return ("NO WAI",)
    elif re.match(OIC_regex, line):
        return ("OIC",)
    elif re.match(COMMA_regex, line):
        return ("COMMA", re.match(COMMA_regex, line).group(0).strip())
    elif re.match(WTF_regex, line):
        return ("WTF?",)
    elif re.match(OMG_regex, line):
        return ("OMG",)
    elif re.match(GTFO_regex, line):
        return ("GTFO",)
    elif re.match(OMGWTF_regex, line):
        return ("OMGWTF",)
    elif re.match(NUMBR_Literal_regex, line):
        return ("NUMBR", re.match(NUMBR_Literal_regex, line).group(0).strip())
    elif re.match(NUMBAR_Literal_regex, line):
        return ("NUMBAR", re.match(NUMBAR_Literal_regex, line).group(0).strip())
    elif re.match(YARN_Literal_regex, line):
        return ("YARN", re.match(YARN_Literal_regex, line).group(0).strip())
    elif re.match(TROOF_Literal_regex, line):
        return ("TROOF", re.match(TROOF_Literal_regex, line).group(0).strip())
    elif re.match(Variable_regex, line):
        return ("VARIABLE", re.match(Variable_regex, line).group(0).strip())
    else:
        return ("Unidentified",)


def check_variable(line):
    pass
    # if re.match()


def find_match(lexeme_dictionary, current_word):
    matched_word = [match for match in lexeme_dictionary.values()
                    if match == current_word]
    return (matched_word.pop())


def own_line_error(keyword, line_number):
    return ("<LINE {}> Syntax Error".format(line_number) + " keyword({}) must have its own line.".format(keyword))


def parse(lexeme_dictionary, line, line_number, max_line_count):
    global USED_HAI, USED_KTHXBYE, USED_VISIBLE, SINGLE_COMMENT_ON, MULTICOMMENT_ON, ARITH_OP, AN_OP, BOOL_OP, AN_OP2, INF_AND, INF_OR, MKAY_BOOL, VISIBLE_ON, MULTICOMMENT_CLOSE, COMP_OP, AN_OP3, IS_SUCCESSFUL, START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED, COMPONENT_CNT, START_GENERAL_IF, START_GENERAL_SWITCH, START_SWITCH, SWITCH_CLOSED, COMPONENT_CNT2

    error = None
    OP_in_INF, AN_in_INF, separating_AN = 0, 0, 0
    isCompleteSet, no_of_boolean_sets = False, 0

    isDeclaring = False
    isNOT_ON = False
    has_bool, has_comp = False, False
    isArithmetic, isLogic, isINF, COMPARISON_ON = False, False, False, False
    check_line = [list(word.values())[0] for word in line]
    check_line_words = [list(word.keys())[0] for word in line]

    # print("token line: ",check_line)

    idx = 0
    # print("before accecssing the line: ", START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED)

    while(idx < len(check_line)):
        # if the multicomment flag is on, all succeeding lines are just treated as comments, so no need to check for syntax
        if(SINGLE_COMMENT_ON):
            break

        if(idx == 0):     # the first lexeme in the line
            if(check_line[idx] in lexeme_dictionary.values()):
                # gets the classification of the current lexeme in check
                current_word = find_match(lexeme_dictionary, check_line[idx])

                # the following code activates some flags for necessary keywords, and checks the validity of the syntax as well
                if(current_word == "Single Line Comment Declaration"):
                    break
                elif(current_word == "Code Delimiter"):
                    USED_HAI = True
                elif(current_word == "End of Code Delimiter"):
                    USED_KTHXBYE = True
                elif(current_word == "Variable Declaration"):
                    isDeclaring = True
                elif(current_word == "Start of Multi-line Comment"):
                    MULTICOMMENT_ON = True
                elif(current_word == "End of Multi-line Comment"):
                    if(MULTICOMMENT_ON != True):
                        # error shown if a TLDR is seen after a TLDR is previously declared
                        error = ("<LINE {}> Syntax Error".format(
                            line_number) + " Referenced to undefined variable TLDR.")
                        IS_SUCCESSFUL = False
                    else:  # otherwise, successfully close the multicomment
                        MULTICOMMENT_CLOSE = True
                # for arithmetic operations
                elif(current_word in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator"]):
                    # will increment the number of arithmetic operators, after finding some
                    ARITH_OP += 1
                    # activate the flag that an arithmetic operation is happening
                    isArithmetic = True
                elif(current_word in ["AND Operator", "OR Operator", "XOR Operator"]):
                    BOOL_OP += 1                         # will increment the number of boolean operators
                    # activate the flag the a boolean operation is happening
                    isLogic = True
                elif(current_word == "NOT Operator"):
                    isNOT_ON = True

                # there are separate flags for these operations with infinite arities
                elif(current_word == "Infinite Arity AND Operator"):
                    INF_AND = True
                elif(current_word == "Infinite Arity OR Operator"):
                    INF_OR = True

                elif(current_word == "Printing Keyword"):
                    VISIBLE_ON = True

                # if a comparison operation is read
                elif(current_word in ["Equality Operator", "Inequality Operator"]):
                    COMP_OP += 1                        # will increment the number of comparison operators
                    # activate the flag that a comparison operation is happening
                    COMPARISON_ON = True

                # when conditional statements are read
                elif(current_word == "Start of IF-Condition Delimiter"):
                    if(START_IF):   # if there are multiple O RLY? keywords found
                        error = ("<LINE {}> Syntax Error: ".format(
                            line_number) + " Expected keyword(YA RLY) Found keyword(O RLY?). ")
                        IS_SUCCESSFUL = False
                    else:
                        START_IF = True
                        COMPONENT_CNT += 1
                elif(current_word == "IF-Clause"):
                    if(START_SWITCH == False):                   # if a switch case is not opened
                        if(YA_RLY_CLAUSE):                       # will check if a YA RLY is found
                            error = ("<LINE {}> Syntax Error: ".format(
                                line_number) + " Invalid keyword at start of expression. ")
                            IS_SUCCESSFUL = False
                        if(START_IF):
                            START_GENERAL_IF = True    # flag for checking the OIC part later
                        # if a YA RLY is found when there is no O RLY? above
                        if(START_IF != True):
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Missing keyword(O RLY?) at the stand of the block.")
                            IS_SUCCESSFUL = False
                        else:
                            YA_RLY_CLAUSE = True
                            COMPONENT_CNT += 1
                    # when a switch case is on and found a YA RLY
                    if(START_IF == False):
                        error = ("<LINE {}> Syntax Error".format(
                            line_number) + " Expected OMG, OMGWTF, or OIC.")
                        IS_SUCCESSFUL = False
                elif(current_word == "ELSE-Clause"):
                    if(START_SWITCH == False):
                        # makes sure that there is always a YA RLY before NO WAI
                        if(NO_WAI_CLAUSE):
                            error = ("<LINE {}> Syntax Error: ".format(
                                line_number) + " Invalid keyword at start of expression. ")
                            IS_SUCCESSFUL = False
                        if(START_IF != True):                    # Missing O RLY? at the start
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Invalid start of conditional block. Expecting keyword(O RLY?). ")
                            IS_SUCCESSFUL = False
                        elif(YA_RLY_CLAUSE != True):             # YA RLY must be present
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Expecting keyword(YA RLY).")
                            IS_SUCCESSFUL = False
                        else:
                            NO_WAI_CLAUSE = True
                            COMPONENT_CNT += 1
                    if(START_IF == False):
                        error = ("<LINE {}> Syntax Error".format(
                            line_number) + " Expected OMG, OMGWTF, or OIC.")
                        IS_SUCCESSFUL = False
                elif(current_word == "Start of Switch-Case Delimiter"):
                    if(START_IF == False):
                        if(START_SWITCH):
                            error = ("<LINE {}> Syntax Error: ".format(
                                line_number) + " Multiple declarations of keyword(WTF?). ")
                            IS_SUCCESSFUL = False
                        else:
                            START_SWITCH = True
                            COMPONENT_CNT2 += 1
                    else:
                        START_SWITCH = True
                        COMPONENT_CNT2 += 1
                elif(current_word == "Case Declaration"):
                    if(START_IF == False):
                        if(START_SWITCH):
                            START_GENERAL_SWITCH = True
                    else:
                        if(START_SWITCH):
                            if(COND_CLOSED == False):
                                error = ("<LINE {}> Syntax Error: ".format(
                                    line_number) + " missing oic sis. ")
                                IS_SUCCESSFUL = False
                            else:
                                next

                        else:
                            error = ("<LINE {}> Syntax Error: ".format(
                                line_number) + " Expected YA RLY, NO WAI, or OIC. ")
                            IS_SUCCESSFUL = False

                # checker for the end condition delimiter OIC
                elif(current_word == "End Condition Delimiter"):
                    # meaning the current opened block is an if block
                    if(START_GENERAL_SWITCH != True):
                        if(START_GENERAL_IF != True):     # if there is no O RLY?
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Missing keyword(O RLY?) at the start of the block.")
                            IS_SUCCESSFUL = False
                        # If there is an O RLY but has no YA RLY
                        elif(START_IF and YA_RLY_CLAUSE == False):
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Missing keyword(YA RLY).")
                            IS_SUCCESSFUL = False
                        else:                              # otherwise, success
                            COND_CLOSED = True
                            COMPONENT_CNT += 1
                    if(START_GENERAL_IF != True):          # meanign the current opened block is a switch
                        if(START_GENERAL_SWITCH != True):
                            error = ("<LINE {}> Syntax Error".format(
                                line_number) + " Found keyword(OIC) with missing keyword(WTF?) at the start of the block.")
                            IS_SUCCESSFUL = False
                        else:
                            SWITCH_CLOSED = True
                            COMPONENT_CNT2 += 1
            else:
                error = ("Syntax Error: Invalid Keyword")
                IS_SUCCESSFUL = False
        else:                                                             # succeeding lexemes in the line

            if(USED_KTHXBYE == True):         # If the KTHXBYE is used already, no more codes are expected
                error = ("<LINE {}> Syntax Error".format(line_number) +
                         " Unexpected input after the program end.")
                IS_SUCCESSFUL = False

            # Assigns the previous lexeme
            previous_word = check_line[idx-1]

            # Start of Code
            if(check_line[idx] == "Code Delimiter"):
                not_allowed_keywords = ["Code Delimiter", "Initialization Assignment Operator", "Addition Operator", "Subtraction Operator", "Multiplication Onitialization Assignment Operator", "Asperator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator", "AND Operator", "OR Operator",
                                        "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator", "Equality Operator", "Inequality Operator", "Operand Separator", "Concatenation Operator", "End Delimiter", "Printing Keyword", "IF-Clause", "Case Declaration", "Default Case Declaration"]
                not_allowed2 = ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Start of Multi-line Comment",
                                "End of Multi-line Comment", "Implicit Variable", "Start of IF-Condition Delimiter", "Start of Switch-Case Delimiter"]
                # there must be no keywords before HAI
                if(previous_word in not_allowed_keywords):
                    error = ("<LINE {}> Syntax Error: Invalid Keyword at start of expression".format(
                        line_number))
                    IS_SUCCESSFUL = False
                elif(previous_word in not_allowed2):
                    error = ("<LINE {}> Syntax Error: Expected: Endline; Got: keyword(HAI)".format(
                        line_number))
                    IS_SUCCESSFUL = False
                # KTHXBYE is declared first before HAI
                elif(previous_word == "End of Code Delimiter"):
                    error = ("<LINE {}> Syntax Error: KTHXBYE is not allowed when HAI is not used.".format(
                        line_number))
                    IS_SUCCESSFUL = False
                # if a GTFO keyword is found not in loops/func
                elif(previous_word == "Case Break"):
                    error = ("<LINE {}> Syntax Error: GTFO must be used inside a loop or a function".format(
                        line_number))
                    IS_SUCCESSFUL = False
                elif(previous_word == "Variable Declaration" or "Input Keyword"):
                    error = ("<LINE {}> Syntax Error: Expected: Identifier; Got: keyword(HAI)".format(
                        line_number))
                    IS_SUCCESSFUL = False

            # NUMBAR Literal (Float)
            elif(check_line[idx] == "NUMBAR Literal"):
                not_allowed = ["Implicit Variable", "Start of IF-Condition Delimiter", "IF-Clause", "ELSE-Clause",
                               "Start of Switch-Case Delimiter", "Case Break", "Default Case Declaration", "End Condition Delimiter"]

                # checks if the HAI is found, then 1.2 is the only thing it can succeed it
                if(previous_word == "Code Delimiter" and float(check_line_words[idx]) != 1.2):
                    error = ("<LINE {}>".format(
                        line_number) + " Expected: float(1.2); Got float({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False

                # all arguments for boolean operations must not contain a numbar literal
                elif(previous_word in ["Operand Separator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator"] and isLogic):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid operation. Expecting Boolean Argument/s. Found a NUMBAR Literal")
                    IS_SUCCESSFUL = False

                # if the previous word is not allowed, returns error
                elif(previous_word in not_allowed):
                    error = (
                        "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                    IS_SUCCESSFUL = False

                # all literals are allowed to preceed and succeed each other if a visible keyword is present
                elif(previous_word in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]):
                    if(VISIBLE_ON):
                        next
                    else:
                        error = (
                            "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                        IS_SUCCESSFUL = False

            # NUMBR Literal (integer)
            elif(check_line[idx] == "NUMBR Literal"):
                # works the same just like in NUMBAR literal syntax checkers
                not_allowed = ["Implicit Variable", "Infinite Arity OR Operator", "Start of IF-Condition Delimiter", "IF-Clause",
                               "ELSE-Clause", "Start of Switch-Case Delimiter", "Case Break", "Default Case Declaration", "End Condition Delimiter"]
                if(previous_word == "Code Delimiter" and int(check_line_words[idx]) != 1.2):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expected: float(1.2); Got int({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False
                elif(previous_word in ["Operand Separator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator"] and isLogic):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid operation. Expecting Boolean Argument/s. Found a NUMBR Literal. ")
                    IS_SUCCESSFUL = False
                elif(previous_word in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]):
                    if(VISIBLE_ON):
                        next
                    else:
                        error = (
                            "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                        IS_SUCCESSFUL = False

            # Variable Identifier
            elif(check_line[idx] == "Variable Identifier"):
                not_allowed = ["End of Code Delimiter", "Implicit Variable", "Start of Switch-Case Delimiter", "Start of IF-Condition Delimiter",
                               "IF-Clause", "ELSE-Clause", "Case Break", "Default Case Declaration", "End Condition Delimiter"]

                # if the keyword before is HAI, then a variable is not allowed, only 1.2 float is allowed
                if(previous_word == "Code Delimiter" and check_line_words[idx] != "1.2"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expected: float(1.2); Got identifier({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False

                # one variable as argument in the ALL OF or ANY OF operation is a complete set already
                elif(previous_word in ["Infinite Arity AND Operator", "Infinite Arity OR Operator"]):
                    isCompleteSet = True

                # if the variable precedes an AN separator and it is the last of the line, it will be a complete set
                elif(previous_word == "Operand Separator" and idx == len(check_line)-1):
                    isCompleteSet = True
                elif(previous_word in not_allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Could not parse literal. ")
                    IS_SUCCESSFUL = False

                # same logic as to the other literals, they can precede and succeed each other if a visible is found
                elif(previous_word in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]):
                    if(VISIBLE_ON):
                        next
                    else:
                        error = (
                            "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                        IS_SUCCESSFUL = False

            # Troof Literal
            elif(check_line[idx] == "TROOF Literal"):
                not_allowed = ["End of Code Delimiter", "Implicit Variable", "Start of Switch-Case Delimiter", "Start of IF-Condition Delimiter",
                               "IF-Clause", "ELSE-Clause", "Case Break", "Default Case Declaration", "End Condition Delimiter"]
                invalid_ops = ["Addition Operator", "Subtraction Operator", "Multiplication Operator",
                               "Division Operator", "Modulo Operator", "Max Operator", "Min Operator"]
                if(previous_word == "Code Delimiter" and check_line_words[idx] != "1.2"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expected: float(1.2); Got troof literal({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False
                elif(previous_word in ["Infinite Arity AND Operator", "Infinite Arity OR Operator"]):
                    isCompleteSet = True
                elif(previous_word == "Operand Separator" and idx == len(check_line)-1):
                    isCompleteSet = True
                elif(previous_word in not_allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Could not parse literal. ")
                    IS_SUCCESSFUL = False
                elif(previous_word in invalid_ops):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid operation. ")
                    IS_SUCCESSFUL = False
                elif(previous_word in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]):
                    if(VISIBLE_ON):
                        next
                    else:
                        error = (
                            "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                        IS_SUCCESSFUL = False

            # YARN Literal
            elif(check_line[idx] == "YARN Literal"):
                allowed = ["Initialization Assignment Operator", "Assignment Operator", "Equality Operator",
                           "Inequality Operator", "Operand Separator", "End Delimiter", "Printing Keyword", "Case Declaration"]
                if(previous_word == "Code Delimiter" and check_line_words[idx] != "1.2"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expected: float(1.2); Got string({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False
                elif(previous_word in ["Operand Separator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator"] and isLogic):
                    print("islogic: ", isLogic)
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid operation. Expecting Boolean Argument/s. Found a YARN Literal. ")
                    IS_SUCCESSFUL = False
                elif(previous_word in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]):
                    if(VISIBLE_ON):
                        next
                    else:
                        error = (
                            "<LINE {}> Syntax Error: Expected endline. ".format(line_number))
                        IS_SUCCESSFUL = False
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error: Expected endline. ")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "Input Keyword"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid keyword at start of expression. ")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "End of Code Delimiter"):
                USED_KTHXBYE = True
                if(previous_word == "Code Delimiter"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expected: float(1.2); Got keyword({}) ".format(check_line_words[idx]))
                    IS_SUCCESSFUL = False

            # Comments (Single-line comment and Multi-line comment)
            elif(check_line[idx] == "Start of Multi-line Comment"):
                not_allowed = ["Code Delimiter", "Initialization Assignment Operator", "Implicit Variable", "Addition Operator", "Subtraction Operator", "Multiplication Onitialization Assignment Operator", "Asperator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator", "Equality Operator",
                               "Inequality Operator", "Operand Separator", "Concatenation Operator", "End Delimiter", "Printing Keyword", "IF-Clause", "Case Declaration", "Default Case Declaration", "NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Start of IF-Condition Delimiter", "Start of Switch-Case Delimiter", "Variable Declaration", "Input Keyword", "End of Multi-line Comment"]
                if(previous_word in not_allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Multiline Comment must start on a new line.")
                    IS_SUCCESSFUL = False
                else:
                    MULTICOMMENT_ON = True
            elif(check_line[idx] == "End of Multi-line Comment"):
                not_allowed = ["Code Delimiter", "Initialization Assignment Operator", "Implicit Variable", "Addition Operator", "Subtraction Operator", "Multiplication Onitialization Assignment Operator", "Asperator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator",
                               "Equality Operator", "Inequality Operator", "Operand Separator", "Concatenation Operator", "End Delimiter", "Printing Keyword", "IF-Clause", "Case Declaration", "Default Case Declaration", "NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Start of IF-Condition Delimiter", "Start of Switch-Case Delimiter", "Variable Declaration", "Input Keyword"]
                if(previous_word in not_allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " TLDR of Multiline Comment must have an own line.")
                    IS_SUCCESSFUL = False
                elif(MULTICOMMENT_CLOSE == True):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Referenced to undefined variable TLDR.")
                    IS_SUCCESSFUL = False
                else:
                    MULTICOMMENT_CLOSE = True
            elif(check_line[idx] == "Single Line Comment Declaration"):
                SINGLE_COMMENT_ON = True

            # Variable Declaration
            elif(check_line[idx] == "Variable Declaration"):
                not_allowed = ["Code Delimiter", "Initialization Assignment Operator", "Implicit Variable", "Addition Operator", "Subtraction Operator", "Multiplication Onitialization Assignment Operator", "Asperator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator",
                               "Equality Operator", "Inequality Operator", "Operand Separator", "Concatenation Operator", "End Delimiter", "Printing Keyword", "IF-Clause", "Case Declaration", "Default Case Declaration", "NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Start of IF-Condition Delimiter", "Start of Switch-Case Delimiter", "Variable Declaration", "Input Keyword"]
                if(previous_word in not_allowed):
                    error = own_line_error(check_line[idx], line_number)
                    IS_SUCCESSFUL = False

            # Variable Assignments and Initializations
            elif(check_line[idx] == "Initialization Assignment Operator"):
                if(previous_word != "Variable Identifier"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expecting an identifier found ({}).".format(check_line_words[idx-1]))
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "Assignment Operator"):
                allowed = ["Variable Identifier", "Implicit Variable"]
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Expecting an identifier found ({}).".format(check_line_words[idx-1]))
                    IS_SUCCESSFUL = False

            elif(check_line[idx] == "Implicit Variable"):
                not_allowed1 = ["Input Keyword", "Start of IF-Condition Delimiter", "IF-Clause", "ELSE-Clause",
                                "Start of Switch-Case Delimiter", "Case Break", "End Condition Delimiter", "Default Case Declaration"]
                if(previous_word in not_allowed1):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " ")
                    IS_SUCCESSFUL = False
                elif(previous_word == "Case Declaration"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Could not parse literal.")
                    IS_SUCCESSFUL = False

            # Arithmetic Operations
            elif(check_line[idx] == "Addition Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                if(isDeclaring == True and previous_word != "Initialization Assignment Operator"):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Assignment of Value.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    print("entered here", previous_word)
                    ARITH_OP += 1
                    isArithmetic = True
                    # AN_OP += 1
            elif(check_line[idx] == "Subtraction Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Multiplication Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Division Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Modulo Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Max Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Min Operator"):
                allowed = ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Max Operator", "Min Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Variable Identifier", "Assignment Operator", "Equality Operator", "Inequality Operator", "Printing Keyword"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    ARITH_OP += 1
                    isArithmetic = True
            elif(check_line[idx] == "Operand Separator"):
                allowed = ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "Addition Operator", "Subtraction Operator", "Multiplication Operator",
                           "Division Operator", "Modulo Operator", "Max Operator", "Min Operator", "Variable Identifier", "YARN Literal"]
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    if(isArithmetic):
                        AN_OP += 1
                    if(isLogic):
                        print("in logic")
                        AN_OP2 += 1
                    if(isNOT_ON and previous_word == "TROOF Literal" and not isLogic):
                        error = ("<LINE {}> Syntax Error".format(
                            line_number) + " Invalid Operation.")
                        IS_SUCCESSFUL = False
                    if(INF_AND or INF_OR):
                        if(isCompleteSet):
                            separating_AN += 1
                        else:
                            AN_in_INF += 1
                    elif(COMPARISON_ON):
                        AN_OP3 += 1

            # Boolean Operations
            elif(check_line[idx] == "AND Operator"):
                isCompleteSet = False
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator",
                           "Operand Separator", "Initialization Assignment Operator", "Assignment Operator", "Equality Operator", "Inequality Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    if(INF_AND or INF_OR):
                        OP_in_INF += 1
                        has_bool = True
                        # isLogic = True
                    else:
                        BOOL_OP += 1
                        isLogic = True
            elif(check_line[idx] == "OR Operator"):
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator",
                           "Infinite Arity OR Operator", "Variable Identifier", "Operand Separator", "Equality Operator", "Inequality Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(previous_word not in allowed):
                    # print("here")
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    BOOL_OP += 1
                    isLogic = True

            elif(check_line[idx] == "XOR Operator"):
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator",
                           "Infinite Arity OR Operator", "Variable Identifier", "Operand Separator", "Equality Operator", "Inequality Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    BOOL_OP += 1
                    isLogic = True
            elif(check_line[idx] == "NOT Operator"):
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Infinite Arity AND Operator",
                           "Infinite Arity OR Operator", "Variable Identifier", "Operand Separator", "Equality Operator", "Inequality Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    isNOT_ON = True

            # Boolean Operation with Infinite Arity
            elif(check_line[idx] == "Infinite Arity AND Operator"):
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Variable Identifier",
                           "Operand Separator", "Equality Operator", "Inequality Operator", "Initialization Assignment Operator", "Assignment Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(INF_AND == True or INF_OR == True):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " ALL OF cannot be nested.")
                    IS_SUCCESSFUL = False
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    INF_AND = True

            elif(check_line[idx] == "Infinite Arity OR Operator"):
                allowed = ["TROOF Literal", "AND Operator", "OR Operator", "XOR Operator", "NOT Operator", "Variable Identifier",
                           "Operand Separator", "Equality Operator", "Inequality Operator", "Initialization Assignment Operator", "Assignment Operator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(INF_OR == True or INF_AND == True):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " ANY OF cannot be nested.")
                    IS_SUCCESSFUL = False
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                else:
                    INF_OR = True

            # Concatenation
            elif(check_line[idx] == "Concaternation Operator"):
                allowed = ["Initialization Assignment Operator",
                           "Assignment Operator", "Implicit Variable"]
                if(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid keyword at start of operation.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "End Delimiter"):
                pass

            # Printing
            elif(check_line[idx] == "Printing Keyword"):
                not_allowed = ["Start of Multi-line Comment", "End of Multi-line Comment", "Variable Declaration", "Initialization Assignment Operator", "Assignment Operator", "Operand Separator", "End Delimiter", "Input Keyword",
                               "Printing Keyword", "Start of IF-Condition Delimiter", "IF-Clause", "ELSE-Clause", "Start of Switch-Case Delimiter", "Case Declaration", "Case Break", "Default Case Declaration", "End Condition Delimiter"]
                if(previous_word in not_allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid operation.")
                    IS_SUCCESSFUL = False

            # Comparison Operator
            elif(check_line[idx] == "Equality Operator"):
                allowed = ["Printing Keyword", "Initialization Assignment Operator", "Assignment Operator", "Equality Operator",
                           "Inequality Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator", "Operand Separator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(INF_AND or INF_OR):
                    if(previous_word == "Operand Separator"):
                        AN_in_INF += 1
                    OP_in_INF += 1
                    has_comp = True
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    COMPARISON_ON = True
                    COMP_OP += 1

            elif(check_line[idx] == "Inequality Operator"):
                allowed = ["Printing Keyword", "Initialization Assignment Operator", "Assignment Operator", "Equality Operator",
                           "Inequality Operator", "Infinite Arity AND Operator", "Infinite Arity OR Operator", "Operand Separator"]
                if(previous_word in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal", "Variable Identifier", "Printing Keyword"] and VISIBLE_ON):
                    next
                elif(INF_AND or INF_OR):
                    if(previous_word == "Operand Separator"):
                        AN_in_INF += 1
                    OP_in_INF += 1
                elif(previous_word not in allowed):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + " Invalid Operation.")
                    IS_SUCCESSFUL = False
                elif(COMPARISON_ON):
                    COMP_OP += 1
                else:
                    COMPARISON_ON = True
                    COMP_OP += 1

            # Conditional Statements

            # IF-ELSE block syntax checking
            elif(check_line[idx] == "Start of IF-Condition Delimiter"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "IF-Clause"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "ELSE-Clause"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False

            # Switch-CASE block syntax checking
            elif(check_line[idx] == "Start of Switch-Case Delimiter"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "Case Declaration"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "Case Break"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False

            elif(check_line[idx] == "Default Case Declaration"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False
            elif(check_line[idx] == "End Condition Delimiter"):
                if(previous_word != None):
                    error = ("<LINE {}> Syntax Error".format(
                        line_number) + "Expected endline.")
                    IS_SUCCESSFUL = False

        # will make sure that all literals can be arguments of the ANY OF and ALL OF
        if(OP_in_INF == AN_in_INF and check_line[idx] in ["TROOF Literal", "Variable Identifier", "NUMBR Literal", "NUMBAR Literal"]):
            # if there is nested boolean operation that has a numbar or numbr argument, will return error
            if(has_bool and check_line[idx] in ["NUMBR Literal", "NUMBAR Literal"]):
                error = ("<LINE {}> Syntax Error".format(
                    line_number) + " Invalid Boolean Operation.")
                IS_SUCCESSFUL = False
            else:
                isCompleteSet = True

        # will count the number of complete sets for the arguments of the boolean operator with infinity arity
        if(INF_AND or INF_OR):
            if(check_line[idx-1] == "Operand Separator" and isCompleteSet):
                no_of_boolean_sets += 1
            elif(check_line[idx] in ["TROOF Literal", "Variable Identifier"] and isCompleteSet):
                no_of_boolean_sets += 1

        idx += 1

    # Will make sure that there will be no more code after KTHXBYE ending code delimiter was met
    if(line_number == max_line_count and (USED_HAI == False and USED_KTHXBYE == True)):
        error = ("<LINE {}> Syntax Error: ".format(line_number) +
                 " KTHXBYE is not allowed when HAI is not used.")
        IS_SUCCESSFUL = False

    # If the multicomment keyword OBTW is declared and there is no TLDR detected
    if(line_number == max_line_count and (MULTICOMMENT_ON and MULTICOMMENT_CLOSE == False)):
        error = ("<LINE {}> Syntax Error: ".format(
            line_number) + " Expected: TLDR; Found none.")
        IS_SUCCESSFUL = False

    # Will restart the flags if both keywords OBTW and TLDR was met, meaning the multiline comment is done
    if((MULTICOMMENT_ON and MULTICOMMENT_CLOSE) == True):
        MULTICOMMENT_ON, MULTICOMMENT_CLOSE = False, False

    if(ARITH_OP != AN_OP):
        error = ("<LINE {}> Syntax Error: ".format(line_number) +
                 " Expected: endline; Invalid Operation")
        IS_SUCCESSFUL = False

    # syntax checker for the validity of the operations (argument wise)
    if(isLogic):                                    # boolen operations
        if(BOOL_OP != AN_OP2):
            error = ("<LINE {}> Syntax Error: ".format(line_number) +
                     " Expected: endline; Invalid Operation")
            IS_SUCCESSFUL = False

    if(COMP_OP != AN_OP3):                          # comparison operations
        error = ("<LINE {}> Syntax Error: ".format(line_number) +
                 " Expected: endline; Invalid Operation")
        IS_SUCCESSFUL = False

    if(INF_AND or INF_OR):                          # boolean operation with infinite arity
        if(OP_in_INF == AN_in_INF):
            if(separating_AN >= no_of_boolean_sets):
                error = ("<LINE {}> Syntax Error: ".format(
                    line_number) + " Missing Argument. ")
                IS_SUCCESSFUL = False
        else:
            error = ("<LINE {}> Syntax Error: ".format(line_number) +
                     " Expected: endline; Invalid Operation")
            IS_SUCCESSFUL = False

    # syntax checking for IF BLOCK
    if(COND_CLOSED or SWITCH_CLOSED):  # if the OIC of if block is found, restart all the flags
        START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED, START_GENERAL_IF = False, False, False, False, False
        START_SWITCH, SWITCH_CLOSED, START_GENERAL_SWITCH = False, False, False
        COMPONENT_CNT, COMPONENT_CNT2 = 0, 0

    # if the line number is the last line of code and still there is no OIC met, will return error
    elif(line_number == max_line_count):
        if(START_IF):   # if the O RLY? keyword is encountered
            if(COMPONENT_CNT == 1):  # will check if the number of components is equal to 1 only, meaning the only component is the O RLY? keyword
                error = ("<LINE {}> Syntax Error: ".format(
                    line_number) + " Unfinished Conditional Statement. ")
                IS_SUCCESSFUL = False

            # these succeeding elif clauses is for the missing OIC keyword based on the number of components met
            elif(START_IF and YA_RLY_CLAUSE and NO_WAI_CLAUSE == False and COMPONENT_CNT == 2):
                error = ("<LINE {}> Syntax Error: ".format(line_number) +
                         " Missing keyword(OIC) at the end of the block. ")
                IS_SUCCESSFUL = False

            elif(START_IF and YA_RLY_CLAUSE and NO_WAI_CLAUSE and COMPONENT_CNT != 4):
                error = ("<LINE {}> Syntax Error: ".format(line_number) +
                         " Missing keyword(OIC) at the end of the block. ")
                IS_SUCCESSFUL = False
        # if the WTF? keyword is encountered
        elif(START_SWITCH):
            if(COMPONENT_CNT2 != 2):
                error = ("<LINE {}> Syntax Error: ".format(line_number) +
                         " Missing keyword(OIC) at the end of the block. ")
                IS_SUCCESSFUL = False

    # reinitalization of flags
    SINGLE_COMMENT_ON = False
    ARITH_OP, AN_OP, BOOL_OP, AN_OP2 = 0, 0, 0, 0
    INF_AND, INF_OR = False, False

    # last checker to know if the line has seen errors
    # if successful, returns the line and None for error
    if(IS_SUCCESSFUL):
        return line, None
    else:                                                 # otherwise, return an empty list and the error
        return [], error


def load_symbol_table():

    if getsize("symbol_table_cache.txt"):
        file_sym_table = open("symbol_table_cache.txt", "r")
        token_list = file_sym_table.read().split("\n")
        for token in token_list:
            if token:
                sep_token = token.split(",")
                new_token = {}
                new_token[sep_token[0]] = sep_token[1]
                new_token["Data Type"] = sep_token[2]
                symbol_table.append(new_token)
        file_sym_table.close()


def save_symbol_table():
    file_sym_table = open("symbol_table_cache.txt", "w")
    for token in symbol_table[1:]:
        keys = list(token.keys())
        values = list(token.values())
        print(keys)
        file_sym_table.write(keys[0]+","+str(values[0])+","+values[1]+"\n")
    file_sym_table.close()


def main():

    global USED_HAI, USED_KTHXBYE, USED_VISIBLE, SINGLE_COMMENT_ON, MULTICOMMENT_ON, ARITH_OP, AN_OP, BOOL_OP, AN_OP2, INF_AND, INF_OR, MKAY_BOOL, VISIBLE_ON, MULTICOMMENT_CLOSE, COMP_OP, AN_OP3, IS_SUCCESSFUL, START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED, COMPONENT_CNT, START_GENERAL_IF, START_GENERAL_SWITCH, START_SWITCH, SWITCH_CLOSED, COMPONENT_CNT2
    USED_HAI, USED_KTHXBYE, USED_VISIBLE, SINGLE_COMMENT_ON, MULTICOMMENT_ON, MULTICOMMENT_CLOSE, VISIBLE_ON, COMPARISON_ON, IS_SUCCESSFUL = False, False, False, False, False, False, False, False, False

    INF_AND, INF_OR, MKAY_BOOL = False, False, False
    START_IF, YA_RLY_CLAUSE, NO_WAI_CLAUSE, COND_CLOSED, COMPONENT_CNT = False, False, False, False, 0
    START_SWITCH, SWITCH_CLOSED, COMPONENT_CNT2 = False, False, 0
    START_GENERAL_IF, START_GENERAL_SWITCH = False, False
    ARITH_OP, AN_OP, BOOL_OP, AN_OP2, COMP_OP, AN_OP3 = 0, 0, 0, 0, 0, 0

    symbol_table = [{"IT": "NOOB", "Data Type": "NOOB Type"}]
    is_o_rly = [0, 0, 0, 0]
    is_wtf = [0, 0, 0, None]
    is_multi_comment = []

    load_symbol_table()

    # file reading
    file_input = open(FILE_INPUT_PATH, "r")
    line_table = [n.strip() for n in file_input.read().split("\n")]
    file_input.close()

    file_output = open(FILE_OUTPUT_PATH, "w")
    file_output.close()

    # contains lexeme and its classification
    lexeme_dictionary = create_lexeme_dictionary()
    is_BTW = False              # single line comment flag
    is_OBTW = False             # multi line comment flag

    line_count = 1          # line counter
    for line in line_table:
        line = line.strip()
        lexeme_tokens_in_line = []          # each line is stored as a list of tokens
        # print("line:", line_count)
        while line:
            lexeme_token = {}               # lexeme token is stored as a dictionary

            # previous lexeme is a BTW / short comment
            if is_BTW:
                lexeme_token[line] = lexeme_dictionary["COMMENT"]
                is_BTW = False
                line = ''

            # previous lexeme is an OBTW / long comment
            elif is_OBTW:
                # print("is_OBTW", line)
                lexeme = re.match(COMMENT_regex, line).group(0).strip()
                if "TLDR" in line:                                         # stops identifying next lines as comments
                    tldr_idx = line.index("TLDR")
                    if tldr_idx == 0:
                        # create lexeme classification as token
                        lexeme_token[line[0:4]] = lexeme_dictionary["TLDR"]
                        lexeme_tokens_in_line.append(lexeme_token)

                        # removes identified lexeme in line
                        line = line.replace(line[0:4], '', 1).strip()

                    else:
                        # create lexeme classification as token
                        lexeme_token[line[:tldr_idx-1]
                                     ] = lexeme_dictionary["COMMENT"]
                        lexeme_tokens_in_line.append(lexeme_token)
                        lexeme_token1 = {}
                        # create lexeme classification as token
                        lexeme_token1[line[tldr_idx:tldr_idx+4]
                                      ] = lexeme_dictionary["TLDR"]
                        lexeme_tokens_in_line.append(lexeme_token1)

                        # removes identified lexeme in line
                        line = line.replace(line[:tldr_idx+4], '', 1).strip()

                    # set multi line comment flag to False
                    is_OBTW = False

                    continue

                else:                                                       # every next line is a comment
                    # identify lexeme classification
                    lexeme_token[line] = lexeme_dictionary["COMMENT"]
                    line = ''                                               # removes the whole line

            # unidentified lexeme / Invalid keyword
            else:
                lexeme = get_type(line)
                if lexeme[0] == "Unidentified":
                    print("Error: Invalid character in line",
                          line_count)       # Error prompt
                    # preemptive exit
                    exit(1)

                # lexeme is a variable/literal/comma
                elif lexeme[0] == "VARIABLE" or lexeme[0] == "NUMBR" or lexeme[0] == "NUMBAR" or lexeme[0] == "YARN" or lexeme[0] == "TROOF" or lexeme[0] == "COMMA":
                    # removes identified lexeme in line
                    line = line.replace(lexeme[1], '', 1).strip()
                    # create lexeme classification as token
                    lexeme_token[lexeme[1]] = lexeme_dictionary[lexeme[0]]

                # short comment / single line comment
                elif lexeme[0] == "BTW":
                    # removes identified lexeme in line
                    line = line.replace(lexeme[0], '', 1).strip()
                    # create lexeme classification as token
                    lexeme_token[lexeme[0]] = lexeme_dictionary[lexeme[0]]
                    # set single line comment flag to True
                    is_BTW = True

                # long comment / multi line comment
                elif lexeme[0] == "OBTW":
                    # removes identified lexeme in line
                    line = line.replace(lexeme[0], '', 1).strip()
                    # create lexeme classification as token
                    lexeme_token[lexeme[0]] = lexeme_dictionary[lexeme[0]]
                    # set single line comment flag to True
                    is_OBTW = True

                # lexeme is a keyword
                else:
                    # removes identified lexeme in line
                    line = line.replace(lexeme[0], '', 1).strip()
                    # create lexeme classification as token
                    lexeme_token[lexeme[0]] = lexeme_dictionary[lexeme[0]]

            # add lexeme tokens to lexeme_tokens_in_line
            lexeme_tokens_in_line.append(lexeme_token)
            # print(lexeme_token)

        curr_line = lexeme_tokens_in_line
        parsed_line, error = parse(
            lexeme_dictionary, curr_line, line_count, len(line_table))
        if error:
            file_output = open(FILE_OUTPUT_PATH, "a")
            file_output.write(error)
            file_output.close()
            print(error)

            return

        semantic_error = semantic_analyzer(
            lexeme_tokens_in_line, symbol_table, is_o_rly, is_wtf, is_multi_comment)
        if semantic_error:
            if semantic_error[0] == 1:
                return print(semantic_error[1])
            else:
                file_output = open(FILE_OUTPUT_PATH, "a")
                file_output.write("<LINE "+str(line_count) +
                                  "> Semantic Error: "+semantic_error)
                file_output.close()
                print("<LINE "+str(line_count) +
                      "> Semantic Error: "+semantic_error)

                return

        # add lexeme_tokens_in_line to overall lexeme table
        lexeme_table.append(lexeme_tokens_in_line)
        # increment line counter
        line_count = line_count+1

    for symbol in symbol_table:
        print(symbol)

    save_symbol_table()

    return(lexeme_table, symbol_table)
    # print(lexeme_table)
    # for line in lexeme_table:
    #     print(line)


if __name__ == '__main__':
    main()
