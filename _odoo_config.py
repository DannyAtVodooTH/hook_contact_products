#!/usr/bin/env python3
"""
Odoo XML-RPC Configuration
Reads from ~/.odoo_config/{env}.conf files and provides XML-RPC connections
Compatible with classify_contacts.py pattern
"""

import xmlrpc.client
import configparser
import os
from pathlib import Path

class OdooConfig:
    """Odoo configuration management - reads from ~/.odoo_config/ files"""
    
    def __init__(self, env_name="hook_local"):
        self.env_name = env_name
        self.config_dir = Path.home() / ".odoo_config"
        self.config_file = self.config_dir / f"{env_name}.conf"
        
        # Default values
        self.url = "http://localhost:8069"
        self.db_name = env_name
        self.username = "admin"
        self.password = "admin"
        
        # XML-RPC connection
        self.uid = None
        self.common = None
        self.models = None
        
        # Load configuration and setup
        self.load_config()
        self.setup_xmlrpc()
    
    def load_config(self):
        """Load configuration from ~/.odoo_config/{env}.conf file"""
        if not self.config_file.exists():
            print(f"Config file {self.config_file} not found, using defaults")
            print(f"Create {self.config_file} with:")
            print("[odoo]")
            print(f"url = {self.url}")
            print(f"db_name = {self.db_name}")
            print(f"username = {self.username}")
            print(f"password = {self.password}")
            return
        
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            if 'odoo' in config:
                odoo_section = config['odoo']
                self.url = odoo_section.get('url', self.url)
                self.db_name = odoo_section.get('db_name', self.db_name)
                self.username = odoo_section.get('username', self.username)
                self.password = odoo_section.get('password', self.password)
            
            print(f"✓ Loaded configuration from {self.config_file}")
            print(f"  URL: {self.url}")
            print(f"  Database: {self.db_name}")
            print(f"  Username: {self.username}")
            
        except Exception as e:
            print(f"Error reading config file: {e}")
    
    def setup_xmlrpc(self):
        """Setup XML-RPC clients"""
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        except Exception as e:
            print(f"Error setting up XML-RPC: {e}")
    
    def authenticate(self):
        """Authenticate with Odoo"""
        if not self.common:
            print("✗ XML-RPC not initialized")
            return False
            
        try:
            self.uid = self.common.authenticate(self.db_name, self.username, self.password, {})
            if self.uid:
                print(f"✓ Authenticated as {self.username} (UID: {self.uid})")
                return True
            else:
                print("✗ Authentication failed")
                return False
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    def test_connection(self):
        """Test Odoo connection and authentication"""
        try:
            # Test connection
            version = self.common.version()
            print(f"✓ Connected to Odoo {version.get('server_version', 'unknown')}")
            
            # Test authentication
            return self.authenticate()
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            print(f"Make sure Odoo is running on {self.url}")
            return False
    
    def execute(self, model, method, *args, **kwargs):
        """Execute model method via XML-RPC"""
        if not self.uid:
            if not self.authenticate():
                return None
        
        try:
            return self.models.execute_kw(
                self.db_name, self.uid, self.password,
                model, method, args, kwargs
            )
        except Exception as e:
            print(f"✗ Error executing {model}.{method}: {e}")
            return None
    
    def search_read(self, model, domain=None, fields=None, limit=None):
        """Search and read records"""
        domain = domain or []
        kwargs = {}
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit
            
        return self.execute(model, 'search_read', domain, **kwargs)

def get_odoo_config(env_name):
    """Get Odoo configuration for specific environment"""
    return OdooConfig(env_name)

# For hook_fix project - use hook_local by default
odoo_config = OdooConfig("hook_local")
