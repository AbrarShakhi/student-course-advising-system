# Student Course Advising System

**[UNDER DEVELOPMENT]**

## Project Structure

```
student-course-advising-system/
├── student_course_advising_system/
│   ├── account/
│   ├── manage.py
│   └── student_course_advising_system/
├── requirements.txt
├── LICENSE
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/student-course-advising-system.git
   cd student-course-advising-system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate # on Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python student_course_advising_system/manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python student_course_advising_system/manage.py runserver
   ```

6. **Access the application:**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Development

- To create a superuser for the admin interface:
  ```bash
  python student_course_advising_system/manage.py createsuperuser
  ```

- API endpoints can be extended in the `account` app using Django REST Framework.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

