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

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

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

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

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

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

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
            self.jump_vel = self.JUMP_VEL #End Of LExis Part

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

#Katie Leung's Part:

class Cloud: # creates a class for the clouds that move in the background
    def __init__(self): # initalizes an object and is called upon the creation of an object in the class this function will run with "self" as a variable the represents the instance of the object???
        self.x = SCREEN_WIDTH + random.randint(800, 1000) # sets the starting x position of the cloud will appear + a random number between 800 and 1000 from the right
        self.y = random.randint(50, 100) # sets the starting y position of the cloud, is randomized within the bounds of 50 and 100 (from the top, (0,0) is the top left corner)
        self.image = CLOUD  # makes the corresponding image of the cloud
        self.width = self.image.get_width() # gets the pixel dimensions/hitbox (width and height) of the cloud image

    def update(self): #creates a function to update the clouds
        self.x -= game_speed # moves the cloud to the left at a rate based on the game speed
        if self.x < -self.width: # once the cloud moves completely offscreen, create a new cloud 
            self.x = SCREEN_WIDTH + random.randint(2500, 3000) # set the x value to be the screen width plus a random integer between 2500 and 3000, FARTHER OUT THIS TIME
            self.y = random.randint(50, 100) # set the y value to be a random integer between 50 and 100 (inclusive)

    def draw(self, SCREEN): # create a function to draw the clouds onto the screen
        SCREEN.blit(self.image, (self.x, self.y)) # blits the image of the clouds at the coordinates of (self.x, self.y) onto the screen


class Obstacle: # create a class named "Obstacle" for the cactus and birds that the player must avoid???
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


def main(): #define our main function where the functions and classes defined above will be called
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles #creates a bunch of global variables
    run = True # sets run equal to true, while the variable is true, the game runs
    clock = pygame.time.Clock() # creates an object to track the time
    player = Dinosaur() # creates an instance of the class Dinosaur()
    cloud = Cloud() # creates an instance of the class Cloud()
    game_speed = 20 # sets the inital game speed to be 20 (the background, clouds, and obstacles are dependent on the game speed)
    x_pos_bg = 0 # sets the x coordinate of the background to be 0 (leftmost side)
    y_pos_bg = 380 # sets the y coordinate of the background to be 380, the height at which the dinosaur will be running on
    points = 0 # sets the inital value of points to be 0
    font = pygame.font.Font("freesansbold.ttf", 20) #define the font to be "freesansbold.ttf" at size 20
    obstacles = [] #creates an empty list for the obstacles
    death_count = 0 # sets the death counter to start at 0
    pause = False #set pause equal to false (since the game is running)

    def score(): # create a function named score()
        global points, game_speed # add the global variables "points" and "game_speed"
        points += 1 # every time the score function is called, increase the number of points the player had by 1
        if points % 100 == 0: # every 100 points, the game speed increases by 1, increasing the difficulty of the game
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR) # display the text of the player's high score and points on the screen in the font colour, black
        textRect = text.get_rect() # get the coords of the rectangle in which the highscore and points are displayed
        textRect.center = (900, 40) # set the centre of the text to the top right corner of the screen
        SCREEN.blit(text, textRect) # blit the highscore and points onto the screen

    def background():
        global x_pos_bg, y_pos_bg # get the global x and y coordinates of the background
        image_width = BG.get_width() # get the dimensions of the background image
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # blit the background image onto the screen at the global x and y coordinates
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # blit another background image onto the screen with a different x position
        if x_pos_bg <= -image_width: # if the background image moves fully off the screen, a new background image is created to replace it
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # blit the replacement background image onto the screen
            x_pos_bg = 0 # set the x position of the background to be 0 WHY???
        x_pos_bg -= game_speed # move the background image to the left based on the game speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True 
    #Joy-Marie Salama's Part Starts

    def paused():
        nonlocal pause #Refers to the variable 'pause' outside of the function. 
        pause = True #Changes the original value of pause (False) to True
        font = pygame.font.Font("freesansbold.ttf", 30) #Creates a new Font by grabbing it from the file 'freesansbold.ttf'. Makes the font size 30.
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR) #Creates an image of the font (Game Paused, Press 'u' to Unpause), that will then be blit to the Screen.
        textRect = text.get_rect() #Return specified rectangular area of the text *but not area is given?
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3) #Centres the image of the to width (width of screen divided by 2) and height (height of screen divided by 3).
        SCREEN.blit(text, textRect) #Copies the text from one surface to the other surface (on the screen).
        pygame.display.update() #Update the window

        while pause: #starts while loop for variable 'pause'
            for event in pygame.event.get(): #For a variable in the queue of events do the following functions.
                if event.type == pygame.QUIT: #If the type of the variable event is equal to type pygame.QUIT do the following functions.
                    pygame.quit() #End the application.
                    quit() #Exit the game.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u: #if the type of the variable event is equal to pressing down and if the user presses u do the following.
                    unpause() #Unpause the game - go to the function unpause

    while run: #starts while loop for the function run
        for event in pygame.event.get(): #For a variable in the queue of events do the following functions.
            if event.type == pygame.QUIT: #If the type of the variable event is equal to pygame.Quit do the following functions.
                run = False #Change run to False (stop the character from running)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #If the type of the variable event is equal to pressing down and if the user presses p do the following.
                run = False #Changes run to False (stop the character from running)
                paused() #Pause the game - go to the function pause

        current_time = datetime.datetime.now().hour #sets the time to the current hour
        if 7 < current_time < 19: #if the time is between 7 to 19, then do the following:
            SCREEN.fill((255, 255, 255)) #Change the screen to the colour white
        else: #if the time is not between 7 to 19, then do the following:
            SCREEN.fill((0, 0, 0)) #Change the screen to the colour black
        userInput = pygame.key.get_pressed() #Returns the state of the key to 1 if it gets pressed, or else it will stay 0

        player.draw(SCREEN) #Draws the dinosaur ontop of the new screen???
        player.update(userInput) #Check what the user input is, and it will update the player's actions because of it.

        if len(obstacles) == 0: #if the length of the variable obstacles is equal to 0, do the following:
            if random.randint(0, 2) == 0: #If the random integerbetween 0 to 2 is equal to 0, do the following:
                obstacles.append(SmallCactus(SMALL_CACTUS)) #Input a small cactus as an obstacle
            elif random.randint(0, 2) == 1: #If the statement above is not fulfilled and if the randon integer between 0 to 2 is equal to 1, do the following:
                obstacles.append(LargeCactus(LARGE_CACTUS)) #Input a large cactus as an obstacle
            elif random.randint(0, 2) == 2: #If the statements above are not fulfilled and if the random integer between 0 to 2 is equal to 2, do the following:
                obstacles.append(Bird(BIRD)) #Inupt a bird as an obstacle

        for obstacle in obstacles: #A for loop for the variable obstacles
            obstacle.draw(SCREEN)  #Draws the new obstacle ontop of the new screen ???
            obstacle.update() #Checks what the obstacle is, and updates the obstacle shown ???
            if player.dino_rect.colliderect(obstacle.rect): # If the dinosaur collides with the obstacles, do the following:
                pygame.time.delay(2000) #Pause the game for 2 seconds
                death_count += 1 #Increase the death count by 1
                menu(death_count) # Create a menu with the number of death counts ??? - I don't know what this does ????

        background() #For the function background

        cloud.draw(SCREEN) #Draw the cloud image onto the screen
        cloud.update() #update the cloud

        score()  #For the function score

        clock.tick(30) #Tells the game to run no more than 30 frames per second.
        pygame.display.update() #update the display


