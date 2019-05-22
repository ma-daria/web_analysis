from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('table', views.table, name='table'),
    path('СorrelationСhemistry', views.СorrelationСhemistry, name='СorrelationСhemistry'),
    path('СorrelationZooplankton', views.СorrelationZooplankton, name='СorrelationZooplankton'),
    path('Сlustering', views.СlusteringStr, name='Сlustering'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)