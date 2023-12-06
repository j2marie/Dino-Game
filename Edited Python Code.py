# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

COIN = [ 
    pygame.image.load(os.path.join("assets/Coins", "coin_00.png")), # LB Added image of the coin
    pygame.image.load(os.path.join("assets/Coins", "coin_00.png")),  
]
COIN = pygame.transform.scale(COIN [0], (35,35))  # LB resized the coin to 35 x 35 

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

POWER = pygame.image.load(os.path.join("assets/Power", "power_star1.png")) #JS Added image of the purple star power-up
POWER1 = pygame.transform.scale(POWER, (80,65)) #JS resized the purple star to 60 x 45

LASER1 = pygame.image.load(os.path.join("assets/Power", "dino_laser.png")) #JS Added image of the laser
LASER2 = pygame.image.load(os.path.join("assets/Power", "dino_laser2.png")) #JS Added image of the laser
RLASER1 = pygame.transform.scale(LASER1, (300,200)) #JS resized the laser image to fit the scale of the game
RLASER2 = pygame.transform.scale(LASER1, (300,200)) #JS resized the laser image to fit the scale of the game
LASER = [RLASER1, RLASER2] #JS Made them into a list


BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

INVINCIBILITY = pygame.image.load("assets/Invincibility.png") # KL: load image of the invincibility star powerup
INVINCIBILITY = pygame.transform.scale(INVINCIBILITY, (40,40)) # KL: resize the image to be 40 X 40

FONT_COLOR=(0,0,0)


class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.laser_img = LASER #JS made variable for the laser

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_laser = False #JS added new initial start for power-up
        self.dino_collided = 0 #JS variable to set standard for dino in regular run

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_laser: #JS if the dino is in the state of dino_laser (it is equal to True)
            self.laser() #JS execute this function

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            self.dino_laser = False #JS Set it to False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.dino_laser = False #JS Set it to False
        elif userInput[pygame.K_RIGHT] and not self.dino_jump: #JS If the user presses the right arrow, do the following
            if self.dino_collided > 0: #JS If the dino_collided is above 0, do the following:
                self.dino_duck = False #JS Set dino_duck to False
                self.dino_run = False #JS Set dino_run to False
                self.dino_jump = False #JS Set dino_jump to False (so not to execute this function)
                self.dino_laser = True #JS Set dino_laser to True (will then allow the laser function to run)
                self.dino_collided -= 1 #JS Subtract the number set to dino_collided by 1. This is to allow the superpower to be available only for an amount of time
            else: #JS if it equal to 0 or below, do the following (the dino will run like normal with no superpower)
                self.dino_duck = False #JS Set dino_duck to False
                self.dino_run = True #JS Set dino_run to true
                self.dino_jump = False #JS Set dino_jump to False
                self.dino_laser = False #JS Set dino_laser to False
            
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            self.dino_laser = False
        

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
    
    def laser(self): #JS the laser function that will run when dino_laser is set to True
        self.image = self.laser_img[self.step_index // 5] #JS Choose the laser image
        self.dino_rect = self.image.get_rect() #JS Put a rectangular box around the image
        self.dino_rect.x = self.X_POS + 25 #JS Put an extra width of 25 around the dino
        self.dino_rect.y = self.Y_POS - 50 #JS set the y location of the dino
        self.step_index += 1 #JS add one to the step_index

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Invincibility: # KL: new class for the Invincibility powerup (star)
    def __init__(self, image):
        self.rect = pygame.Rect(40, 40, 40, 40) # KL: set the collision box to be a 40 x 40 square
        self.rect.x = SCREEN_WIDTH + random.randint(10000, 15000) # KL: draw the invincibility powerup at a random x location such that the powerup is relatively infrequent
        self.rect.y = 225 # KL: set the y location to be 255
        self.image = INVINCIBILITY # KL: get the corresponding image of the invincibility powerup
        self.width = self.image.get_width() # KL: get the hitbox of the image of the powerup

    def update(self): # KL: update the state of the powerup
        self.rect.x -= game_speed # KL: the x coord of the powerup moves to the left at a speed based on game_speed
        if self.rect.x < -self.width: # KL: if the power up moves completely off screen, do the following:
            invincible.pop() # KL: remove the power up

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y)) # KL: blit the powerup onto the screen 


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Power: #JS New class for powerup
    def __init__(self, image):
        self.image = POWER1 # JS Get image of POWER1
        self.rect = pygame.Rect(75, 75, 75, 75) #JS make a square 75x75
        self.rect.x = SCREEN_WIDTH + random.randint(9000,10000) #JS randomize how long the width is
        self.rect.y = 215 #JS keep at certain height
    def update(self):
        self.rect.x -= game_speed #JS subtract the width from the game_speed
        if self.rect.x < -self.rect.width: #JS if the width is smaller than the -width
            powers.pop() #JS make it disappear
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y)) #JS bring it to the surface

