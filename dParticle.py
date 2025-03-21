from random import uniform
from particle import particle

class dParticle(particle):
    def __init__(self, evalPosition, selected_domain, numIterations):
        # Call the parent class's __init__ method
        super().__init__(evalPosition, selected_domain)
        self.iteration = 0
        self.numIterations = numIterations

    def updateVelocity(self, globalBestX, globalBestY):
        #new Vel = interia * old vel + c1 * rand() * (pbest - current) + c2 * rand() * (gbest - current)
        self.xv = (0.2 * self.xv + 2 * uniform(0,1) * (self.bestX - self.xpos) + 2 * uniform(0,1) * (globalBestX - self.xpos)) * (1 - self.iteration/self.numIterations)
        self.yv = (0.2 * self.yv + 2 * uniform(0,1) * (self.bestY - self.ypos) + 2 * uniform(0,1) * (globalBestY - self.ypos)) * (1 - self.iteration/self.numIterations)
        #print(f"gbesyt: {globalBest}")

        self.iteration += 1

        return self.xv, self.yv