#!/usr/bin/env python3
"""
Complete Migration Workflow
Orchestrates the entire Studio fields migration process
"""

import sys
import os
import json
from pathlib import Path

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from _config import db_config
from _studio_analyzer import find_studio_fields, save_analysis_report
from _module_generator import generate_module_structure, load_analysis_report
from _database_cleaner import backup_field_definitions, remove_studio_field_definitions, verify_data_integrity

def step_1_analyze():
    """Step 1: Analyze Studio fields"""
    print("=== Step 1: Analyzing Studio Fields ===")
    
    # Test database connection
    if not db_config.test_connection():
        print("✗ Cannot connect to database")
        return False
    
    # Find Studio fields
    studio_fields = find_studio_fields()
    if not studio_fields:
        print("No Studio fields found")
        return False
    
    print(f"Found {len(studio_fields)} Studio fields")
    
    # Generate analysis report
    report = save_analysis_report(studio_fields, "studio_analysis_report.json")
    
    print(f"✓ Analysis complete - {report['summary']['fields_with_data']} fields have data")
    return True

def step_2_generate_module():
    """Step 2: Generate replacement module"""
    print("\n=== Step 2: Generating Replacement Module ===")
    
    report = load_analysis_report("studio_analysis_report.json")
    if not report:
        print("✗ No analysis report found")
        return False
    
    if report['summary']['fields_with_data'] == 0:
        print("No fields with data - no module needed")
        return True
    
    # Generate module
    module_path = generate_module_structure(report)
    print(f"✓ Module generated at: {module_path}")
    return True

def step_3_backup_and_cleanup():
    """Step 3: Backup and cleanup database"""
    print("\n=== Step 3: Database Backup and Cleanup ===")
    
    # Backup field definitions
    print("Backing up Studio field definitions...")
    if not backup_field_definitions():
        print("✗ Backup failed")
        return False
    
    # Dry run
    print("\nDry run cleanup...")
    if not remove_studio_field_definitions(dry_run=True):
        print("✗ Dry run failed")
        return False
    
    print("✓ Backup and dry run complete")
    return True

def step_4_final_cleanup():
    """Step 4: Final cleanup (interactive)"""
    print("\n=== Step 4: Final Cleanup ===")
    print("This step will actually remove Studio field definitions from the database")
    print("Make sure you have:")
    print("1. Installed the replacement module in Odoo")
    print("2. Verified that all data is accessible")
    print("3. Tested the application thoroughly")
    
    response = input("\nProceed with final cleanup? (yes/no): ").lower()
    if response != 'yes':
        print("Final cleanup postponed")
        return False
    
    # Remove Studio field definitions
    if not remove_studio_field_definitions(dry_run=False):
        print("✗ Cleanup failed")
        return False
    
    # Verify data integrity
    if not verify_data_integrity():
        print("✗ Data integrity check failed")
        return False
    
    print("✓ Final cleanup complete")
    return True

def main():
    """Main workflow"""
    print("=== Captain Hook Studio Fields Migration Workflow ===")
    
    # Step 1: Analyze
    if not step_1_analyze():
        print("Step 1 failed - cannot continue")
        return
    
    # Step 2: Generate module
    if not step_2_generate_module():
        print("Step 2 failed - cannot continue")
        return
    
    # Step 3: Backup and test cleanup
    if not step_3_backup_and_cleanup():
        print("Step 3 failed - cannot continue")
        return
    
    print("\n=== Phase 1 Complete ===")
    print("\nManual steps required:")
    print("1. cd /Users/dgoo2308/git/odoo18")
    print("2. ./manage_odoo.sh install hook_studio_replacement")
    print("3. Test that all Studio fields are working")
    print("4. Verify data integrity in the application")
    print("5. Run this script again to complete final cleanup")
    
    # Ask if they want to continue with final cleanup
    response = input("\nDo you want to proceed with final cleanup now? (yes/no): ").lower()
    if response == 'yes':
        step_4_final_cleanup()
    else:
        print("\nWorkflow paused. Run again when ready for final cleanup.")

if __name__ == "__main__":
    main()
