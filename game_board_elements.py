import pygame
import sys
import random, math



class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos)


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 300
        self.y = 450
       
        bar_3_balls = pygame.image.load("PNG/bar3.png").convert_alpha()
        bar_2_balls = pygame.image.load("PNG/bar2.png").convert_alpha()
        bar_1_ball = pygame.image.load("PNG/bar1.png").convert_alpha()
        bar_0_ball = pygame.image.load("PNG/bar0.png").convert_alpha()

        self.balls_nb = [bar_3_balls, bar_2_balls, bar_1_ball, bar_0_ball]
        self.image = pygame.image.load("PNG/bar3.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x,self.y))

    def bar_image(self, counter):
        if counter == 3: self.image = self.balls_nb[0]
        if counter == 2: self.image = self.balls_nb[1]
        if counter == 1: self.image = self.balls_nb[2]
        if counter == 0:
            self.image = self.balls_nb[3]
            self.rect = self.image.get_rect(midbottom = (self.x,self.y))

    def movement(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.right < 620:
            self.rect.x += 10
        elif pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.left >10:
            self.rect.x -= 10   

    def update(self):
        self.movement()
        #self.bar_image()


class Brick(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, points, hardness = 0):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.points = points
        self.hardness = hardness

    def cracked(self):
       self.hardness = 0
       self.image = pygame.image.load("PNG/brick_cracked3.png").convert_alpha()


class BrickWall():
    def __init__(self):
        pass
        
    def brick_line(self,brickgroup, brick_file, brick_nb, col, row, points, hard):
        global brick_group
        i = 0
        brick_width = 51
        for brick in range(brick_nb):
            new_brick = Brick(brick_file, col+i, row, points)
            new_brick.hardness = hard 
            i= i+ brick_width
            brickgroup.add(new_brick)

    def brickwall_lev1(self, brickgroup):
        global brick_group
        brick_colors = ["PNG/brick_red.png","PNG/brick_blue.png","PNG/brick_yellow.png"]                  
        nb_of_bricks = [ 12 , 11, 12]
        first_brick_x = [ 10 , 35, 10]
        points = 30
        brick_height = 8
        for color, number, x in zip(brick_colors, nb_of_bricks, first_brick_x):
            self.brick_line(brickgroup, color, number, x, brick_height, points, 0)
            brick_height += 26
            points -= 10

    def brickwall_lev2(self, brickgroup):
        global brick_group
        brick_colors = ["PNG/brick_red.png","PNG/brick_green.png","PNG/brick_blue.png",
                        "PNG/brick_yellow.png", "PNG/brick_purple.png"]
        nb_of_bricks = [ 12, 11 , 12, 11, 12]
        first_brick_x = [ 10, 35, 10, 35, 10]
        points = 50
        brick_height = 8
        for color, number, x in zip(brick_colors, nb_of_bricks, first_brick_x):
            self.brick_line(brickgroup, color, number, x, brick_height, points, 0)
            brick_height += 26
            points -= 10

    def brickwall_lev3(self, brickgroup):
        global brick_group
        brick_colors = ["PNG/brick_yellow.png", "PNG/brick.png", "PNG/brick_red.png","PNG/brick_green.png","PNG/brick.png"]
        nb_of_bricks = [ 12, 11 , 12, 11, 12]
        first_brick_x = [10, 35, 10, 35, 10]
        hard = [0, 1, 0, 0 ,1]
        points = 50
        brick_height = 8
        for color, number, x, hard in zip(brick_colors, nb_of_bricks, first_brick_x, hard):
            self.brick_line(brickgroup, color, number, x, brick_height, points, hard)
            brick_height += 26
            points -= 10


class FastBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.uniform(40, 590)
        self.y = 50
        self.image = pygame.image.load("PNG/fast_container.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.speed = 2

    def catch(self, fastgroup, bargroup, ballgroup):
       tollerance = self.speed +5
       self.collide_fast_bar = pygame.sprite.groupcollide(fastgroup, bargroup, True, False)
       if len(self.collide_fast_bar) > 0:
           for sprite in ballgroup:
               sprite.speed += 2 
               sprite.image = pygame.image.load("PNG/fireball.png").convert_alpha()
 
    def movement(self, fastgroup):
        self.rect.y += self.speed
        if self.rect.bottom >= 495:
            pygame.sprite.Sprite.remove(self, fastgroup) 

##    def update(self):
##        self.catch(fastgroup)
##        self.movement(fastgroup)



class Ball(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.x = 300
        self.y = 350
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.angles= [-0.7,-0.5,-0.3, 0.3, 0.5, 0.7]
        self.angle = random.choice(self.angles)
        self.speed = 2
        self.collid_points = 0
        self.fall = False

    def collision(self, ballgroup, brickgroup, bargroup):
        tollerance = self.speed +5
        self.collide_brick = pygame.sprite.groupcollide(ballgroup, brickgroup, False, False)
        if len(self.collide_brick) > 0:
            for sprite in self.collide_brick:
                self.collid_points = self.collide_brick[sprite][0].points
                if abs(self.rect.top - self.collide_brick[sprite][0].rect.bottom) < tollerance:
                    self.rect.top = self.collide_brick[sprite][0].rect.bottom
                    self.angle = math.pi - self.angle
                if abs(self.rect.bottom - self.collide_brick[sprite][0].rect.top) < tollerance:
                    self.rect.bottom = self.collide_brick[sprite][0].rect.top
                    self.angle = math.pi - self.angle
                if abs(self.rect.right - self.collide_brick[sprite][0].rect.left) < tollerance:
                    self.rect.right = self.collide_brick[sprite][0].rect.left
                    self.angle = 2*math.pi - self.angle
                if abs(self.rect.left - self.collide_brick[sprite][0].rect.right) < tollerance:
                    self.rect.left = self.collide_brick[sprite][0].rect.right
                    self.angle = 2*math.pi - self.angle
                if self.collide_brick[sprite][0].hardness == 1:
                   self.collide_brick[sprite][0].cracked()
                else:
                    brickgroup.remove(self.collide_brick[sprite][0])

        self.collide_bar = pygame.sprite.groupcollide(ballgroup, bargroup, False, False)
        if len(self.collide_bar) > 0:
            for sprite in self.collide_bar:
                if abs(self.rect.bottom - self.collide_bar[sprite][0].rect.top) < tollerance:
                    sprite.rect.bottom = self.collide_bar[sprite][0].rect.top
                    sprite.angle = math.pi - self.angle
        self.rect.x += self.speed * math.sin(self.angle)
        self.rect.y -= self.speed * math.cos(self.angle)

    def movement(self, ballgroup):
      if self.rect.left <= 6 or self.rect.right >= 595: 
            self.angle = 2*math.pi - self.angle
      if self.rect.top <= 6: self.angle = math.pi - self.angle
      if self.rect.bottom >= 495:
            pygame.time.delay(300)
            self.fall = True
            for sprite in ballgroup:
               sprite.speed = 2 
               sprite.image = pygame.image.load("PNG/ball.png").convert_alpha()
        
            self.rect.midbottom = (self.x,self.y)
            self.angle = random.choice(self.angles)
      self.rect.x += self.speed * math.sin(self.angle)
      self.rect.y -= self.speed * math.cos(self.angle)

##    def update(self):
##        self.movement()
##        self.collision()



class ExtraBall(Ball): 
    def __init__(self, picture_path, x, y):
        super().__init__(picture_path) 
        self.rect.x = x
        self.rect.y = y
        self.angles= [-0.6,-0.5,-0.3, -0.2, 0.2,0.3, 0.4, 0.5, 0.6]
        self.angle = random.choice(self.angles)

    def movement(self,  extragroup):
          if self.rect.left <= 6 or self.rect.right >= 595: 
                self.angle = 2*math.pi - self.angle
          if self.rect.top <= 6: self.angle = math.pi - self.angle
          if self.rect.bottom >= 495:
             pygame.sprite.Sprite.remove(self, extragroup)

          self.rect.x += self.speed * math.sin(self.angle)
          self.rect.y -= self.speed * math.cos(self.angle)
##    def update(self):
##        self.movement()
##        self.collision(extragroup)
##        self.fall(extragroup)



class BallContainer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.uniform(40, 590)
        self.y = 50
        self.image = pygame.image.load("PNG/ball_container.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.speed = 2
        
    def movement(self, ballcontainergroup):
        self.rect.y += self.speed
        if self.rect.bottom >= 495:
            pygame.sprite.Sprite.remove(self, ballcontainergroup) 

    def catch(self, ballcontainergroup, bagroup, extragroup):
       tollerance = self.speed +5
       self.collide_bar = pygame.sprite.groupcollide(ballcontainergroup, bagroup, True, False)
       if len(self.collide_bar) > 0:
            for i in self.collide_bar:
                if abs(self.rect.bottom - self.collide_bar[i][0].rect.top) < tollerance:
                    for _ in range(3):
                        self.extra_ball = ExtraBall("PNG/ball_extra.png", self.rect.x, self.rect.y)
                        extragroup.add(self.extra_ball) 
##    def update(self):
##        self.movement()
##        self.catch()


        
