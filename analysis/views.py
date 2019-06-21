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
            except Exception as e:
                print(e)
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        data = Data_analysis.Data_analysis()
        data.ReadFile(str(settings.MEDIA_ROOT) + '/' + str(file))
        return redirect('/table')
    return render(request, 'analysis/index.html')

def table(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    name = dat.GetNameAll()
    size = dat.GetSizeData()
    sizeP = name.size
    sizeI = dat.GetSizeChemistry()
    sizeV = dat.GetSizeZooplankton()
    return render(request, 'analysis/table.html', { 'nameC': name, 'size': size, 'sizeP': sizeP, 'sizeI': sizeI, 'sizeV': sizeV})

def Correlation(request):
    form=[]
    data = Data_analysis.Data_analysis()
    data.SetType(Include.CO_CHEMISTRY)
    data.Correlation()
    otvet = []
    dat = data.GetData()
    col = dat.GetNameChemistry()
    sizeI = dat.GetSizeData()
    col1 = dat.GetNameChemistry()
    col2 = dat.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()
    corMax = data.CorrelationMax()
    id = data.GetType()
    size = dat.GetSizeChemistry()
    if request.method == 'POST':
        list = request.POST.getlist('states[]')
        tip = request.POST['name3']
        if tip == 'Химический состав':
            data.SetType(Include.CO_CHEMISTRY)
            id = Include.CO_CHEMISTRY
            data.Correlation()
            col = dat.GetNameChemistry()
            size = dat.GetSizeChemistry()
            corMax = data.CorrelationMax()
        else:
            if tip == 'Видовой состав':
                data.SetType(Include.CO_ZOOPLANKTON)
                id = Include.CO_ZOOPLANKTON
                data.Correlation()
                col = dat.GetNameZooplankton()
                size = dat.GetSizeZooplankton()
                corMax = data.CorrelationMax()
            else:
                data.SetList(list)
                data.SetType(Include.CO_MIX)
                id = Include.CO_MIX
                data.Correlation()
                col = list
                size = dat.GetSizeMix()
                corMax = data.CorrelationMax()
    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': id, 'size': size, 'sizeI': sizeI, 'corMax': corMax})

def PrintListCorrelation(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    size = dat.GetSizeChemistry()
    form=[]
    data = Data_analysis.Data_analysis()
    type = data.GetType()
    otvet = []
    col = dat.GetNameChemistry()
    sizeI = dat.GetSizeData()
    col1 = dat.GetNameChemistry()
    col2 = dat.GetNameZooplankton()
    colS = col1.tolist() + col2.tolist()
    corMax = []
    if request.method == 'POST':
        names = request.POST['name']
        if type == Include.CO_CHEMISTRY:
            otvet = data.AnalysisCorrelation(str(names))
            col = dat.GetNameChemistry()
            size = dat.GetSizeChemistry()
            corMax = data.CorrelationMax()
        else:
            if type == Include.CO_ZOOPLANKTON:
                otvet = data.AnalysisCorrelation(str(names))
                col = dat.GetNameZooplankton()
                size = dat.GetSizeZooplankton()
                corMax = data.CorrelationMax()
            else:
                otvet = data.AnalysisCorrelation(str(names))
                col = Include.pd.Series(dat.GetList())
                size = dat.GetSizeMix()
                corMax = data.CorrelationMax()
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/Correlation.html', {'col': col, 'colS':colS, 'otvet': otvet, 'form': form, 'type': type, 'size': size, 'sizeI': sizeI, 'corMax': corMax})

def ClusteringStr(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    size = dat.GetSizeZooplankton()
    sizeI = dat.GetSizeData()
    data.SetType_cla(Include.CL_ZOOPLANKTON)
    data.Clustering()
    otvet = []
    names = ''
    col = dat.GetNameZooplankton()
    type = Include.CL_ZOOPLANKTON
    otvet2 = []
    val = str(0.2)
    if request.method == 'POST':
        tip = request.POST['name3']
        if tip == 'Точки измерения':
            data.SetType_cla(Include.CL_CHEMISTRY)
            data.Clustering()
            col = dat.GetNameChemistryRes()
            size = dat.GetSizeData()
            sizeI = dat.GetSizeChemistry()
            type = Include.CL_CHEMISTRY
        else:
            data.SetType_cla(Include.CL_ZOOPLANKTON)
            size = dat.GetSizeZooplankton()
            sizeI = dat.GetSizeData()
            data.Clustering()
            col = dat.GetNameZooplankton()
            type = Include.CL_ZOOPLANKTON
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type, 'otvet2': otvet2, 'val': val})

def ClusteringPr(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    size = dat.GetSizeZooplankton()
    sizeI = dat.GetSizeData()
    otvet = []
    names = ''
    col = []
    otvet2 = []
    val = str(0.2)
    if request.method == 'POST':
        type = data.GetType_cla()
        names = request.POST['name']
        if (type == Include.CL_ZOOPLANKTON):
            col = dat.GetNameZooplankton()
            otvet = data.AnalysisClustering(names)
            size = dat.GetSizeZooplankton()
            sizeI = dat.GetSizeData()
        else:
            col = dat.GetNameChemistryRes()
            otvet = data.AnalysisClustering(names)
            size = dat.GetSizeData()
            sizeI = dat.GetSizeChemistry()
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type, 'otvet2': otvet2, 'val': val})

