import matplotlib.pyplot as plt
from BoneMatrix import BoneMatrix

class Simulation:
    def __init__(self, x, y, h, dt, initialNaiveCollagenConc=0, initialCalciumConc=0.086, initialPhosphateConc=0.045, initialHAConc=3.75*10**-6*0.1, finalHAConc=0.000105):
        # initialNaiveCollagenConc=9.4*10**5, initialCalciumConc=1.41*10**6, initialPhosphateConc=6.8*10**5, initialInhibitorConcentration=0.5*9.4*10**5, finalHAConc=9.4*10**5
        self.x = x
        self.y = y
        self.h = h
        self.dt = dt
        self.finalHAConc = finalHAConc
        
        self.bonematrix = BoneMatrix(self.x, x, self.h, self.dt, self.finalHAConc)
        self.bonematrix.setInitialNaiveCollagen(initialNaiveCollagenConc)
        self.bonematrix.setInitialCalcium(initialCalciumConc)
        self.bonematrix.setInitialPhosphate(initialPhosphateConc)
        self.bonematrix.setInitialHA(initialHAConc)
        
        
    def run(self):
        t = 0
        valueArray = []
        timeArray = []
        while self.bonematrix.getOverallConc() <= self.finalHAConc:
            # time in seconds
            valueArray.append(self.bonematrix.getOverallConc())
            timeArray.append(t)
            t += self.dt
            self.bonematrix.update()
            
            if round(t, 1) % 10 == 0:
                self.bonematrix.getCaclium().graph("Calcium Concentration at " + str(round(t,1)) + " days", cmap='Blues', vmax=0.086)
                self.bonematrix.getPhosphate().graph("Phosphate Concentration at " + str(round(t,1)) + " days", cmap='viridis', vmax=0.045)
                self.bonematrix.getNaiveCollagen().graph("Naive Collagen at " + str(round(t,1)) + " days", cmap='Oranges', vmax=5.85*10**-5)
                self.bonematrix.getAssembledCollagen().graph("Assembled Collagen at " + str(round(t,1)) + " days", cmap='Reds', vmax=5.85*10**-5)
                self.bonematrix.getHA().graph("HA Concentration at " + str(round(t,1)) + " days", cmap='bone', vmax=self.finalHAConc)
            
            plt.scatter(timeArray, valueArray, c='blue')