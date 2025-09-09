import random
from typing import Tuple
from robotspeak.maze import Maze, MazeActionError, MazeValidationError

# collection of variables
global lineNumber
maze = None
variabledict = {}
VOCABULARY = {
    "LOAD", "IF", "OTHERWISE", "WHILE", "END", "AND", "OR", "TRUE", "FALSE", 
    "MOVE_FORWARD", "TURN_LEFT", "TURN_RIGHT", "PICK_KEY", "OPEN_DOOR",
    "FRONT_IS_CLEAR", "ON_KEY", "AT_DOOR", "AT_EXIT", "1", "2", "3", ":=",
    #new variables
    "THROW_AWAY_KEY"
}
VALID_LOADING_ENVS = {"1", "2", "3"}

# exceptions
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

# utilities
def remove_comments(line: str) -> str:
    if not isinstance(line, str):
        return ''
    return line.split("@", 1)[0].strip()


def is_ascii_letters(s: str) -> bool:
    return s.isascii() and s.isalpha()

def get_random_point(width: int, length: int) -> Tuple[int, int]:
    x = random.randint(1, width)
    y = random.randint(1, length)
    return [x, y]

def get_random_maze(num_keys: int, is_program1 : bool = False) -> Maze:
    num_points = num_keys + 3 # number of keys + door + exit + robot

    width = random.randint(num_points + 1, 20)
    if is_program1:
        length = 1
    else:
        length = random.randint(num_points + 1, 20)

    locations = []
    while len(locations) != num_points:
        new_location = get_random_point(width, length)
        if new_location not in locations:
            locations.append(new_location)

    key_locations = locations[:-3]
    door_location, exit_location, robot_location = locations[-3:]

    robot_direction = random.choice(['north', 'west', 'south', 'east'])

    maze = Maze(width = width, 
                length = length, 
                key_locations = key_locations,
                door_location = door_location, 
                exit_location = exit_location, 
                robot_location = robot_location,
                robot_direction = robot_direction)

    return maze

# loading different environments
def load_program1():
    global maze
    print("--- Loading Program 1: Twisting Corridor ---")

    maze = get_random_maze(num_keys = 1, is_program1 = True)

    try:
        maze.create_initial_map()

    except MazeValidationError as e:
        print(f"Warning at line 1: {e}")

    print("Initial Maze State:")
    maze.print_map()

#function to load the second scenario
def load_program2():
    global maze
    print("--- Loading Program 2: Orthogonal Corridor ---")

    maze = get_random_maze(num_keys = 1)

    try:
        maze.create_initial_map()

    except MazeValidationError as e:
        print(f"Warning at line 1: {e}")
        
    print("Initial Maze State:")
    maze.print_map()

#function to load the third scenario
def load_program3():
    global maze
    print("--- Loading Program 3: Orthogonal Corridor with multiple keys ---")
    
    num_keys = random.randint(2, 5)
    maze = get_random_maze(num_keys = num_keys)

    try:
        maze.create_initial_map()

    except MazeValidationError as e:
        print(f"Warning at line 1: {e}")
        
    print("Initial Maze State:")
    maze.print_map()

# tokeniser
def tokeniser(line, lineNumber):
    if not line:
        return []
    line = line.split() #should be no whitespace anymore

    for token in line:
        if ":=" in token and token != ":=":
            raise SyntaxErrorException("Why are you slacking on separating := with spaces?????", lineNumber)
        if token in VOCABULARY:
            continue
        if is_ascii_letters(token): #variable name must follow the spec
            continue
        raise SyntaxErrorException("You are using invalid tokens", lineNumber)

    return line


