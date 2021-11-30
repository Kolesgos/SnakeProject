import random
from snake import Snake, Brain, Point, Field


###################################FirstTest####################################

def check_brain_wall_value(brain, wall, i, j, string):
    """ Function checks if wall on i, j in brain is correct. """
        
    if (brain.wall[i][j][string] != wall[i][j][string]):
            err = f"Error in Brain's constructor."
            err += f" Expected brain.wall[i][j][{string}] ="
            err += f"{wall[i][j][{string}]}.\n"
            err += f"But it was {brain.wall[i][j][{string}]}"
            raise ValueError(err)
            
def check_brain_food_value(brain, food, i, j, string):
    """ Function checks if food on i, j in brain is correct. """

    if (brain.food[i][j][string] != food[i][j][string]):
            err = f"Error in Brain's constructor."
            err += f" Expected brain.food[i][j][{string}] ="
            err += f"{food[i][j][{string}]}.\n"
            err += f"But it was {brain.food[i][j][{string}]}"
            raise ValueError(err)
            
def brain_generation(n):
    """ Randomly generates brain. """

    wall = []
    food = []
      
    for i in range(2 * n + 1):
        wall.append([])
        food.append([])
        for j in range(2*n + 1):
            wall[-1].append({'up': random.randint(-5, 5), 
                             'right': random.randint(-5, 5),
                             'down': random.randint(-5, 5),
                             'left': random.randint(-5, 5),})
            food[-1].append({'up': random.randint(-5, 5), 
                             'right': random.randint(-5, 5),
                             'down': random.randint(-5, 5),
                             'left': random.randint(-5, 5),})
    return Brain(wall, food), wall, food
    
def first_test():
    """ Test of brain's constructor """

    n = 5
    brain, wall, food = brain_generation(n)

    for i in range(brain.size):
        for j in range(brain.size):
            check_brain_wall_value(brain, wall, i, j, 'up')
            check_brain_wall_value(brain, wall, i, j, 'down')
            check_brain_wall_value(brain, wall, i, j, 'right')
            check_brain_wall_value(brain, wall, i, j, 'left')

    for i in range(brain.size):
        for j in range(brain.size):
            check_brain_food_value(brain, food, i, j, 'up')
            check_brain_food_value(brain, food, i, j, 'down')
            check_brain_food_value(brain, food, i, j, 'right')
            check_brain_food_value(brain, food, i, j, 'left')

    print("First test passed!!!")

#################################SecondTest####################################

def is_decision_correct(snake):
    """ Checks if snake.make_decision() works correctly. """

    if snake.make_decision() != 'up':
        raise ValueError('Incorrect snale.make_decision() func work!!!')

def second_test():

    all_snakes = []
    head = Point(10, 10)
    positions = [Point(10, 10), Point(10, 11), Point(10, 12), Point(10, 13)]

    field = Field('Fields/Field.txt')

    # step_coord = {'up': Point(-1, 0),
    #               'right': Point(0, 1),
    #               'down': Point(1, 0),
    #               'left': Point(0, -1)}

    wall = []
    food = []
    for i in range(3):
        wall.append([])
        food.append([])
        for j in range(3):
            wall[-1].append({'up':    1,
                             'right': 0,
                             'down':  0,
                             'left':  0})
            food[-1].append({'up':    1,
                             'right': 0,
                             'down':  0,
                             'left':  0})

    brain = Brain(wall, food)

    snake = Snake(field, all_snakes, brain, positions, head,
                  reproductive = False, hungry = False)

    is_decision_correct(snake)

    print("Second test passed!!!")


###################################ThirdTest####################################

def third_test():
    """ Checks if funcs count_food() and make_food() work correctly. """

    field = Field('Fields/Field.txt')

    food_limit = 30
    
    count0 = field.count_food()
    field.make_food(food_limit - count0)

    if field.count_food() != food_limit:
        raise ValueError("Wrong food counting!!!")

    print("Third test passed!!!")

###################################ThirdTest####################################

def fourth_test():
    """ Tests snake.step() func. """

    all_snakes = []
    head = Point(10, 10)
    positions = [Point(10, 10), Point(10, 11), Point(10, 12), Point(10, 13)]
    food_limit = 30

    field = Field('Fields/Field.txt')

    step_coord = {'up': Point(-1, 0),
                  'right': Point(0, 1),
                  'down': Point(1, 0),
                  'left': Point(0, -1)}

    wall = []
    food = []
    for i in range(3):
        wall.append([])
        food.append([])
        for j in range(3):
            wall[-1].append({'up':    1,
                             'right': 0,
                             'down':  0,
                             'left':  0})
            food[-1].append({'up':    1,
                             'right': 0,
                             'down':  0,
                             'left':  0})

    brain = Brain(wall, food)

    snake = Snake(field, all_snakes, brain, positions, head,
                  reproductive = False, hungry = False)

    snake.step()

    if (snake.head.x != 9 or snake.head.y != 10):
        raise ValueError("Incorrect working of snale.step() func!!!")

    print("Fourth test passed!!!")


if __name__ == "__main__":

    first_test()

    second_test()

    third_test()

    fourth_test()
