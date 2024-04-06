import pygame
import math
from Verlet_particles import Particle  
from Verlet_Constraints import Constraint 
#currently useless page this is for future
class object_creator:
    def __init__(self, particles, constraints):
        self.particles = particles
        self.constraints = constraints
        
    def create_flag(self):
        self.create_particles(num_x=20, num_y=20, start_x=500, start_y=100, spacing=5)
        self.create_constraints(10, 15)

    
    
    def create_particles(self,num_x=40, num_y=40, start_x=100, start_y=200, spacing=10.0):

        for j in range(num_y):
            for i in range(num_x):
                x = start_x + i * spacing
                y = start_y + j * spacing
                p = Particle(x, y)
                # anchors
                if j == 0 and (i == 0 or i == num_x - 1):
                    p.fixed = True
                self.particles.append(p)
                
    def create_constraints(self,particles, num_x, num_y):
        for j in range(num_y):
            for i in range(num_x):
                if i < (num_x - 1):
                    particle1 = particles[i + j * num_x]
                    particle2 = particles[(i + 1) + j * num_x]
                    self.constraints.append(Constraint(particle1, particle2))

                if j < (num_y - 1):
                    particle1 = particles[i + j * num_x]
                    particle2 = particles[i + (j + 1) * num_x]
                    self.constraints.append(Constraint(particle1, particle2))
