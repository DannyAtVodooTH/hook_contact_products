#!/usr/bin/env python3
"""
Test database connection
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config import db_config

def main():
    """Test database connection"""
    print("=== Database Connection Test ===")
    print(f"Database: {db_config.db_name}")
    print(f"Host: {db_config.host}")
    print(f"Port: {db_config.port}")
    print(f"User: {db_config.user}")
    
    # Test connection
    success = db_config.test_connection()
    
    if success:
        print("✓ Database connection successful!")
    else:
        print("✗ Database connection failed!")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'hook_local' exists")
        print("3. User 'odoo' has access")

if __name__ == "__main__":
    main()
