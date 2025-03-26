import numpy as np
from random import uniform

class Particle:
    def __init__(self, dim, functionBounds, evalPosition):
        self.dim = dim
        self.xmin = functionBounds[0]
        self.xmax = functionBounds[1]
        self.ymin = functionBounds[2]
        self.ymax = functionBounds[3]
        
        #Initial position within bounds
        self.position = np.array([
            uniform(self.xmin, self.xmax),
            uniform(self.ymin, self.ymax)
        ])
        
        #Velocity
        self.velocity = np.array([
            uniform(self.xmin/2, self.xmax/2),
            uniform(self.ymin/2, self.ymax/2)
        ])
        
        self.vmax = np.array([
            (self.xmax - self.xmin) * 0.2,  # e.g., 10% of world width
            (self.ymax - self.ymin) * 0.2   # e.g., 10% of world height
        ])
        #best positions
        self.personal_best_position = self.position.copy()
        self.personal_best_fitness = float('inf')
        
        #search domain lambda
        self.evalPosition = evalPosition
        self.subswarm_color = 'Null'
        
    def update_position(self, global_best, w=.72984, c1=2.05, c2=2.05):
        """
        Update particle position and velocity using PSO equations
        with strict bounds checking and improved boundary handling
        """
        #random
        r1 = np.random.rand(2)
        r2 = np.random.rand(2)
        
        #Cognitive component (personal best influence)
        cognitive = c1 * r1 * (self.personal_best_position - self.position)
        
        #Social component (global best influence)
        social = c2 * r2 * (global_best - self.position)
        
        #Update velocity (inertia*v + cognitive + social)
        self.velocity = (w * self.velocity + cognitive + social)
        
        #clip the velocity
        self.velocity = np.clip(self.velocity, -self.vmax, self.vmax)
        
        # new position
        new_position = self.position + self.velocity
        
        for i in range(2): #2dimensions
            # If out of bounds,bounce back
            if new_position[i] < (self.xmin if i == 0 else self.ymin):
                new_position[i] = self.xmin if i == 0 else self.ymin
                self.velocity[i] = -self.velocity[i] * 0.5 
            elif new_position[i] > (self.xmax if i == 0 else self.ymax):
                new_position[i] = self.xmax if i == 0 else self.ymax
                self.velocity[i] = -self.velocity[i] * 0.5
        
        # Update particle's position
        self.position = new_position
        
    def update_personal_best(self, fitness):
        """
        Update personal best position if current fitness is better
        """
        if fitness < self.personal_best_fitness:
            self.personal_best_fitness = fitness
            self.personal_best_position = self.position.copy()