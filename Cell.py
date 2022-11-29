class Cell:
    def __init__(self, xLoc, yLoc):
        self.xLoc = xLoc
        self.yLoc = yLoc
        
    def move(self, newX, newY):
        # Function to change location
        self.xLoc = newX
        self.yLoc = newY
        