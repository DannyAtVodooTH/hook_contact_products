#!/usr/bin/env python3
"""
Test script for database cleanup operations
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _database_cleaner import backup_field_definitions, remove_studio_field_definitions, verify_data_integrity

def main():
    """Test database cleanup operations"""
    print("=== Database Cleanup Test ===")
    
    print("1. Testing backup of Studio field definitions...")
    if backup_field_definitions():
        print("✓ Backup successful")
    else:
        print("✗ Backup failed")
        return
    
    print("\n2. Testing dry run removal...")
    if remove_studio_field_definitions(dry_run=True):
        print("✓ Dry run successful")
    else:
        print("✗ Dry run failed")
        return
    
    print("\n3. Testing data integrity verification...")
    if verify_data_integrity():
        print("✓ Data integrity check successful")
    else:
        print("✗ Data integrity check failed")
    
    print("\n=== All Tests Complete ===")
    print("Note: No actual changes were made to the database")

if __name__ == "__main__":
    main()
