from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse

from analysis.static.analysis.pythonCode import Data_analysis, Include
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
        data = Data_analysis.Data_analysis()
        data.readFile(str(settings.MEDIA_ROOT) + '/' + str(file))
        return redirect('/table')

    return render(request, 'analysis/index.html')

def table(request):
    data = Data_analysis.Data_analysis()
    name = data.GetNameAll()
    size = data.GetSizeData()
    sizeP = name.size
    sizeI = data.GetSizeChemistry()
    sizeV = data.GetSizeZooplankton()
    return render(request, 'analysis/table.html', { 'nameC': name, 'size': size, 'sizeP': sizeP, 'sizeI': sizeI, 'sizeV': sizeV})


def Correlation(request):
    form=[]
    data = Data_analysis.Data_analysis()
    data.CorrelationChemistry()
    otvet = []
    col = data.GetNameChemistry()

    col1 = data.GetNameChemistry()
    col2 = data.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()

    id = data.GetType()

    size = data.GetSizeChemistry()

    if request.method == 'POST':
        list = request.POST.getlist('states[]')
        tip = request.POST['name3']
        if tip == 'Химический состав':
            data.SetType(Include.СHEMISTRY)
            id = Include.СHEMISTRY
            data.CorrelationChemistry()
            col = data.GetNameChemistry()
            size = data.GetSizeChemistry()
        else:
            if tip == 'Видовой состав':
                data.SetType(Include.ZOOPLANKTON)
                id = Include.ZOOPLANKTON
                data.CorrelationZooplankton()
                col = data.GetNameZooplankton()
                size = data.GetSizeZooplankton()
            else:
                data.SetType(Include.MIX)
                id = Include.MIX
                data.CorrelationMix(list)
                col = list
                data.SetList(list)
                size = data.GetSizeMix()


    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': id, 'size': size})

def PrintListCorrelation(request):
    size = data.GetSizeChemistry()
    form=[]
    data = Data_analysis.Data_analysis()
    type = data.GetType()
    data.CorrelationChemistry()
    otvet = []
    col = data.GetNameChemistry()

    col1 = data.GetNameChemistry()
    col2 = data.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()

    if request.method == 'POST':
        names = request.POST['name']
        if type == Include.СHEMISTRY:
            otvet = data.AnalysisCorrelationChemistry(str(names))
            col = data.GetNameChemistry()
            size = data.GetSizeChemistry()
        else:
            if type == Include.ZOOPLANKTON:
                otvet = data.AnalysisCorrelationZooplankton(str(names))
                col = data.GetNameZooplankton()
                size = data.GetSizeZooplankton()
            else:
                otvet = data.AnalysisCorrelationMix(str(names))
                col = Include.pd.Series(data.GetList())
                size = data.GetSizeMix()
        col = col[col != names]
        col = [names] + col.tolist()

    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': type, 'size': size})


def ClusteringStr(request):
    data = Data_analysis.Data_analysis()
    data.clustering()
    otvet = []
    names = ''
    col = data.GetNameZooplankton()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisClustering(names)
        col = col[col != names]
        col = [names] + col.tolist()

    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names})

def LSAstr(request):
    data = Data_analysis.Data_analysis()
    data.lsa()
    otvet = []
    col = data.GetNameZooplankton()
    data.CorrelationLSA()
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisLSA(names)
        col = col[col != names]
        col = [names] + col.tolist()

    return render(request, 'analysis/LSA.html', {'Zooplankton': col, 'otvet': otvet})

def photoCorrelation(request):
    data = Data_analysis.Data_analysis()
    type = data.GetType()
    try:
        buffer = data.drawCorrelation(type)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response



def photoClustrering(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawDentogram(0)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoLSA(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawDentogram(1)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoPairplot(request):
    data = Data_analysis.Data_analysis()
    if data.GetType() == Include.MIX:
        try:
            buffer = data.drawPairplot()
        except:
            buffer = Include.io.BytesIO()
            print("Не удалось загрузить график")
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response
    else:
        buffer = Include.io.BytesIO()
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response

def photoPairplot2(request):
    data = Data_analysis.Data_analysis()
    if data.GetType() == Include.MIX:
        try:
            buffer = data.drawPairplot2()
        except:
            buffer = Include.io.BytesIO()
            print("Не удалось загрузить график")
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response
    else:
        buffer = Include.io.BytesIO()
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response

def photoCorLSA(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawCorrelation(4)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response