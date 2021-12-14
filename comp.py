from snake import *
from graph import *
from datetime import datetime
import math
import pygame
pygame.init()


field = Field('Fields/Field.txt')
step_coord = {'up': Point(-1, 0), 'right': Point(0, 1), 'down': Point(1, 0), 'left': Point(0, -1)}

food_limit = 30
n = 5
wall = []
food = []
all_snakes = []
brains_dir = "Brains"

head_h      = Point(10, 10)
positions_h = [Point(10, 10), Point(10, 11), Point(10, 12), Point(10, 13)]

head        = Point(100, 101)
positions   = [Point(100, 101), Point(100, 102), Point(100, 103), Point(100, 104)]

for i in range(2*n+1):
    wall.append([])
    food.append([])
    for j in range(2*n+1):
        wall[-1].append({'up': random.randint(-5, 5), 
                         'right': random.randint(-5, 5),
                         'down': random.randint(-5, 5),
                         'left': random.randint(-5, 5),})
        food[-1].append({'up': random.randint(-5, 5), 
                         'right': random.randint(-5, 5),
                         'down': random.randint(-5, 5),
                         'left': random.randint(-5, 5),})
brain = Brain(wall, food)
for i in range(30):
    brain = brain.mutate()
path = "Step2000k.txt"
file = open(path, 'r')
data = file.read()[:-1]
file.close()
data = data.split('\n####################################\n')
data[-1] = data[-1][:-37]
for i in data:
    brain = brain_from_text(i.split('\n------------------------------\n')[0])
snake_human = Snake(field, all_snakes, brain, positions_h, head_h, reproductive = False, hungry = False)
snake       = Snake(field, all_snakes, brain, positions,   head,   reproductive = False, hungry = False)
all_snakes = [snake_human, snake]

steps    = 200
vision   = 3
vision_h = 3
velocity = 5
direction = "left"
eaten_h = 0
eaten   = 0

#-----------------------------------------------------------------------#
graphics   = Graphics(field, [0, 0], [500, 500], 10)
#graphics_h = Graphics(field, [0, 0], [500, 100], 9)
vel = Slider("Velocity", velocity, 30, 0, [250, 350], graphics)
clock = pygame.time.Clock()
#-----------------------------------------------------------------------#

graphics.print_field_comp_sep(field, snake_human, snake, vision, 1, eaten_h, eaten, steps)
#graphics.print_field_comp("human", field, snake_human, vision_h, 0, eaten_h, steps)
#graphics.print_field_comp("ai", field, snake, vision, 1, eaten, steps)

k = 1
while (k):
    #vel.is_active()
    #vel.draw()
    #velocity = vel.getVal()
    graphics.print_field_comp_sep(field, snake_human, snake, vision, 0, eaten_h, eaten, steps)
    #graphics.print_field_comp("human", field, snake_human, vision_h, 0, eaten_h, steps)
    #graphics.print_field_comp("ai", field, snake, vision, 0, eaten, steps)
    for event in pygame.event.get():
        graphics.print_field_comp_sep(field, snake_human, snake, vision, 0, eaten_h, eaten, steps)
        vel.is_active()
        vel.draw()
        velocity = vel.getVal()
        graphics.print_field_comp_sep(field, snake_human, snake, vision, 1, eaten_h, eaten, steps)
        if (event.type == pygame.KEYDOWN):
            k = 0
velocity = vel.getVal()
pygame.time.set_timer(pygame.USEREVENT, math.ceil((30 - velocity)*1000/60))

while(steps):
    for i in pygame.event.get():
        if i.type == pygame.USEREVENT:
            #-------------------------------------------------------------#
            if graphics.exit():
            	pygame.display.quit()
            	pygame.quit()
            	break
            if (steps == 200):
                graphics.print_field_comp_sep(field, snake_human, snake, vision, 1, eaten_h, eaten, steps)
                #graphics_h.print_field_comp("human", field, snake_human, vision_h, 0, eaten_h, steps)
                #graphics.print_field_comp("ai", field, snake, vision, 0, eaten, steps)
            #-------------------------------------------------------------#	
	        
            field.make_food(food_limit - field.count_food())
            
            #------------------------------------------------#
            direction = graphics.get_unn_direction(direction)
            #------------------------------------------------#
            
            decision  = snake.make_decision()
            
            if (steps != 0):
                snake_human.step(direction)
                snake.step(decision)
                
            #---------------------------------------------------------------#
            graphics.print_field_comp_sep(field, snake_human, snake, vision, 1, eaten_h, eaten, steps)
            #graphics_h.print_field_comp("human", field, snake_human, vision, 0, eaten_h, steps)
            #graphics.print_field_comp("ai", field, snake, vision, 1, eaten, steps)
            #---------------------------------------------------------------#
            
            if (steps != 0):
                steps -= 1
            
            eaten   = len(snake.positions) - len(positions)
            eaten_h = len(snake_human.positions) - len(positions_h)

k = 1
while (k):
    graphics.print_field_comp_sep(field, snake_human, snake, vision, 1, eaten_h, eaten, steps)
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            k = 0
            
pygame.display.quit()
pygame.quit()
            
print('Game Over')
print('Human snake is alive:  ' + str(snake_human.is_alive) + '  had eaten:  ' + str(eaten_h))
print('Machine snake is alive:  ' + str(snake.is_alive) + '  had eaten:  ' + str(eaten))
print('Step: ' + str(200 - steps))
print('velocity:  ' + str(velocity))
