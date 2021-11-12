import os
import time
import random
from snake import *  
from datetime import datetime

def championship(brain, TIME = 400, FOOD = 35):
    all_snakes = []
    field = Field('Fields/Field.txt')
    for i in range(6):
        positions = [Point(10, i+1), Point(11, i+1), Point(12, i+1)]
        all_snakes.append(Snake(field, all_snakes, brain, positions, positions[0], reproductive = False, hungry = False, autofood = True))
    field.make_food(FOOD)
    for step in range(TIME+1):
        for snake in all_snakes:
            if (snake.is_alive):
                snake.step()
    ans = 0
    for snake in all_snakes:
        ans += len(snake.positions)
    return ans / 6
    
def analise(dir_name, file, start_snake = 0, TIMES = 200):
    step = int(file[4:-5])
    path_to_file = f'Analise/{step}/data.txt'
    try:
        os.mkdir(f'Analise/{step}')
    except:
        pass    
    file = open(dir_name+'/'+file, 'r')
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
    results = []
    for i in range(start_snake, len(brains)):
        avg = 0
        comp_start = datetime.now()
        for competition in range(TIMES):
            start = datetime.now()
            curr = championship(brains[i])
            avg += curr
            tab = ' '*(len(str(TIMES))-len(str(competition+1)))
            print(f'Step{step}k. Snake {i+1}/16. Round {competition+1}/{TIMES}: ', end=tab)
            print("%.2f" % curr, end=' ')
            now = datetime.now()
            print(f' |  {"%.6f" % ((now - start).seconds + (now - start).microseconds/1000000)} sec')
        avg /= TIMES
        results.append(avg)
        now = datetime.now()
        print(f'Result: {results[-1]}  |  {((now - start).seconds + (now - comp_start).seconds)} sec')
        print("SAVING...")
        try:
            os.mkdir(f'Analise/{step}/Snake{i+1}')
        except:
            pass         
        curr_snake = open(f'Analise/{step}/Snake{i+1}/data.txt', 'w')
        curr_snake.write(str(avg))
        curr_snake.close()
        print()
    results.sort()
    file = open(path_to_file, 'w')
    file.write(str(sum(results[-4:])/4))
    file.close()
    
def draw(data):
    pass

def TakeData():
    pass

def main():
    dir_name = "Brains"
    files = os.listdir(dir_name)
    files.sort(key = lambda x: int(x[4:-5]))
    step = 0
    snake_num = 0
    if (input('Continue? Y/N\n').lower() == 'y'):
        step = int(input("Enter the number of step:\n"))
        snake_num = int(input("Enter the number of snake:\n"))
        snake_num -= 1
    if (step == 0):
        analise(dir_name, files[0])
    for ind in range(len(files)):
        i = files[ind]
        if (i[:4] == 'Step' and i[-5:] == 'k.txt' and (int(i[4:-5]) % 500 == 0) and (int(i[4:-5]) >= step)):
            if (int(i[4:-5]) >= step):
                start_snake = 0
            analise(dir_name, i, start_snake = snake_num)
main()