# -*- coding: utf-8 -*-

from snake import *
import time

field = Field('Fields/Void.txt', numbers = True, time = 190)
all_snakes = []
food_limit = 200
head = Point(2, 2)

n = 3
wall = []
food = []
for i in range(2*n+1):
    wall.append([])
    food.append([])
    for j in range(2*n+1):
        wall[-1].append({'up': 0, 
                         'right': 0,
                         'down': 0,
                         'left': 0})
        food[-1].append({'up': 0, 
                         'right': 0,
                         'down': 0,
                         'left': 0})
wall[n-1][n]['up']    = -20
wall[n][n-1]['left']  = -20
wall[n][n+1]['right'] = -20
wall[n+1][n]['down']  = -20
food[n][n-1]['left']  = 20
food[n][n+1]['right'] = 20
food[n+1][n]['down']  = 20
food[n-1][n]['up']    = 20

brain = Brain(wall, food)

positions = [head, Point(2, 3), Point(2, 4), Point(3, 4)]

snake = Snake(field, all_snakes, brain, positions, head, chance = 1/4, time_limit = 6, max_length = 16, min_length = 4)

all_snakes.append(snake)

for i in positions:
    field[i] = -1

dead_snakes = []
counter = 0

TIMELIMIT = 10

if (input('Continue? Y/N\n').lower() == 'y'):
    ############################
    num_of_step = int(input("Enter the number of step:\n"))
    path = f'Brains/Step{num_of_step}k.txt'
    counter = num_of_step * 1000
    ############################
    for i in all_snakes:
        i.death()
    all_snakes = []
    file = open(path, 'r')
    data = file.read()[:-1]
    file.close()
    data = data.split('\n####################################\n')
    data[-1] = data[-1][:-37]
    for i in data:
        brain = brain_from_text(i.split('\n------------------------------\n')[0])
        curr_snake = snake_from_text(i.split('\n------------------------------\n')[1], brain, field, all_snakes)
        curr_snake.time_limit = TIMELIMIT
        all_snakes.append(curr_snake)
    
field.make_food(food_limit - field.count_food())
print(field)
while (len(all_snakes) != 0):
    counter += 1
    for i in all_snakes:
        if (i.is_alive):
            i.step()
        else:
            dead_snakes.append(i)
            all_snakes.remove(i)
    if (counter % 10 == 0):
        print(counter)
        if (counter % 100 == 0):
            print(f'-------------------\n{counter/1000}k: {len(all_snakes)}\n-------------------\n', end='')
            if (counter % 1000 == 0):
                print(f'-------------------\nSAVING...\nStep{counter//1000}k.txt\n-------------------\n')
                file = open(f'Brains/Step{counter//1000}k.txt', 'w')
                output = ''
                for i in all_snakes:
                    output += str(i.brain) + '\n------------------------------\n' + str(i) + '\n####################################\n'
                file.write(output)
                file.close()      
    '''time.sleep(0.01)
    print(field)
    print(field)
    key = input()
    while (key != ''):
        try:
            if (key[0] == '\\'):
                exec(key[1:])
            else:
                exec(f'print({key})')
        except:
            print('Error')
        key = input()'''
    field.tick()
print("ALL DEAD")
