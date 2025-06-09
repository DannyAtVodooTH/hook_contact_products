#!/usr/bin/env python3
"""
Test script to analyze Studio fields in the database
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _odoo_config import odoo_config
from _studio_analyzer import find_studio_fields, save_analysis_report

def main():
    """Main test function"""
    print("=== Studio Fields Analysis Test ===")
    
    # Test XML-RPC connection
    print("Testing Odoo connection...")
    if not odoo_config.test_connection():
        print("Cannot proceed without Odoo connection")
        return
    
    # Find Studio fields
    print("\nScanning for Studio fields...")
    studio_fields = find_studio_fields()
    
    if not studio_fields:
        print("No Studio fields found in the database")
        return
    
    print(f"Found {len(studio_fields)} Studio fields")
    
    # Show summary of found fields
    print("\nStudio fields found:")
    for field in studio_fields:
        print(f"  - {field['model']}.{field['name']} ({field['ttype']})")
    
    # Perform detailed analysis
    print("\nPerforming detailed analysis...")
    report = save_analysis_report(studio_fields, "TEST/studio_analysis_report.json")
    
    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    main()
