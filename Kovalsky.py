import os
import time
import random
from draw import *
from snake import *  
from datetime import datetime
import matplotlib.pyplot as plt

def championship(brain, TIME = 400, FOOD = 70):
    all_snakes = []
    field = Field('Fields/Field.txt')
    for i in range(6):
        positions = [Point(10, i+1), Point(11, i+1), Point(12, i+1)]
        all_snakes.append(Snake(field, all_snakes, brain, positions, positions[0], reproductive = False, hungry = False, autofood = True, delete_body = False))
    field.make_food(FOOD)
    for step in range(TIME+1):
        for snake in all_snakes:
            if (snake.is_alive):
                snake.step()
    ans = 0
    for snake in all_snakes:
        ans += len(snake.positions)
    return ans / 6
    
def analise(file, start_snake = 0, TIMES = 200, brains_dir = "Brains", save_dir = "Analise"):
    start_snake = max(start_snake, 0)
    step = int(file[4:-5])
    path_to_file = f'{save_dir}/{step}/data.txt'
    try:
        os.mkdir(f'{save_dir}/{step}')
    except:
        pass    
    file = open(brains_dir+'/'+file, 'r')
    data = file.read()[:-1]
    file.close()
    data = data.split('\n####################################\n')
    data[-1] = data[-1][:-37]
    all_brains = []
    for snake_data in data:
        brain = brain_from_text(snake_data.split('\n------------------------------\n')[0])
        all_brains.append(copy.deepcopy(brain))
    random.shuffle(all_brains)
    brains = all_brains[0:min(16, len(all_brains))]
    for i in range(start_snake, len(brains)):
        avg = 0
        comp_start = datetime.now()
        for competition in range(TIMES):
            start = datetime.now()
            curr = championship(brains[i])
            avg += curr
            tab = ' '*(len(str(TIMES))-len(str(competition+1)))
            print(f'Ep.{num_of_experiment}. Step{step}k. Snake {i+1}/{len(brains)}. Round {competition+1}/{TIMES}: ', end=tab)
            print("%.2f" % curr, end=' '*(5-len("%.2f" % curr)))
            now = datetime.now()
            print(f' |  {"%.2f" % ((now - start).seconds + (now - start).microseconds/1000000)} sec')
        avg /= TIMES
        now = datetime.now()
        print(f'Result: {avg}  |  {"%.2f" % ((now - comp_start).seconds/60)} min')
        print("SAVING...")
        try:
            os.mkdir(f'{save_dir}/{step}/Snake{i+1}')
        except:
            pass         
        curr_snake = open(f'{save_dir}/{step}/Snake{i+1}/data.txt', 'w')
        curr_snake.write(str(avg))
        curr_snake.close()
        print()

if __name__ == '__main__':
    brains_dir = "Brains"
    save_dir   = "Analise"
    
    num_of_experiment = input("Enter number of experiment: ")
    brains_dir += num_of_experiment
    save_dir += num_of_experiment
    
    files = os.listdir(brains_dir)
    files.sort(key = lambda x: int(x[4:-5]))
    step = 0
    if (input('Continue? Y/N\n').lower() == 'y'):
        step = int(input("Enter the number of step:\n"))
        snake_num = int(input("Enter the number of snake:\n"))
        snake_num -= 1
    else:
        snake_num = 0
        
    shift = int(input("Enter the shift:\n")) 
    module = int(input("Enter the module:\n"))
        
    for ind in range(len(files)):
        i = files[ind]
        if (i[:4] == 'Step' and i[-5:] == 'k.txt' and ((int(i[4:-5]) + shift) % module == 0) and (int(i[4:-5]) >= step)):
            if (int(i[4:-5]) > step):
                snake_num = 0
            analise(i, start_snake = snake_num, brains_dir = brains_dir, save_dir = save_dir)
    drawStep(dirr_name = save_dir)