import numpy as np
import matplotlib.pyplot as plt

class Matrix:
    # Define attributes of each Matrix that will be created
    def __init__(self, sizeX, sizeY):
        # Initialize array of given size
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = np.zeros((2, self.sizeY, self.sizeX))
        
    # Function to create a colormap of the matrix
    def graph(self, title, cmap="hot", vmin=0, vmax=1):
        fig, ax = plt.subplots()
        ax.set_title(title)
        im = plt.pcolor(self.matrix[0,:,:], cmap=cmap, vmin=vmin, vmax=vmax)
        plt.colorbar(im)
        plt.show()
        
    # Function to save matrix in a file
    def save(self, fileName):
        with open(fileName, 'wb') as file:
            np.savetxt(file, np.atleast_2d(self.matrix[0,:,:]), fmt='%.7f', delimiter=', ', newline = '\r\n')
        
    # The following functions are getters and setters. They allow for outside files to get values in the matrix as well as set them.
    # Function to set all values in Matrix to an initial value
    def setInitialValue(self, initialValue):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                self.matrix[:,i,j] = initialValue

    # Function to set values at specific locations
    def setValue(self, value, x, y):
        self.matrix[1,y,x] = value

    # Function to get values at specific locations
    def getValue(self, x, y):
        return self.matrix[0,y,x]
    
    # Function to move all new values to the first array held in Matrix
    def update(self):
        self.matrix[0,:,:] = self.matrix[1,:,:]
    
    # Function to get average value from matrix
    def getOverallValue(self):
        return self.matrix.mean()