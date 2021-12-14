# -*- coding: utf-8 -*-
from snake import *
from graph import *
import pygame
pygame.init()

all_snakes = []
field = Field('Fields/Field.txt')
step_coord = {'up': Point(-1, 0), 'right': Point(0, 1), 'down': Point(1, 0), 'left': Point(0, -1)}

def get_direction(s):
    if (s == 'w'):
        return 'up'
    if (s == 'a'):
        return 'left'
    if (s == 's'):
        return 'down'
    if (s == 'd'):
        return 'right'
    return '\\' + s

food_limit = 30
n = 5
wall = []
food = []
head = Point(10, 10)
positions = [Point(10, 10), Point(10, 11), Point(10, 12), Point(10, 13)]
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
snake = Snake(field, all_snakes, brain, positions, head, reproductive = False, hungry = False)

#-------------------------#
graphics = Graphics(field, [0, 0], [500, 100], 18)
direction  = ''
decision   = ''
#-------------------------#

while (snake.is_alive):
	
	#-----------------------------------------------------------------------------#
    if graphics.exit():
    	pygame.display.quit()
    	pygame.quit()
    	break
    graphics.print_field_school(field, direction, decision)
    #-----------------------------------------------------------------------------#	
	
    field.make_food(food_limit - field.count_food())
    decision = snake.make_decision()
    #print(field.get_str_slice(snake.head - Point(snake.vision, snake.vision), snake.head + Point(snake.vision + 1, snake.vision + 1), frame = True))
    #print(decision)
    #direction = get_direction(input())
    
    #----------------------------------#
    direction = graphics.get_direction()
    #----------------------------------#
    
    if (direction == '\\close'):
        break    
    if (direction[0] == '\\'):
        file = open(direction[1:] + '.txt', 'w')
        file.write(str(snake.brain))
        file.close()
        continue
    if (decision == direction):
        snake.step()
        
        #------------------------------------------------------#
        graphics.print_field_school(field, direction, decision)
        #------------------------------------------------------#
        
        continue
        
    print("Correcting...")
    wall_correcting = []
    food_correcting = []
    for i in range(max(0, snake.head.x - snake.vision), min(field.x, snake.head.x + snake.vision + 1)):
        for j in range(max(0, snake.head.y - snake.vision), min(field.y, snake.head.y + snake.vision + 1)):
            if (field[i][j] == -1):
                wall_correcting.append(f'({i}, {j})')
                snake.brain.wall[snake.vision + i - snake.head.x][snake.vision + j - snake.head.y][decision] -= 1
                snake.brain.wall[snake.vision + i - snake.head.x][snake.vision + j - snake.head.y][direction] += 1
            if (field[i][j] == 1):
                food_correcting.append(f'({i}, {j})')
                snake.brain.food[snake.vision + i - snake.head.x][snake.vision + j - snake.head.y][decision] -= 1
                snake.brain.food[snake.vision + i - snake.head.x][snake.vision + j - snake.head.y][direction] += 1
    print('Wall: ', end='')
    print(*wall_correcting, sep = ' ')
    print('Food: ', end='')
    print(*food_correcting, sep = ' ')   
    snake.step(direction)
    
    #------------------------------------------------------#
    graphics.print_field_school(field, direction, decision)
    #------------------------------------------------------#
print('Game Over')
