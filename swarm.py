from particle import Particle
import random
import numpy as np


class Swarm:
    '''
    Initialize the swarm with support for different topologies
    '''
    def __init__(self, 
                 domainFunc, 
                 functionBounds,
                 dim, 
                 num_particles,
                 max_iter, 
                 topology,  # New parameter: "global", "ring", or "vonneumann"
                 regrouping_period=20,
                 num_regions=5):
        self.domainFunc = domainFunc
        self.functionBounds = functionBounds
        self.dim = dim
        self.num_particles = num_particles
        self.num_regions = num_regions
        self.max_iter = max_iter
        self.regrouping_period = regrouping_period
        self.topology = topology  # Store selected topology
        
        # give colours
        self.subswarm_colors = self.generate_colors()
        
        # set up particles
        self.particles = [
            Particle(dim, self.functionBounds, self.domainFunc) 
            for _ in range(num_particles)
        ]
        self.global_best_pos = None
        self.global_best_val = float('inf')
        
        # Calculate the grid size for Von Neumann topology if needed
        if self.topology == "VN":
            # Make sure num_particles is a perfect square for simplicity
            # If not, adjust it to the closest perfect square
            self.grid_size = int(np.sqrt(num_particles))
            if self.grid_size**2 != num_particles:
                self.grid_size = int(np.sqrt(num_particles))
                actual_particles = self.grid_size**2
                print(f"Warning: Adjusted particle count to {actual_particles} for Von Neumann topology")
                # Adjust particles list if necessary
                if actual_particles < num_particles:
                    self.particles = self.particles[:actual_particles]
                elif actual_particles > num_particles:
                    extra_needed = actual_particles - num_particles
                    for _ in range(extra_needed):
                        self.particles.append(Particle(dim, self.functionBounds, self.domainFunc))
                self.num_particles = actual_particles
        
        # make subswarms from particles
        self.subswarms = self.create_subswarms()
        
        # Assign colors
        self.assign_colors()
        
        # Initialize neighborhood best positions based on topology
        self.neighborhood_best_positions = [None] * len(self.particles)
        self.neighborhood_best_values = [float('inf')] * len(self.particles)
        self.update_all_neighborhoods()
    
    def generate_colors(self):
        '''
        generate colors for subswarms
        '''
        return [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255)   # Magenta
        ]
    
    def assign_colors(self):
        """
        give color based on generated colors
        """
        for subswarm_index, subswarm in enumerate(self.subswarms):
            color = self.subswarm_colors[subswarm_index % len(self.subswarm_colors)]
            for particle in subswarm:
                particle.subswarm_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
    
    def create_subswarms(self):
        """
        Divide particles into subswarms
        """
        random.shuffle(self.particles)
        subswarm_size = len(self.particles) // self.num_regions
        # Ensure we include any remainder particles
        subswarms = [
            self.particles[i:i+subswarm_size] 
            for i in range(0, len(self.particles), subswarm_size)
        ]
        
        # If there are remaining particles, distribute them
        remainder = len(self.particles) % self.num_regions
        if remainder:
            for i in range(remainder):
                subswarms[i].append(self.particles[-(i+1)])
        
        return subswarms
    
    def regroup_subswarms(self):
        """
        Regroup subswarms
        shuffles the particles and recreates subswarms
        """
        random.shuffle(self.particles)
        self.subswarms = self.create_subswarms()
        self.assign_colors()
    
    def update_global_best(self, particle, value):
        """
        Update global best position
        """
        if value < self.global_best_val:
            self.global_best_val = value
            self.global_best_pos = particle.position.copy()
    
    def get_ring_neighbors(self, index):
        """
        Get indices of neighbors in a ring topology
        """
        left = (index - 1) % len(self.particles)
        right = (index + 1) % len(self.particles)
        return [left, index, right]
    
    def get_vonneumann_neighbors(self, index):
        """
        Get indices of neighbors in a Von Neumann topology
        """
        row = index // self.grid_size
        col = index % self.grid_size
        
        # Get the indices of the four adjacent neighbors (north, east, south, west)
        north = ((row - 1) % self.grid_size) * self.grid_size + col
        east = row * self.grid_size + ((col + 1) % self.grid_size)
        south = ((row + 1) % self.grid_size) * self.grid_size + col
        west = row * self.grid_size + ((col - 1) % self.grid_size)
        
        # Include the center point itself
        return [north, east, south, west, index]
    
    def update_neighborhood_best(self, index):
        """
        Update the best position in the neighborhood for a particle
        """
        # Determine neighbors based on topology
        if self.topology == "Global":
            # Global best - no need to update individual neighborhoods
            self.neighborhood_best_positions[index] = self.global_best_pos
            self.neighborhood_best_values[index] = self.global_best_val
        elif self.topology == "Ring":
            # Ring topology neighbors
            neighbors = self.get_ring_neighbors(index)
            best_val = float('inf')
            best_pos = None
            
            # Find best among neighbors
            for n_idx in neighbors:
                particle = self.particles[n_idx]
                val = particle.personal_best_fitness
                if val < best_val:
                    best_val = val
                    best_pos = particle.personal_best_position.copy()
            
            self.neighborhood_best_positions[index] = best_pos
            self.neighborhood_best_values[index] = best_val
        
        elif self.topology == "VN":
            # Von Neumann topology neighbors
            neighbors = self.get_vonneumann_neighbors(index)
            best_val = float('inf')
            best_pos = None
            
            # Find best among neighbors
            for n_idx in neighbors:
                particle = self.particles[n_idx]
                val = particle.personal_best_fitness
                if val < best_val:
                    best_val = val
                    best_pos = particle.personal_best_position.copy()
            
            self.neighborhood_best_positions[index] = best_pos
            self.neighborhood_best_values[index] = best_val
    
    def update_all_neighborhoods(self):
        """
        Update the neighborhood best positions for all particles
        """
        for i in range(len(self.particles)):
            self.update_neighborhood_best(i)
    
    def updateSwarm(self):
        """
        Update the entire swarm for one iteration
        """
        # Regrouping to prevent stagnation
        # If initialized iteration count
        if hasattr(self, 'iteration_count'):
            self.iteration_count += 1
            if self.iteration_count % self.regrouping_period == 0:
                self.regroup_subswarms()
        else:  # Initialize
            self.iteration_count = 0
        
        # Evaluate fitness for each particle and update personal best
        for i, particle in enumerate(self.particles):
            value = particle.evalPosition(particle.position[0], particle.position[1])
            particle.update_personal_best(value)
            
            # Update global best
            if value < self.global_best_val:
                self.global_best_val = value
                self.global_best_pos = particle.position.copy()
        
        # Update neighborhood bests based on topology
        self.update_all_neighborhoods()
        
        # Update particle positions using appropriate neighborhood best
        for i, particle in enumerate(self.particles):
            # Use neighborhood best instead of global best
            neighborhood_best = self.neighborhood_best_positions[i]
            particle.update_position(neighborhood_best)
        
        return self.particles
    
    def getResults(self, topology):
        #initialise needed arrays
        final_values = []
        personal_best_values = []
        
        #final position values
        for particle in self.particles:
            final_value = self.domainFunc(particle.position[0], particle.position[1])  # Changed from evalPosition to value
            final_values.append(final_value)
        
        #personal best values
        personal_best_values = [p.evalPosition(p.personal_best_position[0], p.personal_best_position[0]) for p in self.particles]
        
        # Matches bestValue in particle class
        if topology == "Global":
            # Calculate stats for final positions
            final_mean = np.mean(final_values)
            final_std = np.std(final_values)
            # Calculate stats for personal best positions
            pb_mean = np.mean(personal_best_values)
            pb_std = np.std(personal_best_values)
        elif topology == "Ring":
            #Ring topology stats (final positions)
            ring_final_vals = np.array([],dtype=np.float64)
            for i in range(len(self.particles)):
                leftNeighbor = i-1
                rightNeighbor = (i+1)%len(self.particles)
                print(f"left: {leftNeighbor}, right: {rightNeighbor}")
                print([final_values[leftNeighbor], final_values[i], final_values[rightNeighbor]])
                ringNeighbourBest = min([final_values[leftNeighbor], final_values[i], final_values[rightNeighbor]])
                ring_final_vals = np.append(ring_final_vals, ringNeighbourBest)
            final_mean = np.mean(ring_final_vals)
            final_std = np.std(ring_final_vals)
            
            # Ring topology calculations (personal best)
            ring_pb_vals = np.array([],dtype=np.float64)
            for i in range(len(self.particles)):
                leftNeighbor = i-1
                rightNeighbor = (i+1)%len(self.particles)
                ringNeighbourBest = min([personal_best_values[leftNeighbor], personal_best_values[i], personal_best_values[rightNeighbor]])
                ring_pb_vals = np.append(ring_pb_vals, ringNeighbourBest)
            pb_mean = np.mean(ring_pb_vals)
            pb_std = np.std(ring_pb_vals)
        else:
            # Von Neumann topology calculations (final positions)
            n = int(np.sqrt(len(self.particles)))
            final_vals_lattice = np.array(final_values).reshape(n,n)
            VN_final_vals = np.array([],dtype=np.float64)
            for i in range(n):
                for j in range(n):
                    leftNeighbor = (i-1) % n
                    rightNeighbor = (i+1) % n
                    topNeighbor = (j-1) % n
                    bottomNeighbor = (j+1) % n
                    
                    center_val = final_vals_lattice[i,j]
                    left_val = final_vals_lattice[leftNeighbor,j]
                    right_val = final_vals_lattice[rightNeighbor,j]
                    top_val = final_vals_lattice[i,topNeighbor]
                    bottom_val = final_vals_lattice[i,bottomNeighbor]
                    
                    laticeNeighbourBest = min([left_val, right_val, center_val, top_val, bottom_val])
                    VN_final_vals = np.append(VN_final_vals, laticeNeighbourBest)
            final_mean = np.mean(VN_final_vals)
            final_std = np.std(VN_final_vals)
            
            # Von Neumann topology calculations (personal best)
            pb_vals_lattice = np.array(personal_best_values).reshape(n,n)
            VN_pb_vals = np.array([],dtype=np.float64)
            for i in range(n):
                for j in range(n):
                    leftNeighbor = (i-1) % n
                    rightNeighbor = (i+1) % n
                    topNeighbor = (j-1) % n
                    bottomNeighbor = (j+1) % n
                    
                    center_val = pb_vals_lattice[i,j]
                    left_val = pb_vals_lattice[leftNeighbor,j]
                    right_val = pb_vals_lattice[rightNeighbor,j]
                    top_val = pb_vals_lattice[i,topNeighbor]
                    bottom_val = pb_vals_lattice[i,bottomNeighbor]
                    
                    laticeNeighbourBest = min([left_val, right_val, center_val, top_val, bottom_val])
                    VN_pb_vals = np.append(VN_pb_vals, laticeNeighbourBest)
            pb_mean = np.mean(VN_pb_vals)
            pb_std = np.std(VN_pb_vals)
        
        print(f"len particles: {len(self.particles)}")
        #Return the relevant values 
        return (final_mean, final_std, 
            pb_mean, pb_std)