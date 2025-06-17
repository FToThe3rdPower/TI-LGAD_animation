#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Trey Grijalva

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
labelIndent = 10 #μm, indent for the layer labels so they sit in what they label

# particle coloring
pionColor = 'purple'
electronColor = 'blue'
holeColor = 'red'

## doping layer colors
metalizationColor = "silver"
insulationColor = "darkorange"
nPlusPlusColor = "royalblue"
pPlusPlusColor = "indianred"
pPlusGainColor = "lightcoral"
pBulkColor = "mistyrose"


# 'Sim' parameters
n_dots = 15 # number of electrons and holes to animate
thick = 100 # penetration depth AND sensor thickness
width = 185 #3 px wide + 5 in-between +5 on each side
pxPitch = 55 #μm, distance from center of one pixel to the next
pixelGap = 5 #μm

# Trench parameters
numTrenches = 1
trenchDepth = 40 #μm
trenchWidth = 1 #μm
trenchColor = "black"

## doping layer thicknesses.
## layers in order from sensor 'backside' to sensor 'frontside' except for the bulk, since that requires p++ thickness apriori
metalizationLayer = 5 #μm, thickness of the metalization layer
metalizationContactLayer = 10 #μm, thickness of the metalization contact "layer' that extends to the n++ layer
metalizationContactWidth = 3 #μm, width of the metalization contact
insulationLayer = 5 #μm, thickness of the insulation layer
nPlusPlusLayer = 5 #μm, thickness of the n++ layer
pPlusGainLayer = 10 #μm, thickness of the p+ layer
pPlusGainWidth = 35 #μm, width of the p+ gain implant
pPlusPlusLayer = 5 #μm, thickness of the p++ layer
pBulkLayer = int(thick - (pPlusPlusLayer + pPlusGainLayer + nPlusPlusLayer)) #μm, whatever's leftover after the other layers fill the 100μm




# Record the start time using perf_counter
start_time = time.perf_counter()

# Create a figure and axis
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)  # Set figure size in inches

# Set axis limits
ax.set_xlim(0, width)
ax.set_ylim(0, thick)

# set axis labels and ticks to physical units
ax.set_xlabel("\xB5m")
ax.set_ylabel("\xB5m")
ax.set_xticks(np.linspace(0, width, 6))
ax.set_yticks(np.linspace(0, thick, 5))
ax.set_aspect('equal')


# Add a rectangular border
border = patches.Rectangle((0, 0), width, thick, linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(border)


#drawing layers
ax.add_patch(patches.Rectangle((0, thick-metalizationLayer), width, metalizationLayer, color=metalizationColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer)), width, insulationLayer, color=insulationColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer)), width, nPlusPlusLayer, color=nPlusPlusColor))
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer)), width, pBulkLayer, color=pBulkColor))

#calculate the y spacing once
ySpacePgain = thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pPlusGainLayer)

# 3 pixel loop
for pixNum in range(3):

    # Calculate left edge of the current p+ implant
    implantX = 5 + pixNum * (5 + pxPitch)

    # Contact on left side of implant
    contactLeftX = implantX
    ax.add_patch(patches.Rectangle((contactLeftX, thick - metalizationContactLayer), metalizationContactWidth, metalizationContactLayer, color=metalizationColor))

    # Contact on right side of implant
    contactRightX = implantX + pxPitch - metalizationContactWidth
    ax.add_patch(patches.Rectangle((contactRightX, thick - metalizationContactLayer), metalizationContactWidth, metalizationContactLayer, color=metalizationColor))

    # Add the p+ gain implant
    ax.add_patch(patches.Rectangle((implantX, ySpacePgain), pxPitch, pPlusGainLayer, color=pPlusGainColor))

    # Add trench in every gap (i.e., after every implant except the last)
    if numTrenches == 1 and pixNum < 2:
        fileName = f"{filePath}1TR-LGAD.gif"

        # Position the trench in the center of the 5μm gap between implants
        trenchX = implantX + pxPitch + (pixelGap - trenchWidth) / 2
        ax.add_patch(patches.Rectangle((trenchX, thick - trenchDepth), trenchWidth, trenchDepth, color=trenchColor))
        # 5μm sauce: https://indico.cern.ch/event/855994/contributions/3637012/attachments/1947013/3230442/RD50_19_11_Pater.pdf
        # and https://www.mdpi.com/sensors/sensors-23-06225/article_deploy/html/images/sensors-23-06225-g001.png
    
    elif numTrenches == 2 and pixNum < 2:
        fileName = f"{filePath}2TR-LGAD.gif"
        gapStartX = implantX + pxPitch  # Start of the 5μm gap
        trench1X = gapStartX + 1  # First trench 1 μm into the gap
        trench2X = trench1X + trenchWidth + 1  # Second trench after 1 μm spacing
        ax.add_patch(patches.Rectangle((trench1X, thick - trenchDepth), trenchWidth, trenchDepth, color=trenchColor))
        ax.add_patch(patches.Rectangle((trench2X, thick - trenchDepth), trenchWidth, trenchDepth, color=trenchColor))


