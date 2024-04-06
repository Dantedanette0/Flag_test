import pygame
import math

class Constraint:
    def __init__(self, particle1, particle2, size=2, stiffness=0.8):
        self.particle1 = particle1
        self.particle2 = particle2
        delta_x = self.particle1.x - self.particle2.x
        delta_y = self.particle1.y - self.particle2.y
        self.restLength = math.sqrt(delta_x**2 + delta_y**2)
        self.size = size
        self.stiffness = stiffness 

    def update(self):
        #change the particle position based on delta x and y 
        delta_x = self.particle2.x - self.particle1.x
        delta_y = self.particle2.y - self.particle1.y
        deltaLength = math.sqrt(delta_x**2 + delta_y**2)
        diff = (deltaLength - self.restLength) / (deltaLength + 0.00001) * self.stiffness

        if not self.particle1.fixed:
            self.particle1.x += 0.5 * diff * delta_x
            self.particle1.y += 0.5 * diff * delta_y
        if not self.particle2.fixed:
            self.particle2.x -= 0.5 * diff * delta_x
            self.particle2.y -= 0.5 * diff * delta_y

    def draw(self, surf):
        # Calculate color based on delta x and delta y
        delta_x = abs(self.particle2.x - self.particle1.x)
        delta_y = abs(self.particle2.y - self.particle1.y)

        #change color based on delta x and y
        red = int(min(delta_x * 10, 255))
        blue = int(min(delta_y * 10, 255))
        color = (red, 100, blue)  #start from green more delta x = more red and more delta y = more blue

        pygame.draw.line(surf, color, (int(self.particle1.x), int(self.particle1.y)), (int(self.particle2.x), (int(self.particle2.y))), self.size)
