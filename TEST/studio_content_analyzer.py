#!/usr/bin/env python3
"""
Studio Customizations Finder - Find the exact 4 views and 3 reports Studio will delete
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config import connect_odoo, test_connection

def find_studio_customizations():
    """Find the exact Studio customizations that will be deleted"""
    
    print("🎯 FINDING STUDIO CUSTOMIZATIONS")
    print("=" * 60)
    print("Looking for the exact 4 views and 3 reports Studio will delete...")
    
    try:
        info = test_connection('hook_local')
        print(f"✅ Connected to {info['database']} as {info['name']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    models, db, uid, password = connect_odoo('hook_local')
    
    # Find actual Studio customizations (the ones with "Odoo Studio:" prefix or studio keys)
    print("\n🔍 STUDIO CUSTOMIZATION VIEWS")
    
    # Look for views that start with "Odoo Studio:"
    studio_custom_views = models.execute_kw(db, uid, password, 'ir.ui.view', 'search_read',
                                          [[('name', 'like', 'Odoo Studio:%')]], 
                                          {'fields': ['id', 'name', 'model', 'type', 'active']})
    
    print(f"Found {len(studio_custom_views)} 'Odoo Studio:' customization views:")
    for view in studio_custom_views:
        status = "✅" if view['active'] else "❌"
        print(f"  {status} ID:{view['id']}")
        print(f"      Name: {view['name']}")
        print(f"      Model: {view['model']} | Type: {view['type']}")
        print()
    
    # Look for reports with Studio patterns
    print("\n🔍 STUDIO REPORTS")
    
    # Check for custom reports (might not have studio in name)
    # Look for reports that aren't standard Odoo reports
    all_reports = models.execute_kw(db, uid, password, 'ir.actions.report', 'search_read',
                                  [[('report_type', '=', 'qweb-pdf')]], 
                                  {'fields': ['id', 'name', 'model', 'report_name', 'xml_id']})
    
    # Filter for non-standard reports (those without module prefixes or with studio)
    custom_reports = []
    for report in all_reports:
        xml_id = report.get('xml_id', '') or ''
        name = report['name']
        report_name = report['report_name']
        
        # Look for reports that might be Studio-created
        if ('studio' in name.lower() or 
            'studio' in report_name.lower() or
            'studio' in xml_id.lower() or
            not xml_id or  # No XML ID might indicate Studio creation
            xml_id.startswith('__export')):  # Studio exports start with __export
            custom_reports.append(report)
    
    print(f"Found {len(custom_reports)} potentially custom reports:")
    for report in custom_reports:
        xml_id = report.get('xml_id', 'No XML ID') or 'No XML ID'
        print(f"  • ID:{report['id']}")
        print(f"      Name: {report['name']}")
        print(f"      Model: {report['model']}")
        print(f"      Report: {report['report_name']}")
        print(f"      XML ID: {xml_id}")
        print()
    
    # Look for any other custom models or data that Studio might have created
    print("\n🔍 STUDIO DATA RECORDS")
    
    # Check for any records with studio in their XML ID
    studio_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read',
                                  [[('name', 'ilike', 'studio')]], 
                                  {'fields': ['id', 'name', 'model', 'module']})
    
    print(f"Found {len(studio_data)} Studio data records:")
    for data in studio_data[:10]:  # Show first 10
        print(f"  • {data['module']}.{data['name']} ({data['model']})")
    
    # Summary and action plan
    print(f"\n📋 EXPORT CHECKLIST:")
    print(f"✅ Custom Fields: 20 fields - Safe to delete (module replaces them)")
    print(f"🔍 Custom Views: {len(studio_custom_views)} Studio customization views found")
    print(f"🔍 Custom Reports: {len(custom_reports)} potentially custom reports found")
    
    if len(studio_custom_views) > 0 or len(custom_reports) > 0:
        print(f"\n⚠️  ACTION REQUIRED:")
        print("1. Go to Studio app")
        print("2. Export the customization views shown above")
        print("3. Export any custom reports shown above")
        print("4. Add exported XML to hook_studio_replacement module")
        print("5. Upgrade hook_studio_replacement module")
        print("6. Test that customizations work")
        print("7. Then safely uninstall Studio")
    else:
        print(f"\n🎉 No critical customizations found - Studio might be safe to uninstall")
        print("But still backup first!")

if __name__ == "__main__":
    find_studio_customizations()
