from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse

from analysis.static.analysis.pythonCode import Data, Include
import os
import io



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

def Correlation(request):
    form=[]
    data = Data.Data()
    data.CorrelationChemistry()
    otvet = []
    col = data.GetNameChemistry()
    if request.method == 'POST':
        list = request.POST.getlist('states[]')
        tip = request.POST['name3']
        if tip == 'Корреляция химического состава':
            data.SetType(0)
            data.CorrelationChemistry()
            col = data.GetNameChemistry()
        else:
            if tip == 'Корреляция видового состава':
                data.SetType(1)
                data.CorrelationZooplankton()
                col = data.GetNameZooplankton()
            else:
                print(list)

        # обработка вывода списка
        # names = request.POST['name']
        # otvet = data.AnalysisCorrelationChemistry(str(names))
        # otvet = data.AnalysisCorrelationZooplankton(str(names))
    return render(request, 'analysis/Correlation.html', {'col': col, 'otvet': otvet, 'form': form})

def PrintListCorrelation(request):
    form=[]
    data = Data.Data()
    type = data.GetType()
    data.CorrelationChemistry()
    otvet = []
    col = data.GetNameChemistry()
    if request.method == 'POST':
        names = request.POST['name']
        if type == 0:
            otvet = data.AnalysisCorrelationChemistry(str(names))
            col = data.GetNameChemistry()
        else:
            if type == 1:
                data.SetType(1)
                otvet = data.AnalysisCorrelationZooplankton(str(names))
                col = data.GetNameZooplankton()
            else:
                print(type)

    return render(request, 'analysis/Correlation.html', {'col': col, 'otvet': otvet, 'form': form})


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

def photoCorrelation(request):
    data = Data.Data()
    type = data.GetType()
    try:
        buffer = data.drawCorrelation(type)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response



def photoClustrering(request):
    data = Data.Data()
    try:
        buffer = data.drawDentogram(0)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoLSA(request):
    data = Data.Data()
    try:
        buffer = data.drawDentogram(1)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response