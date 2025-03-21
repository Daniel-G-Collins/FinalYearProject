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
            case "StandardWithDampening":
                self.particles = [dParticle(self.evalPosition, self.selected_domain, numIterations) for i in range(numParticles)]
            case "Standard":
                self.particles = [particle(self.evalPosition, self.selected_domain) for i in range(numParticles)]
       
        bestParticle = sorted(self.particles, key=lambda x: x.bestValue, reverse=False)[0]
        self.globalBestX = bestParticle.xpos
        self.globalBestY = bestParticle.ypos
        
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
        pbValues =[p.bestValue for p in self.particles]
        pbValues = np.array(pbValues)
        #print(pbValues[10])
        meanVals = np.zeros(len(self.particles))
        for i in range(len(self.particles)):
            leftNeighbor = i-1
            rightNeighbor = (i+1)%len(self.particles)
            #print(pbValues[leftNeighbor])
            ringNeighbourBest = [pbValues[leftNeighbor], pbValues[i], pbValues[rightNeighbor]]
            #print(ringNeighbourBest)
            meanVals[i] = np.mean(ringNeighbourBest)
            #print(meanVals[i])
        #print(meanVals)
        #print(pbValues)
        ringMean = np.mean(meanVals)
        ringStd = np.std(meanVals)
        

        #Von Neumann (Latice) topology mean and std
        n = np.sqrt(len(self.particles))
        n = int(n)
        pbValsLatice = pbValues.reshape(n,n)
        VNMeanVals = np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                leftNeighbor = i-1
                rightNeighbor = (i+1)%n
                topNeighbor = j-1
                bottomNeighbor = (j+1)%n
                laticeNeighbourBest = [pbValsLatice[leftNeighbor,j], pbValsLatice[rightNeighbor,j], pbValsLatice[i,j], pbValsLatice[i,topNeighbor], pbValsLatice[i,bottomNeighbor]]
                VNMeanVals[i][j] = np.mean(laticeNeighbourBest)
        VNMean = np.mean(VNMeanVals)
        VNStd = np.std(VNMeanVals)
        
        return mean, std, globalMean, globalStd, ringMean, ringStd, VNMean, VNStd