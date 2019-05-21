from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from pythonCode import ReadFile, Data, Сorrelation, AnalysisResult



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
    if request.method == 'POST':
        names = request.POST['name']
        res = AnalysisResult.SortingCorrelation(cor[str(names)])

    return render(request, 'analysis/СorrelationСhemistry.html', {'Сhemistry':data.loc[:, 'О2':'Са+2'].columns, 'resalt': res})
