from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_slovar, name='main_slovar')
]
