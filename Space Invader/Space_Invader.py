import pygame
import random

pygame.init()
pygame.display.set_caption("Space Invaders")
gamescreen = pygame.display.set_mode ((800, 800))
tick = pygame.time.Clock()
timer = 0;
Bye = False
xpos = 400
ypos = 750
vx = 5
moveLeft = False
moveRight = False
shoot = False
numHits = 0
lives = 3
score = 0

class Missile:#-----------------------------------------------------------
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False

    def move(self):
        if self.isAlive == True:
            self.ypos+=10
        if self.ypos > 800:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
    
        
    def draw(self):
        
        if self.isAlive == True:
            pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))

missiles = []
for i in range(100):
    missiles.append(Missile())
class Wall:#---------------------------------------------------------------------
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0

    
    def collide(self, BulletX, BulletY):
        #print("inside wall collide")
        if self.numHits < 3:
            #print("flag1")
            if BulletX > self.xpos:
                if BulletX < self.xpos+40:
                      if BulletY < self.ypos+40:
                          #print("inside bounding box for wall", end = " ")
                          if BulletY > self.ypos:
                               # print("wall hit!")
                                self.numHits += 1
                                return False
        return True


    
 
    def draw(self):
        if self.numHits == 0:
            pygame.draw.rect(gamescreen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 1:
            pygame.draw.rect(gamescreen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHits == 2:
            pygame.draw.rect(gamescreen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))




class Bullet:#---------------------------------------------------------------------
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False

    def move(self, xpos, ypos):
        if self.isAlive == True:
            self.ypos-=10
        if self.ypos < 0:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
    
    def collide(self, xpos, ypos, BulletY, BulletX):

        if self.isAlive:
            if BulletX > self.xpos:
                if BulletX < self.xpos+40:
                    if BulletY < self.ypos:
                        if BulletY >self.ypos + 40:
                            print("hit!")
                            self.isAlive = False
                            return False
        return True
    
    
 
    def draw(self):
        pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))



bullet = Bullet(xpos+28, ypos)


class Alien:#---------------------------------------------------------------------------------------------------
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1

    def draw(self):
        if self.isAlive:
            pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))

    def move(self, timer):

        #moving down
        if timer % 200 == 0:
            self.ypos += 50
            self.direction *=-1
            return 0


        #moving right
        if timer%100==0:
            self.xpos +=50*self.direction
            #print("moving right")

       
            

        return timer

    def collide(self, BulletX, BulletY):

        if self.isAlive:
            if BulletX > self.xpos:
                if BulletX < self.xpos+40:
                    if BulletY < self.ypos +40:
                        if BulletY >self.ypos:
                            print("hit!")
                            self.isAlive = False
                            return False
        return True

armada = []
for i in range (4):
    for j in range(9):
        armada.append(Alien(j*80+65, i*80+50))

walls = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            walls.append(Wall(j*30+200*k+50, i*30+600))




while lives != 0: #gameloop #################################
    tick.tick(60)
    timer+=1

    #Input Section--------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Bye = True

        if event.type == pygame.KEYDOWN:#--------------------------
            if event.key == pygame.K_LEFT:
                moveLeft = True
                
            if event.key == pygame.K_RIGHT:
                moveRight = True

            if event.key == pygame.K_SPACE:
                shoot = True
    
        elif event.type == pygame.KEYUP:#-----------------------------
            if event.key == pygame.K_LEFT:
                moveLeft = False

     
            if event.key == pygame.K_RIGHT:
                moveRight = False

            if event.key == pygame.K_SPACE:
                shoot = False
    
        
            


    #physics section--------------------------------------------
    

    if moveLeft == True:
        vx =- 3
    
    elif moveRight == True:
        vx =+ 3
    else:
        vx = 0

    xpos += vx

    if shoot == True:
        bullet.isAlive = True

    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        

        for i in range (len(armada)):
            bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
            if bullet.isAlive == False:
                score += 50
                break
    else:

        bullet.xpos = xpos +28
        bullet.ypos = ypos

        #shoot walls
    if bullet.isAlive == True:

        for i in range (len(walls)):
            bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
            if bullet.isAlive == False:
                break

    for i in range(len(walls)):
        for j in range(len(missiles)):
            if missiles[j].isAlive == True:
                if walls[i].collide(missiles[j].xpos, missiles[j].ypos) == False:
                    missiles[j].isAlive = False
                    break

    for i in range (len(missiles)):
        missiles[i].move()

    for i in range(len(walls)):
        for j in range(len(missiles)):
            if missiles[j].isAlive == True:
                if walls[i].collide(missiles[j].xpos, missiles [j].ypos) == False:
                    missiles[j].isAlive = False
                    break

        
    rand = random.randrange(0, 100)
    if rand < 2:
        pick = random.randrange(len(armada))
        if armada[pick].isAlive == True:            
            for i in range(len(missiles)):
                if missiles[i].isAlive == False:
                    missiles[i].isAlive = True
                    missiles[i].xpos = armada[pick].xpos+5
                    missiles[i].ypos = armada[pick].ypos+5


    for i in range(len(missiles)):
        if missiles[i].isAlive:
            if missiles[i].xpos > xpos:
                if missiles[i].xpos < xpos + 40:
                   # print("within x")
                    if missiles[i].ypos+10 > ypos:#mo: I just fixed these two lines, signs and numbers were off
                        if missiles[i].ypos < ypos+20:
                            pygame.draw.circle(gamescreen, (255, 255, 0), (xpos, ypos), 30)
                            pygame.display.flip()
                            pygame.time.wait(50)

                            print("ship hit")
                            lives -=  1
                            xpos = 450
                            ypos = 750
                                  
    

    
    
    xpos += vx
    print(lives)
    #render section--------------------------------------------


    gamescreen.fill ((0,0,0))
    bullet.draw()
    missiles[i].draw()
    


    pygame.draw.rect(gamescreen, (0, 200, 0), (xpos, 750, 60, 20))
    pygame.draw.rect(gamescreen, (0, 200, 0), (xpos+5, 745, 50, 20))
    pygame.draw.rect(gamescreen, (0, 200, 0), (xpos+25, 735, 11, 10))
    pygame.draw.rect(gamescreen, (0, 200, 0), (xpos+28, 730, 5, 10))

    
    for i in range (len(walls)):
       walls[i].draw()
    

    for i in range (len(armada)):
        armada[i].draw()

    for i in range (len(armada)):
        timer = armada[i].move(timer)
    
    for i in range (len(missiles)):
        missiles[i].draw()
    
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES:', False, (255, 0, 0))

   
    
    gamescreen.blit(text_surface, (0,0))

    #my_font2 = pygame.font.SysFont('Comic Sans MS', 30)
    #text_surface = my_font.render('SCORE:', score, ' ' , False, (255, 0, 0))

   
    
    gamescreen.blit(text_surface, (600,0))
    
    pygame.display.flip()
#end game loop###################################
if lives <= 0:
    print("Game Over!")
    Bye = True
pygame.quit()
