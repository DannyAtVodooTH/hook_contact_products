#!/usr/bin/env python3
"""
Studio Fields Analyzer - XML-RPC Version
Analyzes Studio fields using Odoo XML-RPC API
"""

import json
from _odoo_config import odoo_config

def find_studio_fields():
    """Find all Studio-created fields via XML-RPC"""
    
    # Search for Studio fields
    domain = [
        ('state', '=', 'manual'),
        ('name', 'like', 'x_studio_%'),
        ('name', '!=', 'x_studio_code')  # Exclude the incorrectly defined field
    ]
    
    fields = [
        'name', 'model', 'ttype', 'relation', 'store',
        'required', 'readonly', 'selection', 'help', 'translate'
    ]
    
    studio_fields = odoo_config.search_read('ir.model.fields', domain, fields)
    
    if not studio_fields:
        print("No Studio fields found")
        return []
    
    # Get model information
    model_names = list(set([field.get('model') for field in studio_fields if field.get('model')]))
    models_info = {}
    
    if model_names:
        models = odoo_config.search_read('ir.model', [('model', 'in', model_names)], ['model', 'name'])
        models_info = {m['model']: m['name'] for m in models}
    
    # Enhance field data with model display names
    for field in studio_fields:
        field['model_display_name'] = models_info.get(field['model'], field['model'])
    
    print(f"Found {len(studio_fields)} Studio fields (excluding x_studio_code)")
    return studio_fields

def analyze_field_data(field_info):
    """Analyze data in a Studio field via XML-RPC"""
    
    model = field_info['model']
    field_name = field_info['name']
    
    try:
        # Count total records in the model
        total_count = odoo_config.execute(model, 'search_count', [])
        
        if total_count == 0:
            return {
                'total_records': 0,
                'non_null_values': 0,
                'has_data': False,
                'sample_values': []
            }
        
        # Count records where the field is not False/empty
        non_null_domain = [(field_name, '!=', False)]
        non_null_count = odoo_config.execute(model, 'search_count', non_null_domain)
        
        # Get sample values (limit 5)
        sample_ids = odoo_config.execute(model, 'search', non_null_domain, {'limit': 5})
        sample_values = []
        
        if sample_ids:
            sample_records = odoo_config.execute(model, 'read', sample_ids, [field_name])
            sample_values = [record.get(field_name) for record in sample_records if record.get(field_name)]
        
        analysis = {
            'total_records': total_count,
            'non_null_values': non_null_count,
            'has_data': non_null_count > 0,
            'sample_values': sample_values[:5]  # Ensure max 5 samples
        }
        
        return analysis
        
    except Exception as e:
        return {'error': str(e)}

def save_analysis_report(studio_fields, filename="studio_fields_analysis.json"):
    """Save complete analysis report"""
    print(f"Analyzing {len(studio_fields)} Studio fields...")
    
    report = {
        'summary': {
            'total_studio_fields': len(studio_fields),
            'fields_with_data': 0,
            'fields_without_data': 0
        },
        'fields': []
    }
    
    for i, field in enumerate(studio_fields, 1):
        print(f"Analyzing field {i}/{len(studio_fields)}: {field['model']}.{field['name']}")
        
        field_analysis = analyze_field_data(field)
        field_report = {
            **field,
            'analysis': field_analysis
        }
        
        if field_analysis.get('has_data', False):
            report['summary']['fields_with_data'] += 1
        else:
            report['summary']['fields_without_data'] += 1
        
        report['fields'].append(field_report)
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nAnalysis complete!")
    print(f"Report saved to: {filename}")
    print(f"Total Studio fields: {report['summary']['total_studio_fields']}")
    print(f"Fields with data: {report['summary']['fields_with_data']}")
    print(f"Fields without data: {report['summary']['fields_without_data']}")
    
    return report
