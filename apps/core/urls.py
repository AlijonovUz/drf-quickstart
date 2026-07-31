from django.urls import path, include

urlpatterns = [
    path("audits/", include("apps.core.audits.urls")),
]


