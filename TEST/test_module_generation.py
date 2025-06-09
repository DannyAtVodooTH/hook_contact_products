#!/usr/bin/env python3
"""
Test script to generate the replacement module
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _module_generator import main as generate_module

def main():
    """Test module generation"""
    print("=== Module Generation Test ===")
    
    # Check if analysis exists
    analysis_file = "studio_analysis_report.json"
    if not os.path.exists(analysis_file):
        print("No analysis report found.")
        print("Run test_studio_analysis.py first")
        return
    
    # Generate the module
    generate_module()

if __name__ == "__main__":
    main()
