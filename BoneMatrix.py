from Matrix import Matrix
from Osteoblast import Osteoblast

class BoneMatrix:
    def __init__(self, x, y, h, dt, targetHADens):
        # Values from the simulation parameters
        self.x = x / 10000
        self.y = y / 10000
        self.h = h / 10000
        self.dt = dt
        self.sizeX = int(x/h)
        self.sizeY = int(y/h)
        self.targetHADens = targetHADens
        
        # Constants
        self.k2 = 0.1
        self.k3 = 2.4*10**8
        self.D = 1.08*10**-5
        self.targetCollagenDens = 5.85*10**-5
        self.dailyCalciumIntake = 2.02*10**-9
        self.dailyPhosphateIntake = 8.06*10**-9
        
        # Matrices holding chemical information
        self.naiveCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.assembledCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.HADensity = Matrix(self.sizeX, self.sizeY)
        self.calciumConc = Matrix(self.sizeX, self.sizeY)
        self.phosphateConc = Matrix(self.sizeX, self.sizeY)
        self.inhibitorConc = Matrix(self.sizeX, self.sizeY)
        
        # Matrix hodling cell information
        self.side1, self.side2 = self.placeCells()
        
    def diffuse(self, ions, nIons):
        # Function to cause ions and inhibitors to diffuse
        k = (self.D*self.dt)/(self.h*self.h)
        for i in range(1, self.sizeY-1):
            for j in range(1, self.sizeX-1):
                newValue = ions.getValue(j,i) + k*(ions.getValue(j,i+1) + ions.getValue(j,i-1) + ions.getValue(j+1,i) + ions.getValue(j-1,i) - 4*ions.getValue(j,i)) - (nIons * self.HADensity.getValue(j,i))
                ions.setValue(newValue, j, i)
                
    def replenish(self, ions, intake):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                newValue = ions.getValue(j,i) + intake * self.dt
                ions.setValue(newValue, j, i)
    
    def formHA(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                if self.HADensity.getValue(j,i) <= self.targetHADens and (self.assembledCollagenDensity.getValue(j,i) + self.naiveCollagenDensity.getValue(j,i)) >= 0.99*self.targetCollagenDens:
                    newValue = self.HADensity.getValue(j,i) + self.k3 * self.calciumConc.getValue(j,i)**5 * self.phosphateConc.getValue(j,i)**3 * self.HADensity.getValue(j,i) * self.dt
                    self.HADensity.setValue(newValue,j,i)
                    
    def formAssembledCollagen(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                if self.assembledCollagenDensity.getValue(j, i) <= self.targetCollagenDens:
                    newValue = self.assembledCollagenDensity.getValue(j,i) + (self.k2 * self.naiveCollagenDensity.getValue(j,i) * self.dt)
                    self.assembledCollagenDensity.setValue(newValue,j,i)
        
    def formCollagen(self):
        for i in range(len(self.side1)):
            self.side1[i].formNaiveCollagen(self.naiveCollagenDensity, self.dt)
            self.side2[i].formNaiveCollagen(self.naiveCollagenDensity, self.dt)
            if self.side1[i].getPosition()[0] <= (len(self.side1)//2):
                self.side1[i].move(self.naiveCollagenDensity, self.assembledCollagenDensity)
            if self.side2[i].getPosition()[0] >= (len(self.side2)//2 - 1):
                self.side2[i].move(self.naiveCollagenDensity, self.assembledCollagenDensity)
        
    def placeCells(self):
        side1 = []
        side2 = []
        for i in range(self.sizeY):
            side1.append(Osteoblast(1,i,-1,0))
            side2.append(Osteoblast(self.sizeX-2,i,1,0))
        return side1, side2
            
    def update(self):
        self.formCollagen()
        self.formAssembledCollagen()
        self.formHA()
        self.diffuse(self.calciumConc, 0.2)
        self.diffuse(self.phosphateConc, 0.567)
        
        self.naiveCollagenDensity.update()
        self.assembledCollagenDensity.update()
        self.HADensity.update()
        self.calciumConc.update()
        self.phosphateConc.update()
        self.replenish(self.calciumConc, self.dailyCalciumIntake)
        self.replenish(self.phosphateConc, self.dailyPhosphateIntake)
        
        
    def getOverallConc(self):
        return self.HADensity.getOverallValue()
    
    def setInitialNaiveCollagen(self, value):
        self.naiveCollagenDensity.setInitialValue(value)
    
    def setInitialCalcium(self, value):
        self.calciumConc.setInitialValue(value)
        
    def setInitialPhosphate(self, value):
        self.phosphateConc.setInitialValue(value)
        
    def setInitialHA(self, value):
        self.HADensity.setInitialValue(value)
        
    def getHA(self):
        return self.HADensity

    def getNaiveCollagen(self):
        return self.naiveCollagenDensity
    
    def getAssembledCollagen(self):
        return self.assembledCollagenDensity
    
    def getCaclium(self):
        return self.calciumConc
    
    def getPhosphate(self):
        return self.phosphateConc
    
    def getCellPostion(self):
        return self.side1[4].getPosition(), self.side2[4].getPosition()