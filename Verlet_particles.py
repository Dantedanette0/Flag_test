import pygame


WIDTH = 1200
HEIGHT = 680

RED = (255, 0, 0)

mouse = False
class Particle:
    def __init__(self, x = 10, y = 10, mass=0.2,size = 0.5):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.mass = mass
        self.fixed = False  
        self.selected = False
        self.force_x = 0
        self.force_y = 10 * self.mass  
        self.size = size
        self.drag = 0.99

    def update(self, dt):
        if not self.fixed and not self.selected:
            
            #since we are working with units of time v is just delta x
            vel_x = (self.x - self.old_x)
            vel_y = (self.y - self.old_y)

            
            damping_factor = 0.02
            vel_x -= vel_x*damping_factor
            vel_y -= vel_y*damping_factor

            self.old_x = self.x
            self.old_y = self.y


            acc_x = self.force_x / self.mass
            acc_y = self.force_y / self.mass


            self.x += vel_x + acc_x * dt * dt
            self.y += vel_y + acc_y * dt * dt

            if self.x < 0 or self.x > WIDTH:
                self.x, self.old_x = self.old_x, self.x
            if self.y < 0 or self.y > HEIGHT:
                self.y, self.old_y = self.old_y, self.y
                
    def get_color_based_on_position(self, width, height):
        red = max(0, min(int((self.x / width) * 255), 255))
        blue = max(0, min(int((self.y / height) * 255), 255))
        green = min(int(self.force_x * 255), 255)
        return (red, green, blue)


    def set_pos(self, pos):
        if not self.fixed:  
            self.x, self.y = pos

    def draw(self, surf):
        color = self.get_color_based_on_position(WIDTH, HEIGHT) if not self.selected else RED
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), self.size)
