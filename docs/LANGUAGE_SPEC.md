# Robotspeak: Language specification

Robotspeak is a programming language for controlling the actions and movements of a small robot, `Runner`, within a virtual 2D environment. The language defines only a small set of instructions and sensors, reflecting deliberate constraints intending to showcase programming design under limitations.

## Lexical Elements

- **Character set:** ASCII
- **Whitespace:** The ASCII space, tab or new line characters; separates tokens, otherwise ignored
- **Comments:** The ASCII at character; start with `@` and continues until the end of the line
- **Identifiers:** The ASCII letters only. Identifiers are variables of Boolean type. All variables are implicitly declared on first assignment

## Keywords and Tokens

- **Actions:** `MOVE_FORWARD`, `TURN_LEFT`, `TURN_RIGHT`, `PICK_KEY`, `OPEN_DOOR`, `THROW_AWAY_KEY`
- **Control and Operators:** `LOAD`, `IF`, `OTHERWISE`, `WHILE`, `END`, `AND`, `OR`
- **Literals:** `TRUE`, `FALSE`
- **Sensors:** `FRONT_IS_CLEAR`, `ON_KEY`, `AT_DOOR`, `AT_EXIT`
- **vocabulary count:** 20


## Grammar (EBNF)

```ebnf
program     ::= "LOAD" env_id { stmt } "END" ;

stmt        ::= action_stmt
              | if_stmt
              | while_stmt
              | assign_stmt ;

action_stmt ::= "MOVE_FORWARD" | "TURN_LEFT" | "TURN_RIGHT"
              | "PICK_KEY" | "OPEN_DOOR" ;

if_stmt     ::= "IF" expr { stmt }
                [ "OTHERWISE" { stmt } ]
                "END" ;

while_stmt  ::= "WHILE" expr { stmt } "END" ;

assign_stmt ::= identifier ":=" expr ;

expr        ::= term { "OR" term } ;
term        ::= factor { "AND" factor } ;
factor      ::= literal | sensor | identifier ;

literal     ::= "TRUE" | "FALSE" ;
sensor      ::= "FRONT_IS_CLEAR" | "ON_KEY" | "AT_DOOR" | "AT_EXIT" ;
env_id      ::= "1" | "2" | "3" ;
```

## Semantics

### Program structure

Programs **MUST** begin with a `LOAD` statement specifying the environment (1, 2 or 3) and **MUST** terminate with `END`. Statements are executed sequentially in the order they appear top to bottom.

### Actions

- **`MOVE_FORWARD`:** Advances the runner by one tile in the current facing direction if `FRONT_IS_CLEAR` is true, otherwise raises MazeActionError
- **`TURN_LEFT`:** Rotates the Runner's facing direction 90° counterclockwise; always succeeds
- **`TURN_RIGHT`:** Rotates the Runner's facing direction 90° clockwise; always succeeds
- **`PICK_KEY`:** Picks up a key if `ON_KEY` is true, otherwise raises MazeActionError
- **`THROW_AWAY_KEY`:** Discards the key currently held by the runner at the runner's location. If no key is held, a MazeActionError is raised
- **`OPEN_DOOR`:** Outputs "MAZE SOLVED!" to the terminal and terminates the program if `AT_DOOR` is true and a correct key has been previously picked up, or `AT_EXIT` is true, otherwise raises MazeActionError. If the program reaches the final `END` without `OPEN_DOOR` ever successfully executing, the program silently terminates

### Sensors

- **`FRONT_IS_CLEAR`:** Assigned true if the next tile in the Runner's facing direction is not a wall, otherwise assigned false
- **`ON_KEY`:** Assigned true if the tile the Runner is on has a key, otherwise assigned false
- **`AT_DOOR`:** Assigned true if the Runner is on a door tile, otherwise assigned false
- **`AT_EXIT`:** Assigned true if the Runner is on an exit tile, otherwise assigned false

### Control

- **`IF…OTHERWISE…END`:** Executes the first block if the condition is true, otherwise executes the `OTHERWISE` block if present
- **`WHILE…END`:** Executes the code block if the condition is true, and perpetually does so until the condition is false after the end of an executed cycle
- **Operator precedence:** `AND` binds tighter than `OR`. Both operators are left-associative.

## Error Model

### Syntax errors

Detected during parsing. A statement with a syntax error **MUST NOT** be executed. Examples: Unknown or invalid token, missing or unmatched `END`, `LOAD` not appearing as the first statement or appearing more than once, malformed expressions.

A syntax error produces a diagnostic message of the form:
```
What ARE YOU DOING?!?!?!? SyntaxError: <description> at line <n> !!!!!
```

### Runtime errors

Detected during runtime. Examples: referencing a variable before it is assigned.

A runtime error produces a diagnostic message of the form:
```
YOOOOOOOO!!!!! What are you doing at line <n> with this RuntimeError!!!?!?!?! <description>
```

### MazeActionErrors

Detected when the runner attempts to perform an invalid action within the maze environment. Examples: moving forward into a wall, picking up a key when none is present.

A MazeActionError produces a diagnostic message of the form:
```
Warning at line <n>: <description>
```

## Example program
```robotspeak
LOAD 1
WHILE FRONT_IS_CLEAR
    MOVE_FORWARD
END
OPEN_DOOR
END
```
### Token counts (line by line)
- `LOAD 1` → [LOAD, 1] (2 tokens)  
- `WHILE FRONT_IS_CLEAR` → [WHILE, FRONT_IS_CLEAR] (2 tokens)  
- `MOVE_FORWARD` → [MOVE_FORWARD] (1 token)  
- `END` → [END] (1 token)  
- `OPEN_DOOR` → [OPEN_DOOR] (1 token)  
- `END` → [END] (1 token)  

### Explanation
This program demonstrates how a runner can escape directly through the exit:

1. The program begins with `LOAD 1`, which initializes environment 1.  
2. The `WHILE` loop executes as long as the sensor `FRONT_IS_CLEAR` is true. Inside the loop, the runner executes `MOVE_FORWARD`, advancing one tile at a time.  
3. Once the runner can no longer move forward (blocked by a wall), the loop ends.  
4. `OPEN_DOOR` is then executed. If the runner happens to be standing on the exit tile at this point, the maze terminates successfully with the message **“MAZE SOLVED!”**.  
5. The program terminates with the last `END`. If the runner is not at the exit, the program simply ends silently.