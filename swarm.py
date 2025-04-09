from particle import particle
from dParticle import dParticle
import numpy as np

class swarm:
    def __init__(self, domainFunc, selected_domain, topology, numParticles, numIterations, pType):
        self.numIterations = numIterations
        self.evalPosition = domainFunc
        self.selected_domain = selected_domain
        self.pType = pType
        self.topology = topology
        match pType:
            case "Constricted":
                self.particles = [dParticle(self.evalPosition, self.selected_domain, numIterations) for i in range(numParticles)]
            case "Standard":
                self.particles = [particle(self.evalPosition, self.selected_domain) for i in range(numParticles)]
       
        bestParticle = sorted(self.particles, key=lambda x: x.bestValue, reverse=False)[0]
        self.globalBestX = bestParticle.bestX
        self.globalBestY = bestParticle.bestY
        self.globalBest = bestParticle.bestValue
        
        #print(f"Global Best: {self.globalBest.xpos}, {self.globalBest.ypos}, {self.globalBest.value}")
        for p in self.particles:
            p.setGlobalBest(self.globalBestX, self.globalBestY) 
        self.domain = domainFunc

    def updateSwarm(self, topology):
        # First update the global best
        bestParticle = sorted(self.particles, key=lambda x: x.bestValue, reverse=False)[0]
        self.globalBestX = bestParticle.bestX
        self.globalBestY = bestParticle.bestY
        self.globalBest = bestParticle.bestValue
        
        # For each particle, find its neighborhood best according to topology
        for i, particle in enumerate(self.particles):
            if topology == "Global":
                # Standard PSO - use global best
                nbest_x, nbest_y = self.globalBestX, self.globalBestY
            elif topology == "Ring":
                # Ring topology
                left_neighbor = (i - 1) % len(self.particles)
                right_neighbor = (i + 1) % len(self.particles)
                
                # Find best among self and neighbors
                neighbors = [self.particles[left_neighbor], particle, self.particles[right_neighbor]]
                best_neighbor = sorted(neighbors, key=lambda p: p.bestValue, reverse=False)[0]
                nbest_x, nbest_y = best_neighbor.bestX, best_neighbor.bestY
            elif topology == "VN":
                # Von Neumann topology
                n = int(np.sqrt(len(self.particles)))
                row, col = i // n, i % n
                #print(f"row: {row}, col: {col}, i: {i}, n: {n}, len: {len(self.particles)}")
                # Find neighbors in lattice
                neighbors = []
                neighbors.append(particle)  # Self
                neighbors.append(self.particles[((row-1) % n) * n + col])  # Top
                neighbors.append(self.particles[((row+1) % n) * n + col])  # Bottom
                neighbors.append(self.particles[row * n + ((col-1) % n)])  # Left
                neighbors.append(self.particles[row * n + ((col+1) % n)])  # Right
                
                best_neighbor = sorted(neighbors, key=lambda p: p.bestValue, reverse=False)[0]
                nbest_x, nbest_y = best_neighbor.bestX, best_neighbor.bestY
            
            particle.update(nbest_x, nbest_y) 

    def getPositionVal(x, y):
        return particle.getValue(x, y)

    def getResults(self, topology):
        #initialise needed arrays
        final_values = []
        personal_best_values = []
        
        #final position values
        for particle in self.particles:
            final_value = particle.value  # Changed from evalPosition to value
            final_values.append(final_value)
        
        #personal best values
        personal_best_values = [p.bestValue for p in self.particles]  # Matches bestValue in particle class
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
        
        #Return the relevant values 
        return (final_mean, final_std, 
            pb_mean, pb_std)