def parser(tokens, lineNumber, numLines, codingList, num_executed_lines = 2):
    #case it is the first line
    if num_executed_lines ==  1:
        if tokens[0] != "LOAD":
            raise SyntaxErrorException("LOAD is not the first token.", lineNumber)
        if len(tokens) == 1:
            raise RuntimeErrorException("You have to specify which program to run", lineNumber)
        if tokens[1] not in VALID_LOADING_ENVS or len(tokens) != 2:
            raise RuntimeErrorException("You've gotta load either program 1, 2 or 3", lineNumber)

        match tokens[1]:
            case "1":
                load_program1()
            case "2":
                load_program2()
            case "3":
                load_program3()
        return
        
    if lineNumber == numLines: #final line
        if len(tokens) == 1 and tokens[0] == "END":
                return "HALT" #end the program
        else:
            raise SyntaxErrorException("END is not the only token on the last line", lineNumber)
    
    # normal lines
    head = tokens[0]
    match head:
        case "LOAD":
            raise SyntaxErrorException("Cannot have more than 1 LOAD", lineNumber)
        case "MOVE_FORWARD":
            try:
                maze.move_forward()
                print(f"\nAction: MOVE_FORWARD {maze.get_status()}")
                maze.print_map()
            except MazeActionError as e:
                print(f"Warning at line {lineNumber}: {e}")
        case "TURN_LEFT":
            maze.turn_left()
            print(f"\nAction: TURN_LEFT {maze.get_status()}")
            maze.print_map()
        case "TURN_RIGHT":
            maze.turn_right()
            print(f"\nAction: TURN_RIGHT {maze.get_status()}")
            maze.print_map()
        case "PICK_KEY":
            try:
                maze.pick_key()
                print(f"\nAction: PICK_KEY {maze.get_status()}")
            except MazeActionError as e:
                print(f"Warning at line {lineNumber}: {e}")
        case "THROW_AWAY_KEY":
            maze.throw_away_key()
            print(f"\nAction: THROW_AWAY_KEY {maze.get_status()}")
        case "OPEN_DOOR":
            try:
                maze.open_door()
                print(f"\nAction: OPEN_DOOR")
                if maze.is_maze_solved():
                    print("\n*** MAZE SOLVED! ***")
                    return "HALT"
            except MazeActionError as e:
                print(f"Warning at line {lineNumber}: {e}")
        case "IF":
            cond_tokens = tokens[1:] #boolean expression

            else_line = None
            end_line = lineNumber + 1
            depth = 0

            while end_line <= numLines:
                raw = codingList[end_line - 1]
                ln = remove_comments(raw)
                tks = tokeniser(ln, end_line)
                if not tks:
                    end_line += 1
                    continue
                hd = tks[0]
                if hd in ("IF", "WHILE"):
                    depth += 1
                elif hd == "END":
                    if depth == 0:
                        break
                    depth -= 1
                elif hd == "OTHERWISE" and depth == 0:
                    if len(tks) != 1:
                        raise SyntaxErrorException("OTHERWISE must be the only token on its line", end_line)
                    else_line = end_line
                end_line += 1
            else:
                raise SyntaxErrorException("Missing END for IF/OTHERWISE", lineNumber)

            if eval_bool_expr(cond_tokens, lineNumber):
                start, stop = lineNumber + 1, (else_line if else_line else end_line)
            elif else_line:
                start, stop = else_line + 1, end_line
            else:
                start = stop = end_line  # skip

            j = start
            while j < stop:
                raw = codingList[j - 1]
                ln = remove_comments(raw)
                tks = tokeniser(ln, j)
                if not tks:
                    j += 1
                    continue
                res = parser(tks, j, numLines, codingList)
                if res == "HALT":
                    return "HALT"
                if isinstance(res, int):
                    j = res
                else:
                    j += 1

            return end_line + 1
            


        case "WHILE":
            cond_tokens = tokens[1:]

            end_line = lineNumber + 1
            depth = 0
            while end_line <= numLines:
                raw = codingList[end_line - 1]
                ln = remove_comments(raw)
                tks = tokeniser(ln, end_line)
                if not tks:
                    end_line += 1
                    continue
                hd = tks[0]
                if hd in ("IF", "WHILE"):
                    depth += 1
                elif hd == "END":
                    if depth == 0:
                        break
                    depth -= 1
                end_line += 1
            else:
                raise SyntaxErrorException("Missing END for WHILE", lineNumber)

            while eval_bool_expr(cond_tokens, lineNumber): #exact same as if but replace if with while
                j = lineNumber + 1
                while j < end_line:
                    raw = codingList[j - 1]
                    ln = remove_comments(raw)
                    tks = tokeniser(ln, j)
                    if not tks:
                        j += 1
                        continue
                    res = parser(tks, j, numLines, codingList)
                    if res == "HALT":
                        return "HALT"
                    if isinstance(res, int):
                        j = res
                    else:
                        j += 1

            return end_line + 1
                
        case _:
            if is_ascii_letters(head):
                #Process for assigning a variable
                if len(tokens) >=3 and tokens[1] == ":=":
                    value = eval_bool_expr(tokens[2:], lineNumber)
                    variabledict[tokens[0]] = value
                    return
                else:
                    raise SyntaxErrorException("Invalid assignment line", lineNumber)
            else:
                raise SyntaxErrorException("Invalid token", lineNumber)

            


def boolConversions(name, lineNumber):
    global maze
    if maze is None:
        raise RuntimeErrorException("Maze has not been loaded yet.", lineNumber)
    
    match name:
        case "FRONT_IS_CLEAR":
            return maze.is_front_clear()
        case "ON_KEY":
            return maze.on_key()
        case "AT_DOOR":
            return maze.at_door()
        case "AT_EXIT":
            return maze.at_exit()
        case "TRUE":
            return True
        case "FALSE":
            return False
        case _:
            if name in variabledict:
                return variabledict[name]
            raise RuntimeErrorException("assigning something undeclared", lineNumber)

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

# compiler
def compiler(robotspeak_program):
    # breaking the program into lines and removing comments
    code_lines = robotspeak_program.strip().split('\n')
    code_lines = [remove_comments(code_line) for code_line in code_lines]

    lineNumber = 0
    num_executed_lines = 0
    numLines = len(code_lines)

    while lineNumber < len(code_lines):
        line = code_lines[lineNumber]
        lineNumber += 1
        tokens = tokeniser(line, lineNumber)
        if not tokens:
            continue
        else:
            num_executed_lines += 1

        #parsing
        result = parser(tokens, lineNumber, numLines, code_lines, num_executed_lines)
        if result == "HALT":
            break

        #if returned a number to jump to
        if isinstance(result, int):
            lineNumber = result - 1
            continue
    
if __name__ == "__main__":
    robotspeak_program = """
    @loading the map
    LOAD 1
    TURN_RIGHT
    MOVE_FORWARD
    END
    """
    print("Starting RobotSpeak Interpreter...")
    try:
        compiler(robotspeak_program)
        print("\nProgram finished.")
    except (SyntaxErrorException, RuntimeErrorException) as e:
        print(f"\n--- ERROR ---\n{e}")