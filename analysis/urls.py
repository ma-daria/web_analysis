from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # пример тупо вызова функции
    path('change', views.change, name='change'),
]