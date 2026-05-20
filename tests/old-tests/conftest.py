"""
Pytest configuration and shared fixtures for springs-of-mud-server tests.
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))
