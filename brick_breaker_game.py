import pygame
import sys
import random, math
import init_variables as ivar
import game_board_elements as gbe 

game = ivar.InVar()

class GameStage():
    def __init__(self):
        self.last_level = 3
        self.level_nb = 0

    def counting(self):
        pygame.mouse.set_visible(False) 

        ball = gbe.Ball("PNG/ball.png")
        ball_group.add(ball)

        extra_balls_group.empty()
        fast_ball_group.empty()
        ball_container_group.empty()
        brick_group.empty()
        
        bar.rect.x , bar.rect.y = 260, 430

        count_lev_1 = ["PNG/count_lev1_3.png", "PNG/count_lev1_2.png","PNG/count_lev1_1.png"] 
        count_lev_2 = ["PNG/count_lev2_3.png", "PNG/count_lev2_2.png","PNG/count_lev2_1.png"]
        count_lev_3 = ["PNG/count_lev3_3.png", "PNG/count_lev3_2.png","PNG/count_lev3_1.png"]

        if self.level_nb == 0: self.count_lev = count_lev_1
        if self.level_nb == 1: self.count_lev = count_lev_2
        if self.level_nb == 2: self.count_lev = count_lev_3  
        for i in range(3):
            self.image = pygame.image.load(self.count_lev[i]).convert_alpha()
            self.image.get_rect()
            win.blit(self.image, (0, 0))
            text_score = "SCORE: " + str(game.score)
            text_surface = game_font.render(text_score,False,(0, 255,0))
            pygame.time.wait(1000)
            win.blit(text_surface, (30,465)) 

            pygame.display.flip()      
            if i == 2:
                pygame.time.wait(1000)
                if self.level_nb == 0:
                    game.level = "level_1"
                    brick_wall = gbe.BrickWall()
                    brick_wall.brickwall_lev1(brick_group)

                if self.level_nb == 1:
                    game.level = "level_2"
                    brick_wall = gbe.BrickWall()
                    brick_wall.brickwall_lev2(brick_group)
                    extra_balls_group.empty()
                    fast_ball_group.empty()
                    ball.speed = 2
                    ball.image = pygame.image.load("PNG/ball.png").convert_alpha()

                if self.level_nb == 2:
                    game.level = "level_3"
                    brick_wall = gbe.BrickWall()
                    brick_wall.brickwall_lev3(brick_group)
                    extra_balls_group.empty()
                    fast_ball_group.empty()
                    ball.speed = 2
                    ball.image = pygame.image.load("PNG/ball.png").convert_alpha()

                if self.level_nb == 3:
                    game.level = "new_game"

    def start(self):
        pygame.mouse.set_visible(True) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.MOUSEBUTTONDOWN , pygame.KEYDOWN]:
                game.level = "counting"
        win.blit(start_bg,(0,0))
        start_btn_group.draw(win)
        pygame.display.flip()

    def level(self):
        global counter, level, brick_group
        pygame.mouse.set_visible(False) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if len(brick_group)== 0:
                pygame.time.wait(1000)
                if game.level == "level_3":
                    self.level_nb = 0
                    game.level = "new_game"
                else:
                    self.level_nb += 1
                    game.counter = 3
                    game.level = "counting"
        if game.counter == 0:
            pygame.time.wait(1000)
            game.level = "new_game"
            self.level_nb = 0

        win.blit(background,(0,0))

        rand_extra = random.randrange(500)
        if rand_extra == 1:
            ball_container = gbe.BallContainer()
            ball_container_group.add(ball_container)
    
        if game.level == "level_1": level_range = 1000
        else: level_range = 400
        rand_fast = random.randrange(level_range)
        if rand_fast == 1:
            fast_ball = gbe.FastBall()
            fast_ball_group.add(fast_ball)

        bar_group.draw(win)
        bar_group.update()
        bar.bar_image(game.counter)

        ball_group.draw(win)
        for sprite in ball_group:
            sprite.collision(ball_group, brick_group, bar_group)
            game.score += sprite.collid_points
            sprite.collid_points = 0
            sprite.movement(ball_group)
            if sprite.fall == True:
                game.counter -= 1
                sprite.fall = False

        extra_balls_group.draw(win)
        for sprite in extra_balls_group:
            sprite.collision(extra_balls_group, brick_group, bar_group)
            game.score += sprite.collid_points
            sprite.collid_points = 0
            sprite.movement(extra_balls_group)

        ball_container_group.draw(win)
        for sprite in ball_container_group:
            sprite.movement(ball_container_group)
            sprite.catch(ball_container_group, bar_group, extra_balls_group)

        fast_ball_group.draw(win)
        for sprite in fast_ball_group:
            sprite.catch(fast_ball_group, bar_group, ball_group)
            sprite.movement(fast_ball_group)

        brick_group.draw(win)
        brick_group.update() 

        text_score = "SCORE: " + str(game.score)
        text_surface = game_font.render(text_score, False,(0, 255,0))
        win.blit(text_surface, (30,465))

        pygame.display.flip()

    def new_game(self):
        pygame.mouse.set_visible(True) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()
                if event.key in [ pygame.K_RETURN, pygame.K_KP_ENTER]:
                    game.level = "counting"
                    game.counter = 3
                    game.score = 0
                    self.level_nb = 0 
            if newgame_btn.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                game.level = "counting"
                game.counter = 3
                game.score = 0
                self.level_nb = 0 
            if exit_btn.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

        win.blit(game_over_bg,(0,0))

        text_score = "SCORE: " + str(game.score)
        text_surface = game_font.render(text_score,False,(0, 255,0))
        win.blit(text_surface, (250,150))
        
        newgame_btn_group.draw(win)
        exit_btn_group.draw(win)

        pygame.display.flip()

    def set_game_level(self):
        if game.level == "start":
           self.start()
        elif game.level == "counting":
           self.counting()
        elif game.level in ["level_1", "level_2", "level_3"]:
           self.level()
        elif game.level == "new_game":
           self.new_game()


#-------START------------

pygame.init()

clock = pygame.time.Clock()

win_width = 630
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Brick Breaker')
icon = pygame.image.load('PNG/icon.png')
pygame.display.set_icon(icon)

game_font = pygame.font.Font('PNG/squaredance10.ttf',24)

start_bg = pygame.image.load("PNG/start.png").convert_alpha()
background = pygame.image.load("PNG/tlo.png").convert_alpha()
game_over_bg = pygame.image.load("PNG/game_over.png").convert_alpha()

start_btn = gbe.Button("PNG/start_button.png",(310,300))
start_btn_group = pygame.sprite.GroupSingle()
start_btn_group.add(start_btn)

newgame_btn = gbe.Button("PNG/new_game_button.png", (300, 350))
newgame_btn_group = pygame.sprite.GroupSingle()
newgame_btn_group.add(newgame_btn)

exit_btn = gbe.Button("PNG/exit_button.png", (300, 420))
exit_btn_group = pygame.sprite.GroupSingle()
exit_btn_group.add(exit_btn)

ball = gbe.Ball("PNG/ball.png")
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

ball_container_group = pygame.sprite.Group()
extra_balls_group = pygame.sprite.Group()
fast_ball_group = pygame.sprite.Group()

brick_group = pygame.sprite.Group()
brick_wall = gbe.BrickWall()
brick_wall.brickwall_lev1(brick_group)

bar = gbe.Bar()
bar_group = pygame.sprite.GroupSingle()
bar_group.add(bar)

game_stage = GameStage()

while True:
    game_stage.set_game_level()
    clock.tick(60)
