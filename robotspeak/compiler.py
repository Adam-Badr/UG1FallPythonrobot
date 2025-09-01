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
    for line in codeList: #For every line, line-by-line
        lineNumber += 1
        line = removecomments(line).strip()#remove all comments from the line to ignore and protect against cases where line = "      @comment"
        tokens = tokeniser(line, lineNumber)
        ##################################################################################
        #parser time
        


















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






    
    

