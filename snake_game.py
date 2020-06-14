import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()

r=20
w=500
h=500
vel=10

bg=pygame.transform.scale(pygame.image.load("snake1.png"),(w,h))

class cube():
    r = 20
    w = 500
    def __init__(self, start, dx = 1, dy = 0, color = (0,255,0)):
        self.pos = start
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0]+self.dx, self.pos[1]+self.dy)

    def draw(self, surface, eyes = False):
        d = self.w // self.r
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*d+1, j*d+1, d-2, d-2))
        if eyes:
            centre = d//2
            rad = 3
            circle_m1 = (i*d+centre-rad, j*d+8)
            circle_m2 = (i*d+d-rad*2, j*d+8)
            pygame.draw.circle(surface, (0,0,0), circle_m1, rad)
            pygame.draw.circle(surface, (0,0,0), circle_m2, rad)

class snake():
    body = []
    turn = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1

    def move(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

            key = pygame.key.get_pressed()

            for k in key:
                if key[pygame.K_LEFT]:
                    self.dx = -1
                    self.dy = 0
                    self.turn[self.head.pos[:]] = [self.dx, self.dy]

                elif key[pygame.K_RIGHT]:
                    self.dx = 1
                    self.dy = 0
                    self.turn[self.head.pos[:]] = [self.dx, self.dy]

                elif key[pygame.K_UP]:
                    self.dx = 0
                    self.dy = -1
                    self.turn[self.head.pos[:]] = [self.dx, self.dy]

                elif key[pygame.K_DOWN]:
                    self.dx = 0
                    self.dy = 1
                    self.turn[self.head.pos[:]] = [self.dx, self.dy]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turn:
                t = self.turn[p]
                c.move(t[0], t[1])
                if i == len(self.body)-1:
                    self.turn.pop(p)
            else:
                if c.dx == -1 and c.pos[0] <= 0:
                    c.pos = (c.r-1, c.pos[1])
                elif c.dx == 1 and c.pos[0] >= c.r-1:
                    c.pos = (0, c.pos[1])
                elif c.dy == 1 and c.pos[1] >= c.r-1:
                    c.pos = (c.pos[0], 0)
                elif c.dy == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.r-1)
                else:
                    c.move(c.dx, c.dy)
                    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turn ={}
        self.dx = 0
        self.dy = 1

    def addcube(self):
        tail = self.body[-1]
        dtx, dty = tail.dx, tail.dy

        if dtx == 1 and dty == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dtx == -1 and dty == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dtx == 0 and dty == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dtx == 0 and dty == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dx = dtx
        self.body[-1].dy = dty
        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def redrawwin(surface):
    global w, r, s, snac
    surface.blit(bg,(0,0))
    s.draw(surface)
    snac.draw(surface)
    lfont=pygame.font.SysFont('comicsans',50)
    txt=lfont.render('Score: '+str(len(s.body)-1),1,(0,0,0))
    surface.blit(txt, (200,10))
    pygame.display.update()

def snack(r, item):
    position = item.body

    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        if len(list(filter(lambda z:z.pos == (x,y), position))) >0:
            continue
        else:
            break
    return (x,y)

def m_box(sub, cont):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(sub, cont)
    try:
        root.destroy()
    except:
        pass


def main():
    global s, snac
    win = pygame.display.set_mode((w, w))
    s = snake((0,0,255), (10,10))
    snac = cube(snack(r, s),(255,0,0))
    run = True
    clock = pygame.time.Clock()

    while run:
        pygame.time.delay(100)

        clock.tick(vel)
        s.move()
        hpos = s.head.pos
        if hpos[0]>=20 or hpos[0]<0 or hpos[1]>=20 or hpos[1]<0:
            m_box('Game Over!','Try again...')
            s.reset((10,10))

        if s.body[0].pos == snac.pos:
            s.addcube()
            snac = cube(snack(r, s),(255,0,0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print("Score: ",len(s.body))
                m_box('Game Over!','Try again...')
                s.reset((10,10))
                break
            
        redrawwin(win)
        
main()
