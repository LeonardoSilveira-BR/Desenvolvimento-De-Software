class Voice:

    def __init__(self, numero, oitava, volume, instrumento, atraso):

        self.numero = numero
        self.oitava = oitava
        self.volume = volume
        self.instrumento = instrumento
        self.atraso = atraso

    def getOitava(self):
        return self.oitava

    def getVolume(self):
        return self.volume

    def getInstrumento(self):
        return self.instrumento

    def getAtraso(self):
        return self.atraso

    def setOitava(self, oitava):
        self.oitava = oitava

    def setVolume(self, volume):
        self.volume = volume

    def setInstrumento(self, instrumento):
        self.instrumento = instrumento
    
    def setAtraso(self, atraso):
        self.atraso = atraso