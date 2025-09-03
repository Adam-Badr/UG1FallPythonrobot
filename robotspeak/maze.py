from typing import Tuple
from itertools import combinations

KEY_SYMBOL = "K"
DOOR_SYMBOL = "D"
EXIT_SYMBOL = "E"
WALL_SYMBOL = "*"
EMPTY_SYMBOL = "."
ROBOT_SYMBOL = "R"

class MazeValidationError(Exception):
    """Custom exception for maze validation errors"""
    pass

class MazeActionError(Exception):
    """Custom exception for maze validation errors"""
    pass

class Maze:
    """
    A maze environment with a robot that can navigate, collect keys, and reach exits.
    
    Uses 1-based coordinate system where (1,1) is the top-left navigable cell.
    Matrix internally uses 0-based indexing with wall borders.
    """
    def __init__(self, 
                 width: int, 
                 length: int, 
                 key_location: Tuple[int, int], 
                 door_location: Tuple[int, int], 
                 exit_location: Tuple[int, int], 
                 robot_location: Tuple[int, int],
                 robot_direction: str = 'north'):
        """
        Initialize a new maze with specified dimensions and object locations.
        
        Args:
            width: Maze width (number of navigable columns)
            length: Maze height (number of navigable rows)  
            key_location: Key position as (x, y) in 1-based coordinates
            door_location: Door position as (x, y) in 1-based coordinates
            exit_location: Exit position as (x, y) in 1-based coordinates
            robot_location: Robot starting position as (x, y) in 1-based coordinates
            robot_direction: Robot starting direction ('north', 'south', 'east', 'west')
        """
        self.width = width
        self.length = length
        self.key_location = key_location
        self.door_location = door_location
        self.exit_location = exit_location
        self.robot_location = robot_location
        self.robot_direction = robot_direction
        self.robot_direction_coordinate = []

        self.map_matrix = []

        self.key_symbol = KEY_SYMBOL
        self.door_symbol = DOOR_SYMBOL
        self.exit_symbol = EXIT_SYMBOL
        self.wall_symbol = WALL_SYMBOL
        self.empty_symbol = EMPTY_SYMBOL
        self.robot_symbol = ROBOT_SYMBOL
        
        self._all_directions = ['north', 'west', 'south', 'east']
        self._all_direction_str = ['▲', '◄', '▼', '►']
        self._all_direction_coordinates = [[0, -1], [-1, 0], [0, 1], [1, 0]]

        self.has_key = False
        self.has_opened_door = False
    
    # getters
    def get_width(self) -> int:
        """Return the maze width."""
        return self.width

    def get_length(self) -> int:
        """Return the maze length."""
        return self.length

    def get_key_location(self) -> Tuple[int, int]:
        """Return the key location as (x, y)"""
        return self.key_location

    def get_door_location(self) -> Tuple[int, int]:
        """Return the door location as (x, y)"""
        return self.door_location
    
    def get_exit_location(self) -> Tuple[int, int]:
        """Return the exit location as (x, y)"""
        return self.exit_location
    
    def get_robot_location(self) -> Tuple[int, int]:
        """Return the robot location as (x, y)"""
        return self.robot_location
    
    def get_robot_direction(self) -> Tuple[int, int]:
        """Return the current robot direction as a string."""
        return self.robot_direction
    
    def get_map_matrix(self) -> list:
        """Return the internal map matrix including wall borders."""
        return self.map_matrix
    
    # setters
    def set_location(self, location: list, symbol: str) -> None:
        """
        Place a symbol at the specified location on the map.
        
        Args:
            location: Position as [x, y] in 1-based coordinates
            symbol: Character symbol to place
            
        Note: If location already has content, symbol is appended.
        """
        x_coordinate, y_coordinate = location

        if self.map_matrix[y_coordinate][x_coordinate] == self.empty_symbol:
            self.map_matrix[y_coordinate][x_coordinate] = symbol
        else:
            self.map_matrix[y_coordinate][x_coordinate] += symbol
    
    def set_direction_coordinate(self) -> None:
        """Update robot_direction_coordinate based on current robot_direction."""
        direction_idx = self._all_directions.index(self.robot_direction)
        self.robot_direction_coordinate = self._all_direction_coordinates[direction_idx]

    # validators
    def _validate_unique_symbols(self) -> None:
        """
        Validate that all object symbols are unique.
        
        Raises:
            MazeValidationError: If any two objects share the same location
        """
        symbols = [
            ["key", self.key_symbol],
            ["door", self.door_symbol],
            ["exit", self.exit_symbol],
            ["wall", self.wall_symbol],
            ["robot", self.robot_symbol],
            ["empty space", self.empty_symbol]
        ]

        combos = list(combinations(symbols, 2))

        for combo in combos:
            symbol1, symbol2 = combo
            # print(combo)
            if symbol1[1] == symbol2[1]:
                raise MazeValidationError(f"You are using the same symbol ({symbol1[1]}) for both {symbol1[0].upper()} and {symbol2[0].upper()}.")
            
    def _validate_dimensions(self, width: int, length: int) -> None:
        """Validate maze dimensions"""
        if not isinstance(width, int) or not isinstance(length, int):
            raise MazeValidationError("Width and length must be integers")
        if width < 1 or length < 1:
            raise MazeValidationError("Width and length must be at least 1")
    
    def _validate_location(self, location: Tuple[int, int], name: str) -> None:
        """Validate a single location"""
        if not isinstance(location, list) or len(location) != 2:
            raise MazeValidationError(f"{name} location must be a list of 2 integers")
        
        x, y = location
        if not isinstance(x, int) or not isinstance(y, int):
            raise MazeValidationError(f"{name} coordinates must be integers")
        
        # 1-based coordinate system validation
        if not (1 <= x <= self.width):
            raise MazeValidationError(f"{name} x-coordinate {x} must be between 1 and {self.width}")
        
        if not (1 <= y <= self.length):
            raise MazeValidationError(f"{name} y-coordinate {y} must be between 1 and {self.length}")
    
    def _validate_direction(self, direction: str) -> None:
        """Validate robot direction"""
        if not isinstance(direction, str):
            raise MazeValidationError("Direction must be a string")
        
        if direction.lower() not in ['north', 'west', 'south', 'east']:
            raise MazeValidationError(f"Direction must be one of: north, west, south, east. Got: {direction}")
    
    def validate_intial_inputs(self):
        """
        Validate all initial maze parameters.
        
        Raises:
            MazeValidationError: If any parameter is invalid
        """
        self._validate_unique_symbols()

        self._validate_dimensions(self.width, self.length)

        self._validate_location(self.key_location, "key")
        self._validate_location(self.door_location, "door")
        self._validate_location(self.exit_location, "exit")
        self._validate_location(self.robot_location, "robot")

        self._validate_direction(self.robot_direction)
    
    # initial setup
    def create_initial_map(self) -> None:
        """
        Create the maze map matrix and place all objects.
        
        Validates inputs, creates bordered matrix with walls, and places
        key, door, exit, and robot at their specified locations.
        """
        self.validate_intial_inputs()
        
        self.map_matrix = []

        self.map_matrix.append([self.wall_symbol] * (self.width + 2))
        for _ in range(self.length):
            self.map_matrix.append([self.wall_symbol] + [self.empty_symbol] * self.width + [self.wall_symbol])
        self.map_matrix.append([self.wall_symbol] * (self.width + 2))

        self.set_location(self.key_location, self.key_symbol)
        self.set_location(self.door_location, self.door_symbol)
        self.set_location(self.exit_location, self.exit_symbol)
        self.set_location(self.robot_location, self.robot_symbol)

        self.set_direction_coordinate()
    
    # sensors
    def is_front_clear(self) -> bool:
        """
        Check if the space directly in front of the robot is clear.
        
        Returns:
            True if front space is navigable (not a wall), False otherwise
        """
        front_x = self.robot_location[0] + self.robot_direction_coordinate[0]
        front_y = self.robot_location[1] + self.robot_direction_coordinate[1]

        if self.map_matrix[front_y][front_x] == self.wall_symbol:
            return False
        
        return True

    def on_key(self) -> bool:
        """
        Check if the robot is currently on the key location.
        
        Returns:
            True if robot's current position contains the key symbol
        """
        return self.key_symbol in self.map_matrix[self.robot_location[1]][self.robot_location[0]]

    def at_door(self) -> bool:
        """
        Check if the robot is currently at the door location.
        
        Returns:
            True if robot's current position contains the door symbol
        """
        return self.door_symbol in self.map_matrix[self.robot_location[1]][self.robot_location[0]]

    def at_exit(self) -> bool:
        """
        Check if the robot is currently at the exit location.
        
        Returns:
            True if robot's current position contains the exit symbol
        """
        return self.exit_symbol in self.map_matrix[self.robot_location[1]][self.robot_location[0]]
    
    # actions
    def move_forward(self) -> None:
        """
        Move the robot one step forward in its current direction.
        
        Does nothing if the front is blocked. Updates robot position
        and map matrix accordingly.
        """
        if not self.is_front_clear():
            raise MazeActionError("Front is not clear, not moving forward")
        
        # removing previous robot
        robot_place = self.map_matrix[self.robot_location[1]][self.robot_location[0]]
        if robot_place == self.robot_symbol:
            self.map_matrix[self.robot_location[1]][self.robot_location[0]] = self.empty_symbol
        else:
            self.map_matrix[self.robot_location[1]][self.robot_location[0]] = robot_place.replace(self.robot_symbol, "")
        
        # moving the robot
        robot_x_new = self.robot_location[0] + self.robot_direction_coordinate[0]
        robot_y_new = self.robot_location[1] + self.robot_direction_coordinate[1]
        self.robot_location = [robot_x_new, robot_y_new]
        self.set_location(self.robot_location, self.robot_symbol)
    
    def turn_right(self) -> None:
        """Turn the robot 90 degrees clockwise (right)."""
        current_idx = self._all_direction_coordinates.index(self.robot_direction_coordinate)

        self.robot_direction = self._all_directions[current_idx - 1]
        self.robot_direction_coordinate = self._all_direction_coordinates[current_idx - 1]

    def turn_left(self) -> None:
        """Turn the robot 90 degrees counter-clockwise (left)."""
        current_idx = self._all_direction_coordinates.index(self.robot_direction_coordinate)

        self.robot_direction = self._all_directions[(current_idx + 1) % 4]
        self.robot_direction_coordinate = self._all_direction_coordinates[(current_idx + 1) % 4]

    def pick_key(self) -> None:
        """
        Pick up the key if the robot is on the key location.
        
        Sets has_key to True if successful. Does nothing if not on key.
        """
        if not self.on_key():
            raise MazeActionError("Not on the key, not picking up")
        
        self.has_key = True
    
    def open_door(self) -> None:
        """
        Open the key if the robot is at the door location and has a key.
        
        Sets has_opened_door to True if successful. Does nothing otherwise.
        """
        if not self.at_door():
            raise MazeActionError("Not on the door, not opening")
        
        if not self.has_key:
            raise MazeActionError("No key found, not opening")
        
        self.has_opened_door = True

    # utilities
    def print_map(self, delimiter: str = ' ') -> None:
        """
        Print the current map matrix to console.
        
        Args:
            delimiter: Character to separate matrix elements (default: space)
        """
        display_matrix = [row[:] for row in self.map_matrix]
    
        # Replace robot symbol with direction arrow
        robot_x, robot_y = self.robot_location
        current_cell = display_matrix[robot_y][robot_x]
        
        # Get direction arrow
        direction_idx = self._all_directions.index(self.robot_direction)
        direction_arrow = self._all_direction_str[direction_idx]
        
        # Replace robot symbol with direction arrow
        if current_cell == self.robot_symbol:
            display_matrix[robot_y][robot_x] = direction_arrow
        else:
            # If robot is on another object, replace R with arrow
            display_matrix[robot_y][robot_x] = current_cell.replace(self.robot_symbol, direction_arrow)
        
        print('\n'.join([delimiter.join(map_row) for map_row in display_matrix]))

    def is_maze_solved(self) -> bool:
        """
        Check if the maze is solved.
        
        Returns:
            True if robot is at exit, or at door with key collected
        """
        if self.at_exit() or self.has_opened_door:
            return True
        
        return False

if __name__ == "__main__":
    print("Creating initial map with 6x5 maze")
    maze = Maze(width = 6, 
                length = 5, 
                key_location = [4, 4], 
                door_location = [6, 5], 
                exit_location = [4, 1], 
                robot_location = [2, 2])
    maze.create_initial_map()
    maze.print_map()

    print()
    print("Moving forward:")
    maze.move_forward()
    maze.print_map()

    print()
    print("Turning left:")
    maze.turn_left()
    maze.print_map()

    print()
    print("Moving forward:")
    maze.move_forward()
    maze.print_map()

    print()
    print("Moving forward:")
    maze.move_forward()
    maze.print_map()
