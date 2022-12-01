from Cell import Cell

class Osteoblast(Cell):
    def __init__(self, xLoc, yLoc, collagenXDirection, collagenYDirection):
        super().__init__(xLoc, yLoc)
        self.collagenXDirection = collagenXDirection
        self.collagenYDirection = collagenYDirection
        self.X = self.xLoc + self.collagenXDirection
        self.Y = self.yLoc + self.collagenYDirection
        self.k1 = 7.02*10**-3
        self.k2 = 0.1
        self.targetConc = 5.85*10**-5

    def formNaiveCollagen(self, nCollagen, dt):
        # function to add collagen to locations within the osteoid
        if nCollagen.getValue(self.X, self.Y) <= self.targetConc:
            newValue = nCollagen.getValue(self.X, self.Y) + (self.k1 - self.k2 * nCollagen.getValue(self.X, self.Y)) * dt
            nCollagen.setValue(newValue,self.X,self.Y)
        
    def move(self, nCollagen, aCollagen):
        if aCollagen.getValue(self.X, self.Y) >= self.targetConc:
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