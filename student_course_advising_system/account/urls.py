from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns(
    [
        path("login", views.LoginStudent.as_view(), name="LoginStudent"),
        path("logout", views.LogoutStudent.as_view(), name="LogoutStudent"),
        path("activate", views.ActivateStudent.as_view(), name="ActivateStudent"),
    ]
)
