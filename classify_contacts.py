#!/usr/bin/env python3
"""
Contact Classification Script
Classify contacts as customers or vendors based on reference patterns
Usage: python classify_contacts.py [--dry-run] [--execute]
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from _config import connect_odoo
from _contact_updater import classify_contacts_by_reference


def main():
    parser = argparse.ArgumentParser(description='Classify contacts by reference patterns')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be updated without making changes (default)')
    parser.add_argument('--execute', action='store_true',
                       help='Actually perform the updates')
    
    args = parser.parse_args()
    
    # Default to dry-run if no specific flag is provided
    dry_run = not args.execute
    
    print("🏷️  Contact Classification Script")
    print("=" * 50)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'EXECUTE (making changes)'}")
    print("-" * 50)
    
    if not dry_run:
        confirm = input("⚠️  You are about to modify contact data. Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.")
            return
    
    try:
        # Connect to Hook Odoo instance
        print("🔌 Connecting to Hook Odoo...")
        models, db, uid, password = connect_odoo('hook')
        print("✅ Connected successfully")
        
        # Run classification
        print("\n🔄 Starting contact classification...")
        results = classify_contacts_by_reference(models, db, uid, password, dry_run=dry_run)
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 CLASSIFICATION RESULTS")
        print("=" * 50)
        print(f"Vendors found: {results['vendors_found']}")
        print(f"Vendors updated: {results['vendors_updated']}")
        print(f"Customers found: {results['customers_found']}")
        print(f"Customers updated: {results['customers_updated']}")
        
        if results['errors']:
            print(f"\n❌ Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                print(f"   - {error}")
        
        total_updated = results['vendors_updated'] + results['customers_updated']
        if dry_run:
            print(f"\n🔍 Would update {total_updated} contacts total")
            print("💡 Run with --execute to perform actual updates")
        else:
            print(f"\n✅ Successfully updated {total_updated} contacts")
            print("🎯 Contacts should now appear in proper sections:")
            print("   - Vendors in Purchasing > Vendors")
            print("   - Customers in Sales > Customers")
        
    except Exception as e:
        print(f"❌ Script failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
