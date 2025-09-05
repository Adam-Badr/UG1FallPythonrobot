# Robotspeak: Language specification

Robotspeak is a programming language for controlling the actions and movements of a small robot, `Runner`, within a virtual 2D environment. The language defines only a small set of instructions and sensors, reflecting deliberate constraints intending to showcase programming design under limitations.

## Lexical Elements

- **Character set:** ASCII
- **Whitespace:** The ASCII space, tab or new line characters; separates tokens, otherwise ignored
- **Comments:** The ASCII at character; start with `@` and continues until the end of the line
- **Identifiers:** The ASCII letters only. Identifiers are variables of Boolean type. All variables are implicitly declared on first assignment

## Keywords and Tokens

- **Actions:** `MOVE_FORWARD`, `TURN_LEFT`, `TURN_RIGHT`, `PICK_KEY`, `OPEN_DOOR`
- **Control and Operators:** `LOAD`, `IF`, `OTHERWISE`, `WHILE`, `END`, `AND`, `OR`
- **Literals:** `TRUE`, `FALSE`
- **Sensors:** `FRONT_IS_CLEAR`, `ON_KEY`, `AT_DOOR`, `AT_EXIT`

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

- **`MOVE_FORWARD`:** Advances the runner by one tile in the current facing direction if `FRONT_IS_CLEAR` is true, otherwise no effect
- **`TURN_LEFT`:** Rotates the Runner's facing direction 90° counterclockwise; always succeeds
- **`TURN_RIGHT`:** Rotates the Runner's facing direction 90° clockwise; always succeeds
- **`PICK_KEY`:** Picks up a key if `ON_KEY` is true, otherwise no effect
- **`OPEN_DOOR`:** Outputs "You escaped!" to the terminal and terminates the program if `AT_DOOR` is true and a correct key has been previously picked up, or `AT_EXIT` is true, otherwise no effect. If the program reaches the final `END` without `OPEN_DOOR` ever successfully executing, the program silently terminates

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