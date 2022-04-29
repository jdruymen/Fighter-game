# -*- coding: utf-8 -*-

#Joshua Ruymen final project
#This should only need pygame and a few images to run correctly
#Game information (like actions taken by the AI) is printed out to the console

import pygame
import random

pygame.init()

#Framerate
clock = pygame.time.Clock()
fps = 144

#Pixel sizes of the game window
action_panel_height = 188
screen_width = 1000
screen_height = 500 + action_panel_height

#Creates the game window
window = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Turn based game")

#Define font for text
healthFont = pygame.font.SysFont('Times New Roman', 14)
actionFont = pygame.font.SysFont('Times New Roman', 42)
descriptionFont = pygame.font.SysFont('Times New Roman', 12)
endFont = pygame.font.SysFont('Times New Roman', 32)

#Define colors
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)


#Loads background images
backgroundImg = pygame.image.load('images/background/background.jpg')
actionImg = pygame.image.load('images/background/actionpanel.jpg')

#Adds the background image to the screen
def draw_background():
    window.blit(backgroundImg, (0, 0))

#Adds the action panel to the bottom of the screen
def draw_action_panel():
    window.blit(actionImg, (0, screen_height - action_panel_height))
    
#Converts text into an image that can be added to the screen at the given location
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    window.blit(img, (x, y))
    
#Checks if the game is won by checking if any enemies remain alive
def checkWin():
    for c in characters:
        if c.friendly == False:
            if c.alive:
                return False
    return True

#Character class - parent class for all characters in the game
class Character():
    def __init__(self, x, y, max_hp, img, friendly):
        #Initializes variables
        self.friendly = friendly
        self.blocking = False
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.alive = True
        self.x = x
        self.y = y
        self.health_bar = HealthBar(self.x - 25, self.y - 65, self.max_hp)
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    #Attacks the target, checks if the target dies and makes sure to keep the HP 0 at a minimum
    def attack(self, target, damage):
        if not target.blocking:
            target.hp -= damage
        else:
            print("Blocked!")
        if target.hp <= 0:
            target.hp = 0
            target.alive = False
   
    #Adds the character, hp text, and hp bar to the screen at the characters x y location
    def draw(self):
        window.blit(self.image, self.rect)
        self.health_bar.draw(self.hp)
        draw_text('HP: ' + str(self.hp), healthFont, green, self.x - 25, self.y - 80)


#Fighter class
class Fighter(Character):
    #Loads the correct image, lets the character init take care of the rest
    def __init__(self, x, y, max_hp):
        img = pygame.image.load('images/Fighter/fighter.png')
        img = pygame.transform.scale(img, (int(img.get_width() / 5), int(img.get_height() / 5)))
   
        Character.__init__(self, x, y, max_hp, img, True)
        
    #Tells character attack the damage
    def attack(self, target):
        Character.attack(self, target, 13)
        
    def heal(self):
        rand = int(random.randrange(1, 13, 1))
        self.hp += rand
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
    #Lets the character class draw everything
    def draw(self):
        Character.draw(self)

#Slime class
class Slime():
    def __init__(self, x, y, max_hp):
        img = pygame.image.load('images/Slime/slime.png')
        img = pygame.transform.scale(img, (int(img.get_width() / 6), int(img.get_height() / 6)))
        self.targeted = False
        
        Character.__init__(self, x, y, max_hp, img, False)
        
    def attack(self, target):
        Character.attack(self, target, 9)

    def draw(self):
        Character.draw(self)
        if self.targeted:
            pygame.draw.circle(window, red, (self.x, self.y - 100), 8)
            
    def takeTurn(self, target, ID):
        #Randomly decides what action the slime will do
        #0: attack  1: block next attack  2: pass turn
        rand = int(random.randrange(0, 3, 1))
        if rand == 0:
            self.attack(target)
            self.blocking = False
            print("Slime ", ID, " attacked!")
        elif rand == 1:
            self.blocking = True
            print("Slime ", ID, " is blocking!")
        else:
            self.blocking = False
            print("Slime ", ID, " took a nap.")
        
