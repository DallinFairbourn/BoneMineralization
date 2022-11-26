import numpy as np
import matplotlib.pyplot as plt

class Matrix:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = np.zeros((2, self.sizeX, self.sizeY))
        
    def setInitialValue(self, initialValue):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                self.matrix[0,i,j] = initialValue

    def setValue(self, value, x, y):
        self.matrix[1,y,x] = value

    def getValue(self, x, y):
        return self.matrix[0,y,x]
    
    def getOverallValue(self):
        return self.matrix.mean()

    def graph(self, title, cmap="hot"):
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.imshow(self.matrix[0,:,:], cmap=cmap)
        plt.show()