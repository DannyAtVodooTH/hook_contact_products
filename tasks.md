# Hook Fix Project Tasks

## Project Overview
This project addresses two main tasks for the Hook Odoo instance:

### Task 1: Contact Classification Fix
**Problem**: Contacts were uploaded as general contacts but not properly classified as customers or vendors, making them not visible in Sales/Customers or Purchasing/Vendors sections.

**Solution**: Classify contacts based on reference field patterns:
- `Vxxxx` references → Mark as Vendor (supplier_rank = 1)
- `Cxxxx` references → Mark as Customer (customer_rank = 1)

### Task 2: Custom Fields Migration
**Problem**: Hong Kong Odoo instance has custom fields created via Studio application in Odoo 18. Need to replace Studio fields with proper custom module for better maintainability and future extensibility.

**Solution**: Create `vct_product_customization` module to replace Studio fields while preserving existing data.

## Task 1: Contact Classification Implementation

### Prerequisites
- Access to Hook Odoo instance via `~/.odoo_config/hook.conf`
- XML-RPC API access
- Read/write permissions on `res.partner` model

### Steps
1. **Analysis Phase** (TEST directory)
   - Test connection to Hook instance
   - Analyze existing contacts with V*/C* reference patterns
   - Identify contacts needing classification

2. **Implementation Phase**
   - Create classification script using `_contact_updater.py` module
   - Implement dry-run functionality for safety
   - Execute classification updates

3. **Validation Phase**
   - Verify contacts appear in correct sections
   - Test customer/vendor functionality

### Files to Create
- `TEST/test_hook_connection.py` - Test connection
- `TEST/analyze_contacts.py` - Analyze contact patterns
- `classify_contacts.py` - Main classification script

## Task 2: Custom Module Migration

### Prerequisites
- Access to Hong Kong Odoo 18 instance
- Studio field definitions and data
- Development environment for custom module creation

### Steps
1. **Analysis Phase**
   - Document existing Studio fields
   - Export current field data
   - Identify field types and dependencies

2. **Module Development**
   - Create `vct_product_customization` module structure
   - Define fields in Python models
   - Create data migration scripts

3. **Migration Phase**
   - Test module in development environment
   - Create data preservation scripts
   - Execute migration with rollback plan

### Files to Create
- `migration_analysis.md` - Studio fields documentation
- `vct_product_customization/` - Custom module directory
- `migrate_studio_fields.py` - Migration script

## Success Criteria

### Task 1
- [ ] All V* referenced contacts appear in Purchasing > Vendors
- [ ] All C* referenced contacts appear in Sales > Customers
- [ ] No data loss or corruption
- [ ] Classification can be verified in contact forms

### Task 2
- [ ] All Studio fields replaced with custom module fields
- [ ] All existing data preserved
- [ ] Module properly installed and functional
- [ ] Future field additions can be done through code

## Risk Management
- **Backup Strategy**: Full database backup before any updates
- **Dry Run Testing**: All scripts support dry-run mode
- **Rollback Plan**: Document rollback procedures for both tasks
- **Validation Scripts**: Create verification scripts to confirm success
