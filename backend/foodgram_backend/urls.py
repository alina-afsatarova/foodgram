from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from recipes.utils import recipe_redirection


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('s/<str:short_link>', recipe_redirection),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
