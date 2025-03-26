import sys
import numpy as np
import matplotlib.pyplot as plt
from swarm import Swarm
import searchDomain
from bounds import Bounds
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors

def main(selected_domain, domain_dict, functionBounds):
    ###
    numIterations = 50
    x_min, x_max = functionBounds[0], functionBounds[1]
    y_min, y_max = functionBounds[2], functionBounds[3]
    #print(f"Bounds: {x_min}, {x_max}, {y_min}, {y_max}")
    x = np.linspace(x_min, x_max, 1000) 
    y = np.linspace(y_min, y_max, 1000)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(domain_dict[selected_domain])(X, Y)
    ###

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')  
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='none', alpha=0.7)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title(f'{selected_domain} Search Domain Visualization')

    
    swarm = Swarm(
        domain_dict[selected_domain],
        functionBounds, 
        dim=2,  #dimension is used later 
        num_particles=100, 
        max_iter=numIterations,
    )

    #starting scatter plot with colors
    scat = ax.scatter(
        [p.position[0] for p in swarm.particles],
        [p.position[1] for p in swarm.particles],
        [domain_dict[selected_domain](p.position[0], p.position[1]) for p in swarm.particles],
        c=[p.subswarm_color for p in swarm.particles],
        s=20, 
        marker='o', 
        edgecolor='black'
    )

    currentIteration = [0] 
    ##update swarm and animation
    def update(frame):
        if currentIteration[0] < numIterations:
            swarm.updateSwarm()  # Update swarm position
            currentIteration[0] += 1
        else:
            ani.event_source.stop()
        
        new_positions = np.array([p.position for p in swarm.particles])
        scat.set_offsets(new_positions)  # Update X and Y positions
        scat.set_3d_properties([domain_dict[selected_domain](p.position[0], p.position[1]) for p in swarm.particles], zdir='z')  # Update Z positions
        
        scat.set_color([p.subswarm_color for p in swarm.particles])

        return scat

    ani = FuncAnimation(fig, update, frames=numIterations, interval=1000, blit=False, repeat=False)
    fig.colorbar(surf)
    plt.show()

if len(sys.argv) > 1:
    selected_domain = sys.argv[1]
    print(f"Received domain: {selected_domain}")
    
    domain_dict = searchDomain.calc_dict(sys.argv[2:])
    bounds = Bounds()
    functionBounds = bounds.getBounds(selected_domain)
    
    if selected_domain in domain_dict:
        print(f"Plotting {selected_domain} function.")
        main(selected_domain, domain_dict, functionBounds)
    else:
        print(f"Error: Domain '{selected_domain}' not found in the dictionary.")
else:
    print("Error receiving domain.")