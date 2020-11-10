import random
import pygame
import tkinter as tk
from tkinter import messagebox
#imported above modules

dis = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game by Tracy')
#Sets window title

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        
        
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #Ensures the game quits if user selects X
                
            keys = pygame.key.get_pressed()
            #Lists what keys have been pressed
           
            for key in keys:
               if keys[pygame.K_LEFT]:
                 self.dirnx = -1
                 self.dirny = 0
                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                 
               if keys[pygame.K_RIGHT]:
                 self.dirnx = 1
                 self.dirny = 0
                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                 
               if keys[pygame.K_UP]:
                 self.dirnx = 0
                 self.dirny = -1
                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] 
                 
               if keys[pygame.K_DOWN]:
                 self.dirnx = 0
                 self.dirny = 1
                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                   
        for i, c in enumerate(self.body):
        #Loop through every cube in the snake body
            p = c.pos[:]
            #Stores positions of cubes
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
            #If the position is where the cube turned, find the direction and move the cube in that direction
                if i == len(self.body)-1:
                    self.turns.pop(p)
                #If it's the last cube of the snake body remove the turn from the dictionary
            
                    
            else:
               if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
               elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
               elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
               elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
               else: c.move(c.dirnx,c.dirny)
               
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        #Need to ensure a new cube is added to the tail of the snake
        
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        #Finds the direction of the snake and position of the tail so we know where thew new cube must be added
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        #Set the direction of the cube as the same direction as the snake
    
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else: 
                c.draw(surface)
       

class cube(object):
    rows = 20
    h = 600
    #need to ensure height is divisible by rows so that we don't end up with decimals
    def __init__(self, start, dirnx=1, dirny=0, color=(255,150,180)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        #Defines starting direction of the snake, right
        
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        
    def draw(self, surface, eyes=False):
        dis = self.h // self.rows
        i = self.pos[0]
        #Row
        j = self.pos[1]
        #Column
        
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        #Helps us determine where to draw it
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre -radius, j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
            #Creates the eyes on the head of the snake
            
    
def drawGrid(h, rows, surface):
    sizeBtwn = h // rows
    #creates the grid for our game
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        
        pygame.draw.line(surface, (255,255,255), (x,0), (x,h))
        pygame.draw.line(surface, (255,255,255), (0,y), (h,y))
#Draws two lines in direction x and direction y in white

def redrawWindow(surface):
    global rows, height, s, food
    surface.fill((159,195,230))
    s.draw(surface)
    food.draw(surface)
    drawGrid(height, rows, surface)
    pygame.display.update()

    
def randomFood(rows, item):
    positions = item.body
    #Obtains all the positions of the cube of the body 
    
    while True:
        x= random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)
#Produces and randomises the position of the food and ensures it doesnt overlap with the snake body

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try: 
        root.destroy()
    except: 
        pass
    #creates message box

def main():
    global height, rows, s, food
    height = 600
    rows = 20
    #det
    win = pygame.display.set_mode((height, height))
    s = snake((255,0,0), (10,10))
    food = cube(randomFood(rows, s), color=(255,255,0))
    score = 0
    flag = True
    
    
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.addCube()
            score += 1
            print(score)
            food = cube(randomFood(rows, s), color=(255,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
            #Checks if any cubes overlap
                print('Score: ', len(s.body))
                message_box('You Lose', 'Play Again')
                s.reset((10,10))
                break
                #Prints score and displays message box whenever user loses 
        
        redrawWindow(win)
        
    pass


main()