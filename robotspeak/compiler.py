from maze import *
#collection of variables
global lineNumber
variabledict = {}





validload = {"1", "2", "3"}




class SyntaxErrorException(Exception):
    def __init__(self, description, lineNumber):
        self.description = description
        self.lineNumber = lineNumber
        super().__init__(f"What ARE YOU DOING?!?!?!? SyntaxError: {description} at line {lineNumber} !!!!!")

class RuntimeErrorException(Exception):
    def __init__(self, description, lineNumber):
        self.description = description
        self.lineNumber = lineNumber
        super().__init__(f"YOOOOOOOO!!!!! What are you doing at line {lineNumber} with this RuntimeError!!!?!?!?! {description}")

def removecomments(line):
    return line.split("@", 1)[0]

vocabulary = {
    "LOAD", "IF", "OTHERWISE", "WHILE", "END", "AND", "OR", "TRUE", "FALSE", 
    "MOVE_FORWARD", "TURN_LEFT", "TURN_RIGHT", "PICK_KEY", "OPEN_DOOR",
    "FRONT_IS_CLEAR", "ON_KEY", "AT_DOOR", "AT_EXIT", "1", "2", "3", ":=" #the numbers and := do not count to vocabulary cap of 20
}

def compiler(codeList): #Each element of the list is a line of code


    lineNumber =0
    numLines = len(codeList)



    while lineNumber<len(codeList): #For every line, line-by-line
        line = codeList[lineNumber]
        lineNumber += 1
        line = removecomments(line).strip()#remove all comments from the line to ignore and protect against cases where line = "      @comment"
        tokens = tokeniser(line, lineNumber)
        if not tokens:
            continue
        ##################################################################################
        #parser time
        res = parser(tokens, lineNumber, numLines, codeList)
        if res == "HALT":
            break
        if isinstance(res, int): #if returned a number to jump to
            lineNumber = res - 1
            continue



def parser(tokens, lineNumber, numLines, codingList):
    #case it is the first line
    if lineNumber ==1:
        if tokens[0] != "LOAD":
            raise SyntaxErrorException("LOAD is not the first token.", lineNumber)
        if len(tokens) == 1:
            raise RuntimeErrorException("You have to specify which program to run", lineNumber)
        if tokens[1] not in validload or len(tokens) != 2:
            raise RuntimeErrorException("You've gotta load either program 1, 2 or 3", lineNumber)

        match tokens[1]:
            case "1":
                program1()
            case "2":
                program2()
            case "3":
                program3()
        return
        
    if lineNumber ==numLines: #final line
        if len(tokens) == 1 and tokens[0] == "END":
                return "HALT" #end the program
        else:
            raise SyntaxErrorException("END is not the only token on the last line", lineNumber)
    #normal lines
    head = tokens[0]
    match head:
        case "LOAD":
            raise SyntaxErrorException("Cannot have more than 1 LOAD", lineNumber)
        case "MOVE_FORWARD":
            lineNumber
        case "TURN_LEFT":
            lineNumber
        case "TURN_RIGHT":
            lineNumber
        case "PICK_KEY":
            lineNumber
        case "OPEN_DOOR":
            lineNumber
        case "IF":
            # condition is everything after IF
            cond_tokens = tokens[1:]

            # find matching END (single-level) and optional OTHERWISE
            else_line = None
            end_line = lineNumber + 1
            while end_line <= numLines:
                raw = codingList[end_line - 1]
                line = removecomments(raw).strip()
                tks = tokeniser(line, end_line)
                if not tks:
                    end_line += 1
                    continue
                if tks[0] == "OTHERWISE" and else_line is None:
                    else_line = end_line
                    end_line += 1
                    continue
                if tks[0] == "END":
                    break
                end_line += 1
            else:
                raise SyntaxErrorException("Missing END for IF/OTHERWISE", lineNumber)

            # decide which block to run
            if eval_bool_expr(cond_tokens, lineNumber):
                start = lineNumber + 1
                stop = else_line if else_line else end_line
            elif else_line:
                start = else_line + 1
                stop = end_line
            else:
                start = end_line
                stop = end_line

            # run the chosen block
            j = start
            while j < stop:
                raw = codingList[j - 1]
                line = removecomments(raw).strip()
                tks = tokeniser(line, j)
                if not tks:
                    j += 1
                    continue
                res = parser(tks, j, numLines, codingList)
                if isinstance(res, int):
                    j = res
                else:
                    j += 1

            # continue after END
            return end_line + 1
            


        case "WHILE":
            # evaluate condition as a list of tokens (AND binds tighter than OR)
            cond_tokens = tokens[1:]

            # find the matching END for this WHILE (single-level)
            end_line = lineNumber + 1
            while end_line <= numLines:
                raw = codingList[end_line - 1]
                line = removecomments(raw).strip()
                tks = tokeniser(line, end_line)
                if tks and tks[0] == "END":
                    break
                end_line += 1
            else:
                raise SyntaxErrorException("Missing END for WHILE", lineNumber)

            # execute the body while condition holds
            while eval_bool_expr(cond_tokens, lineNumber):
                j = lineNumber + 1
                while j < end_line:
                    raw = codingList[j - 1]
                    line = removecomments(raw).strip()
                    tks = tokeniser(line, j)
                    if not tks:
                        j += 1
                        continue
                    res = parser(tks, j, numLines, codingList)
                    if isinstance(res, int):
                        j = res
                    else:
                        j += 1

            # continue after matching END
            return end_line + 1
                
        case _:
            if head[0].isalpha():
                #Process for assigning a variable
                if len(tokens) ==3 and tokens[1] == ":=":
                    variabledict[tokens[0]] = boolConversions(tokens[2], lineNumber)
                else:
                    raise SyntaxErrorException("Invalid assignment line", lineNumber)
            else:
                raise SyntaxErrorException("Invalid token", lineNumber)

            


def boolConversions(name, lineNumber):
    match name:
        case "FRONT_IS_CLEAR":
            license
        case "ON_KEY":
            license
        case "AT_DOOR":
            license
        case "AT_EXIT":
            license
        case _:
            if name in variabledict:
                return variabledict[name]
            raise SyntaxErrorException("assigning something undeclared", lineNumber)

    

















def tokeniser(line, lineNumber):
   
    if not line:
        return []
    line = line.split() #should be no whitespace anymore

    for token in line:
        if ":=" in token and token != ":=":
            raise SyntaxErrorException("Why are you slacking on separating := with spaces?????", lineNumber)
        if token in vocabulary:
            continue
        if token.isalpha():
            continue
        raise SyntaxErrorException("You are using invalid tokens", lineNumber)

    return line


def program1():
    return
def program2():
    return
def program3():
    return

    

def eval_bool_expr(tokens, lineNumber):
    n = len(tokens)
    i = 0 
    def readTerm():
        nonlocal i
        if i >= n:
            raise SyntaxErrorException("Expected boolean term", lineNumber)
        token = tokens[i]
        i += 1
        if token == "TRUE":
            return True
        if token == "FALSE":
            return False
        return boolConversions(token, lineNumber)  
    
    def parse_and():
        nonlocal i
        left = readTerm()
        while i < n and tokens[i] == "AND":
            i += 1
            right = readTerm()
            left = left and right
        return left
    def parse_or():
        nonlocal i
        left = parse_and() 
        while i < n and tokens[i] == "OR":
            i += 1
            right = parse_and()
            left = left or right
        return left
    result = parse_or()
    if i != n:
        raise SyntaxErrorException("Unexpected tokens at end of boolean expression", lineNumber)
    return result