class Coin: # LB created a class for the coins 
    def __init__(self, image):
        self.image = COIN # LB set that the class coinis will use the image of the coin 
        self.rect = pygame.Rect(85,85,85,85) # LB made the rectange or hitbox around the coins 
        self.rect.x = SCREEN_WIDTH + random.randint(500, 900) # LB set how often a coin will spawn on the width of the screen 
        self.rect.y = 340 # LB set how high the coins will spawn on screen 
        for Obstacle in obstacles: # LB assigned it as an obstacles
            if self.rect.colliderect(Obstacle.rect): # LB Makes the coins collude with the dinasaur 
                self.rect.y = 200 # LB when the coin has been collided with move it far wnough down so thatit can not be seen 
    def update(self): 
        self.rect.x -= game_speed # LB the width of the coin will be moving eith the game speed 
        if self.rect.x < -self.rect.width: # LB if the coin sidth is smaller than the negative of the dinasaurs width
            coins.pop() # make is disapear 
        

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y)) # LB bring the coinn to the surface 

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, invincible, powers, coins, collected, reference, invincible_react #Made more global variables to work throughout the function
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    powers = [] #JS start at an empty list
    death_count = 0
    coins = [] #LB strated an empty list for coins 
    pause = False
    collected = 0 # LB creates a new variable for when the coins are collected 
    reference = 0
    invincible = [] # KL: create an empty list for the invicibility powerup
    invincible_react = 0 # KL: add new variable for when the player hits the invinciblity powerup 

    def Collected(): # LB defines the new variable collecteed
        global reference, collected, coins # LB shows what variables will be referenced in this definition and allows them to be used in this def
        collected += 1 # LB when collected is triggered plus one 
        reference -= 1 # LB when refence is triggered minus one 

    def Collected_Screen(): # LB defines what wil show on the scren when coins are collected 
        global collected # LB used the variable collected defined above 
        with open("collected.txt", "r") as f: # LB opens the index collected.txt 
            collected_ints = [int(x) for x in f.read().split()] # LB reads the contents of "collected.txt," splits them into a list of strings and the converts them into an integer
            text = font.render("Coins: " + str(collected), True, FONT_COLOR) # LB makes the message on the screen appear that shows how many coins have been collected 
        textRect = text.get_rect()
        textRect.center = (900, 70)
        SCREEN.blit(text, textRect) 

    def Invincible_update():
        global invincible_react
        if invincible_react > 0: # KL: if the player gets the invincibility power up, subtract one from invicible_react until it equals zero (acts as a timer)
            invincible_react -= 1

    def Invicibility_text():
        global invincible_react
        text = font.render("Invincibility: " + str(invincible_react//10), True, FONT_COLOR) # KL: write text to show how long the invibility powerup will last
        textRect = text.get_rect() # KL: get the dimensions of the text
        textRect.center = (900, 100) # KL: center the text
        SCREEN.blit(text, textRect) # KL: blit it onto the screen
        
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        if len(invincible) == 0:  # KL: if the length of the variable invincible is equal to 0, do the following
            invincible.append(Invincibility(INVINCIBILITY)) # KL: creates a new invincibility power up and adds it to the invincible list

        for i in invincible: # KL: for every object in the list invincible, do the following
            i.draw(SCREEN) # KL: draw the object onto the screen
            i.update() # KL: update the object
            if player.dino_rect.colliderect(i.rect): # KL: if the player collides with the powerup (object)
                invincible.pop() # KL: remove the powerup from the list
                invincible_react = 100 # KL: set the variable invicible_react to 100 (starts the timer)            

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_collided == 6: #JS If the variable is equal to 6 (happens when the right arrow is pressed)
                obstacles.pop() #JS Remove the obstacle infront of it
            if player.dino_rect.colliderect(obstacle.rect) and invincible_react == 0:
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
        
        if len(powers) == 0: #JS if the length of powers (the empty list) is equal to 0, then do the following
            powers.append(Power(POWER1)) #JS add in the power image
        for power in powers: #JS start a for loop for the power image in the list
            power.draw(SCREEN) #JS draw the power image
            power.update() #JS update it
            if player.dino_rect.colliderect(power.rect): #JS if the dino collides with the rectangular area of the power, do the following
                powers.pop() #JS make the power image disappear
                player.dino_collided = 7 #JS make the variable dino_collided to 7, so that it can start the function of the dino using the laser
        
        if len(coins) == 0: # LB  if the length of coins is equal to 0
            coins.append(Coin(COIN)) # LB load the coin image 
        for c in coins: # LB start a loop for the coin image in the list 
            c.draw(SCREEN) # LB draw the image of the coin 
            c.update() # LB update the image 
            if player.dino_rect.colliderect(c.rect): # LB if the dino collides with the coin 
                coins.pop() # LB make the coin disapear 
                reference = 1 # LB make the variable dino_collided to 1 to start the function of the coins disapearing
        
    
        if reference > 0:
            Collected()
        
                
        background()

        cloud.draw(SCREEN)
        cloud.update()

        Invincible_update() #KL: update the invincibility powerup 

        if invincible_react > 0: #KL: only display the timer for the invincibility powerup while it is active
            Invicibility_text()

        Collected_Screen() # LB Displays the amount of coins collected on the screen 
        
        score() 

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, collected
    global FONT_COLOR
    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            amount = font.render("Coins Collected: "+ str(collected), True, FONT_COLOR)
            amountRect = amount.get_rect()
            amountRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(amount, amountRect)
            f = open("collected.txt", "a")
            f.write(str(collected) + "\n")
            f.close()
            with open("collected.txt", "r") as f:
                amount = (
                    f.read())
                collected_ints = [int(x) for x in amount.split()]
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
