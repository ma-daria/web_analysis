from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from pythonCode import ReadFile


def index(request):
    if request.method == 'POST':
        file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        print(str(settings.MEDIA_ROOT)+'/' + str(file))
        print(ReadFile.ReadFile(str(settings.MEDIA_ROOT)+'/' + str(file)))
        return redirect('/table')

    return render(request, 'analysis/index.html')

def table(request):
    return render(request, 'analysis/table.html')

# пример тупо вызова функции
# def change(request):
#     file.SetData(3)
#     return render(request, 'analysis/index.html', {'data': file.GetData()})
