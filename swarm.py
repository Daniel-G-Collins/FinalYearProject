from particle import Particle
import random
import numpy as np


class Swarm:
    '''
    Initialize the swarm (dim may be implemented later)
    '''
    def __init__(self, 
                 domainFunc, 
                 functionBounds,
                 dim, 
                 num_particles,
                 max_iter, 
                 regrouping_period=20,
                 num_regions = 5):
        self.domainFunc = domainFunc
        self.functionBounds = functionBounds
        self.dim = dim
        self.num_particles = num_particles
        self.num_regions = num_regions
        self.max_iter = max_iter
        self.regrouping_period = regrouping_period
        
        #give colours
        self.subswarm_colors = self.generate_colors()
        
        #set up particles
        self.particles = [
            Particle(dim, self.functionBounds ,self.domainFunc) 
            for _ in range(num_particles)
        ]
        self.global_best_pos = None
        self.global_best_val = float('inf')
        
        #make subswarms from particles
        self.subswarms = self.create_subswarms()
        
        #Assign colors
        self.assign_colors()
        
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
            color = self.subswarm_colors[subswarm_index]
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
        shuffles the patricles and recreates subswarms
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
    
    def updateSwarm(self):
        """
        Update the entire swarm for one iteration
        """
        #regrouping to prevent stagnation
        #if initialised iteration count
        if hasattr(self, 'iteration_count'):
            self.iteration_count += 1
            if self.iteration_count % self.regrouping_period == 0:
                self.regroup_subswarms()
        else:#intialise
            self.iteration_count = 0
        
        #eval fitness (position) for each particle
        for particle in self.particles:
            value = particle.evalPosition(particle.position[0], particle.position[1])
            particle.update_personal_best(value)
            
            #global best
            if value < self.global_best_val:
                self.global_best_val = value	
                self.global_best_pos = particle.position.copy()
        
        #update particle positions
        for particle in self.particles:
            #dependant on g.best
            particle.update_position(self.global_best_pos)
        
        return self.particles
    
    def getResults(self):
        final_values = []
        personal_best_values = []
        
        #final positions
        for particle in self.particles:
            final_value = particle.evalPosition(particle.position[0], particle.position[1])
            final_values.append(final_value)
        
        #personal best values
        personal_best_values = [p.personal_best_fitness for p in self.particles]
        
        #Calculate stats for final positions
        final_mean = np.mean(final_values)
        final_std = np.std(final_values)
        
        #Calculate stats for personal best
        pb_mean = np.mean(personal_best_values)
        pb_std = np.std(personal_best_values)
        # Ring topology calculations (final positions)
        ring_final_vals = np.array([],dtype=np.float64)
        for i in range(len(self.particles)):
            leftNeighbor = i-1
            rightNeighbor = (i+1)%len(self.particles)
            ringNeighbourBest = min([final_values[leftNeighbor], final_values[i], final_values[rightNeighbor]])
            ring_final_vals = np.append(ring_final_vals, ringNeighbourBest)
        ring_final_mean = np.mean(ring_final_vals)
        ring_final_std = np.std(ring_final_vals)
        
        #RIng topology calculations (personal best)
        ring_pb_vals = np.array([],dtype=np.float64)
        for i in range(len(self.particles)):
            leftNeighbor = i-1
            rightNeighbor = (i+1)%len(self.particles)
            ringNeighbourBest = min([personal_best_values[leftNeighbor], personal_best_values[i], personal_best_values[rightNeighbor]])
            ring_pb_vals = np.append(ring_pb_vals, ringNeighbourBest)
        ring_pb_mean = np.mean(ring_pb_vals)
        ring_pb_std = np.std(ring_pb_vals)
        
        #Von Neumann topology calculations (final positions)
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
        VN_final_mean = np.mean(VN_final_vals)
        VN_final_std = np.std(VN_final_vals)
        
        #VN topology calculations (personal best)
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
        VN_pb_mean = np.mean(VN_pb_vals)
        VN_pb_std = np.std(VN_pb_vals)
        
        #Return the original values 
        return (final_mean, final_std, 
            pb_mean, pb_std, 
            ring_final_mean, ring_final_std, 
            ring_pb_mean, ring_pb_std, 
            VN_final_mean, VN_final_std, 
            VN_pb_mean, VN_pb_std
            )