from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/user/v1/', include("user.urls")),
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    )
]