def menu(death_count): #Defines a function 'menu' with the variable death_count
    global points #Look for the variable 'points' from the whole code
    global FONT_COLOR #Look for the variable 'Font_color' from the whole code
    run = True #Change run to True
    while run: #Start while loop for variable run
        current_time = datetime.datetime.now().hour #Set the variable 'current_time' to the current tmie in real life
        if 7 < current_time < 19: #if the current time is between 7 to 19, do the following:
            FONT_COLOR=(0,0,0) #Change the font colour to black
            SCREEN.fill((255, 255, 255)) #The screen will be white
        else: #or else (not between 7 to 19)
            FONT_COLOR=(255,255,255) #Change the font colour to white
            SCREEN.fill((128, 128, 128)) #Change the background to grey
        font = pygame.font.Font("freesansbold.ttf", 30) #Make the font of the game size 30 in freesansbold font

        if death_count == 0: #if the death count is equal to 0, do the following:
            text = font.render("Press any Key to Start", True, FONT_COLOR) #Create an image of the font (Press any Key to Start) in the Font described above
        elif death_count > 0: #if the death count is greater than 0, do the following:
            text = font.render("Press any Key to Restart", True, FONT_COLOR) #Create an image of the font (Press any Key to Restart) in the Font described above
            score = font.render("Your Score: " + str(points), True, FONT_COLOR) #Create an image of the words  - Your score - with the string of the points calculated from the game
            scoreRect = score.get_rect() #Returns the image of the rectangle (but no area given???)
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 #Centre the rectangle by the width of the screen divided by 2 and the height of the screen divided by 2 and add 50.
            SCREEN.blit(score, scoreRect) #Copies the score and the rectange onto the screen
            f = open("score.txt", "a") #Open and create the file score.text and return it as a file object
            f.write(str(points) + "\n") #Write the points (as a string) into the file and put in new line after it
            f.close() # Close the file score.txt
            with open("score.txt", "r") as f: #Opens the file score.txt to read it, and after this function is finished, it automatically closes the file.
                score = (
                    f.read()
                )  # Read all file in case values are not on a single line and returns it as a strin
                score_ints = [int(x) for x in score.split()]  # Convert strings to ints
            highscore = max(score_ints)  # sum all elements of the list. Find the highest value in score_ints.
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            ) #Create an image of the text: High Score :, with the string of the integer number from the variable highscore.
            hs_score_rect = hs_score_text.get_rect() #Put the text into a rectangle. 
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100) #Centre the rectangle with the width half the screen width and the height half the screen height + 100.
            SCREEN.blit(hs_score_text, hs_score_rect) #Bring the hs_score_text and hs_score_rect to the Screen.
        textRect = text.get_rect() #create a rectangle for the text
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) #Centre the rectangle with width half the screen width and height half the screen height.
        SCREEN.blit(text, textRect) #Bring the text and textRect to the Screen.
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140)) #Bring the running image (index 0) with width half screen width - 20 and height half screen height - 150 to the Screen ???
        pygame.display.update() #update the Screen
        for event in pygame.event.get(): #For a variable in the queue of events do the following functions.
            if event.type == pygame.QUIT: #if the type of the event is equal to pygame.Quit, then do the following function.
                run = False #Change the value run to False (stop the character from running)
                pygame.display.quit() #Exit the display
                pygame.quit() #exit the game
                exit() #Do the function exit
            if event.type == pygame.KEYDOWN: #if the type of the event is equal to pressing the down key, then do the following function.
                main() #Return to main


t1 = threading.Thread(target=menu(death_count=0), daemon=True) #Return the death count to 0, allow the program to exit
t1.start() #Start the thread
#Parts: 0-123, 123-236, 236-354
