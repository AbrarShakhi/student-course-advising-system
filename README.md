# student-course-advising-system

## Overview
A Flask REST API for managing student course advising, including admin, student, course, faculty, and section management.

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone the repository and enter the project directory
$ git clone <repo-url>
$ cd student-course-advising-system
```

### 2. Install Dependencies
```bash
# (Recommended) Create and activate a virtual environment
$ python3 -m venv venv
$ source venv/bin/activate

# Install required packages
$ pip install -r requirements.txt
```

### 3. Configure Environment
- Copy or create a `.env` file from `config/.example.env` in the project root:
  ```bash
  cp config/.example.env .env
  ```
- **Set your database connection string:**
  - Edit `.env` and set `DATABASE_URL=` to your database URI (e.g., `sqlite:///app.db` or your Postgres/MySQL URI).
- Edit configuration in `config/` as required (see `config/README.md` or script docs).

### 4. Initialize the Database
```bash
# The scripts will auto-create tables if they do not exist
```

### 5. Load Dummy Data (Optional)
To populate the database with sample data:
```bash
$ python scripts/load_dummy_data.py
```

### 6. Create an Admin User
```bash
$ python scripts/create_admin_user.py
```

### 7. Run the Application
```bash
$ python run.py
```

The API and admin panel will be available at `http://localhost:5000/` by default.

## Scripts
- `scripts/create_admin_user.py`: Creates a default admin user.
- `scripts/load_dummy_data.py`: Loads sample data from `scripts/dummy_data.json`.
- `scripts/test_admin.py`: Tests admin system and database setup.

## Troubleshooting
- Ensure you are running scripts from the project root.
- Activate your virtual environment if using one.
- Check your database configuration if you encounter connection issues.

## License
MIT (or your license here)