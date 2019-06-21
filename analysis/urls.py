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
    path('PrintListClustering', views.ClusteringPr, name='PrintListClustering'),
    path('CLUSgroup', views.CLUSgroup, name='CLUSgroup'),
    path('LSA', views.LSAstr, name='LSA'),
    path('LSAgroup', views.LSAgroup, name='LSAgroup'),
    path('LDA', views.LDA, name='LDA'),
    path('Correlation.png', views.photoCorrelation, name='photoCorrelation'),
    path('Clustrering.png', views.photoClustrering, name='photoClustrering'),
    path('LSA.png', views.photoLSA, name='photoLSA'),
    path('pairplot.png', views.photoPairplotDescription, name='pairplot'),
    path('pairplot2.png', views.photoPairplotPlace, name='pairplot2'),
    path('corLSA.png', views.photoCorLSA, name='corLSA'),
    path('PCA.png', views.photoPCA, name='PCA'),
    path('PCAlsa.png', views.photoPCAlsa, name='PCAlsa')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)