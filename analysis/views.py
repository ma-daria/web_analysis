from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from analysis.static.analysis.pythonCode import Data, ReadFile, AnalysisResult, Clustering, Correlation, LSA
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
        Data.SetData(ReadFile.ReadFile(str(settings.MEDIA_ROOT) + '/' + str(file)))
        return redirect('/table')

    return render(request, 'analysis/index.html')

def table(request):
    meas = []
    measur = Data.GetData()
    reservoir = measur['Водоем']
    date = measur['Дата']
    plase = measur['Место измерения']
    point = measur['Описание точки измерения']
    mass = measur['биомасса ФП']
    for i in range(len(reservoir)):
        meas.append([reservoir[i], date[i], plase[i], point[i], mass[i]])
    return render(request, 'analysis/table.html', {'measurement': meas})

def СorrelationСhemistry(request):
    data = Data.GetData()
    cor = Correlation.CreateСorrelationСhemistry(data.loc[:, 'О2':'Са+2'])
    res = []
    ind = []
    if request.method == 'POST':
        names = request.POST['name']
        ress = AnalysisResult.SortingCorrelation(cor[str(names)])
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    otvet = []
    for i in range(len(res)):
        otvet.append([ind[i], res[i]])
    return render(request, 'analysis/СorrelationСhemistry.html', {'Сhemistry':data.loc[:, 'О2':'Са+2'].columns, 'otvet': otvet})

def СorrelationZooplankton(request):
    data = Data.GetData()
    cor = Correlation.CreateСorrelationZooplankton(data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])
    res = []
    ind = []
    if request.method == 'POST':
        names = request.POST['name']
        ress = AnalysisResult.SortingCorrelation(cor[str(names)])
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    otvet = []
    for i in range(len(res)):
        otvet.append([ind[i], res[i]])
    return render(request, 'analysis/СorrelationZooplankton.html', {'Zooplankton':data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns, 'otvet': otvet})

def СlusteringStr(request):
    data = Data.GetData()
    cl = Clustering.Сlustering(data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])
    otvet = []
    col = data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns
    if request.method == 'POST':
        names = request.POST['name']
        i = 0
        for i in range(col.size):
            if col[i] == names:
                break
        otvet = AnalysisResult.GropupСlustering(cl, i, col.size, col)

    return render(request, 'analysis/Сlustering.html', {'Zooplankton':data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns, 'otvet': otvet})

def LSAstr(request):
    data = Data.GetData()
    cl = LSA.lsa(data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])
    otvet = []
    col = data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns
    if request.method == 'POST':
        names = request.POST['name']
        i = 0
        for i in range(col.size):
            if col[i] == names:
                break
        otvet = AnalysisResult.GropupСlustering(cl, i, col.size, col)

    return render(request, 'analysis/LSA.html', {'Zooplankton':data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns, 'otvet': otvet})

