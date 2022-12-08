class Cell:
    # Define attributes of each Cell that will be created
    def __init__(self, xLoc, yLoc):
        # Initialize constants
        self.xLoc = xLoc
        self.yLoc = yLoc
        
    # Function to change location
    def move(self, newX, newY):
        self.xLoc = newX
        self.yLoc = newY
        