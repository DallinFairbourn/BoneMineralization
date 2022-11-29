from BoneMatrix import BoneMatrix

class Simulation:
    def __init__(self, x, y, h, dt, initialNaiveCollagenConc=1, initialCalciumConc=1, initialPhosphateConc=1, initialInhibitorConcentration=0.5, finalHAConc=1):
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
        self.bonematrix.setInitialInhibitor(initialInhibitorConcentration)
        
        
    def run(self):
        t = 0
        while self.bonematrix.getOverallConc() <= self.finalHAConc:
            # time in seconds
            t += self.dt
            self.bonematrix.update(t)
            print(self.bonematrix.getCellPostion())
            
            if t % 100 == 0:
                self.bonematrix.getCaclium().graph("Calcium Concentration at " + str(t) + " seconds", cmap='Blues')
                self.bonematrix.getPhosphate().graph("Phosphate Concentration at " + str(t) + " seconds", cmap='viridis')
                self.bonematrix.getInhibitor().graph("Naive Inhibitor at " + str(t) + " seconds", cmap='hot')
                self.bonematrix.getNaiveCollagen().graph("Naive Collagen at " + str(t) + " seconds", cmap='Oranges')
                self.bonematrix.getAssembledCollagen().graph("Assembled Collagen at " + str(t) + " seconds", cmap='Reds')
                self.bonematrix.getHA().graph("HA Concentration at " + str(t) + " seconds", cmap='bone')