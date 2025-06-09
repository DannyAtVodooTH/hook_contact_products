# Hook Fix Implementation Documentation

## Task 1: Contact Classification Implementation

### Overview
Fix contact classification in Hook Odoo instance where contacts were uploaded but not properly categorized as customers or vendors, making them invisible in Sales/Customers and Purchasing/Vendors sections.

### Technical Approach

#### Problem Analysis
- Contacts have reference patterns: `Vxxxx` (vendors) and `Cxxxx` (customers)
- All contacts were imported as general partners (`res.partner` records)
- Missing classification fields: `customer_rank` and `supplier_rank` set to 0
- Odoo uses these rank fields to determine visibility in customer/vendor views

#### Solution Design
```python
# Classification Logic
if reference.startswith('V'):
    update_fields = {'supplier_rank': 1}  # Makes visible in Vendors
elif reference.startswith('C'):
    update_fields = {'customer_rank': 1}  # Makes visible in Customers
```

#### Implementation Components

**1. Configuration Module (`_config.py`)**
- Handles connection to 'hook' Odoo instance
- Reads from `~/.odoo_config/hook.conf`
- Provides `connect_odoo('hook')` function

**2. Contact Updater Module (`_contact_updater.py`)**
- `find_contacts_by_reference_pattern()` - Search V*/C* patterns
- `get_contact_details()` - Retrieve current classification status
- `update_contact_classification()` - Set customer_rank/supplier_rank
- `classify_contacts_by_reference()` - Main classification function

**3. Main Script (`classify_contacts.py`)**
- Command-line interface with --dry-run and --execute options
- Safety confirmation for actual updates
- Progress reporting and error handling

**4. Testing Scripts (TEST/ directory)**
- `test_hook_connection.py` - Validate Odoo connection
- `analyze_contacts.py` - Analyze current classification status

### Execution Plan

#### Phase 1: Testing & Analysis
1. **Test Connection**
   ```bash
   cd ~/git/hook_fix
   python TEST/test_hook_connection.py
   ```
   - Validates Odoo connection
   - Shows basic system statistics

2. **Analyze Current State**
   ```bash
   python TEST/analyze_contacts.py
   ```
   - Counts V*/C* referenced contacts
   - Identifies which need classification
   - Shows sample contacts needing updates

#### Phase 2: Dry Run Validation
```bash
python classify_contacts.py --dry-run
```
- Shows exactly what would be updated
- No actual changes made
- Validates logic before execution

#### Phase 3: Execute Classification
```bash
python classify_contacts.py --execute
```
- Prompts for confirmation
- Updates contact classifications
- Reports success/failure for each contact

### Expected Results
- V* referenced contacts appear in Purchasing > Vendors
- C* referenced contacts appear in Sales > Customers
- No impact on existing properly classified contacts
- All data preserved, only rank fields updated

### Rollback Procedure
If issues occur:
1. **Database restore** from pre-execution backup
2. **Manual correction** via Odoo interface:
   - Go to Contacts
   - Find affected contacts
   - Uncheck "Is a Customer" or "Is a Vendor" as needed

### Validation Steps
1. **Check Vendor View**: Purchasing > Vendors should show V* contacts
2. **Check Customer View**: Sales > Customers should show C* contacts
3. **Verify Contact Forms**: Individual contacts show correct classification
4. **Test Functionality**: Can create purchase orders for vendors, sales orders for customers

---

## Task 2: Studio Fields Migration Implementation

### Overview
Replace Odoo Studio-created custom fields with proper custom module `vct_product_customization` for better maintainability and future extensibility while preserving all existing data.

### Technical Approach

#### Problem Analysis
- Hong Kong Odoo 18 instance uses Studio application for custom fields
- Studio fields stored in database without proper module structure
- Difficult to version control, deploy, or extend
- Need to preserve all existing field data during migration

#### Solution Design
1. **Analysis Phase**: Document all Studio fields and their data
2. **Module Creation**: Build `vct_product_customization` module
3. **Data Migration**: Transfer Studio field data to module fields
4. **Studio Cleanup**: Remove Studio fields after successful migration

### Implementation Components

#### Phase 1: Studio Field Analysis
**Create analysis script to document:**
- Field names and types
- Field locations (models they're attached to)
- Current data values
- Field properties (required, default values, etc.)
- Dependencies and relationships

**Deliverables:**
- `studio_fields_analysis.py` - Export Studio field definitions
- `studio_data_export.py` - Backup current field data
- `migration_analysis.md` - Documentation of findings

#### Phase 2: Custom Module Development
**Module Structure:**
```
vct_product_customization/
├── __manifest__.py              # Module manifest
├── __init__.py                  # Python package init
├── models/
│   ├── __init__.py
│   ├── product_template.py      # Product template extensions
│   └── product_product.py       # Product variant extensions
├── views/
│   ├── product_views.xml        # Form/tree view modifications
│   └── menu_items.xml           # Menu customizations
├── data/
│   └── default_data.xml         # Default values if needed
└── README.md                    # Module documentation
```

**Key Module Features:**
- Inherit existing Odoo models (product.template, product.product)
- Define custom fields in Python code
- Create proper form views for custom fields
- Ensure field types match Studio field types exactly

#### Phase 3: Data Migration Strategy
**Migration Script Components:**
1. **Pre-migration validation**
   - Verify module installation
   - Confirm field structure matches
   - Backup current data

2. **Data transfer process**
   - Map Studio field data to module fields
   - Handle data type conversions if needed
   - Validate data integrity

3. **Post-migration verification**
   - Confirm all data transferred correctly
   - Test field functionality
   - Verify views and forms work properly

### Development Workflow

#### Step 1: Environment Setup
```bash
# Create development environment
mkdir ~/git/vct_product_customization
cd ~/git/vct_product_customization

# Initialize git repository
git init
git add .
git commit -m "Initial module structure"
```

#### Step 2: Analysis Scripts
Create analysis tools to understand current Studio setup:
- Document field definitions
- Export current data
- Identify dependencies

#### Step 3: Module Development
Build custom module following Odoo development best practices:
- Proper model inheritance
- XML view definitions
- Security rules if needed
- Module dependencies

#### Step 4: Testing & Migration
1. **Development testing** in separate database
2. **Data migration scripts** with rollback capability
3. **Production migration** with full backup

### Risk Mitigation

#### Backup Strategy
- **Full database backup** before any changes
- **Studio field data export** as additional safety
- **Module backup** of custom module files

#### Rollback Plan
If migration fails:
1. **Database restore** from pre-migration backup
2. **Studio field restoration** if partial migration occurred
3. **Module removal** and Studio field recreation if needed

#### Testing Strategy
- **Development environment** for initial testing
- **Staging environment** for full migration rehearsal
- **User acceptance testing** before production deployment

### Success Criteria
- [ ] All Studio fields replaced with module fields
- [ ] All existing data preserved exactly
- [ ] Custom module properly installed and functional
- [ ] Views and forms work identically to Studio version
- [ ] Future field additions can be done through code
- [ ] Module can be version controlled and deployed

### Timeline Estimate
- **Analysis Phase**: 2-3 days
- **Module Development**: 3-5 days
- **Testing & Migration**: 2-3 days
- **Total**: 7-11 days

This documentation provides the framework for both tasks. Task 1 is ready for immediate execution, while Task 2 requires the analysis phase to begin before detailed implementation planning.