def CLUSgroup(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    size = dat.GetSizeZooplankton()
    sizeI = dat.GetSizeData()
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
            size = dat.GetSizeZooplankton()
            sizeI = dat.GetSizeData()
            col = dat.GetNameZooplankton()
        else:
            otvet2 = data.GroupClustering(float(val))
            size = dat.GetSizeData()
            sizeI = dat.GetSizeChemistry()
            col = dat.GetNameChemistryRes()
    return render(request, 'analysis/Clustering.html', {'Zooplankton': col, 'otvet': otvet, 'selec': names, 'size': size, 'sizeI': sizeI, 'type': type,'otvet2': otvet2, 'val': val})

def LSAstr(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    sizeI = dat.GetSizeData()
    size = dat.GetSizeZooplankton()
    data.SetType_cla(Include.CL_LSA)
    data.Clustering()
    otvet = []
    otvet2 = []
    col = dat.GetNameZooplankton()
    data.SetType(Include.CO_LSA)
    data.Correlation()
    val = str(0.2)
    if request.method == 'POST':
        names = request.POST['name']
        otvet = data.AnalysisClustering(names)
        col = col[col != names]
        col = [names] + col.tolist()
    return render(request, 'analysis/LSA.html', {'Zooplankton': col, 'otvet': otvet, 'otvet2': otvet2,'size': size, 'sizeI': sizeI, 'val': val})

def LSAgroup(request):
    data = Data_analysis.Data_analysis()
    dat = data.GetData()
    sizeI = dat.GetSizeData()
    size = dat.GetSizeZooplankton()
    otvet = []
    otvet2 = []
    col = dat.GetNameZooplankton()
    val = str(0.2)
    if request.method == 'POST':
        val = request.POST['name']
        otvet2 = data.GroupClustering(float(val))
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
        buffer = data.drawCorrelation()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoClustrering(request):
    data = Data_analysis.Data_analysis()
    try:
        type = data.GetType_cla()
        buffer = data.drawDentogram()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoLSA(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawDentogram()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoPairplotDescription(request):
    data = Data_analysis.Data_analysis()
    if data.GetType() == Include.CO_MIX:
        try:
            buffer = data.drawPairplot(Include.PA_DESCRIPTION)
        except:
            buffer = Include.io.BytesIO()
            print("Не удалось загрузить график")
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response
    else:
        buffer = Include.io.BytesIO()
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        return response

def photoPairplotPlace(request):
    data = Data_analysis.Data_analysis()
    if data.GetType() == Include.CO_MIX:
        try:
            buffer = data.drawPairplot(Include.PA_PLACE)
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
        buffer = data.drawCorrelation()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoPCA(request):
    data = Data_analysis.Data_analysis()
    try:
        type = data.GetType_cla()
        buffer = data.drawPCA()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response

def photoPCAlsa(request):
    data = Data_analysis.Data_analysis()
    try:
        buffer = data.drawPCA()
    except:
        buffer = Include.io.BytesIO()
        print("Не удалось загрузить график")
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    return response