#!/usr/bin/env python3
"""
Setup Environment for Captain Hook Migration
Creates symlinks, configs, and prepares environment
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Run shell command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return False
    return True

def create_symlink():
    """Create symlink for captain-hook-smoke-house"""
    source = Path("/Users/dgoo2308/git/captain-hook-smoke-house")
    target = Path("/Users/dgoo2308/git/odoo18/hook")
    
    if not source.exists():
        print(f"Error: Source directory {source} does not exist")
        return False
    
    if target.exists() or target.is_symlink():
        print(f"Removing existing {target}...")
        if target.is_symlink():
            target.unlink()
        else:
            # If it's a directory, be careful
            print(f"Warning: {target} exists as directory, not removing automatically")
            return False
    
    print(f"Creating symlink: {target} -> {source}")
    try:
        target.symlink_to(source)
        print("✓ Symlink created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create symlink: {e}")
        return False

def setup_database():
    """Setup local database for testing"""
    print("Setting up local database...")
    
    # Switch to hook_local configuration
    os.chdir("/Users/dgoo2308/git/odoo18")
    
    if not run_command("./switch_config.sh hook_local"):
        return False
    
    print("✓ Switched to hook_local configuration")
    
    # Import the backup
    backup_file = "/Users/dgoo2308/Downloads/odoo-ps-pshk-captain-hook-smoke-house-main-15749793_2025-06-09_042403_exact_fs.zip"
    
    if not Path(backup_file).exists():
        print(f"Warning: Backup file not found: {backup_file}")
        print("You'll need to import the backup manually later")
        return True
    
    print("Importing database backup...")
    if not run_command(f"./import_odoo_backup.sh '{backup_file}'"):
        print("Database import failed, but continuing...")
        return True
    
    print("✓ Database imported successfully")
    return True

def main():
    """Main setup function"""
    print("=== Captain Hook Environment Setup ===")
    
    # Step 1: Create symlink
    print("\n1. Creating symlink...")
    if not create_symlink():
        print("Failed to create symlink")
        return
    
    # Step 2: Setup database
    print("\n2. Setting up database...")
    if not setup_database():
        print("Database setup had issues")
        return
    
    print("\n=== Setup Complete! ===")
    print("\nNext steps:")
    print("1. Test connection: cd /Users/dgoo2308/git/hook_fix && python TEST/test_connection.py")
    print("2. Analyze Studio fields: python TEST/test_studio_analysis.py")
    print("3. Start Odoo: cd /Users/dgoo2308/git/odoo18 && ./manage_odoo.sh start")

if __name__ == "__main__":
    main()
