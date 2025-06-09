#!/usr/bin/env python3
"""
Odoo Connection Configuration
Single configuration module for all Odoo connections via XML-RPC
"""

import xmlrpc.client
import configparser
import os
from pathlib import Path

def get_config(instance_name):
    """Read configuration from ~/.odoo_config/{instance_name}.conf"""
    config_path = Path.home() / '.odoo_config' / f'{instance_name}.conf'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    return {
        'url': config.get('odoo', 'url'),
        'database': config.get('odoo', 'database'), 
        'username': config.get('odoo', 'username'),
        'password': config.get('odoo', 'password')
    }

def connect_odoo(instance_name):
    """Connect to Odoo instance and return API objects"""
    config = get_config(instance_name)
    
    # Setup XML-RPC clients
    common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
    models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
    
    # Authenticate
    uid = common.authenticate(config['database'], config['username'], config['password'], {})
    
    if not uid:
        raise Exception(f"Authentication failed for {config['username']} on {config['database']}")
    
    return models, config['database'], uid, config['password']

def test_connection(instance_name):
    """Test connection and return basic info"""
    try:
        config = get_config(instance_name)
        common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
        
        # Test connection
        version = common.version()
        
        # Test authentication
        uid = common.authenticate(config['database'], config['username'], config['password'], {})
        if not uid:
            raise Exception("Authentication failed")
        
        # Get user info
        models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
        user_info = models.execute_kw(
            config['database'], uid, config['password'],
            'res.users', 'read', [uid], {'fields': ['name', 'login']}
        )[0]
        
        return {
            'instance': instance_name,
            'database': config['database'],
            'user_id': uid,
            'name': user_info['name'],
            'login': user_info['login'],
            'version': version.get('server_version', 'unknown')
        }
        
    except Exception as e:
        raise Exception(f"Connection test failed: {e}")
