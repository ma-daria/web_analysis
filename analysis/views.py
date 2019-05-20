from django.shortcuts import render
from django.http import HttpResponse
from papka import file


def index(request):

    return render(request, 'analysis/index.html', {'data': file.GetData()})

# пример тупо вызова функции
def change(request):
    file.SetData(3)
    return render(request, 'analysis/index.html', {'data': file.GetData()})