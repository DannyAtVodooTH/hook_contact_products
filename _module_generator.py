#!/usr/bin/env python3
"""
Module Generator for Studio Field Replacement
Generates Odoo module to replace Studio fields with proper field definitions
"""

import json
import os
from pathlib import Path

def load_analysis_report(filename="TEST/studio_analysis_report.json"):
    """Load the Studio fields analysis report"""
    if not Path(filename).exists():
        print(f"Analysis report not found: {filename}")
        print("Run test_studio_analysis.py first")
        return None
    
    with open(filename, 'r') as f:
        return json.load(f)

def generate_field_definition(field_info):
    """Generate Python field definition for a Studio field"""
    field_name = field_info['name'].replace('x_studio_', '')
    field_type = field_info['ttype']
    
    # Map Odoo field types to proper definitions
    type_mapping = {
        'char': f"fields.Char(string='{field_name.title().replace('_', ' ')}')",
        'text': f"fields.Text(string='{field_name.title().replace('_', ' ')}')",
        'integer': f"fields.Integer(string='{field_name.title().replace('_', ' ')}')",
        'float': f"fields.Float(string='{field_name.title().replace('_', ' ')}')",
        'boolean': f"fields.Boolean(string='{field_name.title().replace('_', ' ')}')",
        'date': f"fields.Date(string='{field_name.title().replace('_', ' ')}')",
        'datetime': f"fields.Datetime(string='{field_name.title().replace('_', ' ')}')",
        'many2one': f"fields.Many2one('{field_info.get('relation', 'res.partner')}', string='{field_name.title().replace('_', ' ')}')",
        'one2many': f"fields.One2many('{field_info.get('relation', 'res.partner')}', 'parent_id', string='{field_name.title().replace('_', ' ')}')",
        'many2many': f"fields.Many2many('{field_info.get('relation', 'res.partner')}', string='{field_name.title().replace('_', ' ')}')",
        'selection': f"fields.Selection([('option1', 'Option 1'), ('option2', 'Option 2')], string='{field_name.title().replace('_', ' ')}')",
    }
    
    definition = type_mapping.get(field_type, f"fields.Char(string='{field_name.title().replace('_', ' ')}')")
    
    # Add required flag if needed
    if field_info.get('required'):
        definition = definition.replace(')', ', required=True)')
    
    # Add readonly flag if needed  
    if field_info.get('readonly'):
        definition = definition.replace(')', ', readonly=True)')
    
    return f"    {field_name} = {definition}"

def generate_model_file(model_name, fields_for_model):
    """Generate model file content"""
    class_name = model_name.replace('.', '_').title()
    
    content = f'''# -*- coding: utf-8 -*-
from odoo import models, fields, api

class {class_name}(models.Model):
    _inherit = '{model_name}'

'''
    
    for field_info in fields_for_model:
        content += generate_field_definition(field_info) + '\n'
    
    return content

def generate_module_structure(report, module_name="hook_studio_replacement"):
    """Generate complete module structure"""
    module_path = Path(f"/Users/dgoo2308/git/captain-hook-smoke-house/{module_name}")
    
    # Create module directory
    module_path.mkdir(exist_ok=True)
    
    # Group fields by model - include ALL fields, not just those with data
    models_dict = {}
    for field_data in report['fields']:
        model = field_data['model']
        if model not in models_dict:
            models_dict[model] = []
        models_dict[model].append(field_data)
    
    # Generate __manifest__.py
    manifest_content = f'''# -*- coding: utf-8 -*-
{{
    'name': 'Captain Hook Studio Fields Replacement',
    'version': '18.0.1.0.0',
    'summary': 'Replace Studio fields with proper module fields',
    'description': """
        This module replaces Studio-created fields with proper module field definitions.
        Generated automatically from database analysis.
        
        Migrates ALL Studio fields including those with and without data.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'category': 'Technical',
    'depends': ['base', 'product', 'account', 'stock'],
    'data': [
        # Data files will be added here if needed
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}}
'''
    
    with open(module_path / "__manifest__.py", 'w') as f:
        f.write(manifest_content)
    
    # Generate __init__.py
    init_content = "# -*- coding: utf-8 -*-\nfrom . import models\n"
    with open(module_path / "__init__.py", 'w') as f:
        f.write(init_content)
    
    # Create models directory
    models_path = module_path / "models"
    models_path.mkdir(exist_ok=True)
    
    # Generate models __init__.py
    models_init = "# -*- coding: utf-8 -*-\n"
    
    # Generate model files
    for model_name, fields_list in models_dict.items():
        filename = model_name.replace('.', '_') + '.py'
        file_content = generate_model_file(model_name, fields_list)
        
        with open(models_path / filename, 'w') as f:
            f.write(file_content)
        
        models_init += f"from . import {filename[:-3]}\n"
    
    with open(models_path / "__init__.py", 'w') as f:
        f.write(models_init)
    
    total_fields = len(report['fields'])
    print(f"✓ Module generated at: {module_path}")
    print(f"✓ Generated files for {len(models_dict)} models")
    print(f"✓ Total fields migrated: {total_fields} (ALL Studio fields)")
    
    return module_path

def main():
    """Main function to generate replacement module"""
    print("=== Studio Fields Module Generator ===")
    
    # Load analysis report
    report = load_analysis_report()
    if not report:
        return
    
    print(f"Loaded analysis for {report['summary']['total_studio_fields']} Studio fields")
    print(f"Fields with data: {report['summary']['fields_with_data']}")
    
    if report['summary']['fields_with_data'] == 0:
        print("No Studio fields contain data - no module needed")
        return
    
    # Generate module
    module_path = generate_module_structure(report)
    
    print("\n=== Module Generation Complete ===")
    print("Next steps:")
    print("1. Review generated module files")
    print("2. Install module in Odoo")
    print("3. Test that data is preserved")
    print("4. Remove Studio fields from database")

if __name__ == "__main__":
    main()