#Healthbar class
class HealthBar():
    def __init__(self, x, y, max_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        
    def draw(self, hp):
        hpRatio = hp / self.max_hp
        pygame.draw.rect(window, red, (self.x, self.y, 75, 5))
        pygame.draw.rect(window, green, (self.x, self.y, 75 * hpRatio, 5))
        
#Button class for the buttons on the action panel
class Button():
    def __init__(self, x, y, length, height, action):
        self.x = x
        self.y = y
        self.action = action
        self.length = length
        self.height = height
        
    def draw(self):
        pygame.draw.rect(window, green, (self.x, self.y, self.length, self.height))
    
    def draw_label(self):
        draw_text(str(self.action), actionFont, black,  self.x + 190,  self.y + 5)
        if self.action == "Attack":
            description = "Attacks your current target. 13 DMG"
        elif self.action == "Block":
            description = "Prepares for enemy attacks. Blocks any attacks next turn."
        elif self.action == "Heal":
            description = "Heal yourself. Heals for 1-13 HP"
        else:
            description = "Passes turn."
        draw_text(description, descriptionFont, black, self.x + 190, self.y + 50)
    
#Creates characters        
fighter = Fighter(250, 425, 100)
slime1 = Slime(700, 445, 100)
slime2 = Slime(815, 445, 100)

#Character list to iterate through
characters = []
characters.append(fighter)
characters.append(slime1)
characters.append(slime2)

attack = Button(4, 505, 492, 86, "Attack")
block = Button(503, 505, 492, 86, "Block")
heal = Button(4, 598, 492, 86, "Heal")
passTurn = Button(503, 598, 492, 86, "Pass")

#Action buttons
buttons = []
buttons.append(attack)
buttons.append(block)
buttons.append(heal)
buttons.append(passTurn)

#The target the player currently has selected
target = None
#Tracks whos turn it is
turn = 0
#Loops while the game is supposed to be running
runGame = True
#Pause timer so the "AI" doesn't instantly go
pause = 90
lost = False
while runGame:
    #Fixes framerate    
    clock.tick(fps)
    
    #Draws action buttons
    for b in buttons:
        b.draw()
    
    #Draws the background and action panel
    draw_background()
    draw_action_panel()
    
    #Draws characters and their health bars
    for c in characters:
        c.draw()
        
    #Labels all of the buttons (Has to be done after drawing the action panel)
    for b in buttons:
        b.draw_label()
    
    #Checks if the game is won, shows a victory screen
    if checkWin():
        draw_text('VICTORY', endFont, green, 425, 275)
        
    #Checks if the game is lost
    mouse = pygame.mouse.get_pos()
    if fighter.alive:
        #Checks if the player targets one of the available enemies
        for c in characters:
            if not c.friendly and c.alive:
                if c.rect.collidepoint(mouse):
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            target = c
                            c.targeted = True
                            for char in characters:
                                if c != char:
                                    char.targeted = False
                                    
        #Checks if it's the fighters turn                
        if turn == 0 and not checkWin():
            #Checks if the mouse is on a button on the action panel                
            for b in buttons:
                if b.x <= mouse[0] <= b.x + 492 and b.y <= mouse[1] <= b.y + 86:
                    for event in pygame.event.get():
                        #If button is clicked
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #Attacks the target
                            if b.action == "Attack":
                                if target != None:
                                    fighter.blocking = False
                                    fighter.attack(target)
                                    turn += 1
                            #Allows the fighter to block, blocking is reset when the next action is taken by the player
                            elif b.action == "Block":
                                fighter.blocking = True
                                turn += 1
                            #Heals the player for a random amount
                            elif b.action == "Heal":
                                fighter.blocking = False
                                fighter.heal()
                                turn += 1
                            #Allows the player to pass their turn
                            elif b.action == "Pass":
                                fighter.blocking = False
                                turn += 1
        #Iterates through slimes turns
        elif turn >= 1:
            c = characters[turn]
            if c.alive:
                #Timer to make sure the slimes aren't instantly taking their turn
                if pause <= 0:
                    pause = 90
                    c.takeTurn(fighter, turn)
                    turn += 1
                pause -= 1
            else:
                characters.remove(c)
                target = None
    
    #Resets to the players turn once every living character has went
    if turn >= len(characters):
        turn = 0
        
    #Game is lost, shows defeat screen
    if not fighter.alive:
        if not lost:
            characters.remove(fighter)
            lost = True
        draw_text('DEFEAT', endFont, red, 425, 275)
    
    #Checks if game is attempting to be closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
    
    #Refreshes the display
    pygame.display.update()
    
pygame.quit()