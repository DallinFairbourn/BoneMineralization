from Matrix import Matrix

class BoneMatrix:
    def __init__(self, x, y, h, dt):
        self.x = x
        self.y = y
        self.dt = dt
        self.h = h
        self.sizeX = int(x/h)
        self.sizeY = int(y/h)
        self.naiveCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.assembledCollagenDensity = Matrix(self.sizeX, self.sizeY)
        self.nucleatorDensity = Matrix(self.sizX, self.sizeY)
        self.HADensity = Matrix(self.sizeX, self.sizeY)
        self.calciumConc = Matrix(self.sizeX, self.sizeY)
        self.phosphateConc = Matrix(self.sizeX, self.sizeY)
        self.inhibitorConc = Matrix(self.sizeX, self.sizeY)

        
    def diffuse(self, ions, D, k3, nIons):
        # Function to cause ions to diffuse
        k = (D*self.dt)/(self.h*self.h)
        a = 10
        b = 10**57
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                newValue = ions.getValue(j,i) + k*(ions.getValue(j,i+1) + 
                                                   ions.getValue(j,i-1) + 
                                                   ions.getValue(j+1,i) + 
                                                   ions.getValue(j-1,i) - 
                                                   4*ions.getValue(j,i)) - nIons * (b / (b + self.inhibitorConc.getValue(j, i)**a)) * self.nucleatorDensity.getValue(j, i)
                ions.setValue(newValue, j, i)
                
    def formHA(self, )