from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('slovar.urls')),
    path(r'^files/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]
