from BoneMatrix import BoneMatrix

class Simulation:
    def __init__(self, x, y, h, dt, initialNaiveCollagenConc=9.4*10**5, initialCalciumConc=1.41*10**6, initialPhosphateConc=6.8*10**5, initialInhibitorConcentration=0.5*9.4*10**5, finalHAConc=9.4*10**5):
        self.x = x
        self.y = y
        self.h = h
        self.dt = dt
        self.finalHAConc = finalHAConc
        
        self.bonematrix = BoneMatrix(self.x, x, self.h, self.dt)
        self.bonematrix.setInitialNaiveCollagen(initialNaiveCollagenConc)
        self.bonematrix.setInitialCalcium(initialCalciumConc)
        self.bonematrix.setInitialPhosphate(initialPhosphateConc)
        self.bonematrix.setInitialInhibitor(initialInhibitorConcentration)
        
        
    def run(self):
        t = 0
        #while self.bonematrix.getOverallConc <= self.finalHAConc:
        while t <= 60:
            # time in seconds
            t += 1
            self.bonematrix.update()
            print(self.bonematrix.getHA().getOverallValue())
            
            if t % 60 == 0:
                self.bonematrix.getHA().graph("HA Concentration at " + str(t) + " seconds") 