import numpy as np
import matplotlib.pyplot as plt

class Matrix:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = np.zeros((2, self.sizeY, self.sizeX))
        
    def setInitialValue(self, initialValue):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                self.matrix[:,i,j] = initialValue

    def setValue(self, value, x, y):
        self.matrix[1,y,x] = value

    def getValue(self, x, y):
        return self.matrix[0,y,x]
    
    def update(self):
        self.matrix[0,:,:] = self.matrix[1,:,:]
    
    def getOverallValue(self):
        return self.matrix.mean()

    def graph(self, title, cmap="hot"):
        fig, ax = plt.subplots()
        ax.set_title(title)
        im = plt.pcolor(self.matrix[0,:,:], cmap=cmap, vmin=0, vmax=1)
        #im = ax.imshow(self.matrix[0,:,:], cmap=cmap)
        plt.colorbar(im)
        plt.show()