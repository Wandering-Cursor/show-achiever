from django.contrib import admin
from django.urls import path

# If Django admin is not used - feel free to remove this line
urlpatterns = [
    path("admin/", admin.site.urls),
]
