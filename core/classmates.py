import pandas as pd

class Classmates():
    def __init__(self, data):
        self.data = data

    def getNames(self):
        return [i['nombre'] for i in self.data]

    def getDirections(self):
        return [i['direccioncompleta'] for i in self.data]

    def getBirthday(self):
        return [i['fnacimiento'] for i in self.data]

    def getAlldf(self):
        df = pd.DataFrame(
            list(zip(self.getNames(), self.getBirthday(), self.getDirections())),
            columns=["Nombre", "Fecha de Nacimiento", "Dirección"]
        )
        return df
