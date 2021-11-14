# -*- coding: utf-8 -*-

from datetime import datetime
from snake import *
import time

field = Field('Fields/Void.txt', numbers = True)
brains_dir = "Brains2"
all_snakes = []
food_limit = 80
TIMELIMIT  = 8
head = Point(2, 2)

print(f"\nData is saving to {brains_dir}/...\n")

n = 3
wall = []
food = []
for i in range(2*n+1):
    wall.append([])
    food.append([])
    for j in range(2*n+1):
        wall[-1].append({'up': random.randint(-5, 5), 
                         'right': random.randint(-5, 5),
                         'down': random.randint(-5, 5),
                         'left': random.randint(-5, 5)})
        food[-1].append({'up': random.randint(-5, 5), 
                         'right': random.randint(-5, 5),
                         'down': random.randint(-5, 5),
                         'left': random.randint(-5, 5)})
wall[n-1][n]['up']    = -20
wall[n][n-1]['left']  = -20
wall[n][n+1]['right'] = -20
wall[n+1][n]['down']  = -20
food[n][n-1]['left']  = 20
food[n][n+1]['right'] = 20
food[n+1][n]['down']  = 20
food[n-1][n]['up']    = 20

wall[n][n]['up']    = 0
wall[n][n]['left']  = 0
wall[n][n]['right'] = 0
wall[n][n]['down']  = 0
food[n][n]['left']  = 0
food[n][n]['right'] = 0
food[n][n]['down']  = 0
food[n][n]['up']    = 0

brain = Brain(wall, food)

positions = [head, Point(2, 3), Point(2, 4), Point(3, 4)]

snake = Snake(field, all_snakes, brain, positions, head, chance = 1/4, time_limit = TIMELIMIT, max_length = 16, min_length = 4, autofood = True)

all_snakes.append(snake)

for i in positions:
    field[i] = -1

dead_snakes = []
counter = 0

if (input('Continue? Y/N\n').lower() == 'y'):
    ############################
    num_of_step = int(input("Enter the number of step:\n"))
    path = f'{brains_dir}/Step{num_of_step}k.txt'
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
        curr_snake.autofood = True
        all_snakes.append(curr_snake)
else:
    if (input('Resave 0 file? Y/N\n').lower() == 'y'):
        print(f'-------------------\nSAVING...\nStep{counter//1000}k.txt\n-------------------\n')
        file = open(f'{brains_dir}/Step{counter//1000}k.txt', 'w')
        output = ''
        for i in all_snakes:
            output += str(i.brain) + '\n------------------------------\n' + str(i) + '\n####################################\n'
        file.write(output)
        file.close()    
     
field.make_food(food_limit)
curr_time = datetime.now()
saving_time = datetime.now()
while (len(all_snakes) != 0):
    dead_snakes = []
    counter += 1
    for i in all_snakes:
        if (i.is_alive):
            i.step()
        else:
            dead_snakes.append(i)
            all_snakes.remove(i)
    
    if (counter % 100 == 0):
        now = datetime.now()
        avg = 0
        for snake in all_snakes:
            avg += len(snake.positions)
        avg /= len(all_snakes)
        print(f'{counter/1000}k  |   all: {len(all_snakes)}{" "*(2-len(str(len(all_snakes))))}, avg: {"%.2f" % avg}{" "*(2-len(str(int(avg))))}   |  {"%.2f" % ((now - curr_time).seconds + (now - curr_time).microseconds/1000000)} sec')
        curr_time = datetime.now()
        if (counter % 50000 == 0):
            now = datetime.now()
            print(f'-------------------\nSAVING Step{counter//1000}k.txt  |  {"%.2f" % ((now - saving_time).seconds/60)} min\n-------------------')
            saving_time = datetime.now()
            file = open(f'{brains_dir}/Step{counter//1000}k.txt', 'w')
            output = ''
            for i in all_snakes:
                output += str(i.brain) + '\n------------------------------\n' + str(i) + '\n####################################\n'
            file.write(output)
            file.close()    
    
    '''if (counter % 10 == 0):
        print(counter)
        if (counter % 100 == 0):
            print(f'-------------------\n{counter/1000}k: {len(all_snakes)}\n-------------------\n', end='')
            if (counter % 1000 == 0):
                print(f'-------------------\nSAVING...\nStep{counter//1000}k.txt\n-------------------\n')
                file = open(f'{brains_dir}/Step{counter//1000}k.txt', 'w')
                output = ''
                for i in all_snakes:
                    output += str(i.brain) + '\n------------------------------\n' + str(i) + '\n####################################\n'
                file.write(output)
                file.close()  '''
    """time.sleep(0.01)
    print(field)"""
    '''key = input()
    while (key != ''):
        try:
            if (key[0] == '\\'):
                exec(key[1:])
            else:
                exec(f'print({key})')
        except:
            print('Error')
        key = input()'''
    #field.tick()
    
print("ALL DEAD")
print(*dead_snakes, sep = '\n\n')