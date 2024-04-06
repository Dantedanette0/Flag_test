import pygame
import math
from Verlet_particles import Particle  
from Verlet_Constraints import Constraint  
import random

class EventHandler:
    def __init__(self, particles, constraints):
        self.particles = particles
        self.constraints = constraints
        self.wind_active = False
        self.mouse_dragging = False
        self.right_mouse_held = False 
        self.wind_strength = 0.10 

    #god knows what this does at this point
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_mouse_down(event.pos)
                elif event.button == 3:  # Right mouse button
                    self.right_mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    self.handle_mouse_up()
                elif event.button == 3:  # Right mouse button released
                    self.right_mouse_held = False
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_dragging:
                    self.handle_mouse_motion(event.pos)
                if self.right_mouse_held:
                    self.remove_constraint(event.pos)  # Continuously check for removal
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)
        return True


    #when clicking left mouse button track it 
    def handle_mouse_down(self, pos):
        self.mouse_dragging = True
        for particle in self.particles:
            if math.hypot(particle.x - pos[0], particle.y - pos[1]) < 20:  
                particle.selected = True
                break  
    def handle_mouse_up(self):
        self.mouse_dragging = False
        for particle in self.particles:
            particle.selected = False  #
    def handle_mouse_motion(self, pos):
        for particle in self.particles:
            if particle.selected:
                particle.x, particle.y = pos 

                
                
    def point_line_distance(self, point, line_start, line_end):
        x1, y1 = line_start
        x2, y2 = line_end
        x0, y0 = point

        length_squared = (x2 - x1)**2 + (y2 - y1)**2
        if length_squared == 0:
            return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

        t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / length_squared))
        projection = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        return math.sqrt((x0 - projection[0])**2 + (y0 - projection[1])**2)

    def remove_constraint(self, click_pos):
        closest_constraint = None
        min_distance = float('inf')
        for constraint in self.constraints:
            distance = self.point_line_distance(click_pos, (constraint.particle1.x, constraint.particle1.y), (constraint.particle2.x, constraint.particle2.y))
            if distance < min_distance:
                min_distance = distance
                closest_constraint = constraint
        if min_distance < 10:  # how close to click
            self.constraints.remove(closest_constraint)

    
    def handle_keydown(self, key):
        if key == pygame.K_w:
            self.wind_active = True
        elif key == pygame.K_f:
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            self.create_flag(start_x=mouse_x, start_y=mouse_y) 

    def handle_keyup(self, key):
        if key == pygame.K_w:
            self.wind_active = False

    #simulating wind
    def apply_wind(self):
        if self.wind_active:
            for particle in self.particles:
                if not particle.fixed:
                    fake_turbulance = 2
                    
                    particle.x += self.wind_strength
                    #adds a mini sin effect and looks like turbulance 
                    particle.x += self.wind_strength * random.uniform(-fake_turbulance,fake_turbulance) *2
                    
                    particle.y += self.wind_strength * random.uniform(-fake_turbulance,fake_turbulance) *2
                    particle.y -= self.wind_strength
    
    #same thing as the one in the main                
    def create_flag(self, start_x, start_y, num_x=20, num_y=25, spacing=5.0):
        # Nested function to create particles
        def create_particles(start_x, start_y, num_x, num_y, spacing):
            particles = []
            for j in range(num_y):
                for i in range(num_x):
                    x = start_x + i * spacing
                    y = start_y + j * spacing
                    p = Particle(x, y)
                    # Set the first row's first and last particles as fixed to represent flag poles
                    if j == 0 and (i == 0 or i == num_x - 1):
                        p.fixed = True
                    particles.append(p)
            return particles

        # Nested function to create constraints between particles
        def create_constraints(particles, num_x, num_y):
            constraints = []
            for j in range(num_y):
                for i in range(num_x):
                    if i < (num_x - 1):  # Horizontal constraints
                        particle1 = particles[i + j * num_x]
                        particle2 = particles[(i + 1) + j * num_x]
                        constraints.append(Constraint(particle1, particle2))

                    if j < (num_y - 1):  # Vertical constraints
                        particle1 = particles[i + j * num_x]
                        particle2 = particles[i + (j + 1) * num_x]
                        constraints.append(Constraint(particle1, particle2))
            return constraints

        # Create particles and constraints for the flag
        flag_particles = create_particles(start_x, start_y, num_x, num_y, spacing)
        flag_constraints = create_constraints(flag_particles, num_x, num_y)

        # Extend the EventHandler's particle and constraint lists
        self.particles.extend(flag_particles)
        self.constraints.extend(flag_constraints)

        
        
        
        
      
      
