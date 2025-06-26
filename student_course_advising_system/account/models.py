from django.db import models

# Create your models here.


class StudentLogin(models.Model):
    studentId = models.CharField(max_length=13, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.studentId} - {self.email}"
