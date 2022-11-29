from Cell import Cell

class Osteoblast(Cell):
    def __init__(self, xLoc, yLoc, collagenXDirection, collagenYDirection):
        super().__init__(xLoc, yLoc)
        self.collagenXDirection = collagenXDirection
        self.collagenYDirection = collagenYDirection
        self.X = self.xLoc + self.collagenXDirection
        self.Y = self.yLoc + self.collagenYDirection
        self.k1 = 0.1

    def formNaiveCollagen(self, nCollagen, dt):
        # function to add collagen to locations within the osteoid
        newValue = nCollagen.getValue(self.X,self.Y) * (1 - (self.k1 * dt))
        nCollagen.setValue(newValue,self.X,self.Y)
        

    def formAssembledCollagen(self, nCollagen, aCollagen, dt):
        if aCollagen.getValue(self.X, self.Y) <= 1:
            newValue = aCollagen.getValue(self.X,self.Y) + (self.k1 * nCollagen.getValue(self.X,self.Y) * dt)
            aCollagen.setValue(newValue,self.X,self.Y)
        
    def move(self, nCollagen, targetConc):
        if round(nCollagen.getValue(self.X,self.Y), 3) == 0:
            if self.X > self.xLoc:
                self.xLoc -= 1
                self.X -= 1
            elif self.Y > self.yLoc:
                self.yLoc -= 1
                self.Y -= 1
            elif self.X < self.xLoc:
                self.xLoc += 1
                self.X += 1
            elif self.Y < self.yLoc:
                self.yLoc += 1
                self.Y += 1
                
    def getPosition(self):
        return self.xLoc, self.yLoc