import pygame
import sys
import math
#import matplotlib.pyplot as plt
import numpy as np
#from scipy.integrate import ode
import random
Distance = 384400000.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255,155,0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (134,1,175)
PINK = (255,105,180)
rock_colours = (RED,ORANGE,YELLOW,GREEN,BLUE,PINK,PURPLE)

dt = 0.033
class Ship:
    def __init__(self):
        self.center = np.array([430.0,430.0])
        self.length = 40.0
        self.corners = np.array([[self.center[0]-self.length/2,self.center[1]-self.length/2], [self.center[0]-self.length/2, self.center[1]+self.length/2], [self.center[0]+self.length/2, self.center[1]+self.length/2],[self.center[0]+self.length/2,self.center[1]-self.length/2], [self.center[0], self.center[1]-self.length*7/8]])
        #self.world_coord = [[300.0,300.0], [300.0, 340.0], [340.0, 340.0],[340.0,300.0],[320.0, 280.0]]
        self.v = np.array([0.0,0.0])
        self.a = np.array([0.0,0.0])
        self.w = 0.0
        self.r = math.sqrt(800)
    def update(self):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            r = self.corners[-1] - self.center
            self.a = r*0.01
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        #     self.a[1] = self.a[1]+0.25
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #     self.a[0] = self.a[0]-0.25
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        #     self.a[0] = self.a[0]+0.25
        if event.type == pygame.KEYUP and event.key == pygame.K_w:
            self.a = np.array([0.0,0.0])
        # if event.type == pygame.KEYUP and event.key == pygame.K_s:
        #     self.a[1] = 0
        # if event.type == pygame.KEYUP and event.key == pygame.K_a:
        #     self.a[0] = 0
        # if event.type == pygame.KEYUP and event.key == pygame.K_d:
        #     self.a[0] = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.w = -1*math.pi/24 *dt
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            self.w = 0.0        
        self.v += self.a*dt
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.w = math.pi/24 *dt
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            self.w = 0.0        

        #self.corners+= self.r*self.w
        if self.w!=0.0:
            for i in range(len(self.corners)):
                r = np.array([self.corners[i][0]-self.center[0],(self.corners[i][1]-self.center[1])])
                #h = math.sqrt(r[0]**2 + r[1]**2)
                x = math.cos(self.w)*r[0] - math.sin(self.w)*r[1] - r[0]
                y = math.sin(self.w)*r[0] + math.cos(self.w)*r[1] - r[1]

                self.corners[i] += np.array([x,y])
        self.v += self.a*dt
        self.corners+= self.v*dt
        self.center+= self.v*dt        
        if (self.center[0]+self.v*dt)[0]+self.length/2 >= 860 or (self.center[0]+self.v*dt)[0]-self.length/2 <= 0:
            self.v[0] = self.v[0]*-1
        if (self.center[1]+self.v*dt)[1]+self.length/2 >= 860 or (self.center[1]+self.v*dt)[1]-self.length/2 <= 0:
            self.v[1] = self.v[1]*-1       

    def collision(self, rock):
        if abs(rock.x - self.center[0]) < self.length/2 + rock.radius and abs(rock.y - self.center[1]) < self.length/2 + rock.radius:
            pygame.draw.polygon(screen, WHITE, self.corners)
            return True
        else:
            return False
    def draw(self, screen):
        pygame.draw.polygon(screen, WHITE, self.corners)

class Rock:
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.v = np.array([random.random(),random.random()])
        self.pos = np.array([self.x,self.y])
        self.radius = radius
        self.mass = 1
    
    def update(self):
        if (self.pos+self.v*dt)[0]+self.radius >= 860 or (self.pos+self.v*dt)[0]-self.radius <= 0:
            self.v[0] = self.v[0]*-1
        if (self.pos+self.v*dt)[1]+self.radius >= 860 or (self.pos+self.v*dt)[1]-self.radius <= 0:
            self.v[1] = self.v[1]*-1    
        self.pos += self.v*dt
        self.x = self.pos[0]
        self.y = self.pos[1]
        
    def draw(self, screen):
        pygame.draw.circle(screen,self.colour,[self.pos[0],self.pos[1]], self.radius)


