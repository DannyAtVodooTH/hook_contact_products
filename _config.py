#!/usr/bin/env python3
"""
Odoo Configuration Module
Reads connection settings from ~/.odoo_config/{instance}.conf or environment variables
Environment variables take priority over config file values.
"""

import os
import configparser
import xmlrpc.client


def load_odoo_config(instance_name='kdm'):
    """
    Load Odoo connection configuration from standard location or environment
    
    Args:
        instance_name (str): Name of the instance config file (default: 'kdm')
                            Will load from ~/.odoo_config/{instance_name}.conf
    
    Environment variables (take priority):
        ODOO_DB - Database name
        ODOO_URL - Odoo server URL  
        ODOO_USER - Username
        ODOO_PASSWORD - Password
    """
    config_path = os.path.expanduser(f'~/.odoo_config/{instance_name}.conf')
    
    # Initialize config with environment variables (highest priority)
    config_data = {
        'url': os.getenv('ODOO_URL'),
        'database': os.getenv('ODOO_DB'), 
        'username': os.getenv('ODOO_USER'),
        'password': os.getenv('ODOO_PASSWORD')
    }
    
    # Load from config file if it exists and fill missing values
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if 'odoo' in config:
            # Only use config file values if not already set by environment
            if not config_data['url']:
                config_data['url'] = config.get('odoo', 'url', fallback=None)
            if not config_data['database']:
                config_data['database'] = config.get('odoo', 'database', fallback=None)
            if not config_data['username']:
                config_data['username'] = config.get('odoo', 'username', fallback=None)
            if not config_data['password']:
                config_data['password'] = config.get('odoo', 'password', fallback=None)
    
    # Validate required fields
    missing_fields = [key for key, value in config_data.items() if not value]
    if missing_fields:
        raise ValueError(
            f"Missing Odoo configuration: {', '.join(missing_fields)}\n"
            f"Please set environment variables or create {config_path} with:\n"
            "[odoo]\n"
            "url = https://your-odoo-instance.com\n"
            "database = your_database\n"
            "username = your_username\n"
            "password = your_password\n"
        )
    
    return config_data


def connect_odoo(instance_name='kdm'):
    """
    Connect to Odoo using configuration for specified instance
    
    Args:
        instance_name (str): Name of the instance config (default: 'kdm')
        
    Returns:
        tuple: (models, database, uid, password)
    """
    config = load_odoo_config(instance_name)
    
    try:
        common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
        uid = common.authenticate(config['database'], config['username'], 
                                config['password'], {})
        
        if not uid:
            raise Exception("Authentication failed - check username/password")
        
        models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
        
        return models, config['database'], uid, config['password']
        
    except Exception as e:
        raise Exception(f"Failed to connect to Odoo: {e}")


def test_connection(instance_name='kdm'):
    """
    Test Odoo connection and return user info
    
    Args:
        instance_name (str): Name of the instance config (default: 'kdm')
    """
    models, db, uid, password = connect_odoo(instance_name)
    
    # Test connection by getting user info
    user_info = models.execute_kw(db, uid, password, 'res.users', 'read', [uid], 
                                 {'fields': ['name', 'login']})
    
    return {
        'user_id': uid,
        'name': user_info[0]['name'],
        'login': user_info[0]['login'],
        'database': db,
        'instance': instance_name
    }


if __name__ == "__main__":
    # Test the connection
    import sys
    
    # Allow specifying instance name as command line argument
    instance = sys.argv[1] if len(sys.argv) > 1 else 'kdm'
    
    try:
        info = test_connection(instance)
        print(f"✅ Connection successful!")
        print(f"   Instance: {info['instance']}")
        print(f"   User: {info['name']} ({info['login']})")
        print(f"   Database: {info['database']}")
        print(f"   User ID: {info['user_id']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
