#!/usr/bin/env python3
"""
Program 3 Test Runner: Multi-Key Rectangular Room Navigation
Creates and tests multiple room scenarios with multiple keys, one door, one exit.
Only one key opens the door. Start position and facing direction are unknown.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robotspeak.maze import Maze
from robotspeak.compiler import compiler

class MultiKeyRoomMaze(Maze):
    """Custom maze class supporting multiple keys where only one is correct"""
    
    def __init__(self, room_map, correct_key_location, robot_direction='north'):
        """
        Create a rectangular room from a 2D map where:
        * = wall, . = floor, K = key, D = door, E = exit, R = robot
        Multiple K's may exist; only the key at correct_key_location opens the door.
        Coordinates are 1-based including the outer wall border in the map matrix.
        """

        self.room_map = room_map
        self.height = len(room_map)
        self.width = len(room_map[0])

        # Derive positions from the map (will finalize after create_initial_map)
        self._derived_robot_location = None
        self._derived_door_location = None
        self._derived_exit_location = None
        self._derived_key_locations = []

        # Store correct key location (1-based coordinates within the bordered map)
        self.correct_key_location = correct_key_location

        # Temporary placeholders; will be overwritten in create_initial_map
        super().__init__(
            width=self.width, 
            length=self.height,
            key_locations=[correct_key_location],
            door_location=[1, 1], 
            exit_location=[1, 1],
            robot_location=[1, 1],
            robot_direction=robot_direction
        )

        # Additional state
        self.has_correct_key = False

    def create_initial_map(self):
        """Create the room map from the provided pattern and derive object locations"""
        # Build map directly from provided strings
        self.map_matrix = [list(row) for row in self.room_map]

        # Derive coordinates from the map
        self._derived_robot_location = None
        self._derived_key_locations = []
        self._derived_door_location = None
        self._derived_exit_location = None

        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[y])):
                cell = self.map_matrix[y][x]
                if 'R' in cell:
                    self._derived_robot_location = [x, y]
                if 'K' in cell:
                    self._derived_key_locations.append([x, y])
                if 'D' in cell:
                    self._derived_door_location = [x, y]
                if 'E' in cell:
                    self._derived_exit_location = [x, y]

        # Apply derived positions to Maze base fields
        if self._derived_robot_location is not None:
            self.robot_location = self._derived_robot_location
        if self._derived_door_location is not None:
            self.door_location = self._derived_door_location
        if self._derived_exit_location is not None:
            self.exit_location = self._derived_exit_location

        # Ensure direction vectors reflect current direction
        self.set_direction_coordinate()

    # Sensors
    def on_key(self) -> bool:
        return 'K' in self.map_matrix[self.robot_location[1]][self.robot_location[0]]

    # Actions
    def pick_key(self) -> None:
        if not self.on_key():
            from robotspeak.maze import MazeActionError
            raise MazeActionError("Not on a key, cannot pick")
        self.has_key = True
        # Determine if this is the correct key
        if self.robot_location == self.correct_key_location:
            self.has_correct_key = True

    def open_door(self) -> None:
        from robotspeak.maze import MazeActionError
        # Exit hatch always wins
        if self.at_exit():
            self.has_opened_door = True
            return
        if not self.at_door():
            raise MazeActionError("Not at the door, cannot open")
        if not self.has_key:
            raise MazeActionError("No key, cannot open door")
        if not self.has_correct_key:
            raise MazeActionError("Wrong key, door does not open")
        self.has_opened_door = True


def create_test_rooms():
    """
    Create 3 rectangular room scenarios for Program 3:
    - Multiple keys (K) present, only one correct key opens the door
    - Robot starts at unknown tile and orientation
    - No obstacles, orthogonal room, 4-wall border
    """

    test_cases = []

    # Test Case 1: Small room with 2 keys
    print("Creating Test Case 1: Small Multi-Key Room")
    room1_map = [
        "*****",
        "*K.E*",
        "*RDK*",
        "*****"
    ]
    # Keys at (1,1) and (3,2) in 0-based map indices; choose the left key
    correct_key_loc_1 = [1, 1]
    test1 = MultiKeyRoomMaze(
        room_map=room1_map,
        correct_key_location=correct_key_loc_1,
        robot_direction='west'  # Unknown orientation simulated
    )
    test_cases.append(("Small Multi-Key Room", test1))

    # Test Case 2: Medium room with 3 keys; exit reachable earlier path
    print("Creating Test Case 2: Medium Multi-Key Room")
    room2_map = [
        "********",
        "*..E...*",
        "*..K...*",
        "*R.....*",
        "*..K..D*",
        "*...K..*",
        "********"
    ]
    # Keys at (3,2), (3,4), (4,5); choose the bottom key (4,5)
    correct_key_loc_2 = [4, 5]
    test2 = MultiKeyRoomMaze(
        room_map=room2_map,
        correct_key_location=correct_key_loc_2,
        robot_direction='south'
    )
    test_cases.append(("Medium Multi-Key Room", test2))

    # Test Case 3: Large room with 4 keys; door requires top-left key
    print("Creating Test Case 3: Large Multi-Key Room")
    room3_map = [
        "**********",
        "*K....E..*",
        "*........*",
        "*....K...*",
        "*........*",
        "*..K...D.*",
        "*........*",
        "*R...K...*",
        "**********"
    ]
    # Choose the top-left key at (1,1) in 0-based map indices
    correct_key_loc_3 = [1, 1]
    test3 = MultiKeyRoomMaze(
        room_map=room3_map,
        correct_key_location=correct_key_loc_3,
        robot_direction='east'
    )
    test_cases.append(("Large Multi-Key Room", test3))

    return test_cases


def display_room_map(maze, test_name):
    """Display the room map with description"""
    print(f"\n🏠 {test_name}")
    print("=" * 50)
    print("Legend: R=Robot, K=Key, D=Door, E=Exit, *=Wall, .=Floor")
    print(f"Robot starts at {maze.robot_location} facing {maze.robot_direction}")
    print("Environment: Rectangular room, no obstacles")
    maze.print_map()
    print()


def run_program3_on_room(test_name, maze):
    """Run Program 3 on a specific room test case"""

    print(f"🚀 RUNNING PROGRAM 3 ON: {test_name}")
    print("=" * 60)

    # Initialize the maze
    try:
        maze.create_initial_map()
        display_room_map(maze, test_name)
    except Exception as e:
        print(f"❌ Error creating maze: {e}")
        return False

    # Load Program 3 code
    try:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        program3_path = os.path.join(repo_root, 'algorithms', 'program3.txt')
        with open(program3_path, 'r') as f:
            program3_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: program3.txt not found at {program3_path}")
        return False

    print("📋 Program 3 Strategy:")
    print("• Normalize from unknown start: go to wall, turn left, go to corner")
    print("• Snake sweep the entire room")
    print("• Pick keys when found; only correct key opens the door")
    print("• Escape via exit hatch if encountered")
    print()

    # Override the load_program3 function to use our custom maze
    import robotspeak.compiler as compiler_module

    def custom_load_program3():
        compiler_module.maze = maze
        print(f"--- Loading Custom Multi-Key Room: {test_name} ---")
        print("Initial Room State:")
        maze.print_map()

    # Temporarily replace the load function
    original_load = compiler_module.load_program3
    compiler_module.load_program3 = custom_load_program3

    print("🎬 EXECUTING PROGRAM 3...")
    print("-" * 40)

    try:
        # Monkey patch the parser to check for maze solved after each action
        original_parser = compiler_module.parser

        def enhanced_parser(tokens, lineNumber, numLines, codingList, num_executed_lines=2):
            result = original_parser(tokens, lineNumber, numLines, codingList, num_executed_lines)
            if compiler_module.maze and compiler_module.maze.is_maze_solved():
                print("\n*** MAZE SOLVED! ***")
                return "HALT"
            return result

        compiler_module.parser = enhanced_parser

        compiler(program3_code)

        # Restore original functions
        compiler_module.load_program3 = original_load
        compiler_module.parser = original_parser

        print("-" * 40)
        if maze.is_maze_solved():
            print(f"✅ SUCCESS: {test_name} - Robot escaped!")
            print(f"Robot final position: {maze.robot_location}")
            print(f"Has key: {maze.has_key}")
            # Reveal whether the correct key was picked (runner-only insight)
            has_correct = getattr(maze, 'has_correct_key', False)
            print(f"Has correct key: {has_correct}")
            print(f"Door opened: {maze.has_opened_door}")
            print(f"At exit: {maze.at_exit()}")
            return True
        else:
            print(f"⚠️  INCOMPLETE: {test_name} - Robot did not escape")
            return False

    except Exception as e:
        print(f"❌ ERROR: {test_name} - {e}")
        # Restore original functions even on error
        try:
            compiler_module.load_program3 = original_load
            compiler_module.parser = original_parser
        except Exception:
            pass
        return False


def main():
    """Main test runner for Program 3"""

    print("🎯 PROGRAM 3 - MULTI-KEY ROOM TEST SUITE")
    print("=" * 60)
    print("Testing multi-key exploration from unknown start and orientation")
    print("Requirements:")
    print("• Rectangular room with 4 walls, no obstacles")
    print("• Multiple keys present; only one opens the door")
    print("• One door, one exit hatch")
    print("• Unknown starting tile and orientation")
    print()

    # Create test rooms
    test_cases = create_test_rooms()

    # Run tests
    results = []
    for test_name, maze in test_cases:
        success = run_program3_on_room(test_name, maze)
        results.append((test_name, success))
        print("\n" + "="*60 + "\n")

    # Summary
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    successful = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            successful += 1

    print(f"\nOverall: {successful}/{len(results)} tests passed")

    if successful == len(results):
        print("🎉 ALL TESTS PASSED! Program 3 works correctly!")
    else:
        print("⚠️  Some tests failed. Program 3 needs debugging.")


if __name__ == "__main__":
    main()


