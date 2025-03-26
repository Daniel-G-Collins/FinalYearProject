from particle import particle
from dParticle import dParticle
import numpy as np

class swarm:
    def __init__(self, domainFunc, selected_domain, numParticles, numIterations, pType):
        self.numIterations = numIterations
        self.evalPosition = domainFunc
        self.selected_domain = selected_domain
        self.pType = pType
        match pType:
            case "StandardWithDampeningFactor":
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

    def updateSwarm(self):
        for particle in self.particles:
            particle.update(self.globalBestX, self.globalBestY)

    def getPositionVal(x, y):
        return particle.getValue(x, y)

    def getResults(self):
        # Prepare lists to store values
        final_values = []
        personal_best_values = []
        
        # Collect final position values
        for particle in self.particles:
            final_value = particle.value  # Changed from evalPosition to value
            final_values.append(final_value)
        
        # Collect personal best values
        personal_best_values = [p.bestValue for p in self.particles]  # Matches bestValue in particle class
        
        # Calculate statistics for final positions
        final_mean = np.mean(final_values)
        final_std = np.std(final_values)
        # Calculate statistics for personal best positions
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
        
        # Ring topology calculations (personal best)
        ring_pb_vals = np.array([],dtype=np.float64)
        for i in range(len(self.particles)):
            leftNeighbor = i-1
            rightNeighbor = (i+1)%len(self.particles)
            ringNeighbourBest = min([personal_best_values[leftNeighbor], personal_best_values[i], personal_best_values[rightNeighbor]])
            ring_pb_vals = np.append(ring_pb_vals, ringNeighbourBest)
        ring_pb_mean = np.mean(ring_pb_vals)
        ring_pb_std = np.std(ring_pb_vals)
        
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
        VN_final_mean = np.mean(VN_final_vals)
        VN_final_std = np.std(VN_final_vals)
        
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
        VN_pb_mean = np.mean(VN_pb_vals)
        VN_pb_std = np.std(VN_pb_vals)
        
        # Return the original values 
        return (final_mean, final_std, 
            pb_mean, pb_std, 
            ring_final_mean, ring_final_std, 
            ring_pb_mean, ring_pb_std, 
            VN_final_mean, VN_final_std, 
            VN_pb_mean, VN_pb_std
            )