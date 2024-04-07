#main file Run this to see flag

import pygame
import math
from Verlet_particles import Particle  
from Verlet_Constraints import Constraint 
from UI import main_menu 
from UI import Button
from UI import draw_text
from Event_handler import EventHandler 
#import librosa



#filename = 'Aces.mp3'
#rms_energy = librosa.feature.rms(y=y)




pygame.init()

FPS = 200# frames per second setting
fpsClock = pygame.time.Clock()
WIDTH = 1200
HEIGHT = 680
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Verlet System')
BLACK = (255, 255, 255)   
delta_t = 0.1
NUM_ITER = 2  #number of times we calculate distance for each dt
# main meny
if not main_menu(screen, fpsClock, FPS, WIDTH, HEIGHT):
    raise SystemExit  

#Create the particles for the grid for flag
NUM_X = 45
NUM_Y = 30
start_x = 100
start_y=200
spacing=5

def create_particles(num_x, num_y, start_x, start_y, spacing):
    particles = []
    for j in range(num_y):
        for i in range(num_x):
            x = start_x + i * spacing
            y = start_y + j * spacing
            p = Particle(x, y)
            # anchors
            #and (i == 0 or i == num_x - 1 )
            if j == 0 :
                p.fixed = True
            particles.append(p)
    return particles

#create the verlet springs to connect the particles
def create_constraints(particles, num_x, num_y):
    constraints = []
    for j in range(num_y):
        for i in range(num_x):
            
            if i < (num_x - 1):
                #Horizantal
                particle1 = particles[i + j * num_x]
                particle2 = particles[(i + 1) + j * num_x]
                c = Constraint(particle1, particle2)
                constraints.append(c)

            if j < (num_y - 1):
                # Vertical
                particle1 = particles[i + j * num_x]
                particle2 = particles[i + (j + 1) * num_x]
                c = Constraint(particle1, particle2)
                constraints.append(c)

            #diagonals
            #if i < (num_x - 1) and j < (num_y - 1):
                # Diagonal constraint (bottom-right)
             #   particle1 = particles[i + j * num_x]
             #   particle2 = particles[(i + 1) + (j + 1) * num_x]
               # c = Constraint(particle1, particle2)
             #   constraints.append(c)

            #if i > 0 and j < (num_y - 1):
                # Diagonal constraint (bottom-left)
                #particle1 = particles[i + j * num_x]
               # particle2 = particles[(i - 1) + (j + 1) * num_x]
                #c = Constraint(particle1, particle2)
                #constraints.append(c)

    return constraints



particles = create_particles(NUM_X, NUM_Y, start_x, start_y, spacing)
constraints = create_constraints(particles, NUM_X, NUM_Y)
  
event_handler = EventHandler(particles, constraints)

Running = True
while Running:
    screen.fill(BLACK)

    # Handle events with the event handlerw
    Running = event_handler.handle_events() 
    if event_handler.wind_active:
        event_handler.apply_wind()  





   #Update
    for particle in particles:
        if not particle.selected or event_handler.wind_active:
            particle.update(delta_t)
    # we update contraints for the minimum of 2 times because they need to fix particles movement before and after the update
    for i in range(NUM_ITER):
        for constraint in constraints:
            constraint.update()

    #Draw 
    for particle in particles:
        particle.draw(screen)  
    for constraint in constraints:
        constraint.draw(screen)  

    
    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
