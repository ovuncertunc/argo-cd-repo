from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('django.contrib.auth.urls'))
]

admin.site.site_header = "Community Builder"
admin.site.site_title = "Community Builder"
admin.site.index_title = "Welcome to Community Builder!"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)