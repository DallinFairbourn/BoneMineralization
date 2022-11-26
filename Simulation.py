from BoneMatrix import BoneMatrix

class Simulation:
    def __init__(self, sizeX, sizeY, h, dt, initialCalciumConc=2, initialPhosphateConc=3, finalHAConc=20):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.h = h
        self.dt = dt
        self.initialCalciumConc = initialCalciumConc
        self.initialPhosphateConc = initialPhosphateConc
        self.finalHAConc = finalHAConc
        
        self.bonematrix = BoneMatrix(self.sizeX, self.sizeY)
        
    def run():
        t = 0
        