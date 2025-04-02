import sys
import numpy as np
import matplotlib.pyplot as plt
from swarm import swarm
import searchDomain
from bounds import Bounds
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors

# handle passed domain
if len(sys.argv) > 1:
    #####
    numIterations = 100
    ####
    selected_domain = sys.argv[1]
    topology = sys.argv[2].replace(" ", "")
    pType = sys.argv[3].replace(" ", "")
    print(f"Received domain: {selected_domain}")
    domain_dict = searchDomain.calc_dict(sys.argv[3:])
    bounds = Bounds()
    functionBounds = bounds.getBounds(selected_domain)
    if selected_domain in domain_dict:
        print(f"Plotting {selected_domain} function.")
        

        x_min, x_max = functionBounds[0], functionBounds[1]
        y_min, y_max = functionBounds[2], functionBounds[3]


        x = np.linspace(x_min, x_max, 1000) 
        y = np.linspace(y_min, y_max, 1000)
        X, Y = np.meshgrid(x, y)

        
        # Default case for most domain functions
        Z = np.vectorize(domain_dict[selected_domain])(X, Y)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')  
        surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.7)

        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_title(f'{selected_domain} Search Domain Visualization')
        #ax.set_zlim(-0.0002, 0.0001)

        print(f"ptype:{pType}")
        #numParticles must be a perfect square for VN topology !!!!!!!!!!!!!!!!!!!!!!!!
        swarm = swarm(domain_dict[selected_domain], selected_domain, topology, numParticles=100, numIterations=numIterations, pType=pType)
        scat = ax.scatter(
            [p.xpos for p in swarm.particles],
            [p.ypos for p in swarm.particles],
            [p.value for p in swarm.particles],
            color='orange', s=20, marker='o', edgecolor='purple'
        )

        currentIteration = [0] 

        def update(frame):
            #nonlocal currentIteration
            if currentIteration[0] < numIterations:
                swarm.updateSwarm(topology)  # Update swarm position based on velocity and best position
                currentIteration[0] += 1
            else:
                ani.event_source.stop()
            new_positions = np.array([[p.xpos, p.ypos] for p in swarm.particles])
            scat.set_offsets(new_positions)  # Update X and Y positions
            scat.set_3d_properties([p.value for p in swarm.particles], zdir='z')  # Update Z positions

            return scat

        ani = FuncAnimation(fig, update, frames=numIterations, interval=1000, blit=False, repeat=False)
        fig.colorbar(surf)
        plt.show()
        
    else:
        print(f"Error: Domain '{selected_domain}' not found in the dictionary.")
else:
    print("Error receiving domain.")