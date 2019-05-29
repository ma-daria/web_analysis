from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('table', views.table, name='table'),
    path('CorrelationChemistry', views.CorrelationChemistry, name='CorrelationСhemistry'),
    path('CorrelationZooplankton', views.CorrelationZooplankton, name='CorrelationZooplankton'),
    path('Clustering', views.ClusteringStr, name='Clustering'),
    path('LSA', views.LSAstr, name='LSA'),
    path('CorrelationChemistry.png', views.photoCorrelationChemistry, name='photoCorrelationChemistry'),
    path('CorrelationZooplankton.png', views.photoCorrelationZooplankton, name='photoCorrelationZooplankton')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)