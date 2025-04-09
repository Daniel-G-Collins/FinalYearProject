from random import uniform
from particle import particle

class dParticle(particle):
    def __init__(self, evalPosition, selected_domain, numIterations):
        # Call the parent class's __init__ method
        super().__init__(evalPosition, selected_domain)
        self.iteration = 0
        self.numIterations = numIterations

    def updateVelocity(self, globalBestX, globalBestY):
        #interia calculated using Clerc and Kennedy formula (2002)
        constrictionFactor = 0.72984
        c1 = 2.05
        c2 = 2.05
        r1 = uniform(0,1)
        r2 = uniform(0,1)
        #new Vel = ( interia * old vel + c1 * rand() * (pbest - current) + c2 * rand() * (gbest - current) ) * (1 - currentIteration/MacxIterations)
        self.xv = constrictionFactor * (self.xv + c1 * r1 * (self.bestX - self.xpos) + c2 * r2 * (globalBestX - self.xpos)) 
        self.yv = constrictionFactor * (self.yv + c1 * r1 * (self.bestY - self.ypos) + c2 * r2 * (globalBestY - self.ypos))
        #print(f"gbesyt: {globalBest}")

        self.iteration += 1

        return self.xv, self.yv