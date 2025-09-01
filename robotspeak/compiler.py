#collection of variables
global seenload
seenload = False
global worldArray






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
    while lineNumber<len(codeList): #For every line, line-by-line
        line = codeList[lineNumber]
        lineNumber += 1
        line = removecomments(line).strip()#remove all comments from the line to ignore and protect against cases where line = "      @comment"
        tokens = tokeniser(line, lineNumber)
        ##################################################################################
        #parser time




def parser(tokens, lineNumber):
    #case it is the first line
    if lineNumber ==1 and tokens[0] != "LOAD":
        raise SyntaxErrorException("LOAD is not the first token.", lineNumber)
    if lineNumber ==1 and len(tokens) == 1:
        raise RuntimeErrorException("You have to specify which program to run", lineNumber)
    if lineNumber ==1 and tokens[0] == "LOAD" and tokens[1] not in validload:
        raise RuntimeErrorException("You've gotta load either program 1, 2 or 3", lineNumber)
    if lineNumber ==1 and tokens[0] == "LOAD" and tokens[1] in validload and len(tokens) == 2:
        #valid load has taken place
        match tokens[1]:
            case "1":
                program1()
            case "2":
                program2()
            case "3":
                program3()
        seenload = True
        return
    if seenload and "LOAD" in tokens:
        #LOAD has appeared a second time
        raise SyntaxErrorException("LOAD can only be present once", lineNumber)
    


    
    

















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

    
    

