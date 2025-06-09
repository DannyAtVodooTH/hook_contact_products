#!/usr/bin/env python3
"""
Quick Start Script for Captain Hook Migration
Sets up everything and runs initial analysis
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_path, description):
    """Run a Python script and report results"""
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to run {description}: {e}")
        return False

def main():
    """Quick start workflow"""
    print("=== Captain Hook Migration Quick Start ===")
    
    # Step 1: Setup environment
    if not run_script("setup_environment.py", "Environment Setup"):
        print("Environment setup failed - check the errors above")
        return
    
    # Step 2: Test connection
    if not run_script("TEST/test_connection.py", "Database Connection Test"):
        print("Database connection failed - check your setup")
        return
    
    # Step 3: Analyze Studio fields
    if not run_script("TEST/test_studio_analysis.py", "Studio Fields Analysis"):
        print("Studio fields analysis failed")
        return
    
    # Step 4: Generate module
    if not run_script("TEST/test_module_generation.py", "Module Generation"):
        print("Module generation failed")
        return
    
    print("\n=== Quick Start Complete! ===")
    print("\nFiles created:")
    print("- studio_analysis_report.json")
    print("- /Users/dgoo2308/git/captain-hook-smoke-house/hook_studio_replacement/ (module)")
    
    print("\nNext steps:")
    print("1. Review the generated module")
    print("2. Install module: cd /Users/dgoo2308/git/odoo18 && ./manage_odoo.sh install hook_studio_replacement")
    print("3. Test thoroughly in Odoo")
    print("4. Run: python migration_workflow.py (for final cleanup)")

if __name__ == "__main__":
    main()
