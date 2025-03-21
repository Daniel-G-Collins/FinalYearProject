from random import uniform
from bounds import Bounds
class particle:
    def __init__(self, evalPosition, selected_domain):
        self.globalBest = 0
        self.evalPosition = evalPosition
        self.bounds = Bounds()
        self.xmin, self.xmax, self.ymin, self.ymax = self.bounds.getBounds(selected_domain)
        self.xpos = uniform(self.xmin, self.xmax)
        self.ypos = uniform(self.ymin, self.ymax)
        self.bestX = self.xpos
        self.bestY = self.ypos
        self.xv = uniform(self.xmin/2, self.xmax/2)
        self.yv = uniform(self.ymin/2, self.ymax/2)
        self.value = self.getValue(self.xpos, self.ypos)
        self.bestValue = self.value
        
    

    '''  
    pseudocode:

    vid = vid +c1(pid −xid)+c2(pgd −xid)
    xid = xid +vid

    for each time step t do
        for each particle i in the swarm do
            update position x_t using eqs 1 & 2
            calculate particle fitness f(x_t)
            update p_i, p_g
        end for
    end for

    '''
    def update(self, globalBestX, globalBestY):
        self.globalBestX = globalBestX
        self.globalBestY = globalBestY      
        self.xpos += self.xv
        self.ypos += self.yv

        if self.xpos < self.xmin:
            self.xpos = self.xmin
        if self.xpos > self.xmax:
            self.xpos = self.xmax
        if self.ypos < self.ymin:
            self.ypos = self.ymin
        if self.ypos > self.ymax:
            self.ypos = self.ymax

        
        self.value = self.getValue(self.xpos, self.ypos)
        if self.value < self.bestValue:
            self.bestValue = self.value
            self.bestX = self.xpos
            self.bestY = self.ypos

        self.xv, self.yv = self.updateVelocity(globalBestX, globalBestY)


    def updateVelocity(self, globalBestX, globalBestY):
        #new Vel = interia * old vel + c1 * rand() * (pbest - current) + c2 * rand() * (gbest - current)
        self.xv = 0.2 * self.xv + 2 * uniform(0,1) * (self.bestX - self.xpos) + 2 * uniform(0,1) * (globalBestX - self.xpos)
        self.yv = 0.2 * self.yv + 2 * uniform(0,1) * (self.bestY - self.ypos) + 2 * uniform(0,1) * (globalBestY - self.ypos)
        #print(f"gbesyt: {globalBest}")
        return self.xv, self.yv

    def setGlobalBest(self, globalBestX, globalBestY):
        self.globalBestx = globalBestX
        self.globalBesty = globalBestY

    def getValue(self, x, y):
        return self.evalPosition(x, y)

