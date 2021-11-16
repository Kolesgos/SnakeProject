# -*- coding: utf-8 -*-
import copy
import random

class Field():

    """ Playing field for snakes """

    def __init__(self, path_to_file, numbers = False, time = 20):
        """Creates the field from file <path_to_file>
        
        Keyword arguments:
        self            -- class instance
        path_to_file    -- path to the field file
        numbers         -- is it needed to print indexes of strings and colums
        time            -- integer number that shows after what number of moves
                           food appears on the cell

        """
        self.data = []
        self.time = time
        file = open(path_to_file, 'r')
        data = file.read()
        file.close()
        self.data = []
        for i in data.split('\n'):
            self.data.append([])
            for j in i:
                if (j == '#'):
                    self.data[-1].append(-1)
                elif (j == ' '):
                    self.data[-1].append(0)
                elif (j == 'O'):
                    self.data[-1].append(1)
                else:
                    self.data[-1].append(j)
        self.x = len(self.data)
        self.y = len(self.data[0])
        self.Timer = [[random.randint(1, time-1)
                       for j in range(self.y)] for i in range(self.x)]
        self.numbers = numbers
        
    def tick(self):
        """Playing field moves one time.

        If the timer of cell expires and this cell is not filled the food appears
        in it. Every move increases the timer of not filled cells only.

        """
        for i in range(self.x):
            for j in range(self.y):
                if (self.data[i][j] == 0):
                    self.Timer[i][j] = (self.Timer[i][j] + 1) % self.time
                    if (self.Timer[i][j] == 0):
                        self.data[i][j] = 1
              
    def get_str_slice(self, top_left, bot_right, frame = False):
        """Returns the visible for snake part of field

        Keyword arguments:
        top_left        -- top left coord of visible part
        bot_right       -- bottom left coord of visible part
        frame           -- boolian value which is needed to be true if you want
                           '_' to be displayed above and below

        """
        ans = ''
        if (frame):
            ans += '_'*(bot_right.x - top_left.x) + '\n'
        for i in range(top_left.x, bot_right.x):
            if (frame):
                ans += '|'
            for j in range(top_left.y, bot_right.y):
                if (self[Point(i, j)] == -1):
                    ans += '#'
                if (self[Point(i, j)] == 0):
                    ans += ' '  
                if (self[Point(i, j)] == 1):
                    ans += 'O'  
            if (frame):
                ans += '|'            
            ans += '\n'
        if (frame):
            ans += '_'*(bot_right.x - top_left.x)        
        return ans[:-1]
                    
    def make_food(self, n):
        """Tries to create <n> number of food on field

        Keyword arguments:
        n       -- number of food to create

        Returns number of food we could not create

        """
        empty = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if (self.data[i][j] == 0):
                    empty.append(Point(i, j))
        random.shuffle(empty)
        for i in range(min(n, len(empty))):
            self[empty[i]] = 1
        return max(0, n - len(empty))
    
    def count_food(self):
        """ Returns number of food on field. """
        ans = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if (self.data[i][j] == 1):
                    ans += 1
        return ans
                
    def __repr__(self):
        ans = ''
        if (self.numbers):
            ans += ' '
            for i in range(len(self.data[0])):
                ans += str(i%10)
            ans += '\n'
        for i in range(len(self.data)):
            if (self.numbers):
                ans += f'{i%10}'
            for j in self.data[i]:
                if (j == -1):
                    ans += '#'
                elif (j == 0):
                    ans += ' '
                elif (j == 1):
                    ans += 'O'
                else:
                    ans += j
            ans += '\n'
        return ans
    
    def __getitem__(self, item_):
        """Returns the data that corresponds to key==<item_>

        The field closed to itself vertically and horizontally.

        Keyward argument:
        item_       -- value could be instance of Point class or the number. If it
                       is a number it works a lot slowly.

        """
        item = copy.deepcopy(item_)
        if (isinstance(item, Point)):
            if (item.x < 0):
                item.x -= (item.x // len(self.data))*len(self.data)
            if (item.x >= len(self.data)):
                item.x %= len(self.data)
            if (item.y < 0):
                item.y -= (item.y // len(self.data[0]))*len(self.data[0])
            if (item.y >= len(self.data[0])):
                item.y %= len(self.data[0])            
            return self.data[item.x][item.y]
        if (item < 0):
            item -= (item // len(self.data))*len(self.data)
        if (item >= len(self.data)):
            item %= len(self.data)
        return self.data[item]
    
    def __setitem__(self, key, value):
        """Sets the data corresponded to key==<key> value.

        The field closed to itself vertically and horizontally.

        Keyward argument:
        key         -- could be instance of Point class or integer number. It is
                       the key to correspond the data
        value       -- Value to be written in the data[key]

        """
        if (isinstance(key, Point)):
            if (key.x < 0):
                key.x -= (key.x // len(self.data))*len(self.data)
            if (key.x >= len(self.data)):
                key.x %= len(self.data)
            if (key.y < 0):
                key.y -= (key.y // len(self.data[0]))*len(self.data[0])
            if (key.y >= len(self.data[0])):
                key.y %= len(self.data[0])               
            self.data[key.x][key.y] = value
            return
        if (key < 0):
            key -= (key // len(self.data))*len(self.data)
        if (key >= len(self.data)):
            key %= len(self.data)        
        self.data[key] = copy.deepcopy(value)

class Brain():

    """ Snake brain. Linear classifier. """

    def __init__(self, wall, food):
        """Creates snake's brain from two lists.

        Keyward arguments:
        wall        -- the list which is filled with masses of desision depended
                       on previous one. Depends on how often snake ate walls.
        food        -- the list which is filled with masses of desisin depended
                       on previous one. Depends on how often snake ate food.

        """
        if (not (len(wall) == len(wall[0]) == len(food) == len(food[0]))):
            raise ValueError("")
        self.direction = ['up', 'right', 'down', 'left']
        self.wall = copy.deepcopy(wall)
        self.food = copy.deepcopy(food)
        self.size = len(wall)
        
    def mutate(self, value = 5, position_of_mutation = 'random'):
        """Returns mutated brain of snake.

        Element with psition <position_of_mutation> changes to a random number in
        in range of [-<value>, <value>].
        If <position_of_mutation> is not set, it selects randomly.

        Keyward arguments:
        value                   -- range of mutation magnitude
        position_of_mutation    -- the name says all you need to know...

        """
        if (value <= 0 or int(value) != value):
            raise ValueError("")

        if (position_of_mutation == 'random'):
            position_of_mutation = [random.randint(0, self.size - 1),
                                    random.randint(0, self.size - 1)]

        new_brain = Brain(self.wall, self.food)
        if position_of_mutation == [(self.size-1)//2, (self.size-1)//2]:
            return new_brain

        new_brain.wall[position_of_mutation[0]]                 \
                      [position_of_mutation[1]]                 \
                      [self.direction[random.randint(0,3)]]     \
                      += random.randint(-value, value)

        new_brain.food[position_of_mutation[0]]                 \
                      [position_of_mutation[1]]                 \
                      [self.direction[random.randint(0,3)]]     \
                      += random.randint(-value, value)

        return new_brain
    
    def __repr__(self):
        ans = 'Wall (up, right, down, left):\n'
        for i in range(self.size):
            for j in range(self.size):
                ans += f"""[{self.wall[i][j]['up']},
                            {self.wall[i][j]['right']},
                            {self.wall[i][j]['down']},
                            {self.wall[i][j]['left']}] """
            ans = ans[:-1]
            ans += '\n'
        ans += 'Food (up, right, down, left):\n'
        for i in range(self.size):
            for j in range(self.size):
                ans += f"""[{self.food[i][j]['up']},
                            {self.food[i][j]['right']},
                            {self.food[i][j]['down']},
                            {self.food[i][j]['left']}] """
            ans = ans[:-1]
            ans += '\n'

        return ans[:-1]

def brain_from_text(data):
    """Returns brain that was converted from text file

    Keyward argument:
    data        -- text representation of brain

    """
    data = data.split('\n')
    wall = []
    food = []
    n = len(data[1].split('] ['))
    for i in range(1, n+1):
        wall.append([])
        for j in data[i][1:-1].split('] ['):
            curr = j.split(', ')
            curr = list(map(int, curr))            
            wall[-1].append({'up': curr[0], 'right': curr[1],
                             'down': curr[2], 'left': curr[3]})
    for i in range(n+2, 2*n+2):
        food.append([])
        for j in data[i][1:-1].split('] ['):
            curr = j.split(', ')
            curr = list(map(int, curr))  
            food[-1].append({'up': curr[0], 'right': curr[1],
                             'down': curr[2], 'left': curr[3]})
    ans = Brain(wall, food)
    return ans

def snake_from_text(data, brain, field, all_snakes):
    """Returns snake that was converted from text file.

    Keyeard arguments:
    data        -- text representation of snake
    brain       -- brain of snake to be created
    field       -- nothing to say there...
    all_snakes  -- list of all snakes

    """
    data = data.split('\n')
    head = Point(int(data[1][7:-1].split()[0]), int(data[1][7:-1].split()[1]))
    positions = []
    for i in data[2][7:-2].split(') ('):
        positions.append(Point(int(i.split()[0]), int(i.split()[1])))
    snake = Snake(field, all_snakes, brain, positions, head)
    snake.min_length = int(data[3].split()[2])
    snake.hungry = False
    snake.reproductive = False
    for i in data[5:-1]:
        if (i[:6] == 'Hungry'):
            snake.hungry = True
            snake.time_limit = int(i.split()[2].split('/')[1])
            snake.suplies = int(i.split()[2].split('/')[0])
        if (i[:12] == 'Reproductive'):
            snake.reproductive = True
            snake.max_length = int(i.split()[1][:-1])
            snake.chance = float(i.split()[3])
    snake.generation = int(data[-1].split()[1])
    return snake

class Point():

    """ Point with set coords. """

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __getitem__(self, item):
        if (item == 0):
            return self.x
        return self.y
    
    def __add__(self, other):
        """

        Returns point on which will indicate radius vector of point <other>,
        applied to the point <self>.

        """
        return Point(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        """

        Returns point on which wikk indicate radius vector of point <self>,
        multiplied on value <other>

        """
        return Point(self.x * other, self.y * other)
    
    def __sub__(self, other):
        return self + (other * -1)
    
    def __div__(self, other):
        return self * (1 / other)

class Snake():

    """ Snake. The main game unit. """

    def __init__(self, field, all_snakes, brain, positions, head,               \
                 reproductive = True, max_length = 16, min_length = 3,          \
                 mutating = True, chance = 1/4, hungry = True, time_limit = 20):
        """
        Creates Snake. Sorry for gachimuchi.

        Keyword arguments:
        field           -- instance of class Field, playing field.
        all_snakes      -- list of all snakes.
        brain           -- instance of class Brain. Snake's brain.
        position        -- list of instances of class Point, coords of snake's
                           body. It sorted in natural order (from head to tail).
        head            -- coords of snake's head.
        reproductive    -- shows ability of snake to have $sex$ (children).
        max_length      -- integer number. Length of the snake, when snake starts
                           to have $sex$
        min_length      -- integer number. Length of snake when snakes stops to
                           decrease.
        mutation        -- shows if brain changes when $sex$ is $cumming$
        chance          -- chance of mutation.
        hungry          -- shows if snake is hungry.
        time_limit      -- integer number, whuch shows how much moves snakes can
                           live without hunger and injure.

        """
        self.field = field
        self.all_snakes = all_snakes
        self.direction = ['up', 'right', 'down', 'left']
        self.brain = copy.deepcopy(brain)
        self.positions = copy.deepcopy(positions)
        self.length = len(positions)
        self.head = copy.deepcopy(head)
        self.vision = (self.brain.size - 1)//2
        self.is_alive = True
        self.reazon_of_death = 'None'
        self.reproductive = reproductive
        self.max_length = max_length
        self.min_length = min_length
        self.mutating = mutating
        self.chance = chance
        self.hungry = hungry
        self.time_limit = time_limit
        self.suplies = time_limit
        for i in self.positions:
            self.field[i] = -1
        self.generation = 1
    
    def make_decision(self):
        """

        Returns moving direction (up, right, down, left),
        in which snake is moving.

        """

        arr = [0, 0, 0, 0]
        for i in range(self.vision * 2 + 1):
            for j in range(self.vision * 2 + 1):
                point_on_field = self.head + Point(i, j) - Point(self.vision, self.vision)
                if (self.field[point_on_field] == -1):
                    arr[0] += self.brain.wall[i][j]['up']
                    arr[1] += self.brain.wall[i][j]['right']
                    arr[2] += self.brain.wall[i][j]['down']
                    arr[3] += self.brain.wall[i][j]['left']
                if (self.field[point_on_field] == 1):
                    arr[0] += self.brain.food[i][j]['up']
                    arr[1] += self.brain.food[i][j]['right']
                    arr[2] += self.brain.food[i][j]['down']
                    arr[3] += self.brain.food[i][j]['left']
        max_value = max(arr)
        if (arr.count(max_value) == 1):
            return self.direction[arr.index(max_value)]
        max_index = []
        for i in range(4):
            if (arr[i] == max_value):
                max_index.append(i)
        return self.direction[max_index[random.randint(0, len(max_index)-1)]]
    
    def step(self, direction_ = 'default'):
        """ Snake moves one time. """

        if not(self.is_alive):
            return
        step_coord = {'up': Point(-1, 0), 'right': Point(0, 1), 'down': Point(1, 0), 'left': Point(0, -1)}
        decision = self.make_decision()
        if (direction_ != 'default'):
            decision = direction_
        if (self.field[self.head + step_coord[decision]] == -1):
            self.death('Wall')
            return
        if (self.field[self.head + step_coord[decision]] == 0):
            self.field[self.positions[-1]] = 0      
            self.positions = [self.head + step_coord[decision]] + self.positions[:-1]
            self.head += step_coord[decision]
            self.field[self.head] = -1
        else:
            if (self.field[self.head + step_coord[decision]] == 1):
                self.head += step_coord[decision]
                self.positions = [self.head] + self.positions
                self.field[self.head] = -1    
                self.suplies = self.time_limit + 1
                if (self.reproductive and (len(self.positions) >= self.max_length)):
                    self.all_snakes.append(self.divide())
        if (self.hungry):
            self.suplies -= 1
            if (self.suplies == 0):
                self.suplies = self.time_limit
                self.field[self.positions[-1]] = 0
                self.positions = self.positions[:-1]
                if (len(self.positions) <= self.min_length):
                    self.death('Hunger')
    
    def divide(self):
        """ Snakes has $sex$. Head of new one - tail of the parent. """

        child = copy.deepcopy(self)
        if (self.mutating and (random.random() <= self.chance)):
            child.brain = self.brain.mutate()
        else:
            child.brain = self.brain
        child.field = self.field
        child.all_snakes = self.all_snakes
        child.positions = self.positions[len(self.positions)//2:][::-1]
        child.head = self.positions[-1]
        self.positions = self.positions[0:len(self.positions)//2]
        child.generation += 1
        return child
        
    def death(self, reason = 'Unnown'):
        """ The death of the snake! """

        self.is_alive = False
        self.reason_of_death = reason
        for i in self.positions:
            self.field[i] = 0
        
    def __repr__(self):
        if (self.is_alive):
            ans = 'ALIVE\n'
        else:
            ans = f"DEAD: {self.reason_of_death}\n"
        ans += f'Head: ({self.head.x} {self.head.y})\nBody: '
        for i in self.positions:
            ans += f"({i.x} {i.y}) "
        ans += f'\nLength: {len(self.positions)}, {self.min_length}'
        ans += f'\nVision: {self.vision}\n'
        if (self.hungry):
            ans += f'Hungry, suplies: {self.suplies}/{self.time_limit}\n'
        if (self.reproductive):
            ans += f'Reproductive: {self.max_length}, '
            if (self.mutating):
                ans += f'mutating: {self.chance}'      
            else:
                ans += f'mutating: 0'
        ans += f'\nGeneration: {self.generation}'
        return ans
