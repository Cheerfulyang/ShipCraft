import pygame          
from random import randint
from pygame.locals import *    
from sys import exit         
import math   

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

ticks = 0
ticks1 = 0
ticks2 = 0
clock = pygame.time.Clock()

offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0, pygame.K_l:0}

offset_enemy = {pygame.K_a:0, pygame.K_d:0, pygame.K_w:0, pygame.K_s:0, pygame.K_g:0}

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 6
        self.bullets1 = pygame.sprite.Group()
        self.direction = 1
        self.is_hit = False
        self.life = 3

    def move(self, offset):
        
        if offset[pygame.K_d] > 0:
            self.direction = 1
        if offset[pygame.K_a] > 0:
            self.direction = 0    
        
        x = self.rect.left + offset[pygame.K_d] - offset[pygame.K_a]
        y = self.rect.top + offset[pygame.K_s] - offset[pygame.K_w]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
            
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y
            
    def single_shoot(self, bullet_surface):
        if offset_enemy[pygame.K_g] > 0:
            if self.direction == 0:
                bullet1 = Bullet(bullet_surface[0], (self.rect.left, self.rect.top+self.rect.height/3))
            if self.direction == 1:
                bullet1 = Bullet2(bullet_surface[1], (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(bullet1)
            return 1
        return 0
        #print("bullet's amount: %d" %len(self.bullets1.sprites()))


class Hero(pygame.sprite.Sprite):
    
    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.bullets1 = pygame.sprite.Group()
        self.direction = 0
        self.is_hit = False
        self.life = 3

    def move(self, offset):
        
        if offset[pygame.K_RIGHT] > 0:
            self.direction = 1
        if offset[pygame.K_LEFT] > 0:
            self.direction = 0    
        
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
            
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y
            
    def single_shoot(self, bullet_surface):
        if offset[pygame.K_l] > 0:
            if self.direction == 0:
                bullet1 = Bullet(bullet_surface[0], (self.rect.left, self.rect.top+self.rect.height/3))
            if self.direction == 1:
                bullet1 = Bullet2(bullet_surface[1], (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(bullet1)
            return 1
        return 0
        #print("bullet's amount: %d" %len(self.bullets1.sprites()))


class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed1 = 10
        self.speed2 = 10

    def update(self):
        #self.rect.top += self.speed1
        self.rect.left -= self.speed2
        if self.rect.top < -self.rect.height:
            self.kill()
        if self.rect.left < -self.rect.width:
            self.kill()
            
class Bullet2(pygame.sprite.Sprite):

    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed1 = 5
        self.speed2 = 10

    def update(self):
        #self.rect.top += self.speed1
        self.rect.left += self.speed2
        if self.rect.top < -self.rect.height:
            self.kill()
        if self.rect.left < -self.rect.width:
            self.kill()


  
  
pygame.init()                  
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])     

pygame.display.set_caption('This is my first game-program for my darling')      

#load background image 230*240
background = pygame.image.load("resources/image/ocean2.png").convert_alpha()

shipleft_img = pygame.image.load('resources/image/bb2.png').convert_alpha()
shipright_img = pygame.image.load('resources/image/bb3.png').convert_alpha()

enemyleft_img = pygame.image.load('resources/image/ca1.png').convert_alpha()
enemyright_img = pygame.image.load('resources/image/ca2.png').convert_alpha()

shoot_left_img = pygame.image.load('resources/image/bullet_left.png').convert_alpha()
shoot_right_img = pygame.image.load('resources/image/bullet_right.png').convert_alpha()
enemywin = pygame.image.load('resources/image/enemywin.png').convert_alpha()
herowin = pygame.image.load('resources/image/herowin.png').convert_alpha()


#hero1_rect = pygame.Rect(70, 30, 330, 330)
#hero2_rect = pygame.Rect(70, 30, 330, 330)
#hero1 = shoot_img.subsurface(hero1_rect)
#hero2 = shoot_img.subsurface(hero2_rect)
#hero_pos = [SCREEN_WIDTH/2 - 130, SCREEN_HEIGHT/2 - 130]


hero_surface = []
hero_surface.append(shipleft_img)
hero_surface.append(shipright_img)


enemy_surface = []
enemy_surface.append(enemyleft_img)
enemy_surface.append(enemyright_img)
#hero_surface.append(shoot_img.subsurface(pygame.Polygon((1,1), (1,100), (100,1), (100,100))))
hero_pos = [SCREEN_WIDTH, SCREEN_HEIGHT/2 - 130]
enemy_pos = [0, SCREEN_HEIGHT/2 - 130]

bullet_surface = [shoot_left_img, shoot_right_img]

down_surface = pygame.image.load('resources/image/boom.png').convert_alpha()
#.subsurface(pygame.Rect(0, 0, 10, 10))

hero = Hero(hero_surface[0], hero_pos)
enemy = Enemy(enemyright_img, enemy_pos)



down_group = pygame.sprite.Group()

while True:
    clock.tick(60) #Limit the maximum number of frames
    
    #place background
    
    screen.blit(background, (0, 0))
    #if ticks >= 30:
    #    ticks = 0
    #hero.image = hero_surface[ticks//(30//2)]

    
    '''
    angle = wrap_angle(angle +90)
    pos.x = math.cos(math.radians(angle))*20
    pos.y = math.sin(math.radians(angle))*20
    hero.image = pygame.transform.rotate(hero.image,180-angle)
    if ticks >= 100:
        ticks = 0
        #hero.image = pygame.transform.rotate(hero.image,9)
        hero.image = pygame.transform.rotate(hero.image,180-angle)
    '''
    
    screen.blit(hero.image, hero.rect)
    screen.blit(enemy.image, enemy.rect)
    ticks += 1  
    ticks1 += 1
    ticks2 += 1   
    
    #screen.blit(hero.image,(220+pos.x,250+pos.y))
    
    
    hero.bullets1.update()
    hero.bullets1.draw(screen)
    enemy.bullets1.update()
    enemy.bullets1.draw(screen)
    
    #refresh screen
    
    #pygame.display.flip()
    #pygame.draw.polygon(hero_surface[0],(0,255,0),((1,1), (1,100), (100,1), (100,100)),width=0)
    
    #hit down judge
    hero_down = pygame.sprite.spritecollide(hero, enemy.bullets1, True)
    if len(hero_down) > 0:
        down_group.add(hero_down)
        hero.is_hit = True
        hero.life -= 1
    
    enemy_down = pygame.sprite.spritecollide(enemy, hero.bullets1, True)
    if len(enemy_down) > 0:
        down_group.add(enemy_down)
        enemy.is_hit = True
        enemy.life -= 1
    
    for element_down in down_group:
        screen.blit(down_surface, element_down.rect)
        down_group.remove(element_down)        

    if hero.life <= 0:
        screen.blit(enemywin, (0, 0))
        break
        
    if enemy.life <= 0:
        screen.blit(herowin, (0, 0))
        break
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

         
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = hero.speed
            if event.key in offset_enemy:
                offset_enemy[event.key] = hero.speed
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
            if event.key in offset_enemy:
                offset_enemy[event.key] = 0
        if ticks1 > 20:
            if hero.single_shoot(bullet_surface):
                ticks1 = 0
        if ticks2 > 20:
            if enemy.single_shoot(bullet_surface):
                ticks2 = 0
                

    hero.move(offset)
    enemy.move(offset_enemy)
    if hero.direction == 1:
        hero.image = hero_surface[1]
    if hero.direction == 0:
        hero.image = hero_surface[0]
        
    if enemy.direction == 1:
        enemy.image = enemy_surface[1]
    if enemy.direction == 0:
        enemy.image = enemy_surface[0]    
    
    pygame.display.update()
    

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()