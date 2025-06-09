#!/usr/bin/env python3
"""
Contact Classification Updater Module
Handles updating contact classification (customer/vendor) in Odoo
based on reference field patterns (Vxxxx = Vendor, Cxxxx = Customer)
"""

import sys
from pathlib import Path

# Add current directory to Python path to import our config
sys.path.insert(0, str(Path(__file__).parent))

from _config import connect_odoo


def find_contacts_by_reference_pattern(models, db, uid, password, pattern):
    """Find contacts by reference pattern (V* for vendors, C* for customers)"""
    try:
        contact_ids = models.execute_kw(
            db, uid, password, 'res.partner', 'search',
            [[['ref', '=like', pattern]]]
        )
        return contact_ids
    except Exception as e:
        print(f"Error finding contacts with pattern {pattern}: {e}")
        return []


def get_contact_details(models, db, uid, password, contact_ids):
    """Get contact details including current classification"""
    try:
        contacts = models.execute_kw(
            db, uid, password, 'res.partner', 'read',
            [contact_ids], {'fields': ['id', 'name', 'ref', 'is_company', 'customer_rank', 'supplier_rank']}
        )
        return contacts
    except Exception as e:
        print(f"Error getting contact details: {e}")
        return []


def update_contact_classification(models, db, uid, password, contact_id, is_customer=False, is_vendor=False):
    """
    Update contact classification by setting customer_rank and supplier_rank
    
    Args:
        contact_id: Partner ID
        is_customer: Set as customer (customer_rank = 1)
        is_vendor: Set as vendor (supplier_rank = 1)
    """
    try:
        update_data = {}
        
        if is_customer:
            update_data['customer_rank'] = 1
        
        if is_vendor:
            update_data['supplier_rank'] = 1
            
        if not update_data:
            return False, "No classification specified"
        
        result = models.execute_kw(
            db, uid, password, 'res.partner', 'write',
            [contact_id, update_data]
        )
        
        return result, "Success"
        
    except Exception as e:
        return False, f"Error updating classification: {e}"


def classify_contacts_by_reference(models, db, uid, password, dry_run=True):
    """
    Classify all contacts based on reference field patterns
    V* = Vendor, C* = Customer
    
    Args:
        dry_run: If True, only show what would be updated without making changes
    """
    results = {
        'vendors_found': 0,
        'customers_found': 0,
        'vendors_updated': 0,
        'customers_updated': 0,
        'errors': []
    }
    
    try:
        # Find vendor contacts (V*)
        vendor_ids = find_contacts_by_reference_pattern(models, db, uid, password, 'V%')
        vendor_contacts = get_contact_details(models, db, uid, password, vendor_ids)
        results['vendors_found'] = len(vendor_contacts)
        
        print(f"Found {len(vendor_contacts)} contacts with vendor reference pattern (V*)")
        
        for contact in vendor_contacts:
            if contact['supplier_rank'] == 0:  # Not yet classified as vendor
                if not dry_run:
                    success, message = update_contact_classification(
                        models, db, uid, password, contact['id'], is_vendor=True
                    )
                    if success:
                        results['vendors_updated'] += 1
                        print(f"✅ Updated vendor: {contact['name']} ({contact['ref']})")
                    else:
                        results['errors'].append(f"Vendor {contact['name']}: {message}")
                        print(f"❌ Failed vendor: {contact['name']} - {message}")
                else:
                    results['vendors_updated'] += 1
                    print(f"🔍 Would update vendor: {contact['name']} ({contact['ref']})")
            else:
                print(f"⏭️  Already vendor: {contact['name']} ({contact['ref']})")
        
        # Find customer contacts (C*)
        customer_ids = find_contacts_by_reference_pattern(models, db, uid, password, 'C%')
        customer_contacts = get_contact_details(models, db, uid, password, customer_ids)
        results['customers_found'] = len(customer_contacts)
        
        print(f"Found {len(customer_contacts)} contacts with customer reference pattern (C*)")
        
        for contact in customer_contacts:
            if contact['customer_rank'] == 0:  # Not yet classified as customer
                if not dry_run:
                    success, message = update_contact_classification(
                        models, db, uid, password, contact['id'], is_customer=True
                    )
                    if success:
                        results['customers_updated'] += 1
                        print(f"✅ Updated customer: {contact['name']} ({contact['ref']})")
                    else:
                        results['errors'].append(f"Customer {contact['name']}: {message}")
                        print(f"❌ Failed customer: {contact['name']} - {message}")
                else:
                    results['customers_updated'] += 1
                    print(f"🔍 Would update customer: {contact['name']} ({contact['ref']})")
            else:
                print(f"⏭️  Already customer: {contact['name']} ({contact['ref']})")
                
    except Exception as e:
        results['errors'].append(f"General error: {e}")
        print(f"❌ Error during classification: {e}")
    
    return results