class Universe:
    def __init__(self):
        self.w, self.h = 2.6*Distance, 2.6*Distance 
        self.ship = Ship()
        self.objects = [self.ship]
        # self.rock1 = Rock()
        # self.rock2 = Rock()
        # self.rock3 = Rock()
        # self.rock4 = Rock()
        # self.rock5 = Rock()
        # self.rock6 = Rock()
        # self.rock7 = Rock()
        # self.rock8 = Rock()
        # self.rock9 = Rock()
        # self.rock10 = Rock()
        
        for i in range(10):
            self.add_rock()

        self.objLen = len(self.objects)
        #self.objects = pygame.sprite.Group()
        self.dt = 10.0
        self.collisions = []

    def add_rock(self):
        #self.objects_dict[body.name] = body
        x = random.random()*820.0+20.0
        y = random.random()*820.0+20.0
        colour = rock_colours[random.randint(0,6)]
        r = 20.0
        while True:
            if abs(x - self.ship.center[0]) < self.ship.length/2 + r and abs(y - self.ship.center[1]) < self.ship.length/2 + r: 
                x = random.random()*820.0+20.0
                y = random.random()*820.0+20.0
            else: 
                break
        for j in self.objects[1:]:
            
            if detect_collision(j,x,y,r):
                x = random.random()*820.0+20.0
                y = random.random()*820.0+20.0
                j = 0

        self.objects.append(Rock(x,y,r,colour))

    # def to_screen(self, pos):
    #     return [int((pos[0] + 1.3*Distance)*640//self.w), int((pos[1] + 1.3*Distance)*640.//self.h)]

    def update(self):
        for x in self.objects:
            x.update()
        for x in range(1, self.objLen):
            
            if self.ship.collision(self.objects[x]):
                pygame.quit()
                sys.exit(0)
            for y in range(x+1, self.objLen):
                
                if detect_collision(self.objects[x],self.objects[y].x,self.objects[y].y,self.objects[y].radius):
                    self.collisions.append([self.objects[x],self.objects[y]])
        for x in self.collisions:
            collision_response(x)
        self.collisions = []
        
    #     for o in self.objects:
    #         # Compute positions for screen
    #         obj = self.objects[o]
    #         # obj.update1(self.objects, self.dt)
    #         p = self.to_screen(obj.pos)

    #             print ('Name', obj.name)
    #             print ('Position in simulation space', obj.pos)
    #             print ('Position on screen', p)

    #         # Update sprite locations
    #         obj.rect.x, obj.rect.y = p[0]-obj.radius, p[1]-obj.radius
    #     self.objects.update()
        
    def draw(self, screen):
        for i in self.objects:
            i.draw(screen)

def detect_collision(rock1,x,y,r ):
    if math.sqrt((rock1.x-x)*(rock1.x-x) + (rock1.y-y)*(rock1.y-y)) < rock1.radius + r:
        return True
    else:
        return False


def collision_response(rocks):
    rock1 = rocks[0]
    rock2 = rocks[1]
    #d = math.sqrt((rock1.x-rock2.x)*(rock1.x-rock2.x) + (rock1.y-rock2.y)*(rock1.y-rock2.y))
    n = (rock1.pos-rock2.pos)/abs(rock1.pos-rock2.pos)
    v = rock1.v - rock2.v
    j = (-1)*2*v*n/((1/rock1.mass)+(1/rock2.mass))
    rock1.v = rock1.v + (j*n/rock1.mass)
    rock2.v = rock2.v - (j*n/rock2.mass)
    
if __name__ == "__main__":
    #space_rocks = SpaceRocks()
    #space_rocks.main_loop()
    pygame.init()
    win_width = 860
    win_height = 860
    screen = pygame.display.set_mode((win_width, win_height)) 
    universe = Universe()
    #ship = Ship()
    iter_per_frame = 1

    frame = 0
    while True:
        if False:
            print ('Frame number', frame)        

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        
        # elif event.type == pygame.KEYUP and event.key == pygame.K_w:
        #     ship.
        else:
            pass
            
        universe.update()
        #ship.update()

        screen.fill(BLACK) # clear the background
        universe.draw(screen)
        #ship.draw(screen)
        pygame.display.flip()
        if frame == 20000:
            universe.add_rock()
            frame = 0

        frame += 1
