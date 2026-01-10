#!/usr/bin/env python3
"""
Main entry point for PE Assessment System
Run this file to start the system
"""

import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Now import and run main
from main import main

if __name__ == "__main__":
    main()
