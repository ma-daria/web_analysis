from pythonCode import Include
from django.conf import settings

def ToFloat(measurement):
    for name in measurement:
        measurement[name] = Include.pd.to_numeric(measurement[name], errors='coerce')
    measurement = measurement.fillna(0)
    return measurement

def CreateFolder():
    Include.os.mkdir(str(settings.MEDIA_ROOT)+"/Result")

def ReadFile(name):
    CreateFolder()
    measurement = Include.pd.read_csv(name, sep=';', decimal=',',  header=1)
    # measurement.fillna(0, inplace=True)
    measurement = measurement.rename(columns={'Unnamed: 0': 'Водоем'})
    measurement = measurement.rename(columns={'Unnamed: 1': 'Дата'})
    measurement = measurement.rename(columns={'Unnamed: 2': 'Место измерения'})
    measurement = measurement.rename(columns={'Unnamed: 3': 'Описание точки измерения'})
    measurement = measurement.rename(columns={'Unnamed: 4': 'pH'})
    measurement = measurement.rename(columns={'Unnamed: 5': 'Минерализация'})
    measurement = measurement.rename(columns={'Unnamed: 6': 't'})
    measurement = measurement.rename(columns={'Unnamed: 16': 'биомасса ФП'})

    measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'] = ToFloat(
        measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])

    # print(measurement['Ch. ovalis Kurz'])

    new_measurement = measurement
    for number in measurement.columns:
        if measurement[number].dtypes == 'float64':
            if measurement[number].sum() == 0:
                del new_measurement[number]
                # print(number)
    measurement = new_measurement
    # print(measurement.loc[0])
    return measurement


