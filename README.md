# Hook Fix Project

Fix contact classification and custom field migration for Hook Odoo instance.

## Quick Start

### Task 1: Contact Classification

1. **Test connection**:
   ```bash
   python TEST/test_hook_connection.py
   ```

2. **Analyze current state**:
   ```bash
   python TEST/analyze_contacts.py
   ```

3. **Run dry-run**:
   ```bash
   python classify_contacts.py --dry-run
   ```

4. **Execute classification**:
   ```bash
   python classify_contacts.py --execute
   ```

### Prerequisites
- Hook Odoo configuration in `~/.odoo_config/hook.conf`
- Python 3.x with required libraries
- Database backup before execution

## Project Structure
- `_config.py` - Odoo connection module
- `_contact_updater.py` - Classification logic
- `classify_contacts.py` - Main script
- `TEST/` - Testing and analysis scripts
- `tasks.md` - Detailed task documentation
- `implementation.md` - Technical implementation guide

## Safety
- Always run dry-run first
- Backup database before making changes
- Validate results after execution

See `implementation.md` for detailed technical documentation.
