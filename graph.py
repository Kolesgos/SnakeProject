from snake import *
import pygame
pygame.init()

AQUA_MARINE     = (127, 255, 212) # food color
SLATE_BLUE      = (106, 90, 205)  # head color (human)
DARK_SLATE_BLUE = (72, 61, 139)   # field color
MEDIUM_PURPLE   = (147, 112, 219) # snake color (human)
ORCHID          = (218, 112, 214) # snake color (AI)
VIOLET          = (238, 130, 238) # head color (AI)

class Graphics():


    def __init__(self, field, pos, size, p):
    
        """ Creates window and parametres of blocks """
        
        self.HEIGHT = p * (len(field.data[0]))
        self.WEIGHT = p * (len(field.data))

        self.BLOCK_H = self.HEIGHT/len(field.data[0])
        self.BLOCK_W = self.WEIGHT/len(field.data)
        self.pos     = pos
        self.size    = size
        self.param   = p
        
        self.surf     = pygame.Surface((self.HEIGHT, self.WEIGHT))
        self.surf_all = pygame.Surface((self.HEIGHT, self.WEIGHT))
        
        self.sc = pygame.display.set_mode((self.HEIGHT + size[0], self.WEIGHT + size[1]));      
        pygame.display.update()
    
    def getSc(self):
        return self.sc
    
    def exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
    
    
    def print_text(self, text, pos):
        
        """ Prints text on given position """
        
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(text, False, (255, 255, 0))
        self.sc.blit(textsurface,(pos))


    def print_field_school(self, field, direct, dec):
    
        """ Draws field, snake, food and inf on school """
        
        for j in range(len(field.data)):
            for i in range(len(field.data[j])):
                point = Point(j, i) 
                if field[point] == -1:
                    pygame.draw.rect(self.sc, (255, 0, 0), (i * self.BLOCK_H, j * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif field[point] == 1:
                    pygame.draw.rect(self.sc, (0, 255, 0), (i * self.BLOCK_H, j * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
        self.print_text('Direction:   ' + direct, (self.HEIGHT/2 + 600, self.WEIGHT/6))
        self.print_text('Decision:    ' + dec, (self.HEIGHT/2 + 600, self.WEIGHT/6 * 2))
        pygame.display.flip()
        pygame.display.update()
        self.sc.fill((0, 0, 0))
        

    def print_field_polygon(self, all_snakes, field, food_limit, time_limit):
    
        """ Draws field, snakes, food and inf on polygon. Draws snakes separatly """
        
        for j in range(len(field.data) + 1):
            for i in range(len(field.data[0]) + 1):
                point = Point(j, i) 
                if field[point] == -1:
                    pygame.draw.rect(self.sc, (20, 0, 255), (i * self.BLOCK_H, j * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif field[point] == 1:
                    pygame.draw.rect(self.sc, (0, 255, 0), (i * self.BLOCK_H, j * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
        for snake in all_snakes:
            for i in range(len(snake.positions)):
                if(i == 0):
                    pygame.draw.rect(self.sc, (255, 0, 0), (snake.positions[i].x * self.BLOCK_H, snake.positions[i].y * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                else:
                    pygame.draw.rect(self.sc, (255, 255, 0), (snake.positions[i].y * self.BLOCK_H, snake.positions[i].x * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)


        self.print_text('Food limit:   ' + str(food_limit), (600, 200))
        self.print_text('Time limit:   ' + str(time_limit), (600, 400))
        pygame.display.flip()
        pygame.display.update()
        self.sc.fill((0, 0, 0))
        
    
    def print_field_comp(self, performer, field, snake, fill):
        
        """ Draws snake and field with fog of war """
        
        if (performer == "ai"):
            color = [VIOLET, ORCHID]
            pos = [(800, 400), (600, 600)]
        else:
            color = [SLATE_BLUE, MEDIUM_PURPLE]
            pos = [(600, 200), (600, 300)]
        for j in range(len(field.data)):
            for i in range(len(field.data[j])):
                point = Point(j, i)
                """if (point.x == 0) or (point.x == len(field.data) - 1) or (point.y == 0) or (point.y == len(field.data[0]) - 1):
                    pygame.draw.rect(self.sc, (255, 0, 0), ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                if (field[point] == -1) and (abs(snake.positions[0].x - point.x) <= vision) and (abs(snake.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.sc, color[1], ((i + self.pos[0])* self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif (field[point] == 1) and (abs(snake.positions[0].x - point.x) <= vision) and (abs(snake.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.sc, AQUA_MARINE, ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)"""
                if (point.x == 0) or (point.x == len(field.data) - 1) or (point.y == 0) or (point.y == len(field.data[0]) - 1):
                    pygame.draw.rect(self.surf_all, (255, 0, 0), ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                if (field[point] == -1):
                    pygame.draw.rect(self.surf_all, color[1], ((i + self.pos[0])* self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif (field[point] == 1):
                    pygame.draw.rect(self.surf_all, AQUA_MARINE, ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
        if(fill):
            self.sc.blit(self.surf_all, (0, 250))
            self.sc.fill((0, 0, 0))
            
    def print_field_comp_sep(self, field, snake_h, snake, vision, fill, eaten_h, eaten, step):
        
        """ Draws snake and field with fog of war """
        
        color_ai = [VIOLET, ORCHID]
        pos_ai = [(600, 600), (600, 350)]
        color_h = [SLATE_BLUE, MEDIUM_PURPLE]
        pos_h = [(600, 100), (600, 300)]
        
        for j in range(len(field.data)):
            for i in range(len(field.data[j])):
                point = Point(j, i)
                #if (point.x == 0) or (point.x == len(field.data) - 1) or (point.y == 0) or (point.y == len(field.data[0]) - 1):
                #    pygame.draw.rect(self.sc, (255, 0, 0), ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                if (field[point] == -1) and (abs(snake_h.positions[0].x - point.x) <= vision) and (abs(snake_h.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.sc, color_h[1], ((i + self.pos[0])* self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif (field[point] == 1) and (abs(snake_h.positions[0].x - point.x) <= vision) and (abs(snake_h.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.sc, AQUA_MARINE, ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
        
                    
        for j in range(len(field.data)):
            for i in range(len(field.data[j])):
                point = Point(j, i)
                #if (point.x == 0) or (point.x == len(field.data) - 1) or (point.y == 0) or (point.y == len(field.data[0]) - 1):
                #    pygame.draw.rect(self.surf, (255, 0, 0), ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                if (field[point] == -1) and (abs(snake.positions[0].x - point.x) <= vision) and (abs(snake.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.surf, color_ai[1], ((i + self.pos[0])* self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
                elif (field[point] == 1) and (abs(snake.positions[0].x - point.x) <= vision) and (abs(snake.positions[0].y - point.y) <= vision):
                    pygame.draw.rect(self.surf, AQUA_MARINE, ((i + self.pos[0]) * self.BLOCK_H, (j + self.pos[1]) * self.BLOCK_W, self.BLOCK_W/2, self.BLOCK_H/2), 0)
               
        self.print_field_comp("ai", field, snake, 0)
        self.print_field_comp("human", field, snake_h, 0)                 
                    
        self.print_text('Eaten by human snake:    ' + str(eaten_h), pos_h[0])
        self.print_text('Eaten by machine snake:  ' + str(eaten), pos_ai[0])        
        self.print_text('Steps left: ' + str(step), pos_ai[1])
        
        self.sc.blit(self.surf, (0, 500))
        self.surf.fill((0, 0, 0))
        self.sc.blit(self.surf_all, (0, 250))
        self.surf_all.fill((0, 0, 0))
        
        pygame.draw.rect(self.sc, (255, 0, 0), (self.pos[0] + 1, self.pos[1], self.HEIGHT, self.WEIGHT * 3), 3)
                
        if(fill):
            pygame.display.flip()
            pygame.display.update()
            self.sc.fill((0, 0, 0))
    
    def print_window(self):
        pygame.display.flip()
        pygame.display.update()                    
    
    def get_direction(self):
    
        """ Processing events from keyboard """
        
        k = 0
        while(not k):
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_w):
                        return 'up'
                        k = 1
                    if (event.key == pygame.K_a):
                        return 'left'
                        k = 1
                    if (event.key == pygame.K_s):
                        return 'down'
                        k = 1
                    if (event.key == pygame.K_d):
                        return 'right'
                        k = 1
    
    def get_unn_direction(self, direction):
    
        """ Processing events from keyboard """
        
        k = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w]):
            return 'up'
        if (keys[pygame.K_a]):
            return 'left'
        if (keys[pygame.K_s]):
            return 'down'
        if (keys[pygame.K_d]):
            return 'right'
        else:
             return direction



class Slider():

    """ Creates slider for param """

    def __init__(self, name, val, max_val, min_val, pos, graphics):
        self.val = val
        self.max_val = max_val
        self.min_val = min_val
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.surf  = pygame.surface.Surface((100, 50)) 
        self.hit   = False
        self.font  = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = graphics.getSc()     

        self.txt_surf = self.font.render(name, 1, (255, 255, 0))
        self.txt_rect = self.txt_surf.get_rect(center = (50, 15))
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, (100, 100, 100), [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, (200, 200, 0), [10, 30, 80, 5], 0)
        self.surf.blit(self.txt_surf, self.txt_rect)
        
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill((250, 0, 0))
        self.button_surf.set_colorkey((250, 0, 0))
        self.button_rect = pygame.Rect((0, 0, 0, 0))
        pygame.draw.circle(self.button_surf, (0, 0, 0), (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, (230, 130, 0), (10, 10), 4, 0)


    """ Returns value to change param """    

    def getVal(self):
        return self.val
    

    """ Draws slider """   

    def draw(self):
        surf = self.surf.copy()
        pos  = (10 +int((self.val - self.min_val)/(self.max_val - self.min_val)*80), 33)
        self.button_rect = self.button_surf.get_rect(center = pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.x_pos, self.y_pos)
        self.screen.blit(surf, (self.x_pos, self.y_pos))
        pygame.display.flip()
        pygame.display.update()


    """ Moves slider """

    def move(self):
        self.val = (pygame.mouse.get_pos()[0] - self.x_pos - 10) / 80 * (self.max_val - self.min_val) + self.min_val
        if self.val < self.min_val:
            self.val = self.min_val
        if self.val > self.max_val:
            self.val = self.max_val
    

    """ Checks if slider was moved or not """    

    def is_active(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.button_rect.collidepoint(pos):
                    self.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.hit = False
        if self.hit:
             self.move()
