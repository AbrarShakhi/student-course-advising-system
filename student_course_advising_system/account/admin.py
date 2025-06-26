from django.contrib import admin
from .models import StudentLogin


@admin.register(StudentLogin)
class StudentLoginAdmin(admin.ModelAdmin):
    list_display = ("studentId", "email")
    search_fields = ("studentId", "email")
