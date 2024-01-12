import pygame
import random
import os
import time
import sys
#initialize

pygame.font.init() 
# variables
WHITE = (255, 20, 255)
pygame.init()
x = 400
y = 400
black = (0, 0, 0)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Second Game!")
FPS = 60
VEL = 0.025


# render text
myFont = pygame.font.SysFont("cambria",100)
main_font = pygame.font.SysFont("cambria", 40)
# IMAGES
square_image = pygame.image.load(os.path.join('Assets', 'Crate.png'))
Jumper_image = pygame.image.load(os.path.join('Assets', 'Jumper.png'))
button_surface1 = pygame.image.load(os.path.join('Assets', 'Play_button1.png'))
button_surface1 = pygame.transform.scale(button_surface1, (100, 75))

# the main character
class Jumper:
    def __init__(self, filename, x, y, width, height):
        self.filename = filename
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            self.filename, (self.width, self.height))

    def controls(self, keys_pressed, VEL):
        if keys_pressed[pygame.K_RIGHT] and self.x <= 330:  # right
            self.x += VEL
        if keys_pressed[pygame.K_LEFT] and self.x >= -30:  # Left
            self.x -= VEL
        screen.blit(self.image, (self.x, self.y))

# The crate
class FallingImage:
    def __init__(self, file, x, y, width, height):
        self.file = file
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.file, (self.width, self.height))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# button class
class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
            return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "black")
        else:
            self.text = main_font.render(self.text_input, True, "white")

# objects
Main_char = Jumper(Jumper_image, 200, 330, 100, 100)
falling_img = FallingImage(square_image, 300, -100, 50, 100)
button = Button(button_surface1, 200, 100, "Play")
score = Button(button_surface1, 200, 100, "Score")
quit = Button(button_surface1, 200, 260, "QUIT")
LeaderBoard = Button(pygame.transform.scale(button_surface1, (220, 75)), 200, 180, "Leaderboard")
back = Button(button_surface1, 200, 350, "Back")
score_Storage = [0,0]
# main game loop
def mainGameLoop(score_Storage):
    Score_first = 0
    
    
    while True:
        
        keys_pressed = pygame.key.get_pressed()
        pygame.display.set_caption("Jumper!")
        screen.fill((0, 0, 0))

        
        falling_img.draw()
        falling_img.y += 25
        if falling_img.y > 400:
            falling_img.y = -150
            falling_img.x = random.randint(0, 330)
        for event in pygame.key.get_pressed():
            Main_char.controls(keys_pressed, VEL)
            #checking for X out and pause(key: p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if (keys_pressed[pygame.K_p]):
                mainMenu(button, quit, LeaderBoard)
            
        check(Score_first, score,score_Storage)
        Score_first += 1

        pygame.display.update()
        
    # checking for contact 
def check(Score_first, score,score_Storage):
    #checking height of camparing player and falling img
    if Main_char.y <= falling_img.y:
        #the first one is left hand side while the right is the right hand side
        if Main_char.x <= falling_img.x and Main_char.x+65 >= falling_img.x:
            # printing score to terminal
            print(Score_first)
            print("|"+"\n"*2)
            pygame.time.delay(10*100)
            # adding score to list
            score_Storage[1] = Score_first
            if score_Storage[1]>=score_Storage[0]:
                score_Storage[0]=score_Storage[1]  
            falling_img.y = 0
            falling_img.x = random.randint(0, 330)
            mainMenu(button, quit, LeaderBoard)

def leaderboard(back,score_Storage):
    pygame.display.set_caption("Leaderboard")
    screen.fill((173, 216, 230))
    
  
    backMenu = False
    while backMenu == False:
        #where to put score
        score = str(score_Storage[0])
        numLenMove = 0
        numLen = len(score)
        if numLen > 1:
            numLenMove = 15 * int(numLen)
        # Label score
        label = myFont.render(str(score_Storage[0]),3,black)
        screen.blit(label,(175-numLenMove,100))
        #mouse position
        mouse_pos = pygame.mouse.get_pos()
        for Button in [back]:
            Button.changeColor(mouse_pos)
            Button.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #exit leaderboard
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.checkForInput(mouse_pos):
                    backMenu = True
        
        
        pygame.display.update()
    mainMenu(button, quit, LeaderBoard)
# mainMenu
def mainMenu(button, quit, LeaderBoard):
    running = True
    while running == True:
        pygame.display.set_caption("Menu")

        mouse_pos = pygame.mouse.get_pos()

        screen.fill((173, 216, 230))
        for Button in [button, quit, LeaderBoard]:
            Button.changeColor(mouse_pos)
            Button.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (quit.checkForInput(mouse_pos)):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif (LeaderBoard.checkForInput(mouse_pos)):
                    leaderboard(back,score_Storage)
                elif (button.checkForInput(mouse_pos)):
                    mainGameLoop(score_Storage)
        pygame.display.update()


def Main():

    Start = False
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        
        mainMenu(button, quit, LeaderBoard)
        pygame.display.update()

# checking if not being imported
if __name__ == "__main__":
    Main()
