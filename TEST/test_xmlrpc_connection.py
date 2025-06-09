#!/usr/bin/env python3
"""
Test XML-RPC connection to Odoo
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _odoo_config import odoo_config

def main():
    """Test XML-RPC connection"""
    print("=== XML-RPC Connection Test ===")
    print(f"Environment: {odoo_config.env_name}")
    print(f"Config file: {odoo_config.config_file}")
    
    # Test connection
    success = odoo_config.test_connection()
    
    if success:
        print("✓ XML-RPC connection successful!")
        
        # Test a simple query
        try:
            user_count = odoo_config.execute('res.users', 'search_count', [])
            print(f"✓ Found {user_count} users in the system")
        except Exception as e:
            print(f"✗ Error testing query: {e}")
    else:
        print("✗ XML-RPC connection failed!")
        print("\nMake sure:")
        print("1. Odoo is running on http://localhost:8069")
        print("2. Database 'hook_local' exists and is accessible")
        print("3. Admin user credentials are correct")

if __name__ == "__main__":
    main()
