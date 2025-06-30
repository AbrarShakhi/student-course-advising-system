from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=13, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, unique=True)
    guardian_name = models.CharField(max_length=128)
    guardian_phone = models.CharField(max_length=20)
    is_dismissed = models.BooleanField(default=False)
    is_graduated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"


class StudentLogin(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return f"{self.student.student_id}"
