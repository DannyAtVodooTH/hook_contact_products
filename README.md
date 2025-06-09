# Captain Hook Studio Fields Migration

This project manages the migration from Odoo Studio fields to proper module fields while preserving all data and field names.

## Project Structure

```
hook_fix/
├── _config.py                 # Database configuration
├── _studio_analyzer.py        # Studio fields analysis
├── _module_generator.py       # Generates replacement module
├── _database_cleaner.py       # Database cleanup operations
├── setup_environment.py       # Environment setup
├── migration_workflow.py      # Complete migration workflow
├── TEST/
│   ├── test_connection.py     # Test database connection
│   ├── test_studio_analysis.py # Test Studio fields analysis
│   ├── test_module_generation.py # Test module generation
│   └── test_database_cleanup.py # Test cleanup operations
└── README.md
```

## Quick Start

### 1. Environment Setup

```bash
# Setup the environment (creates symlink, configs, database)
python setup_environment.py
```

### 2. Test Database Connection

```bash
cd TEST
python test_connection.py
```

### 3. Run Complete Migration

```bash
# Run the complete migration workflow
python migration_workflow.py
```

## Step-by-Step Process

### Phase 1: Analysis and Preparation

1. **Analyze Studio Fields**
   ```bash
   python TEST/test_studio_analysis.py
   ```
   - Scans database for Studio fields (`x_studio_*`)
   - Analyzes which fields contain data
   - Generates `studio_analysis_report.json`

2. **Generate Replacement Module**
   ```bash
   python TEST/test_module_generation.py
   ```
   - Creates proper Odoo module with field definitions
   - Only includes fields that contain data
   - Module location: `/Users/dgoo2308/git/captain-hook-smoke-house/hook_studio_replacement/`

3. **Backup and Test Cleanup**
   ```bash
   python TEST/test_database_cleanup.py
   ```
   - Backs up Studio field definitions
   - Performs dry-run cleanup
   - Tests data integrity verification

### Phase 2: Odoo Module Installation

1. **Install the Generated Module**
   ```bash
   cd /Users/dgoo2308/git/odoo18
   ./manage_odoo.sh install hook_studio_replacement
   ```

2. **Verify Everything Works**
   - Test all forms and views
   - Verify data is accessible
   - Check reports and exports

### Phase 3: Final Cleanup

1. **Remove Studio Field Definitions**
   ```bash
   python migration_workflow.py
   # Choose to proceed with final cleanup when prompted
   ```

## Environment Configurations

### Local Testing Environment
- **Config**: `hook_local.conf`
- **Database**: `hook_local`
- **Purpose**: Safe testing without affecting production

### Staging Environment  
- **Config**: `hook.conf`
- **Database**: `hook`
- **Purpose**: Final testing before production

### Production Environment
- **Database**: Production Captain Hook database
- **Purpose**: Final migration

## Configuration Files Created

### `/Users/dgoo2308/git/odoo18/hook_local.conf`
```ini
[options]
admin_passwd = admin
db_name = hook_local
db_host = localhost
addons_path = ./odoo/addons,./enterprise,./hook
# ... other settings
```

### Symlink Created
```bash
/Users/dgoo2308/git/odoo18/hook -> /Users/dgoo2308/git/captain-hook-smoke-house
```

## Safety Features

- **Dry Run**: All operations support dry-run mode
- **Backups**: Field definitions backed up before removal
- **Data Preservation**: Only removes field definitions, never data columns
- **Verification**: Data integrity checks at each step
- **Rollback**: Backup files allow restoration if needed

## Files Generated

- `studio_analysis_report.json` - Complete analysis of Studio fields
- `studio_fields_backup.json` - Backup of field definitions
- Module files in `/Users/dgoo2308/git/captain-hook-smoke-house/hook_studio_replacement/`

## Important Notes

1. **Data Safety**: The process never removes data columns, only field definitions
2. **Field Names**: Original field names (`x_studio_*`) are preserved in the database
3. **Module Fields**: New module uses clean field names (without `x_studio_` prefix)
4. **Testing**: Always test in local environment first
5. **Backup**: Database backups should be taken before any production changes

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Check database exists
psql -U odoo -l | grep hook_local
```

### Module Installation Issues
```bash
# Check Odoo logs
tail -f /Users/dgoo2308/git/odoo18/odoo.log

# Restart Odoo
./manage_odoo.sh restart
```

### Permission Issues
```bash
# Check file permissions in captain-hook-smoke-house directory
ls -la /Users/dgoo2308/git/captain-hook-smoke-house/
```

## Next Steps After Migration

1. **Remove Studio App**: Uninstall Studio from Odoo if no longer needed
2. **Update Documentation**: Document the new field structure
3. **Monitor Performance**: Check if there are any performance improvements
4. **Clean Exports**: Update any data exports to use new field names
