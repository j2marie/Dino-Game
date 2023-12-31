# Group: Lexi Baatje, Katie Leung (KL), Joy Marie Salama

# !/usr/bin/python
# -*- coding: utf-8 -*-
#Lexi Baatje's Part Starts
import datetime #imports date time from computer
import os #lets the file interact with the underlying operating system
import random #makes it so that things can be spawned at random 
import threading #this finction allows multiple threads of execution to take place

import pygame #this imports pygame the module that mkaes this a video game 

pygame.init() #initializes all imported pygame modules

# Global Constants

SCREEN_HEIGHT = 600 #creates a variable of screen height and sets it to the value they want 
SCREEN_WIDTH = 1100 #creates a variable of screen height and sets it to the value they want 
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #takes the two values of screen height adn screen width and sets them as the screen hight and width 

pygame.display.set_caption("Chrome Dino Runner") #shows the words on the start screen

Ico = pygame.image.load("assets/DinoWallpaper.png") # sets Ico to load the wallpaper for the dino game 
pygame.display.set_icon(Ico) #displays Ico or the background of the dino game 

RUNNING = [ #creates a list of the images included under this catagory 
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")), #goes into the assets folder and then the dino folder and loads the first DinoRun image
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")), #goes into the assets folder and then the dino folder and loads the second DinoRun image
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [ #creates a list of the images included under this catagory
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")), #goes into the assets folder and then the dino folder and loads the first DinoDuck image
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")), #goes into the assets folder and then the dino folder and loads the second DinoDuck image
]

SMALL_CACTUS = [ #creates a list of the images included under this catagory
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")), #goes into the assets folder and then the cactus folder and loads the first SmallCactus image
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")), #goes into the assets folder and then the cactus folder and loads the second SmallCactus image
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")), #goes into the assets folder and then the cactus folder and loads the third SmallCactus image
]
LARGE_CACTUS = [ #creates a list of the images included under this catagory
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")), #goes into the assets folder and then the cactus folder and loads the first LargeCactus image
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")), #goes into the assets folder and then the cactus folder and loads the second LargeCactus image
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")), #goes into the assets folder and then the cactus folder and loads the third LargeCactus image
]

BIRD = [ # creates a list of the images under this catagory 
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")), #goes into the assets folder and then the bird folder and loads the first Bird image
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")), #goes into the assets folder and then the bird folder and loads the second Bird image
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png")) #goes into the assets folder and then the Other folder and loads the Cloud image

BG = pygame.image.load(os.path.join("assets/Other", "Track.png")) #goes into the assets folder and then the Other folder and loads the Track image to be the ground 

FONT_COLOR=(0,0,0) #sets the font colour

class Dinosaur: # makes a class for the dinasaur where how it moves and works will be defined 

    X_POS = 80 # width of the dinasaur is set to 80 
    Y_POS = 310 # height of dinasaur is set to 310
    Y_POS_DUCK = 340 # height of the dinasaur when ducking set to 340 (the higher the number the lower the height)  
    JUMP_VEL = 8.5 # the height of the jump 

    def __init__(self): # initalizes an object and is called upon the creation of an object in the class this function will run with "self" as a variable the represents the instance of the object
        self.duck_img = DUCKING # uses the image defined earlier for the dino ducking 
        self.run_img = RUNNING  # uses the image defined earlier for the dino running
        self.jump_img = JUMPING  # uses the image defined earlier for the dino jumping 

        self.dino_duck = False # says that dino duck will not be going at all times
        self.dino_run = True # says that dino run will be going at all times
        self.dino_jump = False # says that dino jump will not be going at all times

        self.step_index = 0 # sets the variable self.step_index to zero as this variable will be used in the def of self, run and jump and represents that the game is in the first phase
        self.jump_vel = self.JUMP_VEL # sets this variable as the height of the jump defined above 
        self.image = self.run_img[0] # uses the dinp run list of images and toggles between them 
        self.dino_rect = self.image.get_rect() # this makes a rectagnles around the dinosaur image that is its hit box 
        self.dino_rect.x = self.X_POS # sets this variable as the width of the dino defined above
        self.dino_rect.y = self.Y_POS # sets this variable as the height of the dino defined above

    def update(self, userInput): # creates a function to update the dino 
        if self.dino_duck: # if the user uses the duck command (the dino duck is set to true)
            self.duck() # make the dinosaur duck 
        if self.dino_run: # while dino run is set as true 
            self.run() # make the dino run foward
        if self.dino_jump: # if the user uses the jump command (the dino jump is set to true)
            self.jump() # make the dino jump 

        if self.step_index >= 10: # is the phase of the game is less than of equal to zero 
            self.step_index = 0 # set it back to zero 

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump: # If the user uses the space bar or the up arrow
            self.dino_duck = False # set dino duck to false meaning the dino does not duck 
            self.dino_run = False # set dino run to false meaning the dino is not running 
            self.dino_jump = True # set dino jump to true menaing the dino will jump when the space of up arrow key is pressed 
        elif userInput[pygame.K_DOWN] and not self.dino_jump: # If user presses the down arrow while playing 
            self.dino_duck = True # set dino duck to true meaning that when the down arrow is pressed the dino will duck 
            self.dino_run = False # set dino run to false 
            self.dino_jump = False # set dino jump to false 
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # if no button is pressed 
            self.dino_duck = False # keep the dino duck at false 
            self.dino_run = True # keep the dino run at true meaning it will not stop running unless the space bar, up arrow or down arrow are pressed
            self.dino_jump = False # keep the dino jump false

    def duck(self): # defining what happens when the dinosaur ducks 
        self.image = self.duck_img[self.step_index // 5] # selects the dino ducking image when the dino is ducking 
        self.dino_rect = self.image.get_rect() # sets the rectangle around the dinosaur to a different one so that the dino is able to go below some obstacles 
        self.dino_rect.x = self.X_POS # the width of the dino stays the same  
        self.dino_rect.y = self.Y_POS_DUCK # the height of the dino while ducking is set to the vaiable defined above
        self.step_index += 1 # increasing the step index for the next frame of the ducking animation

    def run(self): # defining what happens when the dinosaur runs 
        self.image = self.run_img[self.step_index // 5] # selects the dino run images while dino is running 
        self.dino_rect = self.image.get_rect() # sets the rectangle around the dinosaur 
        self.dino_rect.x = self.X_POS # the width and height of the dino stay the same 
        self.dino_rect.y = self.Y_POS
        self.step_index += 1 # increasing the step index for the next frame of the ducking animation

    def jump(self):  # defining what happens when the dinosaur jumps
        self.image = self.jump_img # selects the dino jump image while dino is jumping 
        if self.dino_jump: # is the dino jumps 
            self.dino_rect.y -= self.jump_vel * 4 # the height of the dino minus the jump velocity 
            self.jump_vel -= 0.8 # the jump velocity minus 0.8 
        if self.jump_vel < -self.JUMP_VEL: # if the jump velocity is smaller than the JUMP_VEL
            self.dino_jump = False # then dino will not jump 
            self.jump_vel = self.JUMP_VEL # and the jump velocity and JUMP_VEL will be set equal 

    def draw(self, SCREEN): # create a function to draw the player onto the screen
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) # blit the image of the player onto the screen at the coordinates (self.dino_rect.x, self.dino_rect.y)

#Katie Leung's Part:

class Cloud: # creates a class for the clouds that move in the background
    def __init__(self): # initalizes the attribute of a class when an object is created with that class 
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

class Obstacle: # create a class named "Obstacle" for the cacti and birds that the player must avoid
    def __init__(self, image, type): # create a intializing function with self, image, and type as its parameters
        self.image = image # assign the "image" parameter to the attribute "image"
        self.type = type # assign the "type" parameter to the attribute "type"
        self.rect = self.image[self.type].get_rect() # get the dimensions (coordinates) of the image
        self.rect.x = SCREEN_WIDTH # set the inital x coordinate of the obstacle to be the screen width (just off the right side of the screen)

    def update(self): # create a function to update the state of the obstacle
        self.rect.x -= game_speed # move the obstacle to the left by subtracting the game_speed from the x coordinate
        if self.rect.x < -self.rect.width: # if the obstacle moves completely off screen, do the following:
            obstacles.pop() # remove the obstacle

    def draw(self, SCREEN): # create a function to draw the obstacle onto the screen
        SCREEN.blit(self.image[self.type], self.rect) # blit the image of the obstacle onto the screen


class SmallCactus(Obstacle): # create a subclass of Obstacle named SmallCactus
    def __init__(self, image): # initalizes the small cactus object
        self.type = random.randint(0, 2) # set the type to be a random integer from 0 to 2 to get one of the 3 possible small cacti
        super().__init__(image, self.type) # intialize the __init__ method of the parent class, Obstacle
        self.rect.y = 325 #set the y coordinate of the small cactus to 325


class LargeCactus(Obstacle): # create a subclass of Obstacle named LargeCactus
    def __init__(self, image): # initalizes the large cactus object
        self.type = random.randint(0, 2) # set the type to be a random integer from 0 to 2 to get one of the 3 possible large cacti
        super().__init__(image, self.type) # intialize the __init__ method of the parent class, Obstacle
        self.rect.y = 300 # set the y coordinate of the large cactus to 300


class Bird(Obstacle): # create a subclass of Obstacle named Bird
    BIRD_HEIGHTS = [250, 290, 320] # make a list of possible bird heights and assign it to the variable BIRD_HEIGHTS

    def __init__(self, image): # initalizes the bird object
        self.type = 0 # set the type to zero since there is only one type of bird
        super().__init__(image, self.type) # intialize the __init__ method of the parent class, Obstacle
        self.rect.y = random.choice(self.BIRD_HEIGHTS) #set the y coordinate of the bird to be one of the 3 possibilities within the list BIRD_HEIGHTS
        self.index = 0 # set the inital index to be zero

    def draw(self, SCREEN): # create a new draw function that overrides the one in the parent class, Obstacle, since the bird is animated
        if self.index >= 9: # if the index reaches a value of 9, do the following: 
            self.index = 0 # reset the index to be zero
        SCREEN.blit(self.image[self.index // 5], self.rect) # blit the bird onto the screen, such that when the index is between 0-4, the first image will be drawn while when the index is between 5-9, the 2nd image is drawn
        self.index += 1 # increment the index by one


def main(): #Create a function "main" where the functions and classes defined above will be called
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles # the variables listed here are defined as global variables, meaning they can be accessed and changed througout the entire program
    run = True # Set run equal to true. While the variable is true, the game runs
    clock = pygame.time.Clock() # creates an object to track the time and assigns it to the variable clock
    player = Dinosaur() # creates an instance of the class Dinosaur and assigns it to the variable player
    cloud = Cloud() # creates an instance of the class Cloud and assigns it to the variable cloud
    game_speed = 20 # sets the inital game speed to be 20 (the background, clouds, player, and obstacles are dependent on the game speed)
    x_pos_bg = 0 # sets the intial x coordinate of the background to be 0 
    y_pos_bg = 380 # sets the inital y coordinate of the background to be 380 
    points = 0 # sets the inital value of points to be 0
    font = pygame.font.Font("freesansbold.ttf", 20) #create a font from the file "freesansbold.ttf" and set it to size 20 
    obstacles = [] #creates an empty list for the obstacles
    death_count = 0 # sets the death counter to start at 0
    pause = False #set pause equal to false (since the game is running)

    def score(): # create a function named score
        global points, game_speed # use the global variables "points" and "game_speed" (definied in main() )
        points += 1 # every time the score function is called, increase the number of points the player has by 1
        if points % 100 == 0: # every 100 points, the game speed increases by 1, increasing the difficulty of the game
            game_speed += 1 # increase the game speed by 1
        current_time = datetime.datetime.now().hour # get the current hour in the datetime module
        with open("score.txt", "r") as f: # open and read the score.txt file and assign the open file to the variable f, automatically close it once it is done reading
            score_ints = [int(x) for x in f.read().split()] # read "score.txt" and split it into a list of strings, then convert the strings into integers for all the items in the file
            highscore = max(score_ints) # find the highest value of the scores to find the current highscore
            if points > highscore: #if the player's current points are higher than the highscore, do the following:
                highscore = points # set the new highscore to be the player's current score
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR) # display the text of the player's high score and points on the screen in the font colour black 
        textRect = text.get_rect() # get the coordinates of the rectangle in which the highscore and points are displayed
        textRect.center = (900, 40) # set the centre of the text to the top right corner of the screen
        SCREEN.blit(text, textRect) # blit the highscore and points onto the screen

    def background(): # create a function called background
        global x_pos_bg, y_pos_bg # get the global x and y coordinates of the background 
        image_width = BG.get_width() # get the dimensions of the background image
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # blit the background image onto the screen at the global x and y coordinates
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # blit another background image onto the screen to the right of the first one to make it seem like a continous track
        if x_pos_bg <= -image_width: # if the background image moves fully off the screen, a new background image is created to replace it
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # blit the replacement background image onto the screen
            x_pos_bg = 0 # reset the x position of the background back to 0 
        x_pos_bg -= game_speed # move the background image to the left based on the game speed

    def unpause(): # create a function called unpause
        nonlocal pause, run # uses the variables "pause" and "run" that are defined in main(), its parent class 
        pause = False #set the variable "pause" equal to false
        run = True #set the variable "run" equal to True (so the game will run)
    
    
    #Joy-Marie Salama's Part Starts

    def paused():
        nonlocal pause #Refers to the variable 'pause' outside of the function. 
        pause = True #Changes the original value of pause (False) to True. This starts the game
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

        player.draw(SCREEN) #Draws the dinosaur ontop of the new screen
        player.update(userInput) #Check what the user input is, and it will update the player's actions because of it.

        if len(obstacles) == 0: #if the length of the variable obstacles is equal to 0, do the following:
            if random.randint(0, 2) == 0: #If the random integer between 0 to 2 is equal to 0, do the following:
                obstacles.append(SmallCactus(SMALL_CACTUS)) #Input a small cactus as an obstacle
            elif random.randint(0, 2) == 1: #If the statement above is not fulfilled and if the randon integer between 0 to 2 is equal to 1, do the following:
                obstacles.append(LargeCactus(LARGE_CACTUS)) #Input a large cactus as an obstacle
            elif random.randint(0, 2) == 2: #If the statements above are not fulfilled and if the random integer between 0 to 2 is equal to 2, do the following:
                obstacles.append(Bird(BIRD)) #Inupt a bird as an obstacle

        for obstacle in obstacles: #A for loop for the variable obstacles
            obstacle.draw(SCREEN)  #Draws the new obstacle ontop of the new screen
            obstacle.update() #Checks what the obstacle is, and updates the obstacle shown 
            if player.dino_rect.colliderect(obstacle.rect): # If the dinosaur collides with the obstacles, do the following:
                pygame.time.delay(2000) #Pause the game for 2 seconds
                death_count += 1 #Increase the death count by 1, this allows the second if statement below to run
                menu(death_count) # Go to the menu that shows the final score and highscore

        background() #Run the background function

        cloud.draw(SCREEN) #Draw the cloud image onto the screen
        cloud.update() #update the cloud

        score()  #Run the score function

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
            scoreRect = score.get_rect() #Returns the image of the rectangle 
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50) #Centre the rectangle by the width of the screen divided by 2 and the height of the screen divided by 2 and add 50.
            SCREEN.blit(score, scoreRect) #Copies the score and the rectange onto the screen
            f = open("score.txt", "a") #Open and create the file score.txt and return it as a file object
            f.write(str(points) + "\n") #Write the points (as a string) into the file and put in new line after it
            f.close() # Close the file score.txt
            with open("score.txt", "r") as f: #Opens the file score.txt to read it, and after this function is finished, it automatically closes the file.
                score = (
                    f.read()
                )  # Input the score in the score.text
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
#Parts: Lexi: 0-123, Katie: 123-236, Joy: 236-354