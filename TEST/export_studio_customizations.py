#!/usr/bin/env python3
"""
Final Studio Export - Properly handle view inheritance 
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _config import connect_odoo, test_connection

def create_final_studio_replacement():
    """Create final working Studio replacement with proper inheritance"""
    
    print("🎯 FINAL STUDIO REPLACEMENT")
    print("=" * 60)
    
    try:
        info = test_connection('hook_local')
        print(f"✅ Connected to {info['database']} as {info['name']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    models, db, uid, password = connect_odoo('hook_local')
    
    module_path = "/Users/dgoo2308/git/odoo18/hook/hook_studio_replacement"
    
    # Get Studio views with inheritance info
    studio_views = models.execute_kw(db, uid, password, 'ir.ui.view', 'search_read',
                                   [[('name', 'like', 'Odoo Studio:%')]], 
                                   {'fields': ['id', 'name', 'model', 'type', 'arch_db', 'inherit_id', 'priority']})
    
    print(f"\n📋 CREATING VIEWS WITH PROPER INHERITANCE")
    
    # Map common base views
    base_view_map = {
        'account.move': 'account.view_move_form',
        'product.template': 'product.product_template_only_form_view', 
        'stock.lot': 'stock.view_production_lot_form',
        'res.partner': 'base.view_partner_form'
    }
    
    views_xml = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
'''
    
    for view in studio_views:
        model = view['model']
        base_view = base_view_map.get(model, f'base.view_{model.replace(".", "_")}_form')
        
        print(f"  📄 {view['name']} -> inherits from {base_view}")
        
        arch_content = view['arch_db'].strip()
        if arch_content.startswith('<data>') and arch_content.endswith('</data>'):
            arch_content = arch_content[6:-7].strip()
        
        views_xml += f'''
        <record id="hook_studio_view_{view['id']}" model="ir.ui.view">
            <field name="name">{view['name'].replace('Odoo Studio:', 'Hook Studio:')}</field>
            <field name="model">{view['model']}</field>
            <field name="inherit_id" ref="{base_view}"/>
            <field name="priority">{view['priority']}</field>
            <field name="arch" type="xml">
                {arch_content}
            </field>
        </record>
'''
    
    views_xml += '''
    </data>
</odoo>'''
    
    with open(f"{module_path}/views/studio_views.xml", "w", encoding='utf-8') as f:
        f.write(views_xml)
    
    print(f"  ✅ Created {len(studio_views)} inheritance views")
    
    # Keep reports simple for now - just export the definitions
    print(f"\n📊 CREATING REPORT DEFINITIONS")
    target_reports = ['PDF copy(1)', 'PDF copy(2)', 'PDF without Payment copy(2)']
    
    reports_xml = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Studio Reports Preserved -->
'''
    
    exported_count = 0
    for report_name in target_reports:
        reports = models.execute_kw(db, uid, password, 'ir.actions.report', 'search_read',
                                  [[('name', '=', report_name)]], 
                                  {'fields': ['id', 'name', 'model', 'report_name', 'report_type']})
        
        for report in reports:
            print(f"  📊 {report['name']} -> preserved as comment")
            
            reports_xml += f'''
        <!-- Report: {report['name']} -->
        <!-- Original report_name: {report['report_name']} -->
        <!-- Model: {report['model']} -->
        <!-- Type: {report['report_type']} -->
'''
            exported_count += 1
    
    reports_xml += '''
        <!-- 
        Note: Studio reports are complex to migrate automatically.
        The original 3 reports are preserved above as comments.
        You can manually recreate them or export from Studio if needed.
        -->
    </data>
</odoo>'''
    
    with open(f"{module_path}/reports/studio_reports.xml", "w", encoding='utf-8') as f:
        f.write(reports_xml)
    
    print(f"  ✅ Documented {exported_count} reports for manual recreation")
    
    print(f"\n✅ FINAL STUDIO REPLACEMENT READY")
    print(f"📋 Views: {len(studio_views)} with proper inheritance")
    print(f"📊 Reports: {exported_count} documented (manual recreation needed)")
    print(f"\n🔄 Next: ./manage_odoo.sh update hook_studio_replacement")

if __name__ == "__main__":
    create_final_studio_replacement()
