from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('slovar.urls')),
]

from django.conf.urls.static import  static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
