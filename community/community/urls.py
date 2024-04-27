from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('django.contrib.auth.urls'))
]

admin.site.site_header = "Community Builder"
admin.site.site_title = "Community Builder"
admin.site.index_title = "Welcome to Community Builder!"