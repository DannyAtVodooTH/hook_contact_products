#!/usr/bin/env python3
"""
Analyze Contact Classification
Detailed analysis of contacts needing classification in Hook Odoo
"""

import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from _config import connect_odoo


def analyze_contacts():
    """Analyze contacts that need classification"""
    print("🔍 Analyzing Contact Classification Status...")
    print("-" * 60)
    
    try:
        models, db, uid, password = connect_odoo('hook')
        
        # Get vendor contacts (V* references)
        print("\n📊 VENDOR ANALYSIS (V* references)")
        print("-" * 40)
        
        vendor_ids = models.execute_kw(
            db, uid, password, 'res.partner', 'search',
            [[['ref', '=like', 'V%']]]
        )
        
        if vendor_ids:
            vendors = models.execute_kw(
                db, uid, password, 'res.partner', 'read',
                [vendor_ids], {'fields': ['name', 'ref', 'supplier_rank', 'customer_rank']}
            )
            
            needs_vendor_classification = [v for v in vendors if v['supplier_rank'] == 0]
            already_vendors = [v for v in vendors if v['supplier_rank'] > 0]
            
            print(f"Total V* contacts: {len(vendors)}")
            print(f"Already classified as vendors: {len(already_vendors)}")
            print(f"Need vendor classification: {len(needs_vendor_classification)}")
            
            if needs_vendor_classification:
                print("\nContacts needing vendor classification:")
                for contact in needs_vendor_classification[:10]:  # Show first 10
                    print(f"  - {contact['name']} ({contact['ref']})")
                if len(needs_vendor_classification) > 10:
                    print(f"  ... and {len(needs_vendor_classification) - 10} more")
        else:
            print("No contacts found with V* reference pattern")
        
        # Get customer contacts (C* references)
        print("\n📊 CUSTOMER ANALYSIS (C* references)")
        print("-" * 40)
        
        customer_ids = models.execute_kw(
            db, uid, password, 'res.partner', 'search',
            [[['ref', '=like', 'C%']]]
        )
        
        if customer_ids:
            customers = models.execute_kw(
                db, uid, password, 'res.partner', 'read',
                [customer_ids], {'fields': ['name', 'ref', 'supplier_rank', 'customer_rank']}
            )
            
            needs_customer_classification = [c for c in customers if c['customer_rank'] == 0]
            already_customers = [c for c in customers if c['customer_rank'] > 0]
            
            print(f"Total C* contacts: {len(customers)}")
            print(f"Already classified as customers: {len(already_customers)}")
            print(f"Need customer classification: {len(needs_customer_classification)}")
            
            if needs_customer_classification:
                print("\nContacts needing customer classification:")
                for contact in needs_customer_classification[:10]:  # Show first 10
                    print(f"  - {contact['name']} ({contact['ref']})")
                if len(needs_customer_classification) > 10:
                    print(f"  ... and {len(needs_customer_classification) - 10} more")
        else:
            print("No contacts found with C* reference pattern")
        
        # Summary
        total_needing_update = len(needs_vendor_classification) + len(needs_customer_classification)
        print(f"\n📋 SUMMARY")
        print("-" * 20)
        print(f"Total contacts needing classification: {total_needing_update}")
        print(f"- Vendors to update: {len(needs_vendor_classification)}")
        print(f"- Customers to update: {len(needs_customer_classification)}")
        
        if total_needing_update > 0:
            print(f"\n🚀 Ready to run classification script!")
        else:
            print(f"\n✅ All contacts already properly classified!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


if __name__ == "__main__":
    analyze_contacts()
