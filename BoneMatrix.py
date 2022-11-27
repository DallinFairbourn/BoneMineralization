import scipy as sp
import numpy as np
from Matrix import Matrix
from Osteoblast import Osteoblast

class BoneMatrix:
    def __init__(self, x, y, h, dt):
        # Values from the simulation parameters
        self.x = x
        self.y = y
        self.dt = dt
        self.h = h
        self.sizeX = int(x/h)
        self.sizeY = int(y/h)
        
        # Constants
        self.k1 = 1.16*10**-6
        self.k2 = 1
        self.k3 = 0.0116
        self.a = 10
        self.b = 10**57
        self.r1 = 2.31*10**-12
        self.r2 = 2.82*10**-32
        self.v1 = 1.0*10**-6
        
        # Matrices holding chemical information
        self.naiveCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.assembledCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.nucleatorDensity = Matrix(self.sizeX, self.sizeY)
        self.HADensity = Matrix(self.sizeX, self.sizeY)
        self.calciumConc = Matrix(self.sizeX, self.sizeY)
        self.phosphateConc = Matrix(self.sizeX, self.sizeY)
        self.inhibitorConc = Matrix(self.sizeX, self.sizeY)
        
        # Matrix hodling cell information
        self.side1, self.side2 = self.placeCells()

        
    def diffuse(self, ions, D, nIons):
        # Function to cause ions to diffuse
        k = (D*self.dt)/(self.h*self.h)
        for i in range(self.sizeY-1):
            for j in range(self.sizeX-1):
                newValue = ions.getValue(j,i) + k*(ions.getValue(j,i+1) + ions.getValue(j,i-1) + ions.getValue(j+1,i) + ions.getValue(j-1,i) - 4*ions.getValue(j,i)) - nIons * self.k3 * (sp.divide(self.b, (self.b + self.inhibitorConc.getValue(j, i)**self.a))) * self.nucleatorDensity.getValue(j, i)
                ions.setValue(newValue, j, i)
                
    def consumeInhibitor(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                newValue = self.inhibitorConc.getValue(j,i) * (1 - self.r1 * self.assembledCollagenDensity.getValue(j,i) * self.dt) + (self.v1 * self.naiveCollagenDensity.getValue(j,i) * self.dt)
                self.inhibitorConc.setValue(newValue,j,i)
    
    def formHA(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                newValue = self.HADensity.getValue(j,i) + self.k3 * (self.b / (self.b + self.inhibitorConc.getValue(j,i)**self.a)) * self.nucleatorDensity.getValue(j,i) * self.dt
                self.HADensity.setValue(newValue,j,i)
        
    def formNucleator(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                newValue = self.nucleatorDensity.getValue(j,i) + (self.k2 * self.naiveCollagenDensity.getValue(j,i) * self.k1 * self.dt) - (self.r2 * self.k3 * (sp.divide(self.b, (self.b + self.inhibitorConc.getValue(j, i)**self.a))) * self.nucleatorDensity.getValue(j,i)**2 * self.dt)
                self.nucleatorDensity.setValue(newValue,j,i)
        
    def formAssembledCollagen(self):
        for i in range(len(self.side1)):
            self.side1[i].formNaiveCollagen(self.naiveCollagenDensity, self.dt)
            self.side2[i].formNaiveCollagen(self.naiveCollagenDensity, self.dt)
            self.side1[i].formAssembledCollagen(self.naiveCollagenDensity, self.assembledCollagenDensity, self.dt)
            self.side2[i].formAssembledCollagen(self.naiveCollagenDensity, self.assembledCollagenDensity, self.dt)
        
    def placeCells(self):
        side1 = []
        side2 = []
        for i in range(self.sizeY):
            side1.append(Osteoblast(1,i,-1,0))
        for i in range(self.sizeY):
            side2.append(Osteoblast(self.sizeX-2,i,1,0))
        return side1, side2
            
    def update(self):
        self.formAssembledCollagen()
        self.consumeInhibitor()
        self.formHA()
        self.formNucleator()
        self.diffuse(self.calciumConc, 10**5, 10)
        self.diffuse(self.phosphateConc, 10**5, 6)
        self.diffuse(self.inhibitorConc, 10**5, 0)
        
        self.naiveCollagenDensity.update()
        self.assembledCollagenDensity.update()
        self.nucleatorDensity.update()
        self.HADensity.update()
        self.calciumConc.update()
        self.phosphateConc.update()
        self.inhibitorConc.update()
        
        
    def getOverallConc(self):
        return self.HADensity.getOverallValue()
    
    def setInitialNaiveCollagen(self, value):
        self.naiveCollagenDensity.setInitialValue(value)
    
    def setInitialCalcium(self, value):
        self.calciumConc.setInitialValue(value)
        
    def setInitialPhosphate(self, value):
        self.phosphateConc.setInitialValue(value)
        
    def setInitialInhibitor(self, value):
        self.inhibitorConc.setInitialValue(value)
        
    def getHA(self):
        return self.HADensity

    def getNaiveCollagen(self):
        return self.naiveCollagenDensity
    
    def getAssembledCollagen(self):
        return self.assembledCollagenDensity
    
    def getNucleator(self):
        return self.nucleatorDensity
    
    def getCaclium(self):
        return self.calciumConc
    
    def getPhosphate(self):
        return self.phosphateConc
    
    def getInhibitor(self):
        return self.inhibitorConc