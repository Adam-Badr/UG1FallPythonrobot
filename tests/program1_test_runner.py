#!/usr/bin/env python3
"""
Program 1 Test Runner: Twisting Corridor Navigation
Creates and tests 3 different corridor scenarios with Program 1
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robotspeak.maze import Maze
from robotspeak.compiler import compiler

class CorridorMaze(Maze):
    """Custom maze class for creating actual corridors with walls"""
    
    def __init__(self, corridor_map, key_location, door_location, exit_location, robot_location, robot_direction='north'):
        """
        Create a corridor from a 2D map where:
        * = wall, . = floor, K = key, D = door, E = exit, R = robot
        """
        self.corridor_map = corridor_map
        self.height = len(corridor_map)
        self.width = len(corridor_map[0])
        
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
        """Create the corridor map from the provided pattern"""
        self.validate_intial_inputs()
        
        # Create map from the corridor pattern (objects already placed in the map)
        self.map_matrix = []
        for row in self.corridor_map:
            self.map_matrix.append(list(row))
        
        # Objects (K, D, E, R) are already placed in the corridor_map
        # No need to place them again
        
        self.set_direction_coordinate()

def create_test_corridors():
    """
    Create 3 ACTUAL twisting corridor scenarios for Program 1:
    - Narrow corridors with walls and turns
    - Blocked at both ends
    - Contains key, door, and exit in the corridor path
    - Unknown robot starting position and direction
    """
    
    test_cases = []
    
    # Test Case 1: L-shaped corridor with narrow passages
    print("Creating Test Case 1: L-shaped Corridor")
    corridor1_map = [
        "*********",
        "*R*******",
        "*K*******", 
        "*.*******",
        "*.*******",
        "*E....D.*",
        "*********"
    ]
    test1 = CorridorMaze(
        corridor_map=corridor1_map,
        key_location=[2, 3],      # Key in vertical section
        door_location=[7, 6],     # Door at bottom right end
        exit_location=[2, 6],     # Exit in bottom horizontal section
        robot_location=[2, 2],    # Robot at top of vertical section
        robot_direction='south'   # Unknown direction
    )
    test_cases.append(("L-shaped Corridor", test1))
    
    # Test Case 2: S-shaped winding corridor
    print("Creating Test Case 2: S-shaped Corridor")
    corridor2_map = [
        "***********",
        "*R......D.*", 
        "*.*********",
        "*.*********",
        "*.*********",
        "*.*********",
        "*.K......*",
        "*********.*",
        "*********.*",
        "*E.......*",
        "***********"
    ]
    test2 = CorridorMaze(
        corridor_map=corridor2_map,
        key_location=[3, 7],      # Key in middle horizontal section (updated position)
        door_location=[9, 2],     # Door at top right corridor
        exit_location=[2, 10],    # Exit at bottom left corridor  
        robot_location=[2, 2],    # Robot in top horizontal section
        robot_direction='east'    # Unknown direction
    )
    test_cases.append(("S-shaped Corridor", test2))
    
    # Test Case 3: Complex zigzag corridor
    print("Creating Test Case 3: Zigzag Corridor")
    corridor3_map = [
        "*********",
        "*R......*",
        "*******.*", 
        "*K.....D*",
        "*.*******",
        "*.......*",
        "*******.*", 
        "*E......*",
        "*********"
    ]
    test3 = CorridorMaze(
        corridor_map=corridor3_map,
        key_location=[2, 4],      # Key in middle horizontal section
        door_location=[8, 4],     # Door at right side  
        exit_location=[2, 8],     # Exit at bottom
        robot_location=[2, 2],    # Robot at top left corridor
        robot_direction='south'   # Unknown direction
    )
    test_cases.append(("Zigzag Corridor", test3))
    
    return test_cases

def display_corridor_map(maze, test_name):
    """Display the corridor map with description"""
    print(f"\n🗺️  {test_name}")
    print("=" * 50)
    print("Legend: R=Robot, K=Key, D=Door, E=Exit, *=Wall, .=Floor")
    print(f"Robot starts at {maze.robot_location} facing {maze.robot_direction}")
    maze.print_map()
    print()

def run_program1_on_corridor(test_name, maze):
    """Run Program 1 on a specific corridor test case"""
    
    print(f"🚀 RUNNING PROGRAM 1 ON: {test_name}")
    print("=" * 60)
    
    # Initialize the maze
    try:
        maze.create_initial_map()
        display_corridor_map(maze, test_name)
    except Exception as e:
        print(f"❌ Error creating maze: {e}")
        return False
    
    # Load Program 1 code
    try:
        with open('../algorithms/program1.txt', 'r') as f:
            program1_code = f.read()
    except FileNotFoundError:
        print("❌ Error: solve_map.txt not found")
        return False
    
    print("📋 Program 1 Strategy:")
    print("• Left-hand wall following algorithm")
    print("• Collect key when found")
    print("• Open door when at door location")
    print("• Navigate unknown corridor layout")
    print()
    
    # Override the load_program1 function to use our custom maze
    import robotspeak.compiler as compiler_module
    
    def custom_load_program1():
        compiler_module.maze = maze
        print(f"--- Loading Custom Corridor: {test_name} ---")
        print("Initial Maze State:")
        maze.print_map()
    
    # Temporarily replace the load function
    original_load = compiler_module.load_program1
    compiler_module.load_program1 = custom_load_program1
    
    print("🎬 EXECUTING PROGRAM 1...")
    print("-" * 40)
    
    try:
        compiler(program1_code)
        
        # Restore original load function
        compiler_module.load_program1 = original_load
        
        print("-" * 40)
        if maze.is_maze_solved():
            print(f"✅ SUCCESS: {test_name} - Robot escaped!")
            print(f"Robot final position: {maze.robot_location}")
            print(f"Has key: {maze.has_key}")
            print(f"Door opened: {maze.has_opened_door}")
            return True
        else:
            print(f"⚠️  INCOMPLETE: {test_name} - Robot did not escape")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {test_name} - {e}")
        return False

def main():
    """Main test runner for Program 1"""
    
    print("🎯 PROGRAM 1 - TWISTING CORRIDOR TEST SUITE")
    print("=" * 60)
    print("Testing corridor navigation with unknown starting position")
    print("Requirements:")
    print("• Twisting corridor with turns")
    print("• Blocked at both ends") 
    print("• Contains key, door, and exit")
    print("• Robot position and direction unknown")
    print()
    
    # Create test corridors
    test_cases = create_test_corridors()
    
    # Run tests
    results = []
    for test_name, maze in test_cases:
        success = run_program1_on_corridor(test_name, maze)
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
        print("🎉 ALL TESTS PASSED! Program 1 works correctly!")
    else:
        print("⚠️  Some tests failed. Program 1 needs debugging.")

if __name__ == "__main__":
    main()
