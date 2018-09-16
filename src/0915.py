import pygame          
#from random import randint
from pygame.locals import *    
from sys import exit         
import math   

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

ticks = 0
ticks1 = 0
ticks2 = 0
clock = pygame.time.Clock()

offset_Player2 = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0, pygame.K_l:0, pygame.K_SPACE:0}

offset_Player1 = {pygame.K_a:0, pygame.K_d:0, pygame.K_w:0, pygame.K_s:0, pygame.K_g:0, pygame.K_h:0}

class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    #x = property(getx, setx)

    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    #y = property(gety, sety)

def funcleft(x, w, dist, h):
    y = -0.005*(x-w)*(x - w + dist) + h
    return y
def funcright(x, w, dist, h):
    y = -0.005*(x-w)*(x - w - dist) + h
    return y

class Player1(pygame.sprite.Sprite):
    
    def __init__(self, Player1_surface, Player1_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = Player1_surface
        self.direction = 1
        self.rect = self.image[self.direction].get_rect()
        self.rect.topleft = Player1_init_pos
        self.speed = 6
        self.bullets1 = pygame.sprite.Group()
        self.is_hit = False
        self.life = 3
        self.ready = 0
        self.tick = 0
        self.shell_switch = 0
        self.shell_ticks = 0

    def move(self, offset):
        
        if offset[pygame.K_d] > 0:
            self.direction = 1
        if offset[pygame.K_a] > 0:
            self.direction = 0    
        
        x = self.rect.left + offset_Player1[pygame.K_d] - offset_Player1[pygame.K_a]
        y = self.rect.top + offset_Player1[pygame.K_s] - offset_Player1[pygame.K_w]
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
        if offset_Player1[pygame.K_g] > 0:
            if self.direction == 0:
                bullet1 = Bullet(bullet_surface[0], (self.rect.left, self.rect.top+self.rect.height/3))
            if self.direction == 1:
                bullet1 = Bullet2(bullet_surface[1], (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(bullet1)
            return 1
        return 0
        #print("bullet's amount: %d" %len(self.bullets1.sprites()))
    def shell_handle(self, distance):
        if self.shell_ticks and not self.shell_switch:
            self.single_Shell(distance)
            self.shell_ticks = 0   
        if self.shell_switch:
            self.shell_ticks += 10
        else:
            self.shell_ticks = 0
            
    def single_Shell(self, distance):
        if distance > 0:
            if self.direction == 0:
                shell1 = Shell(shell_surface[0], distance, self.direction, \
                               (self.rect.left, self.rect.top+self.rect.height/3))
            else:
                shell1 = Shell(shell_surface[1], distance, self.direction, \
                               (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(shell1)
            return 1
        return 0


class Player2(pygame.sprite.Sprite):
    
    def __init__(self, Player2_surface, Player2_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = Player2_surface
        self.direction = 0
        self.rect = self.image[self.direction].get_rect()
        self.rect.topleft = Player2_init_pos
        self.speed = 6
        self.bullets1 = pygame.sprite.Group()
        self.is_hit = False
        self.life = 3
        self.ready= 0
        self.tick = 0
        self.shell_switch = 0
        self.shell_ticks = 0

    def move(self, offset_Player2):
        
        if offset_Player2[pygame.K_RIGHT] > 0:
            self.direction = 1
        if offset_Player2[pygame.K_LEFT] > 0:
            self.direction = 0    
        
        x = self.rect.left + offset_Player2[pygame.K_RIGHT] - offset_Player2[pygame.K_LEFT]
        y = self.rect.top + offset_Player2[pygame.K_DOWN] - offset_Player2[pygame.K_UP]
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
        if offset_Player2[pygame.K_l] > 0:
            if self.direction == 0:
                bullet1 = Bullet(bullet_surface[0], (self.rect.left, self.rect.top+self.rect.height/3))
            if self.direction == 1:
                bullet1 = Bullet2(bullet_surface[1], (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(bullet1)
            return 1
        return 0
        #print("bullet's amount: %d" %len(self.bullets1.sprites()))
        
    def shell_handle(self, distance):
        if self.shell_ticks and not self.shell_switch:
            self.single_Shell(distance)
            self.shell_ticks = 0   
        if self.shell_switch:
            self.shell_ticks += 10
        else:
            self.shell_ticks = 0
        
    def single_Shell(self, distance):
        print("P2 fire~")
        if distance > 0:
            if self.direction == 0:
                shell1 = Shell(shell_surface[0], distance, self.direction, \
                                     (self.rect.left, self.rect.top+self.rect.height/3))
            if self.direction == 1:
                shell1 = Shell(shell_surface[1], distance, self.direction, \
                                     (self.rect.left + self.rect.width/2, self.rect.top+self.rect.height/3))
            self.bullets1.add(shell1)
            return 1
        return 0


class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed1 = 10
        self.speed2 = 10
        self.down_index = 0

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
        self.down_index = 0

    def update(self):
        #self.rect.top += self.speed1
        self.rect.left += self.speed2
        if self.rect.top < -self.rect.height:
            self.kill()
        if self.rect.left < -self.rect.width:
            self.kill()

class Shell(pygame.sprite.Sprite):
    def __init__(self, Shell_surface, distance, direction, Shell_init_pos):
        pygame.sprite.Sprite.__init__(self)            
        self.image = Shell_surface
        self.range = distance
        self._direction = direction
        self.rect = self.image.get_rect()
        self.rect.topleft = Shell_init_pos
        self.curplace = self.rect.topleft[0]
        self.speed1 = 10
        self.speed2 = 6
        self.down_index = 0
        self.init_pos = Shell_init_pos
        self.pos = Point(0, 0)
        print self.init_pos
        
        

    def update1(self):
        #self.rect.top += self.speed1
        if self._direction == 0:
            self.rect.left -= self.speed2
            if self.rect.left < self.curplace-self.range:
                self.image = blank_surface
                screen.blit(boom_surface[self.down_index], (self.curplace-self.range, self.rect.top))
                if self.down_index < 6:
                    self.down_index += 1
                else:
                    self.kill()
        if self._direction == 1:
            self.rect.left += self.speed2
            if self.rect.left > self.curplace+self.range:
                self.image = blank_surface
                screen.blit(boom_surface[self.down_index], (self.curplace+self.range, self.rect.top))
                if self.down_index < 6:
                    self.down_index += 1
                else:
                    self.kill()
        if self.rect.top < -self.rect.height:
            self.kill()
        if self.rect.left < -self.rect.width:
            self.kill()
 
    def update(self):
        if self._direction == 0:
            self.rect.left -= self.speed2
            self.pos.setx(self.rect.left)
            self.pos.sety( funcleft( self.pos.getx(), self.init_pos[0], self.range, -self.init_pos[1]) )
            self.rect.top = -self.pos.gety()
            if self.rect.left < self.init_pos[0]-self.range:
                self.image = blank_surface
                screen.blit(boom_surface[self.down_index], (self.init_pos[0]-self.range, self.rect.top))
                if self.down_index < 6:
                    self.down_index += 1
                else:
                    self.kill()

        if self._direction == 1:
            self.rect.left += self.speed2
            self.pos.setx(self.rect.left)
            self.pos.sety( funcright( self.pos.getx(), self.init_pos[0], self.range, -self.init_pos[1]) )
            self.rect.top = -self.pos.gety()
            if self.rect.left > self.init_pos[0]+self.range:                    
                self.image = blank_surface
                screen.blit(boom_surface[self.down_index], (self.init_pos[0]+self.range, self.rect.top))
                if self.down_index < 6:
                    self.down_index += 1
                else:
                    self.kill()
        if self.rect.top < -self.rect.height:
            self.kill()
        if self.rect.left < -self.rect.width:
            self.kill()  
  
pygame.init()                  
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  
pygame.display.set_caption('ShipCraft')  


#load background image 230*240
pick_background = pygame.image.load("resources/image/selectbg2.jpg").convert_alpha()
background = pygame.image.load("resources/image/ocean2.png").convert_alpha()

Player2left_img = pygame.image.load('resources/image/bb2.png').convert_alpha()
Player2right_img = pygame.image.load('resources/image/bb3.png').convert_alpha()

Player1left_img = pygame.image.load('resources/image/ca1.png').convert_alpha()
Player1right_img = pygame.image.load('resources/image/ca2.png').convert_alpha()

shoot_left_img = pygame.image.load('resources/image/bullet_left.png').convert_alpha()
shoot_right_img = pygame.image.load('resources/image/bullet_right.png').convert_alpha()
shell_left = pygame.image.load('resources/image/shell_left.png').convert_alpha()
shell_right = pygame.image.load('resources/image/shell_right.png').convert_alpha()

Player1win = pygame.image.load('resources/image/Player1win.png').convert_alpha()
Player2win = pygame.image.load('resources/image/Player2win.png').convert_alpha()
ready_image = pygame.image.load('resources/image/ready.png').convert_alpha()
down_surface = pygame.image.load('resources/image/boom.png').convert_alpha()
boom_surface1 = pygame.image.load('resources/image/boom_water1.png').convert_alpha()
boom_surface2 = pygame.image.load('resources/image/boom_water2.png').convert_alpha()
boom_surface3 = pygame.image.load('resources/image/boom_water3.png').convert_alpha()
boom_surface4 = pygame.image.load('resources/image/boom_water4.png').convert_alpha()
boom_surface5 = pygame.image.load('resources/image/boom_water5.png').convert_alpha()
boom_surface6 = pygame.image.load('resources/image/boom_water6.png').convert_alpha()
boom_surface7 = pygame.image.load('resources/image/boom_water7.png').convert_alpha()
blank_surface = pygame.image.load('resources/image/blank.png').convert_alpha()

imagebool = []
imagebool.append(Player2left_img)
imagebool.append(Player1left_img)

BB_surface = []
BB_surface.append(Player2left_img)
BB_surface.append(Player2right_img)


CA_surface = []
CA_surface.append(Player1left_img)
CA_surface.append(Player1right_img)
bullet_surface = [shoot_left_img, shoot_right_img]
shell_surface = []
shell_surface.append(shell_left)
shell_surface.append(shell_right)
boom_surface = []
boom_surface.append(boom_surface1)
boom_surface.append(boom_surface2)
boom_surface.append(boom_surface3)
boom_surface.append(boom_surface4)
boom_surface.append(boom_surface5)
boom_surface.append(boom_surface6)
boom_surface.append(boom_surface7)


Player2_pos = [SCREEN_WIDTH, SCREEN_HEIGHT/2 - 130]
Player1_pos = [0, SCREEN_HEIGHT/2 - 130]


P2 = Player2(BB_surface, Player2_pos)
P1 = Player1(CA_surface, Player1_pos)
down_group = pygame.sprite.Group()

#pick mode
while True:
    clock.tick(10) #Limit the maximum number of frames
    screen.blit(pick_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                P1.ready = 1
            if event.key == pygame.K_l:
                P2.ready = 1
                
            if event.key == pygame.K_LEFT:
                offset_Player2[event.key] = P2.speed
            if event.key == pygame.K_RIGHT:
                offset_Player2[event.key] = P2.speed
                
            if event.key == pygame.K_a:
                offset_Player1[event.key] = P1.speed
            if event.key == pygame.K_d:
                offset_Player1[event.key] = P1.speed
    
    if offset_Player2[pygame.K_LEFT] > 0:
        if P2.tick < 1:
            P2.tick += 1
        else:
            P2.tick = 0
        offset_Player2[pygame.K_LEFT] = 0
    if offset_Player2[pygame.K_RIGHT] > 0:
        if P2.tick > 0:
            P2.tick -= 1
        else:
            P2.tick = 1
        
        offset_Player2[pygame.K_RIGHT] = 0 
    if offset_Player1[pygame.K_a] > 0:
        if P1.tick < 1:
            P1.tick += 1
        else:
            P1.tick = 0
        
        offset_Player1[pygame.K_a] = 0 
    if offset_Player1[pygame.K_d] > 0:
        if P1.tick > 0:
            P1.tick -= 1
        else:
            P1.tick = 1
        
        offset_Player1[pygame.K_d] = 0
        

    
    if P1.ready == 1:
        if P1.tick == 1:
            P1.image = CA_surface
        else:
            P1.image = BB_surface

        screen.blit(ready_image, (500, 100)) 
    else:
        screen.blit(imagebool[P1.tick], (500, 100))
    if P2.ready == 1:
        if P2.tick == 1:
            P2.image = CA_surface
        else:
            P2.image = BB_surface
        screen.blit(ready_image, (500, 330))
    else:
        screen.blit(imagebool[P2.tick], (500, 330))            
    if P1.ready == 1 and P2.ready == 1:
        break
    
    pygame.display.update()        


#pvp mode
Player1_distance = 0
Player2_distance = 0
shell_ticks1 = 0
shell_ticks2 = 0
shell_switch1 = 0
shell_switch2 = 0
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
    
    screen.blit(P2.image[P2.direction], P2.rect)
    screen.blit(P1.image[P1.direction], P1.rect)
    ticks += 1  
    ticks1 += 1
    ticks2 += 1   
    
    #screen.blit(hero.image,(220+pos.x,250+pos.y))
    
    
    P2.bullets1.update()
    P2.bullets1.draw(screen)
    P1.bullets1.update()
    P1.bullets1.draw(screen)
    
    #refresh screen
    
    #pygame.display.flip()
    #pygame.draw.polygon(hero_surface[0],(0,255,0),((1,1), (1,100), (100,1), (100,100)),width=0)
    
    #hit down judge
    Player2_down = pygame.sprite.spritecollide(P2, P1.bullets1, True)
    if len(Player2_down) > 0:
        down_group.add(Player2_down)
        P2.is_hit = True
        P2.life -= 1
    
    Player1_down = pygame.sprite.spritecollide(P1, P2.bullets1, True)
    if len(Player1_down) > 0:
        down_group.add(Player1_down)
        P1.is_hit = True
        P1.life -= 1
    
    for element_down in down_group:
        screen.blit(down_surface, element_down.rect)
        if element_down.down_index < 10:
            element_down.down_index += 1
        else:
            down_group.remove(element_down)   

    if P2.life <= 0:
        screen.blit(Player1win, (0, 0))
        break
        
    if P1.life <= 0:
        screen.blit(Player2win, (0, 0))
        break
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

         
        if event.type == pygame.KEYDOWN:
            if event.key in offset_Player2:
                offset_Player2[event.key] = P2.speed
            if event.key in offset_Player1:
                offset_Player1[event.key] = P1.speed

            if event.key == pygame.K_h:
                P1.shell_switch = 1
            if event.key == pygame.K_SPACE:
                P2.shell_switch = 1
            
        elif event.type == pygame.KEYUP:
            if event.key in offset_Player2:
                offset_Player2[event.key] = 0
            if event.key in offset_Player1:
                offset_Player1[event.key] = 0
            if event.key == pygame.K_h:
                P1.shell_switch = 0
            if event.key == pygame.K_SPACE:
                P2.shell_switch = 0


        #if P1.shell_ticks and not P1.shell_switch:
        #    P1.single_Shell(P1.shell_ticks)

            
        if ticks1 > 20:
            if P1.single_shoot(bullet_surface):
                ticks1 = 0
        if ticks2 > 20:
            if P2.single_shoot(bullet_surface):
                ticks2 = 0

    P1.shell_handle(P1.shell_ticks) 
    P2.shell_handle(P2.shell_ticks) 

    P2.move(offset_Player2)
    P1.move(offset_Player1)
    
    pygame.display.update()
    

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()