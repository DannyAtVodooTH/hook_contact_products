#!/usr/bin/env python3
"""
Test Hook Odoo Connection
Validates connection to Hook Odoo instance and basic API functionality
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from _config import test_connection, connect_odoo


def main():
    """Test connection to Hook Odoo instance"""
    print("🔌 Testing Hook Odoo Connection...")
    print("-" * 50)
    
    try:
        # Test basic connection
        info = test_connection('hook')
        print(f"✅ Connection successful!")
        print(f"   Instance: {info['instance']}")
        print(f"   User: {info['name']} ({info['login']})")
        print(f"   Database: {info['database']}")
        print(f"   User ID: {info['user_id']}")
        
        # Test API functionality
        print("\n🔍 Testing API functionality...")
        models, db, uid, password = connect_odoo('hook')
        
        # Count total partners
        partner_count = models.execute_kw(
            db, uid, password, 'res.partner', 'search_count', [[]]
        )
        print(f"✅ Total contacts in system: {partner_count}")
        
        # Count contacts with references starting with V or C
        v_count = models.execute_kw(
            db, uid, password, 'res.partner', 'search_count',
            [[['ref', '=like', 'V%']]]
        )
        c_count = models.execute_kw(
            db, uid, password, 'res.partner', 'search_count',
            [[['ref', '=like', 'C%']]]
        )
        
        print(f"✅ Contacts with V* reference: {v_count}")
        print(f"✅ Contacts with C* reference: {c_count}")
        
        print(f"\n🎯 Ready to proceed with contact classification!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure ~/.odoo_config/hook.conf exists with:")
        print("   [odoo]")
        print("   url = https://your-hook-instance.com")
        print("   database = your_database")
        print("   username = your_username")
        print("   password = your_password")
        return False
    
    return True


if __name__ == "__main__":
    main()
