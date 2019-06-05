from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('table', views.table, name='table'),
    path('Correlation', views.Correlation, name='Correlation'),
    path('PrintListCorrelation', views.PrintListCorrelation, name='PrintListCorrelation'),
    path('Clustering', views.ClusteringStr, name='Clustering'),
    path('LSA', views.LSAstr, name='LSA'),
    path('Correlation.png', views.photoCorrelation, name='photoCorrelation'),
    path('Clustrering.png', views.photoClustrering, name='photoClustrering'),
    path('LSA.png', views.photoLSA, name='photoLSA'),
    path('pairplot.png', views.photoPairplot, name='pairplot'),
    path('pairplot2.png', views.photoPairplot2, name='pairplot2')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)