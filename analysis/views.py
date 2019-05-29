from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from analysis.static.analysis.pythonCode import Data
import os


def index(request):
    if request.method == 'POST':

        folder = settings.MEDIA_ROOT
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        data = Data.Data()
        data.readFile(str(settings.MEDIA_ROOT) + '/' + str(file))
        return redirect('/table')

    return render(request, 'analysis/index.html')

def table(request):
    data = Data.Data()
    meas = data.GetDataTable()
    return render(request, 'analysis/table.html', {'measurement': meas})

def CorrelationChemistry(request):
    data = Data.Data()
    data.CorrelationChemistry()
    otvet = []
    chim = data.GetNameChemistry()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisCorrelationChemistry(str(names))
    return render(request, 'analysis/CorrelationСhemistry.html', {'Сhemistry': chim, 'otvet': otvet})

def CorrelationZooplankton(request):
    data = Data.Data()
    data.CorrelationZooplankton()
    otvet = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisCorrelationZooplankton(str(names))
    return render(request, 'analysis/CorrelationZooplankton.html', {'Zooplankton': col, 'otvet': otvet})

def ClusteringStr(request):
    data = Data.Data()
    data.clustering()
    otvet = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisClustering(names)

    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet})

def LSAstr(request):
    data = Data.Data()
    data.lsa()
    otvet = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisLSA(names)

    return render(request, 'analysis/LSA.html', {'Zooplankton': col, 'otvet': otvet})

