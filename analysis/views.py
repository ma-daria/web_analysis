from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse

from analysis.static.analysis.pythonCode import Data_analysis, Include
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
    data.Correlation(0)
    otvet = []
    col = data.GetNameChemistry()
    sizeI = data.GetSizeData()
    col1 = data.GetNameChemistry()
    col2 = data.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()
    corMax = data.CorrelationMax(0)
    id = data.GetType()
    size = data.GetSizeChemistry()
    if request.method == 'POST':
        list = request.POST.getlist('states[]')
        tip = request.POST['name3']
        if tip == 'Химический состав':
            data.SetType(Include.CHEMISTRY)
            id = Include.CHEMISTRY
            data.Correlation(id)
            col = data.GetNameChemistry()
            size = data.GetSizeChemistry()
            corMax = data.CorrelationMax(id)
        else:
            if tip == 'Видовой состав':
                data.SetType(Include.ZOOPLANKTON)
                id = Include.ZOOPLANKTON
                data.Correlation(id)
                col = data.GetNameZooplankton()
                size = data.GetSizeZooplankton()
                corMax = data.CorrelationMax(id)
            else:
                data.SetList(list)
                data.SetType(Include.MIX)
                id = Include.MIX
                data.Correlation(id)
                col = list
                size = data.GetSizeMix()
                corMax = data.CorrelationMax(id)
    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': id, 'size': size, 'sizeI': sizeI, 'corMax': corMax})

def PrintListCorrelation(request):
    data = Data_analysis.Data_analysis()
    size = data.GetSizeChemistry()
    form=[]
    data = Data_analysis.Data_analysis()
    type = data.GetType()
    otvet = []
    col = data.GetNameChemistry()
    sizeI = data.GetSizeData()
    col1 = data.GetNameChemistry()
    col2 = data.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()
    corMax = []
    if request.method == 'POST':
        names = request.POST['name']
        if type == Include.CHEMISTRY:
            otvet = data.AnalysisCorrelation(str(names), type)
            col = data.GetNameChemistry()
            size = data.GetSizeChemistry()
            corMax = data.CorrelationMaxChemistry()
        else:
            if type == Include.ZOOPLANKTON:
                otvet = data.AnalysisCorrelation(str(names), type)
                col = data.GetNameZooplankton()
                size = data.GetSizeZooplankton()
                corMax = data.CorrelationMaxZooplankton()
            else:
                otvet = data.AnalysisCorrelation(str(names), type)
                col = Include.pd.Series(data.GetList())
                size = data.GetSizeMix()
                corMax = data.CorrelationMaxMix()
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': type, 'size': size, 'sizeI': sizeI, 'corMax': corMax})


def ClusteringStr(request):
    data = Data_analysis.Data_analysis()
    size = data.GetSizeZooplankton()
    sizeI = data.GetSizeData()
    data.Clustering(0)
    otvet = []
    names = ''
    col = data.GetNameZooplankton()
    type = Include.CL_ZOOPLANKTON
    otvet2 = []
    val = str(0.2)
    if request.method == 'POST':
        tip = request.POST['name3']
        if tip == 'Точки измерения':
            data.SetType_cla(Include.CL_CHEMISTRY)
            data.Clustering(Include.CL_CHEMISTRY)
            col = data.GetNameChemistryRes()
            size = data.GetSizeData()
            sizeI = data.GetSizeChemistry()
            type = Include.CL_CHEMISTRY
        else:
            data.SetType_cla(Include.CL_ZOOPLANKTON)
            size = data.GetSizeZooplankton()
            sizeI = data.GetSizeData()
            data.Clustering(Include.CL_ZOOPLANKTON)
            col = data.GetNameZooplankton()
            type = Include.CL_ZOOPLANKTON
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type, 'otvet2': otvet2, 'val': val})

def ClusteringPr(request):
    data = Data_analysis.Data_analysis()
    size = data.GetSizeZooplankton()
    sizeI = data.GetSizeData()
    otvet = []
    names = ''
    col = []
    otvet2 = []
    val = str(0.2)
    if request.method == 'POST':
        type = data.GetType_cla()
        names = request.POST['name']
        if (type == Include.CL_ZOOPLANKTON):
            col = data.GetNameZooplankton()
            otvet = data.AnalysisClustering(names)
            size = data.GetSizeZooplankton()
            sizeI = data.GetSizeData()
        else:
            col = data.GetNameChemistryRes()
            otvet = data.AnalysisClusteringChemistry(names)
            size = data.GetSizeData()
            sizeI = data.GetSizeChemistry()
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type, 'otvet2': otvet2, 'val': val})

def CLUSgroup(request):
    data = Data_analysis.Data_analysis()
    size = data.GetSizeZooplankton()
    sizeI = data.GetSizeData()
    otvet = []
    names = ''
    col = []
    val = str(0.2)
    otvet2 = []
    type = 0
    if request.method == 'POST':
        type = data.GetType_cla()
        val = request.POST['name']
        if (type == Include.CL_ZOOPLANKTON):
            otvet2 = data.GroupClustering(float(val))
            size = data.GetSizeZooplankton()
            sizeI = data.GetSizeData()
            col = data.GetNameZooplankton()
        else:
            otvet2 = data.GroupClusteringChemistry(float(val))
            size = data.GetSizeData()
            sizeI = data.GetSizeChemistry()
            col = data.GetNameChemistryRes()
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type,'otvet2': otvet2, 'val': val})

def LSAstr(request):
    data = Data_analysis.Data_analysis()
    sizeI = data.GetSizeData()
    size = data.GetSizeZooplankton()
    data.Clustering(1)
    otvet = []
    otvet2 = []
    col = data.GetNameZooplankton()
    data.Correlation(3)
    val = str(0.2)
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisLSA(names)
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/LSA.html', {'Zooplankton': col, 'otvet': otvet, 'otvet2': otvet2,'size': size, 'sizeI': sizeI, 'val': val})


def LSAgroup(request):
    data = Data_analysis.Data_analysis()
    sizeI = data.GetSizeData()
    size = data.GetSizeZooplankton()
    otvet = []
    otvet2 = []
    col = data.GetNameZooplankton()
    val = str(0.2)
    if request.method == 'POST':
        val = request.POST['name']
        otvet2 = data.GroupLSA(float(val))
    return render(request, 'analysis/LSA.html',{'Zooplankton': col, 'otvet': otvet, 'otvet2': otvet2, 'size': size, 'sizeI': sizeI, 'val': val})

def LDA(request):

    data = Data_analysis.Data_analysis()
    data.LDA()
    otvet = data.NAnalysisLDA()
    otvet2 =[]
    val = str(300)
    if request.method == 'POST':
        val = request.POST['vali']
        otvet2 = data.AnalysisLDA(float(val))
    return render(request, 'analysis/LDA.html', {'otvet':  otvet, 'otvet2':  otvet2, 'val':val})


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
        type = data.GetType_cla()
        buffer = data.drawDentogram(type)
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
            buffer = data.drawPairplotDescription()
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
            buffer = data.drawPairplotPlace()
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

def photoPCA(request):
    data = Data_analysis.Data_analysis()
    try:
        type = data.GetType_cla()
        buffer = data.drawPCA(type)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoPCAlsa(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawPCA(1)
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response