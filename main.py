from Simulation import Simulation
import matplotlib.pyplot as plt

# Initialize simulation values
simulation = Simulation(1000, 1000, 0.1)

# Run simulation
simX, simY = simulation.run()

for i in range(len(simY)):
    simY[i] = simY[i] / (1.25*10**-7)

# Import data from Komarova et al. They built an analytical model to assess bone growth over time.
''' Additionally, information from Sheen et al. was used to verify the timing of different bone growth stages.
    Hydoxyapatite formation would begin around day 11, and it could last 4-5 weeks.'''
f = open('KomarovaData.csv')

x = []
y = []

for line in f:
    data = line.split(",")
    x.append(float(data[0]))
    # The data from this paper is normalized, so it must be multiplied by normal bone hydroxyapatite density
    y.append(float(data[1])*840)
    
f.close()

# Plot both data on same plot.
fig1, ax1 = plt.subplots()
ax1.set_title("Bone Mineralization Model Comparison")
ax1.set_xlabel("Time (days)")
ax1.set_ylabel("Hydroxyapatite Density (mg/$cm^3$)")

ax1.plot(x, y, color='blue', label="Komarova et al")
ax1.plot(simX, simY, color='red', label="Current Model")
ax1.legend()

# Write simulation data to file
with open('SimulationData.txt', 'wb') as file:
    file.write(''.encode())
    it = 0
    for t in simX:
        file.write(str('{:.3f}'.format(t)).encode() + ', '.encode() + str('{:.3f}\n'.format(simY[it])).encode())
        it += 1
        
# Save final HA concentration matrix (in units of mg/micrometers cubed)
simulation.bonematrix.HADensity.save('Final_HA_Density.txt')