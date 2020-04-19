#setup
import pygame 
import time
import random 
import math
import tkinter
pygame.mixer.init()
pygame.init()

#loading background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
#setting up fonts
myfont = pygame.font.SysFont("monospace", 25)
myfont2 = pygame.font.SysFont("monospace", 40) 

#window settings
screenW = 1000 
screenH = 600

win = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Asteroido Dodgeo Maino')
background = pygame.image.load('background.jpg')

clock = pygame.time.Clock()

def redrawGameWindow():
    win.blit(background,(0,0))
    ship.draw(win)
    for asteroid in asteroids:
        asteroid.draw(win)
    for bullet in bullets:
        bullet.draw(win)
        bullet.y -= bullet.vel
    label = myfont.render("Ammo: " + str(ship.ammo), 1 , (255,255,255))
    label2 = myfont.render("Score: " + str(ship.score), 1 , (255,255,255))
    label3 = myfont.render("Lvl: " + str(Asteroid.lvl), 1 , (255,255,255))
    win.blit(label, (5, 5))
    win.blit(label2,(450,5))
    win.blit(label3, (900, 5))
    pygame.display.update()

def gameOver(win):
    gameover = myfont2.render("GAME OVER -> SCORE: " + str(ship.score), 1, (255,255,255), (0,0,0))
    win.blit(gameover,(screenW/2 - 250, screenH/2 - 20))
    Asteroid.lvl = 0
    del bullets[:]
    del asteroids[:]
    ship.x = screenW //2
    ship.y = 500
    ship.score = 0 
    ship.vel = 10.5
    ship.ammo = 3
    ship.lvlPoints = 0
    allowSpawn = 1000
    for i in range(5,0,-1):
        restart = myfont2.render("Game will restart in " + str(i) + "s",True,(255,255,255) ,(0,0,0))
        win.blit(restart,(screenW/2- 260, screenH/2 + 20))
        pygame.display.update()
        time.sleep(1)
    Play()

def distance(x,y):
    xDistance = ship.centerX - x
    yDistance = ship.centerY - y

    return  math.sqrt(xDistance**2 + yDistance**2)
    
class Ship(object):

    def __init__(self):
        self.x = screenW //2 
        self.y = 500
        self.width = 50
        self.height = 50 
        self.image = pygame.transform.scale((pygame.image.load('ship.png')),(self.width,self.height))
        self.vel = 10.5
        self.score = 0
        self.lvlPoints = 0
        self.centerX = self.x+(self.width//2)
        self.centerY = self.y+(self.height//2)
        self.radius = 20
        self.ammo = 2000


    def draw(self, win):
        self.centerX = self.x+(self.width//2)
        self.centerY = self.y+(self.height//2)
        #pygame.draw.circle(win, (0,255,0),  (self.centerX,self.centerY) , self.radius, 2)
        win.blit(self.image, (self.x, self.y))


class Asteroid(object):

    lvl = 0
    def __init__(self):
        self.x = random.randint(0,1000)
        self.y = random.randint(-300,0)
        self.width = random.randint(80,120)
        self.height = self.width
        self.image = pygame.transform.scale((pygame.image.load('asteroid.png')),(self.width,self.height))
        self.vel = [random.randint(12,18),random.randint(14,20),random.randint(16,22),random.randint(18,24),random.randint(20,26),random.randint(23,29)] 
        self.centerX = self.x+(self.width//2)
        self.centerY = self.y+(self.height//2)
        self.radius = 45

    def draw(self,win):
        self.centerX = self.x+(self.width//2)
        self.centerY = self.y+(self.height//2)
        #pygame.draw.circle(win, (255,0,0), (self.centerX,self.centerY) ,self.radius, 2)
        win.blit(self.image, (self.x,self.y))

class Bullet(object):

    def __init__(self, shooter):
        self.x = shooter.centerX 
        self.y = shooter.centerY - shooter.radius
        self.width = 5
        self.height = 12
        self.hitbox = (self.x, self.y , self.width, self.height)
        self.vel = 20
        
    def draw(self,win):
        self.hitbox = (self.x, self.y , self.width, self.height)
        pygame.draw.rect(win,(0,255,0),self.hitbox)
            

def Play():
    global allowSpawn, allowShooting, shootLoop
    
    run = True
    while run:

        clock.tick(30)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if ship.y >= 0:
                ship.y -= ship.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if ship.y < 600 - ship.height:
                ship.y += ship.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if ship.x <= 1000 - ship.width:
                ship.x += ship.vel
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if ship.x >= 0:
                ship.x -= ship.vel 
        if keys[pygame.K_SPACE] and shootLoop == 0:
            if ship.ammo > 0:
                bullets.append(Bullet(ship))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('laser.wav'))
                ship.ammo -= 1
            shootLoop = 1

        if allowSpawn <= 0:
            allowSpawn = 1000
        else:
            for i in range(1):
                if len(asteroids) <= 4:
                    asteroids.append(Asteroid())
            allowSpawn -= 1

        for asteroid in asteroids:
            for bullet in bullets:
                if bullet.hitbox[1] < asteroid.centerY + asteroid.radius and bullet.hitbox[1] + bullet.hitbox[3] > asteroid.centerY - asteroid.radius:
                    if bullet.hitbox[0] > asteroid.centerX - asteroid.radius and bullet.hitbox[0] + bullet.hitbox[2] < asteroid.centerX + asteroid.radius:
                        asteroids.pop(asteroids.index(asteroid))
                        bullets.pop(bullets.index(bullet))
            
            if distance(asteroid.centerX, asteroid.centerY) < (ship.radius + asteroid.radius):
                run = False
                gameOver(win)
            if asteroid.y >= 600:
                ship.score += 1
                ship.lvlPoints += 1
                asteroids.pop(asteroids.index(asteroid))
            else:
                asteroid.y += asteroid.vel[Asteroid.lvl]

        if ship.lvlPoints >= 50:
            if ship.ammo < 3:
                ship.ammo += 1
            if Asteroid.lvl < 5:
                Asteroid.lvl += 1
                ship.vel += 0.5
                
            ship.lvlPoints = 0
        
       
        redrawGameWindow()

#mainLoop
ship = Ship()
asteroids = []
bullets = []
allowSpawn = 1000
allowShooting = 1000
shootLoop = 0
Play()
