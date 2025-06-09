# Claude Development Guidelines

Guidelines for python script based data processing for Odoo development

## Environment Setup
- **Working Directory**: `/Users/dgoo2308/git/hook_fix`
- **Local Odoo**: `/Users/dgoo2308/git/odoo18` 
- **Custom Addons**: Located in hook directory within odoo18
- **Database**: `hook_local` (configured in odoo.conf)
- **Config**: `~/.odoo_config/hook_local.conf` (DO NOT edit - read only via `_config.py`)
- **Connection**: Use `connect_odoo('hook_local')` from `_config.py` for all XML-RPC connections

## Working Together Rules

### Code Organization
- **Keep programs small**: Split functionality into separate modules
- **Module naming**: Prefix all modules with underscore `_` (e.g., `_config.py`, `_contact_updater.py`)
- **No version suffixes**: Avoid names like `fixed`, `improved`, `final`, `v2` - work with one file and rewrite if needed
- **Clean workspace**: Avoid creating a mess of files

### Testing & Experimentation
- **TEST directory**: For small tests, data analysis, or inquiry scripts, create a `TEST/` directory
- **Reuse modules**: Always use our proven modules in tests - avoid duplicate code
- **No optimization focus**: Use proven modules to get the job done, optimization is not the priority

### Development Workflow
- **Git management**: 
  - Run `git init` at project start
  - Commit after each iteration
- **Proven solutions**: Use existing working modules rather than reinventing

### Logging & Output
- **Minimal verbosity**: Keep script output concise
- **Essential logging**:
  - Always log errors
  - Log warnings when appropriate
  - Show progress for long operations
- **Progress indicators**: 
  - For bulk operations (e.g., 100,000 records), show counters
  - Update progress every 50-100 operations so we know things are progressing

### File Structure Example
```
project_name/
├── _config.py          # Configuration module
├── _data_handler.py    # Data processing module
├── _odoo_client.py     # Odoo API client module
├── main_script.py      # Main execution script
├── TEST/               # Testing directory
│   ├── test_connection.py
│   └── analyze_data.py
└── README.md
```

### File Writing Guidelines
- Files over 50 lines get a warning but still work
- For better performance, aim for chunks under 45 lines when possible
- Don't worry about the warning - it's informational, not an error
- Large files can be written in one go if needed

### Example Progress Logging
```python
total = len(records)
for i, record in enumerate(records, 1):
    # Process record
    if i % 50 == 0 or i == total:
        print(f"Progress: {i}/{total} ({i/total*100:.1f}%)")
```

## Hook Fix Project Specific Guidelines

### Project Structure
```
hook_fix/
├── _config.py                    # Odoo connection module (supports 'hook' instance)
├── _contact_updater.py          # Contact classification module
├── classify_contacts.py         # Main classification script
├── tasks.md                     # Project tasks documentation
├── claude.md                    # This file - development guidelines
├── TEST/                        # Testing and analysis scripts
│   ├── test_hook_connection.py  # Test connection to Hook Odoo
│   └── analyze_contacts.py      # Analyze contact classification status
└── README.md                    # Project documentation
```

### Hook Odoo Instance Configuration
- **Config file**: `~/.odoo_config/hook_local.conf`
- **Database name**: `hook_local`
- **Instance name**: 'hook_local' (used in _config.py calls)
- **Access pattern**: Use `connect_odoo('hook_local')` for connections
- **Security**: NEVER read config files in scripts - they contain credentials

### Contact Classification Rules
- **Vendor Pattern**: Reference field starts with "V" (V1234, V5678, etc.)
  - Set `supplier_rank = 1` to make visible in Purchasing > Vendors
- **Customer Pattern**: Reference field starts with "C" (C1234, C5678, etc.)  
  - Set `customer_rank = 1` to make visible in Sales > Customers

### Task 1: Contact Classification
1. **Always use dry-run first**: Test with `--dry-run` before `--execute`
2. **Progress logging**: Show counts and progress for bulk operations
3. **Error handling**: Log all errors and continue processing other contacts
4. **Validation**: Verify contacts appear in correct Odoo sections after update

### Task 2: Studio Fields Migration (Future)
- **Target module**: `vct_product_customization`
- **Data preservation**: Critical - no data loss during migration
- **Backup requirement**: Full database backup before migration
- **Development approach**: Create module structure, test thoroughly, migrate data

### Safety Requirements
- **Backup before execution**: Always backup database before making changes
- **Dry-run validation**: Never skip dry-run testing
- **Rollback plan**: Document how to undo changes if needed
- **Small batches**: Process contacts in manageable batches for large datasets

### Odoo API Patterns for This Project
```python
# Connect to Hook local instance
models, db, uid, password = connect_odoo('hook_local')

# Search for vendor references
vendor_ids = models.execute_kw(
    db, uid, password, 'res.partner', 'search',
    [[['ref', '=like', 'V%']]]
)

# Update contact classification
models.execute_kw(
    db, uid, password, 'res.partner', 'write',
    [contact_id, {'supplier_rank': 1}]  # For vendors
)
```

### Testing Workflow
1. **Connection test**: `python TEST/test_hook_connection.py`
2. **Analysis**: `python TEST/analyze_contacts.py`
3. **Dry run**: `python classify_contacts.py --dry-run`
4. **Execute**: `python classify_contacts.py --execute`

---
*Focus: Safe, validated contact classification with zero data loss.*
