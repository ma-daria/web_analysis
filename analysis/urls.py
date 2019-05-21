from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table', views.table, name='table')
    # пример тупо вызова функции
    # path('change', views.change, name='change'),
]