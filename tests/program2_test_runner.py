#!/usr/bin/env python3
"""
Program 2 Test Runner: Rectangular Room Navigation
Creates and tests multiple room scenarios with Program 2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robotspeak.maze import Maze
from robotspeak.compiler import compiler

class RectangularRoomMaze(Maze):
    """Custom maze class for creating rectangular rooms with no obstacles"""
    
    def __init__(self, room_map, key_location, door_location, exit_location, robot_location, robot_direction='north'):
        """
        Create a rectangular room from a 2D map where:
        * = wall, . = floor, K = key, D = door, E = exit, R = robot
        """
        self.room_map = room_map
        self.height = len(room_map)
        self.width = len(room_map[0])
        
        super().__init__(
            width=self.width, 
            length=self.height,
            key_location=key_location,
            door_location=door_location, 
            exit_location=exit_location,
            robot_location=robot_location,
            robot_direction=robot_direction
        )
    
    def create_initial_map(self):
        """Create the room map from the provided pattern"""
        # Build map directly from provided strings
        self.map_matrix = [list(row) for row in self.room_map]

        # Derive coordinates from the map to ensure consistency
        derived_robot = None
        derived_key = None
        derived_door = None
        derived_exit = None

        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[y])):
                cell = self.map_matrix[y][x]
                if 'R' in cell:
                    derived_robot = [x, y]
                if 'K' in cell:
                    derived_key = [x, y]
                if 'D' in cell:
                    derived_door = [x, y]
                if 'E' in cell:
                    derived_exit = [x, y]

        # Fallback to provided if symbol not present
        if derived_robot is not None:
            self.robot_location = derived_robot
        if derived_key is not None:
            self.key_location = derived_key
        if derived_door is not None:
            self.door_location = derived_door
        if derived_exit is not None:
            self.exit_location = derived_exit

        # Set direction vector for current direction
        self.set_direction_coordinate()

def create_test_rooms():
    """
    Create 3 rectangular room scenarios for Program 2:
    - Different room sizes
    - Various object placements  
    - Robot starts at lower-left facing north
    - No obstacles in rooms
    """
    
    test_cases = []
    
    # Test Case 1: Small 4x3 room
    print("Creating Test Case 1: Small Room (4x3)")
    room1_map = [
        "*****",
        "*K.E*",
        "*R.D*", 
        "*****"
    ]
    test1 = RectangularRoomMaze(
        room_map=room1_map,
        key_location=[2, 2],      # Key in room  
        door_location=[4, 3],     # Door in room
        exit_location=[4, 2],     # Exit in room
        robot_location=[2, 3],    # Robot at lower-left 
        robot_direction='north'   # Facing north
    )
    test_cases.append(("Small Room (4x3)", test1))
    
    # Test Case 2: Medium 6x4 room
    print("Creating Test Case 2: Medium Room (6x4)")
    room2_map = [
        "********",
        "*....E.*", 
        "*......*",
        "*..K...*",
        "*....D.*",
        "*R.....*",
        "********"
    ]
    test2 = RectangularRoomMaze(
        room_map=room2_map,
        key_location=[4, 4],      # Key in middle area
        door_location=[6, 5],     # Door on right side  
        exit_location=[6, 2],     # Exit at top right
        robot_location=[2, 6],    # Robot at lower-left
        robot_direction='north'   # Facing north
    )
    test_cases.append(("Medium Room (6x4)", test2))
    
    # Test Case 3: Large 8x5 room with strategic placement
    print("Creating Test Case 3: Large Room (8x5)")
    room3_map = [
        "**********",
        "*......E.*",
        "*........*", 
        "*........*",
        "*..K.....*",
        "*......D.*",
        "*R.......*",
        "**********"
    ]
    test3 = RectangularRoomMaze(
        room_map=room3_map,
        key_location=[4, 5],      # Key in lower area
        door_location=[8, 6],     # Door at bottom right
        exit_location=[8, 2],     # Exit at top right
        robot_location=[2, 7],    # Robot at lower-left
        robot_direction='north'   # Facing north
    )
    test_cases.append(("Large Room (8x5)", test3))
    
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

def run_program2_on_room(test_name, maze):
    """Run Program 2 on a specific room test case"""
    
    print(f"🚀 RUNNING PROGRAM 2 ON: {test_name}")
    print("=" * 60)
    
    # Initialize the maze
    try:
        maze.create_initial_map()
        display_room_map(maze, test_name)
    except Exception as e:
        print(f"❌ Error creating maze: {e}")
        return False
    
    # Load Program 2 code
    try:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        program2_path = os.path.join(repo_root, 'algorithms', 'program2.txt')
        with open(program2_path, 'r') as f:
            program2_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: program2.txt not found at {program2_path}")
        return False
    
    print("📋 Program 2 Strategy:")
    print("• Snake-like systematic room sweep")
    print("• Go north until wall, then right, down, left, up, etc.")
    print("• Collect key when found")
    print("• Open door when at door location with key")
    print("• Escape via exit hatch if found first")
    print("• No obstacles - pure rectangular room")
    print()
    
    # Override the load_program2 function to use our custom maze
    import robotspeak.compiler as compiler_module
    
    def custom_load_program2():
        compiler_module.maze = maze
        print(f"--- Loading Custom Room: {test_name} ---")
        print("Initial Room State:")
        maze.print_map()
    
    # Temporarily replace the load function
    original_load = compiler_module.load_program2
    compiler_module.load_program2 = custom_load_program2
    
    print("🎬 EXECUTING PROGRAM 2...")
    print("-" * 40)
    
    try:
        # Monkey patch the parser to check for maze solved after each action
        original_parser = compiler_module.parser
        
        def enhanced_parser(tokens, lineNumber, numLines, codingList, num_executed_lines=2):
            result = original_parser(tokens, lineNumber, numLines, codingList, num_executed_lines)
            
            # Check if maze is solved after any action (not just OPEN_DOOR)
            if compiler_module.maze and compiler_module.maze.is_maze_solved():
                print("\n*** MAZE SOLVED! ***")
                return "HALT"
            
            return result
        
        # Temporarily replace the parser
        compiler_module.parser = enhanced_parser
        
        compiler(program2_code)
        
        # Restore original functions
        compiler_module.load_program2 = original_load
        compiler_module.parser = original_parser
        
        print("-" * 40)
        if maze.is_maze_solved():
            print(f"✅ SUCCESS: {test_name} - Robot escaped!")
            print(f"Robot final position: {maze.robot_location}")
            print(f"Has key: {maze.has_key}")
            print(f"Door opened: {maze.has_opened_door}")
            print(f"At exit: {maze.at_exit()}")
            return True
        else:
            print(f"⚠️  INCOMPLETE: {test_name} - Robot did not escape")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {test_name} - {e}")
        # Restore original functions even on error
        compiler_module.load_program2 = original_load
        if 'enhanced_parser' in locals():
            compiler_module.parser = original_parser
        return False

def main():
    """Main test runner for Program 2"""
    
    print("🎯 PROGRAM 2 - RECTANGULAR ROOM TEST SUITE")
    print("=" * 60)
    print("Testing systematic room exploration")
    print("Requirements:")
    print("• Orthogonal rectangular room with 4 walls")
    print("• No obstacles in room") 
    print("• Robot starts at lower-left facing north")
    print("• Find key + open door OR exit hatch (whichever first)")
    print()
    
    # Create test rooms
    test_cases = create_test_rooms()
    
    # Run only first test case for now to avoid infinite loops
    # test_cases = [test_cases[0]]
    
    # Run tests
    results = []
    for test_name, maze in test_cases:
        success = run_program2_on_room(test_name, maze)
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
        print("🎉 ALL TESTS PASSED! Program 2 works correctly!")
    else:
        print("⚠️  Some tests failed. Program 2 needs debugging.")

if __name__ == "__main__":
    main()
