import argparse
import sys
from robotspeak.compiler import (
    compiler,
    SyntaxErrorException,
    RuntimeErrorException,
)


def main():
    """
    The main entry point for the Robotspeak CLI.
    Parses command-line arguments, reads the source file,
    and executes the compiler.
    """
    parser = argparse.ArgumentParser(
        description="Robotspeak Interpreter: Executes a .txt file containing Robotspeak code."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="The path to the Robotspeak source file (.txt).",
    )

    args = parser.parse_args()

    try:
        with open(args.filepath, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.filepath}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not read the file '{args.filepath}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- Starting Robotspeak Interpreter for {args.filepath} ---")
    try:
        compiler(source_code)
        print("\n--- Program finished successfully. ---")
    except (SyntaxErrorException, RuntimeErrorException) as e:
        # Your custom exceptions already print nicely formatted messages
        print(f"\n--- ERROR ---\n{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"\n--- An unexpected error occurred ---\n{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()