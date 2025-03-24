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
        #mean and standard deviation
        mean = sum([p.value for p in self.particles]) / len(self.particles)
        std = (sum([(p.value - mean)**2 for p in self.particles]) / len(self.particles))**0.5
        globalMean = sum([p.bestValue for p in self.particles]) / len(self.particles)
        globalStd = (sum([(p.bestValue - globalMean)**2 for p in self.particles]) / len(self.particles))**0.5
        
        #ring topology mean and std
        pbValues = np.array([p.bestValue for p in self.particles], dtype=np.float64)
        #print(pbValues[10])
        ringBestVals = np.array([],dtype=np.float64)
        for i in range(len(self.particles)):
            leftNeighbor = i-1
            rightNeighbor = (i+1)%len(self.particles)
            #print(pbValues[leftNeighbor])
            ringNeighbourBest = min([pbValues[leftNeighbor], pbValues[i], pbValues[rightNeighbor]])
            if self.selected_domain == "Weierstrass" and self.pType == "Standard":
                print(f"ring neighbour best swarm.py{ringNeighbourBest}")
            ringBestVals = np.append(ringBestVals, ringNeighbourBest)
            #print(meanVals[i])
        #print(meanVals)
        #print(pbValues)
        ringMean = np.mean(ringBestVals)
        ringStd = np.std(ringBestVals)
        if self.selected_domain == "Weierstrass" and self.pType == "Standard":
            print(f" >0ringMean???{ringMean}")
            #print(f" >0???{sum([p.bestValue for p in self.particles])/1024}")

        #Von Neumann (Latice) topology mean and std
        n = np.sqrt(len(self.particles))
        n = int(n)
        pbValsLatice = pbValues.reshape(n,n)
        VNBestVals = np.array([],dtype=np.float64)
        for i in range(n):
            for j in range(n):
                leftNeighbor = i-1 % n
                rightNeighbor = (i+1)%n
                topNeighbor = j-1 % n
                bottomNeighbor = (j+1)%n
                
                center_val = pbValsLatice[i,j]
                left_val = pbValsLatice[leftNeighbor,j]
                right_val = pbValsLatice[rightNeighbor,j]
                top_val = pbValsLatice[i,topNeighbor]
                bottom_val = pbValsLatice[i,bottomNeighbor]
                
                
            
                laticeNeighbourBest = min([left_val, right_val, center_val, top_val, bottom_val])
                if self.selected_domain == "Weierstrass" and self.pType == "Standard":
                    print(f"VN neighborhood at [{i},{j}]: C:{center_val:.6f}, L:{left_val:.6f}, R:{right_val:.6f}, T:{top_val:.6f}, B:{bottom_val:.6f}")
                    print(f"best min: {laticeNeighbourBest}")
                
                VNBestVals = np.append(VNBestVals, laticeNeighbourBest)

        
        VNMean = np.mean(VNBestVals)
        VNStd = np.std(VNBestVals)
        #if self.selected_domain == "Weierstrass" and self.pType == "StandardWithDampeningFactor":
         #           print(f"mean and std: {VNMean}, {VNStd} and then number of particles: {len(VNBestVals)}")
          #          for p in VNBestVals:
           #             print(f"p: {p}")
        return mean, std, globalMean, globalStd, ringMean, ringStd, VNMean, VNStd