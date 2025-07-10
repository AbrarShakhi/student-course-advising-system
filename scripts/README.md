# Scripts Directory

This directory contains utility scripts for the Student Course Advising System.

## Available Scripts

### `create_admin_user.py`
Creates the first admin user for the system.

**Usage:**
```bash
python scripts/create_admin_user.py
```

**What it does:**
- Creates database tables if they don't exist
- Creates a default admin user with credentials from config
- Default credentials (can be changed via environment variables):
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@example.com`

### `test_admin.py`
Tests the admin system to ensure everything is working correctly.

**Usage:**
```bash
python scripts/test_admin.py
```

**What it does:**
- Tests database table creation
- Tests AdminUser model functionality
- Creates and cleans up a test admin user
- Provides setup instructions

## Configuration

The scripts use the configuration system from the `config/` directory. You can customize the admin credentials by setting environment variables:

```bash
export ADMIN_USERNAME=myadmin
export ADMIN_PASSWORD=mypassword
export ADMIN_EMAIL=myadmin@example.com
```

Or by copying `config/env.example` to `.env` and modifying the values.

## Running Scripts

Make sure you're in the project root directory when running scripts:

```bash
cd /path/to/student-course-advising-system
python scripts/create_admin_user.py
```

## Troubleshooting

If you encounter import errors, make sure:
1. You're running the script from the project root directory
2. All dependencies are installed (`pip install -r requirements.txt`)
3. The virtual environment is activated (if using one)

## Adding New Scripts

When adding new scripts to this directory:

1. Follow the existing pattern with proper imports
2. Use the configuration system from `config/`
3. Add proper error handling
4. Update this README with documentation
5. Make scripts executable if needed: `chmod +x scripts/your_script.py` 