#!/usr/bin/env python3

import sys
from .cli import main as cli_main

def main():
    """Main entry point for Kitsunari CLI"""
    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()