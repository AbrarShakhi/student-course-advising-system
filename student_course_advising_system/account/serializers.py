from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
            "phone_no",
            "guardian_name",
            "guardian_phone",
            "is_dismissed",
            "is_graduated",
        ]
