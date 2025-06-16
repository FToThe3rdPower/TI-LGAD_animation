import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
import time


# Save the animation as a GIF in the folder
filePath = '/home/trey/Desktop/school/thesisStuff/TI-LGAD_animation/'

# Graphics params
numFrames = 100 #was 1000
fps = 10 

#Protons are red, Neutrons are grey, electrons are yellow, holes are blue, 
pionColor = 'purple'
electronColor = 'yellow'
holeColor = 'blue'

# 'Sim' parameters
n_dots = 15 # number of electrons and holes to animate
thick = 100 # penetration depth AND sensor thickness
width = 180 #3 px wide + a lil extra
pxPitch = 55 #μm, distance from center of one pixel to the next

#dummy doping layers for formatting
#implantSizeX = 35
#implantSizeY = 5

# Trench dimensions
numTrenches = 1
trenchDepth = 40 #μm
trenchWidth = 1 #μm
trenchGap = 5 #μm
trenchColor = "black"

# name the files appropriately based on the number of trenches
if numTrenches == 1:
    fileName = f"{filePath}1TR-LGAD.gif"
elif numTrenches == 2:
    fileName = f"{filePath}2TR-LGAD.gif"

## doping layer thicknesses.
## layers in order from sensor 'backside' to sensor 'frontside' except for the bulk, since that requires p++ thickness apriori
metalizationLayer = 5 #μm, thickness of the metalization layer
metalizationContactLayer = 10 #μm, thickness of the metalization contact "layer' that extends to the n++ layer
insulationLayer = 5 #μm, thickness of the insulation layer
nPlusPlusLayer = 5 #μm, thickness of the n++ layer
pPlusGainLayer = 10 #μm, thickness of the p+ layer
pPlusGainWidth = 35 #μm, width of the p+ gain implant
pPlusPlusLayer = 5 #μm, thickness of the p++ layer
pBulkLayer = int(thick - (pPlusPlusLayer + pPlusGainLayer + nPlusPlusLayer)) #μm, whatever's leftover after the other layers fill the 100μm

## doping layer colors
metalizationColor = "silver"
insulationColor = "olivedrab"
nPlusPlusColor = "orange"
pPlusPlusColor = "lightcoral"
pPlusGainColor = "turquoise"
pBulkColor = "cadetblue"


# Record the start time using perf_counter
start_time = time.perf_counter()

# Create a figure and axis
fig, ax = plt.subplots()


# Set axis limits
ax.set_xlim(0, width)
ax.set_ylim(0, thick)

# set axis labels and ticks to physical units
ax.set_xlabel("\xB5m")
ax.set_ylabel("\xB5m")
ax.set_xticks(np.linspace(0, width, 7))
ax.set_yticks(np.linspace(0, thick, 6))
ax.set_aspect('equal')



# Add a rectangular border
border = patches.Rectangle((0, 0), width, thick, linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(border)



# (x position, y pos), xSize, ySize like
# ax.add_patch(patches.Rectangle((55*2.5-implantSizeX/2, thick-implantSizeY), implantSizeX, implantSizeY, color='teal'))

#drawing layers
ax.add_patch(patches.Rectangle((0, thick-metalizationLayer), width, metalizationLayer, color=metalizationColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer)), width, insulationLayer, color=insulationColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer)), width, nPlusPlusLayer, color=nPlusPlusColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer)), width, pBulkLayer, color=pBulkColor))

#calculate the y spacing once
ySpacePgain = thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pPlusGainLayer)

#3 pixel loop
for pixNum in range(3):
    ax.add_patch(patches.Rectangle(((pixNum*pxPitch)+(pPlusGainWidth/2), ySpacePgain), pPlusGainWidth, pPlusGainLayer, color=pPlusGainColor))
    
    #no need for trench 0 to make labelling harder
    if pixNum>0 and numTrenches == 1:
        ax.add_patch(patches.Rectangle((pixNum*pPlusGainWidth+pixNum*pxPitch/(pixNum+1), thick-trenchDepth), trenchWidth, trenchDepth, color=trenchColor)) #!!! Fix the magic number here
    # sauce: https://www.mdpi.com/sensors/sensors-23-06225/article_deploy/html/images/sensors-23-06225-g001.png
    
    #elif pixNum>0 and numTrenches ==2:


# #Draw the metal contact to the n++ layer over the insulation layer
# for contact in range(numTrenches):
#     #Left contact
#     ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer)), width, metalizationContactLayer, color=metalizationColor))
#     #Right contact 
#     ax.add_patch(patches.Rectangle((width-metalizationContactLayer, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer)), metalizationContactLayer, nPlusPlusLayer, color=metalizationColor))


#add the p++ as the bottom layer
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+pPlusGainLayer+pBulkLayer)), width, pPlusPlusLayer, color=pPlusPlusColor))




## doping layer labeling
ax.annotate("metalization", xy=(1, thick-metalizationLayer/2), color="k", fontsize=8, ha='left', va='center')
ax.annotate('insulation', xy=(1, thick-(metalizationLayer+insulationLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('n++', xy=(1, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p+ (gain)', xy=(1, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pPlusGainLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p- (bulk)', xy=(1, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p++', xy=(1, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer+pPlusPlusLayer/2)), color='black', fontsize=8, ha='left', va='center')

# Initialize the purple dot at starting position
pion, = ax.plot([], [], 'o', color=pionColor, markersize=10)

# Initialize the e- (using Line2D objects)
dotse = [ax.plot([], [], 'o', color=electronColor, markersize=3)[0] for _ in range(n_dots)]
# now the holes
dotsh = [ax.plot([], [], 'o', markersize=5, markerfacecolor='none', markeredgewidth=2, markeredgecolor=holeColor)[0] for _ in range(n_dots)]

# Randomly initialize starting positions and velocities for the dots
y_pose = np.random.uniform(low=10, high=(thick-10), size=(n_dots))
x_pose = 100-(thick-y_pose)*0.15-0.2
y_posh = y_pose*1
x_posh = 100-(thick-y_posh)*0.15+0.2

# add a legend for the different particles
ax.legend([pion, dotse[0], dotsh[0]], ['Pion', 'Electron', 'Hole'], loc='lower right')

# Initialize the line for the pion's trail
line, = ax.plot([], [], lw=2, color=pionColor)

# Lists to store the dot's path (history of positions)
x_data, y_data = [], []

# Function to update the position of the purple dot
def update(frame):
    x = 100 - frame * 3  # Move the dot horizontally
    y = thick-frame*20  # Keep the dot vertically centered
    x_data.append(x)
    y_data.append(y)
    pion.set_data([x], [y]) # Pass x and y as lists
    line.set_data(x_data, y_data)
    if (frame<5):
        for i in range(n_dots):
            dotse[i].set_data([1000],[1000])
            dotsh[i].set_data([1000],[1000])
    else:
        for i in range(n_dots):
            y_pose[i]=y_pose[i]+0.6 # electrons move 3 times as fast as holes
            y_posh[i]=y_posh[i]-0.2
            if y_pose[i]>thick:
                y_pose[i]=1000
            if y_posh[i]<1:
                y_posh[i]=1000
            dotse[i].set_data([x_pose[i]],[y_pose[i]])
            dotsh[i].set_data([x_posh[i]],[y_posh[i]])
    #if positions[i][0] < or positions[i][0] > 8.5:
    return pion,line#,dots

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(numFrames), blit=True)
ani.save(fileName, writer=PillowWriter(fps=fps))

# Record the end time using perf_counter
end_time = time.perf_counter()

# Calculate the time elapsed making and saving the animation
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.5f} seconds")