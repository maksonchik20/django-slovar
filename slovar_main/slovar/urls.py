from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.main_slovar, name='main_slovar'),
    path('api/v1/get_data/<str:word>/', views.get_data_for_word, name='get_data_for_word'),
]
