from django.contrib import admin

from .models import Student, StudentLogin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "last_name",
        "email",
        "phone_no",
        "guardian_name",
        "guardian_phone",
        "is_dismissed",
        "is_graduated",
    )
    search_fields = ("student_id", "first_name", "last_name", "email", "phone_no")


class StudentLoginAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(StudentLogin, StudentLoginAdmin)
