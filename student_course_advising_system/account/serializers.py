from rest_framework import serializers
from .models import StudentLogin

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLogin
        fields = ['studentId', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} 