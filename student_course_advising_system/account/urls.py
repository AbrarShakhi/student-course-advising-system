from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = format_suffix_patterns(
    [path("test/", views.TestView.as_view(), name="login")]
)
