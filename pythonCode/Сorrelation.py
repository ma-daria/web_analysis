from pythonCode import Include

def CreateСorrelationСhemistry(measurement):
    mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
    Include.plt.figure(figsize=(15, 15), dpi=200)
    сorrelationСhemistry = measurement.corr()
    Include.sns.heatmap(сorrelationСhemistry, cmap=mapPalette, vmin=-1, vmax=1, annot=True)
    Include.plt.savefig("Result/СorrelationСhemistry.png")
    # plt.show()
    # print(measurement.corr())
    return сorrelationСhemistry


def CreateСorrelationZooplankton(measurement):
    mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
    Include.plt.figure(figsize=(20, 20), dpi=200)
    сorrelationZooplankton = measurement.corr()
    Include.sns.heatmap(сorrelationZooplankton, cmap=mapPalette, vmin=-1, vmax=1)
    Include.plt.savefig("Result/СorrelationZooplankton.png")
    # plt.show()
    # print(measurement.corr())
    return сorrelationZooplankton

def CreateСorrelationZooplanktonEnvironment(measurement, environment):
    mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
    Include.plt.figure(figsize=(10, 20), dpi=200)
    test = measurement.corrwith(environment['О2'])
    teste = Include.pd.DataFrame(test)
    teste = teste.rename(columns={0: 'О2'})

    test = measurement.corrwith(environment['БПК5'])
    teste['БПК5'] = test

    test = measurement.corrwith(environment['НСО3–'])
    teste['НСО3–'] = test
    # teste = teste.fillna(0)
    Include.sns.heatmap(teste, cmap=mapPalette, vmin=-1, vmax=1)
    Include.plt.savefig("Result/СorrelationZooplanktonEnvironment.png")