#add the p++ as the bottom layer
ax.add_patch(patches.Rectangle((0, thick-(metalizationLayer+insulationLayer+pPlusGainLayer+pBulkLayer)), width, pPlusPlusLayer, color=pPlusPlusColor))


## doping layer labeling
ax.annotate("metalization", xy=(labelIndent, thick-metalizationLayer/2), color="k", fontsize=8, ha='left', va='center')
ax.annotate('insulation', xy=(labelIndent, thick-(metalizationLayer+insulationLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('n++', xy=(labelIndent, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p+ (gain)', xy=(labelIndent, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pPlusGainLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p- (bulk)', xy=(labelIndent, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer/2)), color='black', fontsize=8, ha='left', va='center')
ax.annotate('p++', xy=(labelIndent, thick-(metalizationLayer+insulationLayer+nPlusPlusLayer+pBulkLayer+pPlusPlusLayer/2)), color='black', fontsize=8, ha='left', va='center')

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

# Thresholds where particles should be removed, the n++ and p++ layers
nPlusPlusTop = thick - (metalizationLayer + insulationLayer + nPlusPlusLayer/2)  # middle of n++ layer
pPlusPlusBottom = thick - (metalizationLayer + insulationLayer + nPlusPlusLayer + pBulkLayer + pPlusPlusLayer/2)  # middle of p++ layer

# add a legend for the different particles
ax.legend([pion, dotse[0], dotsh[0]], ['Pion', 'Electron', 'Hole'], loc='lower right')

# Initialize the line for the pion's trail
line, = ax.plot([], [], lw=2, color=pionColor)

# Lists to store the dot's path (history of positions)
x_data, y_data = [], []

# Function to update the position of the purple dot
def update(frame):
    x = 100 - frame * 3  # Move the dot horizontally
    y = thick - frame * 20  # Move the dot vertically
    x_data.append(x)
    y_data.append(y)
    pion.set_data([x], [y])
    line.set_data(x_data, y_data)

    if frame < 5:
        for i in range(n_dots):
            dotse[i].set_data([1000], [1000])  # hide electrons
            dotsh[i].set_data([1000], [1000])  # hide holes
    else:
        for i in range(n_dots):
            # Update electron
            y_pose[i] += 0.6  # electrons go downward
            if y_pose[i] > nPlusPlusTop:
                dotse[i].set_data([1000], [1000])  # remove electron
            else:
                dotse[i].set_data([x_pose[i]], [y_pose[i]])

            # Update hole
            y_posh[i] -= 0.2  # holes go upward
            if y_posh[i] < pPlusPlusBottom:
                dotsh[i].set_data([1000], [1000])  # remove hole
            else:
                dotsh[i].set_data([x_posh[i]], [y_posh[i]])

    return pion, line, *dotse, *dotsh


# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(numFrames), blit=True)
ani.save(fileName, writer=PillowWriter(fps=fps))

# Record the end time using perf_counter
end_time = time.perf_counter()

# Calculate the time elapsed making and saving the animation
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.5f} seconds")