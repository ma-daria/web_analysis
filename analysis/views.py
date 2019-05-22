from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from pythonCode import ReadFile, Data, Сorrelation, AnalysisResult, Include



def index(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        print(str(settings.MEDIA_ROOT)+'/' + str(file))
        Data.SetData(ReadFile.ReadFile(str(settings.MEDIA_ROOT)+'/' + str(file)))
        return redirect('/table')

    return render(request, 'analysis/index.html')

def table(request):
    # return render(request, 'analysis/table.html', {'measurement': [['0', '1'],['2', '3']]})
    return render(request, 'analysis/table.html', {'measurement': Data.GetData()})

def СorrelationСhemistry(request):
    data = Data.GetData()
    cor = Сorrelation.CreateСorrelationСhemistry(data.loc[:, 'О2':'Са+2'])
    res = []
    ind = []
    if request.method == 'POST':
        names = request.POST['name']
        ress = AnalysisResult.SortingCorrelation(cor[str(names)])
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    return render(request, 'analysis/СorrelationСhemistry.html', {'Сhemistry':data.loc[:, 'О2':'Са+2'].columns, 'resalt': res, 'ind': ind})

def СorrelationZooplankton(request):
    data = Data.GetData()
    cor = Сorrelation.CreateСorrelationZooplankton(data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])
    res = []
    ind = []
    if request.method == 'POST':
        names = request.POST['name']
        ress = AnalysisResult.SortingCorrelation(cor[str(names)])
        ind = ress.index.tolist()
        res = ress.tolist()
        print(ind)
        # print(res.index)
    return render(request, 'analysis/СorrelationZooplankton.html', {'Zooplankton':data.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'].columns, 'resalt': res, 'ind': ind})