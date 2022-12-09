from Simulation import Simulation
import matplotlib.pyplot as plt

# Initialize simulation values
simulation = Simulation(0.1, 0.1, 0.1)

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
plt.show()

# Write simulation data to file
with open('SimulationData.txt', 'wb') as file:
    file.write(''.encode())
    it = 0
    for t in simX:
        file.write(str('{:.3f}'.format(t)).encode() + ', '.encode() + str('{:.3f}\n'.format(simY[it])).encode())
        it += 1
        
# Save final HA concentration matrix (in units of mg/micrometers cubed)
simulation.bonematrix.HADensity.save('Final_HA_Density.txt')


# Run simulations with varying lengths
x0, y0 = Simulation(0.01, 0.01, 0.1).run()
x1, y1 = Simulation(0.025, 0.025, 0.1).run()
x2, y2 = Simulation(0.05, 0.05, 0.1).run()
x3, y3 = Simulation(0.075, 0.075, 0.1).run()

sims = [y1, y2, y3, y0]

for sim in sims:
    for i in range(len(sim)):
        sim[i] = sim[i] / (1.25*10**-7)

x4 = simX
y4 = simY

simsX = [x0, x1, x2, x3, x4]
simsY = [y0, y1, y2, y3, y4]

titles = ['100', '250', '500', '750', '1000']
colors = ['blue', 'red', 'magenta', 'green', 'cyan', 'yellow']
symbols = ['o', '^', 's', 'P', 'D', 'X']

units = ' $\mu$'+'m'

fig2, ax2 = plt.subplots()

it = 0
for x in simsX:
    ax2.plot(x, simsY[it], color=colors[it], label=titles[it]+units)
    it += 1

ax2.set_title("Bone Mineralization Over Different Gap Sizes")
ax2.set_xlabel("Time (days)")
ax2.set_ylabel("Hydroxyapatite Density (mg/$cm^3$)")
ax2.legend()
plt.show()