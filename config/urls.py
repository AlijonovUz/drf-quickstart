from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

handler400 = "apps.utils.exceptions.handler400"
handler403 = "apps.utils.exceptions.handler403"
handler404 = "apps.utils.exceptions.handler404"
handler500 = "apps.utils.exceptions.handler500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
