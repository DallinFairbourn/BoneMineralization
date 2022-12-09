import numpy as np
import matplotlib.pyplot as plt

class Matrix:
    # Define attributes of each Matrix that will be created
    def __init__(self, sizeX, sizeY, h):
        # Initialize array of given size
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.v = h**3
        self.h = h
        self.matrix = np.zeros((2, self.sizeY, self.sizeX))
        
    # Function to create a colormap of the matrix
    def graph(self, title, cmap="hot", vmin=0, vmax=1,):
        fig, ax = plt.subplots()
        xLabel = []
        x = []
        yLabel = []
        y = []
        for i in range(self.sizeX):
            xLabel.append(int(i*self.h*10000))
            x.append(i)
        for i in range(self.sizeY):
            yLabel.append(int(i*self.h*10000))
            y.append(i)
        plt.xticks(x, xLabel, rotation=50)
        plt.yticks(y, yLabel)
        ax.set_title(title)
        ax.set_xlabel('$\mu$m')
        ax.set_ylabel('$\mu$m')
        im = plt.pcolor(self.matrix[0,:,:]/self.v, cmap=cmap, vmin=vmin, vmax=vmax)
        cbar = plt.colorbar(im)
        cbar.set_label('Concentration (mg/$cm^3$)', rotation=270, labelpad=20)
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