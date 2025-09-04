# Student Course Advising System (Backend)

A Python Flask RESTful API for managing student course advising, including admin, student, course, faculty, and section management.
This backend powers the following mobile and web clients:
- [Student Course Advising Native (React Native)](https://github.com/Brick-C/student-course-advising-native)
- [Student Course Advising Admin Panel](https://github.com/Brick-C/student-course-advising-admin)

## Features

- Student, course, faculty, and section management
- Admin panel for user and data management
- RESTful API endpoints for mobile and web clients
- JWT authentication, OTP, and email notifications

## Showcase Videos

### Class Schedule Generation
[![Class Schedule Generation](https://img.youtube.com/vi/Srvguocoa8I/0.jpg)](https://youtu.be/Srvguocoa8I)
<iframe width="560" height="315" src="https://www.youtube.com/embed/Srvguocoa8I" frameborder="0" allowfullscreen></iframe>

### React Native Mobile App
[![React Native Mobile App](https://img.youtube.com/vi/B77Ff4M3OSE/0.jpg)](https://youtu.be/B77Ff4M3OSE)
<iframe width="560" height="315" src="https://www.youtube.com/embed/B77Ff4M3OSE" frameborder="0" allowfullscreen></iframe>

### Admin Panel
[![Admin Panel](https://img.youtube.com/vi/5QeuAQ-lrA8/0.jpg)](https://youtu.be/5QeuAQ-lrA8)
<iframe width="560" height="315" src="https://www.youtube.com/embed/5QeuAQ-lrA8" frameborder="0" allowfullscreen></iframe>

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd student-course-advising-system
```

### 2. Install Dependencies

It’s recommended to use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

- Copy the example environment file:
  ```bash
  cp config/.example.env .env
  ```
- Edit `.env` and set `DATABASE_URL` to your database URI (e.g., `sqlite:///app.db`).

### 4. Initialize the Database

Tables will be auto-created on first run.

### 5. (Optional) Load Dummy Data

```bash
python scripts/load_dummy_data.py
```

### 6. Create an Admin User

```bash
python scripts/create_admin_user.py
```

### 7. Run the Application

```bash
python run.py
```

The API and admin panel will be available at [http://localhost:5000/](http://localhost:5000/).

## Project Structure

- `app/` - Main application code (routes, controllers, models)
- `config/` - Configuration files
- `scripts/` - Utility scripts (admin creation, dummy data)
- `tests/` - Test cases

## Troubleshooting

- Run scripts from the project root
- Activate your virtual environment
- Check your database configuration if you encounter connection issues

## License

MIT (or specify your license)