from BoneMatrix import BoneMatrix

class Simulation:
    # Define attributes of the simulation (defined in units of milligrams and micrometers)
    def __init__(self, x, y, dt, h=0.005, initialCalciumConc=0.086, initialPhosphateConc=0.045, initialHAConc=12.75*10**-6*0.1, finalHAConc=0.000105):
        self.x = x
        self.y = y
        self.h = h
        self.v = h**3
        self.dt = dt
        self.finalHAConc = finalHAConc
        self.Ca = initialCalciumConc
        self.PO = initialPhosphateConc
        
        self.bonematrix = BoneMatrix(self.x, x, self.h, self.dt, self.finalHAConc)
        self.bonematrix.setInitialCalcium(initialCalciumConc)
        self.bonematrix.setInitialPhosphate(initialPhosphateConc)
        self.bonematrix.setInitialHA(initialHAConc)
        
    # Run simulation until final hydroxyapatite concentration is met
    def run(self):
        t = 0
        valueArray = []
        timeArray = []
        while self.bonematrix.getOverallConc() <= self.finalHAConc:
            valueArray.append(self.bonematrix.getOverallConc())
            timeArray.append(t)
            t += self.dt
            self.bonematrix.update()
            if round(t, 1) % 10 == 0:
                self.bonematrix.getHA().graph("HA Concentration at " + str(round(t, 1)) + " days", cmap='bone', vmax=self.finalHAConc / self.v)
        # Return overall HA values characteristic of the simulation
        return timeArray, valueArray
