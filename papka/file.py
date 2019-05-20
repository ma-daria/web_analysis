# пример тупо вызова функции
# мб переделать на класс

data = 0
# print(data)

def GetData():
    # print(data)
    global data
    return data

def SetData(d):
    global data
    data = d