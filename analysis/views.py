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
    meas = []
    data = Data.Data()
    measur = data.GetData()
    reservoir = measur['Водоем']
    date = measur['Дата']
    plase = measur['Место измерения']
    point = measur['Описание точки измерения']
    mass = measur['биомасса ФП']
    for i in range(len(reservoir)):
        meas.append([reservoir[i], date[i], plase[i], point[i], mass[i]])
    return render(request, 'analysis/table.html', {'measurement': meas})

def CorrelationChemistry(request):
    data = Data.Data()
    data.CorrelationChemistry()
    res = []
    ind = []
    chim = data.GetNameChemistry()
    if request.method == 'POST':
        names = request.POST['name']
        ress = data.AnalysisCorrelationChemistry(str(names))
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    otvet = []
    for i in range(len(res)):
        otvet.append([ind[i], res[i]])
    return render(request, 'analysis/СorrelationСhemistry.html', {'Сhemistry': chim, 'otvet': otvet})

def CorrelationZooplankton(request):
    data = Data.Data()
    data.CorrelationZooplankton()
    res = []
    ind = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        ress = data.AnalysisCorrelationZooplankton(str(names))
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    otvet = []
    for i in range(len(res)):
        otvet.append([ind[i], res[i]])
    return render(request, 'analysis/СorrelationZooplankton.html', {'Zooplankton': col, 'otvet': otvet})

def ClusteringStr(request):
    data = Data.Data()
    data.clustering()
    otvet = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        i = 0
        for i in range(col.size):
            if col[i] == names:
                break
        otvet = data.AnalysisClustering(i)

    return render(request, 'analysis/Сlustering.html', {'Zooplankton': col, 'otvet': otvet})

def LSAstr(request):
    data = Data.Data()
    data.lsa()
    otvet = []
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        i = 0
        for i in range(col.size):
            if col[i] == names:
                break
        otvet = data.AnalysisLSA(i)

    return render(request, 'analysis/LSA.html', {'Zooplankton': col, 'otvet': otvet})

