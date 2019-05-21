from django.shortcuts import render, redirect
from django.http import HttpResponse
# from papka import file


def index(request):
    if request.method == 'POST':
        file = request.FILES['document']
        print(file.path)
        return redirect('/table')
    return render(request, 'analysis/index.html')

def table(request):
    return render(request, 'analysis/table.html')

# пример тупо вызова функции
# def change(request):
#     file.SetData(3)
#     return render(request, 'analysis/index.html', {'data': file.GetData()})