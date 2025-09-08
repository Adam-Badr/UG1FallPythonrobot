# robotspeak: The Vault Runner Interpreter

**Project for Group Assignment at AI1030 - Python Programming, MBZUAI**

**You can find our [reflection](files/reflection.md) about designing the language and [walkthrough video](https://youtu.be/XfELJU1mRMg)**.

This repository contains the source code for a custom programming language, **robotspeak**, and its interpreter, designed to solve the "Vault Runner" challenge. The project involves navigating a robot through a 2D maze to find a key, open a door, or reach a direct exit.

The goal of this assignment was to design and implement a simple, constrained programming language from scratch. The language, robotspeak, provides a small set of commands and sensors for a robot to interact with its environment.

## Setup and Installation

To run the robotspeak interpreter, you need Python 3.6+ and `pip`.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Adam-Badr/UG1FallPythonrobot.git
    cd UG1FallPythonrobot/
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the project in editable mode:**
    This command installs any dependencies and makes the `robotspeak` command available in your terminal.
    ```bash
    pip install -e .
    ```

## How to Use

You can write robotspeak code in any plain text file (e.g., `program.txt`) and execute it using the `robotspeak` command.

1.  **Create a program file.** For example, create `solve_maze.txt` with the following code to implement a simple "left-hand wall following" algorithm:

    ```robotspeak
    @ Load the twisting corridor environment
    LOAD 1

    @ Main loop to keep the robot moving
    WHILE TRUE
        @ If we find the key, pick it up
        IF ON_KEY
            PICK_KEY
        END

        @ If we are at the door with the key, open it
        IF AT_DOOR
            OPEN_DOOR
        END

        @ If the left side is clear, turn left and move
        TURN_LEFT
        IF FRONT_IS_CLEAR
            MOVE_FORWARD
        OTHERWISE
            @ Left is blocked, so turn back right and try forward
            TURN_RIGHT
            IF FRONT_IS_CLEAR
                MOVE_FORWARD
            OTHERWISE
                @ Front is also blocked, must be a corner, turn right again
                TURN_RIGHT
            END
        END
    END
    ```

2.  **Run the interpreter:**
    ```bash
    robotspeak solve_maze.txt
    ```

The interpreter will print the robot's actions and the state of the maze at each step.

## Language Documentation

For a detailed guide to the robotspeak language syntax, keywords, control structures, and semantics, please see the **[Language Specification](docs/LANGUAGE_SPEC.md)**.

## Team Members
- Adam Badr
- Abror Shopulatov
- Yelarys Yertaiuly