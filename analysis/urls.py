from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('table', views.table, name='table'),
    path('СorrelationСhemistry', views.CorrelationChemistry, name='СorrelationСhemistry'),
    path('СorrelationZooplankton', views.CorrelationZooplankton, name='СorrelationZooplankton'),
    path('Сlustering', views.ClusteringStr, name='Сlustering'),
    path('LSA', views.LSAstr, name='LSA')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)