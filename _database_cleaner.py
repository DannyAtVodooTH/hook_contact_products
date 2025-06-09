#!/usr/bin/env python3
"""
Database Cleanup Module
Removes Studio field definitions while preserving data
"""

import json
from _config import db_config

def backup_field_definitions():
    """Backup Studio field definitions before removal"""
    conn = db_config.get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Get all Studio field definitions
    query = """
    SELECT 
        f.id, f.name, f.model, f.ttype, f.relation, f.store,
        f.required, f.readonly, f.selection, f.help, f.translate,
        m.model as model_name, m.name as model_display_name
    FROM ir_model_fields f
    JOIN ir_model m ON f.model_id = m.id
    WHERE f.state = 'manual'
    AND f.name LIKE 'x_studio_%'
    ORDER BY f.model, f.name;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    backup_data = []
    for row in results:
        field_backup = {
            'id': row[0],
            'name': row[1],
            'model': row[2],
            'ttype': row[3],
            'relation': row[4],
            'store': row[5],
            'required': row[6],
            'readonly': row[7],
            'selection': row[8],
            'help': row[9],
            'translate': row[10],
            'model_name': row[11],
            'model_display_name': row[12]
        }
        backup_data.append(field_backup)
    
    # Save backup
    with open('studio_fields_backup.json', 'w') as f:
        json.dump(backup_data, f, indent=2, default=str)
    
    print(f"✓ Backed up {len(backup_data)} Studio field definitions")
    cursor.close()
    conn.close()
    return True

def remove_studio_field_definitions(dry_run=True):
    """Remove Studio field definitions (keeping data columns)"""
    conn = db_config.get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Find Studio fields to remove
    query = """
    SELECT id, name, model
    FROM ir_model_fields
    WHERE state = 'manual'
    AND name LIKE 'x_studio_%'
    ORDER BY model, name;
    """
    
    cursor.execute(query)
    fields_to_remove = cursor.fetchall()
    
    print(f"Found {len(fields_to_remove)} Studio field definitions to remove")
    
    if dry_run:
        print("DRY RUN - No changes will be made")
        for field_id, field_name, model in fields_to_remove:
            print(f"  Would remove: {model}.{field_name} (ID: {field_id})")
        cursor.close()
        conn.close()
        return True
    
    # Actually remove the field definitions
    removed_count = 0
    for field_id, field_name, model in fields_to_remove:
        try:
            # Remove from ir_model_fields
            cursor.execute("DELETE FROM ir_model_fields WHERE id = %s", (field_id,))
            print(f"✓ Removed field definition: {model}.{field_name}")
            removed_count += 1
        except Exception as e:
            print(f"✗ Failed to remove {model}.{field_name}: {e}")
    
    # Commit changes
    conn.commit()
    print(f"✓ Removed {removed_count} Studio field definitions")
    
    cursor.close()
    conn.close()
    return True

def verify_data_integrity():
    """Verify that data columns still exist after field definition removal"""
    conn = db_config.get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Load our analysis to know what to check
    try:
        with open('TEST/studio_analysis_report.json', 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        print("No analysis report found - cannot verify data integrity")
        return False
    
    print("Verifying data integrity...")
    
    for field_data in report['fields']:
        if not field_data['analysis'].get('has_data', False):
            continue  # Skip fields without data
        
        model = field_data['model']
        field_name = field_data['field_name']
        table_name = model.replace('.', '_')
        
        try:
            # Check if column still exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = %s AND column_name = %s
                );
            """, (table_name, field_name))
            
            column_exists = cursor.fetchone()[0]
            
            if column_exists:
                # Check if data is still there
                cursor.execute(f"SELECT COUNT({field_name}) FROM {table_name} WHERE {field_name} IS NOT NULL")
                data_count = cursor.fetchone()[0]
                expected_count = field_data['analysis']['non_null_values']
                
                if data_count == expected_count:
                    print(f"✓ {model}.{field_name}: Data intact ({data_count} records)")
                else:
                    print(f"✗ {model}.{field_name}: Data mismatch! Expected {expected_count}, found {data_count}")
            else:
                print(f"✗ {model}.{field_name}: Column missing!")
        
        except Exception as e:
            print(f"✗ {model}.{field_name}: Error checking - {e}")
    
    cursor.close()
    conn.close()
    return True

def main():
    """Main cleanup function"""
    print("=== Database Cleanup ===")
    
    # Step 1: Backup field definitions
    print("1. Backing up Studio field definitions...")
    if not backup_field_definitions():
        print("Backup failed - aborting")
        return
    
    # Step 2: Dry run removal
    print("\n2. Dry run removal...")
    if not remove_studio_field_definitions(dry_run=True):
        print("Dry run failed - aborting")
        return
    
    # Step 3: Ask for confirmation
    print("\n3. Ready to remove Studio field definitions")
    print("This will remove the field definitions but keep the data columns")
    response = input("Continue? (yes/no): ").lower()
    
    if response != 'yes':
        print("Aborted by user")
        return
    
    # Step 4: Actual removal
    print("\n4. Removing Studio field definitions...")
    if not remove_studio_field_definitions(dry_run=False):
        print("Removal failed")
        return
    
    # Step 5: Verify data integrity
    print("\n5. Verifying data integrity...")
    verify_data_integrity()
    
    print("\n=== Cleanup Complete ===")

if __name__ == "__main__":
    main()
