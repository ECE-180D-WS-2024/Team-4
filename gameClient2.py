import subprocess
import sys
import get_pip
import os
import velocity
import audio
import app
import time as time_mod
import random


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")

    import pygame

import physics
import math
import courses
import startScreen
from time import sleep, time
import tkinter as tk
from tkinter import messagebox
import sys

# INITIALIZATION
pygame.init()

SOUND = True

winwidth = 1080
winheight = 600
pygame.display.set_caption('Super Minigolf')

# LOAD IMAGES
icon = pygame.image.load(os.path.join('img', 'icon.ico'))
icon = pygame.transform.scale(icon, (32,32))
background = pygame.image.load(os.path.join('img', 'back.png'))
sand = pygame.image.load(os.path.join('img', 'sand.png'))
edge = pygame.image.load(os.path.join('img', 'sandEdge.png'))
bottom = pygame.image.load(os.path.join('img', 'sandBottom.png'))
green = pygame.image.load(os.path.join('img', 'green.png'))
flag = pygame.image.load(os.path.join('img', 'flag.png'))
water = pygame.image.load(os.path.join('img', 'water.png'))
laser = pygame.image.load(os.path.join('img', 'laser.png'))
sticky = pygame.image.load(os.path.join('img', 'sticky.png'))
coinPics = [pygame.image.load(os.path.join('img', 'coin1.png')), pygame.image.load(os.path.join('img', 'coin2.png')), pygame.image.load(os.path.join('img', 'coin3.png')), pygame.image.load(os.path.join('img', 'coin4.png')), pygame.image.load(os.path.join('img', 'coin5.png')), pygame.image.load(os.path.join('img', 'coin6.png')), pygame.image.load(os.path.join('img', 'coin7.png')), pygame.image.load(os.path.join('img', 'coin8.png'))]

mysteryBox = pygame.image.load(os.path.join('img', 'box.png'))

powerMeter = pygame.image.load(os.path.join('img', 'power.png'))
powerMeter = pygame.transform.scale(powerMeter, (150,150))

# SET ICON
pygame.display.set_icon(icon)

# GLOBAL VARIABLES
coinTime = 0
coinIndex = 0
time = 0
rollVel = 0
strokes = 0
strokes_1 = 0
strokes_2 = 0
par = 0
#OG lvl = 8??
level = 1
flagx = 0
coins = 0
shootPos = ()
ballColor = (255,255,255)
ballColor2 = (255,0,0)
ballStationary = ()
ballStationary2 = ()
line = None
power = 0
hole = ()
objects = []
put = False
shoot = False
start = True
player1attacked = False
player2attacked = False

powerUpPlayer1 = False
powerUpPlayer2 = False

powerup_number = 1

handGesture = "none"
player1_turn = True

#Set to true if level 1 is involved
tutorial = False

#set tut_seq to zero if we want to have full turoital
tut_seq = 0
spell_seq = 0
hole_seq = 0
h1 = 0
h2 = 0

player1Round = 0
player2Round = 0

# LOAD MUSIC
if SOUND:
    wrong = pygame.mixer.Sound(os.path.join('sounds', 'wrong12.wav'))
    puttSound = pygame.mixer.Sound(os.path.join('sounds', 'putt.wav'))
    inHole = pygame.mixer.Sound(os.path.join('sounds', 'inHole.wav'))
    song = pygame.mixer.music.load(os.path.join('sounds', 'music.mp3'))
    splash = pygame.mixer.Sound(os.path.join('sounds', 'splash.wav'))
    #pygame.mixer.music.play(-1)

# POWER UP VARS
powerUps = 7
hazard = False
#Ball Sticks to walls etc...
stickyPower = False
#Ball swings is much more sensitive
heavyHanded = False
#Makes gravity stronger
blackHole = False
#Makes gravity less strong
moonGravity = False
#Strokes don't add to a player when hit into water until level is over
waterWizard = False

mullagain = False
superPower = False
powerUpButtons = [[900, 35, 20, 'P', (255,69,0)],[1000, 35, 20, 'S', (255,0,255)], [950, 35, 20, 'M', (105,105,105)]]

# FONTS
myFont = pygame.font.SysFont('comicsansms', 50)
parFont = pygame.font.SysFont('comicsansms', 30)

win = pygame.display.set_mode((winwidth, winheight))

class scoreSheet():
    def __init__(self, parr):
        self.parList = parr
        self.par = sum(self.parList)
        self.holes = 9
        self.finalScore = None
        self.parScore = 0
        self.strokes = []
        self.win = win
        self.winwidth = winwidth
        self.winheight = winheight
        self.width = 400
        self.height = 510
        self.font = pygame.font.SysFont('comicsansms', 22)
        self.bigFont = pygame.font.SysFont('comicsansms', 30)

    def getScore(self):
        return sum(self.strokes) - sum(self.parList[:len(self.strokes)])

    def getPar(self):
        return self.par

    def getStrokes(self):
        return sum(self.strokes)

    def drawSheet(self, score=0):
        grey = (220, 220, 220)
        '''
        
        self.strokes.append(score)
        
        grey = (220, 220, 220)

        text = self.bigFont.render('Strokes: ' + str(sum(self.strokes)), 1, grey)
        self.win.blit(text, (800, 330))
        text = self.bigFont.render('Par: ' + str(self.par), 1, grey)
        self.win.blit(text, (240 - (text.get_width()/2), 300 - (text.get_height()/2)))
        text = self.bigFont.render('Score: ', 1, grey)
        self.win.blit(text, (800, 275))

        scorePar = sum(self.strokes) - sum(self.parList[:len(self.strokes)])
        if scorePar < 0:
            color = (0,166,0)
        elif scorePar > 0:
            color = (255,0,0)
        else:
            color = grey

        textt = self.bigFont.render(str(scorePar), 1, color)
        win.blit(textt, (805 + text.get_width(), 275))

        startx = self.winwidth/2 - self.width /2
        starty = self.winheight/2 - self.height/2
        pygame.draw.rect(self.win, grey, (startx, starty, self.width, self.height))

        # Set up grid
        for i in range(1,4):
            # Column Lines
            pygame.draw.line(self.win, (0,0,0), (startx + (i * (self.width/3)), starty), (startx + (i * (self.width/3)), starty + self.height), 2)
        for i in range(1, 11):
            # Rows
            if i == 1:  # Display all headers for rows
                blit = self.font.render('Hole', 2, (0,0,0))
                self.win.blit(blit, (startx + 40, starty + 10))
                blit = self.font.render('Par', 2, (0,0,0))
                self.win.blit(blit, (startx + 184, starty + 10))
                blit = self.font.render('Stroke', 2, (0,0,0))
                self.win.blit(blit, (startx + 295, starty + 10))
                blit = self.font.render('Press the mouse to continue...', 1, (128,128,128))
                self.win.blit(blit, (384, 565))
            else:  # Populate rows accordingly
                blit = self.font.render(str(i - 1), 1, (128,128,128))
                self.win.blit(blit, (startx + 56, starty + 10 + ((i - 1) * (self.height/10))))

                blit = self.font.render(str(self.parList[i - 2]), 1, (128,128,128))
                self.win.blit(blit, (startx + 60 + 133, starty + 10 + ((i - 1) * (self.height/10))))
                try:  # Catch the index out of range error, display the stokes each level
                    if self.strokes[i - 2] < self.parList[i - 2]:
                        color = (0,166,0)
                    elif self.strokes[i - 2] > self.parList[i - 2]:
                        color = (255,0,0)
                    else:
                        color = (0,0,0)

                    blit = self.font.render(str(self.strokes[i - 2]), 1, color)
                    self.win.blit(blit, ((startx + 60 + 266, starty + 10 + ((i - 1) * (self.height/10)))))
                except:
                    blit = self.font.render('-', 1, (128,128,128))
                    self.win.blit(blit, (startx + 62 + 266, starty + 10 + ((i - 1) * (self.height/10))))

            # Draw row lines
            pygame.draw.line(self.win, (0,0,0), (startx, starty + (i * (self.height/10))), (startx + self.width, starty + (i * (self.height / 10))), 2)
'''

def error():
    if SOUND:
        wrong.play()
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showerror('Out of Powerups!', 'You have no more powerups remaining for this course, press ok to continue...')
    try:
        root.destroy()
    except:
        pass


def endScreen(): # Display this screen when the user completes the course
    global start, starting, level, sheet, coins
    starting = True
    start = True

    # Draw all text to display on screen
    win.blit(background, (0,0))
    text = myFont.render('Course Completed!', 1, (64,64,64))
    win.blit(text, (winwidth/2 - text.get_width()/2, 210))
    text = parFont.render('Par: ' + str(sheet.getPar()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 320)))
    text = parFont.render('Strokes: ' + str(sheet.getStrokes()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 280)))
    blit = parFont.render('Press the mouse to continue...', 1, (64, 64, 64))
    win.blit(blit, (winwidth/2 - blit.get_width()/2, 510))
    text = parFont.render('Score: ' + str(sheet.getScore()), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 360)))
    text = parFont.render('Coins Collected: ' + str(coins), 1, (64,64,64))
    win.blit(text, ((winwidth/2 - text.get_width()/2, 470)))
    pygame.display.update()


    # RE-WRITE TEXT FILE Contaning Scores
    oldscore = 0
    oldcoins = 0
    file = open('scores.txt', 'r')
    f = file.readlines()
    for line in file:
        l = line.split()
        if l[0] == 'score':
            oldscore = str(l[1]).strip()
        if l[0] == 'coins':
            oldcoins = str(l[1]).strip()

    file = open('scores.txt', 'w')
    if str(oldscore).lower() != 'none':
        if sheet.getScore() < int(oldscore):
            text = myFont.render('New Best!', 1, (64, 64, 64))
            win.blit(text, (winwidth/2 - text.get_width()/2, 130))
            
            pygame.display.update()
            file.write('score ' + str(sheet.getScore()) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
        else:
            file.write('score ' + str(oldscore) + '\n')
            file.write('coins ' + str(int(oldcoins) + coins) + '\n')
    else:
        file.write('score ' + str(sheet.getScore()) + '\n')
        file.write('coins ' + str(int(oldcoins) + coins) + '\n')

    co = 0
    for line in f:
        if co > 2:
            file.write(line)
        co += 1

    file.close()

    # Wait
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
                break
    #UNCOMMENT?
    #level = 1
    setup(level - 1)
    list = courses.getPar(1)
    par = list[level - 1]
    sheet = scoreSheet(list)
    #Set starting to True if we want a start screen
    starting = True
    hover = False

    while starting:
        pygame.time.delay(10)
        startScreen.mainScreen(hover)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hover = startScreen.shopClick(pos)
                course = startScreen.click(pos)
                startScreen.mouseOver(course != None)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startScreen.click(pos) != None:
                    starting = False
                    break
                if startScreen.shopClick(pos) == True:
                    surface = startScreen.drawShop()
                    win.blit(surface, (0, 0))
                    pygame.display.update()
                    shop = True
                    while shop:
                        for event in pygame.event.get():
                            pygame.time.delay(10)
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if pos[0] > 10 and pos[0] < 100 and pos[1] > 560:
                                    shop = False
                                    break
                                surface = startScreen.drawShop(pos, True)
                                win.blit(surface, (0, 0))
                                pygame.display.update()

            if event.type == pygame.QUIT:
                pygame.quit()
                break




def setup(level):  # Setup objects for the level from module courses
    global line, par, hole, power, ballStationary, ballStationary2, objects, ballColor, ballColor2, stickyPower, superPower, mullagain
    ballColor = (255,255,255)
    stickyPower = False
    superPower = False
    mullagain = False
    if level >= 10:
        endScreen()  # Completed the course
    else:
        list = courses.getPar(1)
        par = list[level - 1]
        pos = courses.getStart(level, 1)
        ballStationary = pos
        ballStationary2 = (pos[0] - 10, pos[1])
        objects = courses.getLvl(level)

        # Create the borders if sand is one of the objects
        for i in objects:
            if i[4] == 'sand':
                objects.append([i[0] - 16, i[1], 16, 64, 'edge'])
                objects.append([i[0] + ((i[2] // 64) * 64), i[1], 16, 64, 'edge'])
                objects.append([i[0], i[1] + 64, i[2], 16, 'bottom'])
            elif i[4] == 'flag':
                # Define the position of the hole
                hole = (i[0] + 2, i[1] + i[3])

        line = None
        power = 1


def fade():  # Fade out screen when player gets ball in hole
    print("Get In")
    global hole_seq
    global h1, h2
    if(hole_seq == 2 or (h1 == 1 and h2 == 1)):
        print("entered")
        hole_seq = 0
        h1 = 0
        h2 = 0
        fade = pygame.Surface((winwidth, winheight))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            redrawWindow(ballStationary, ballStationary2, None, False, False)
            win.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(1)


def showScore():  # Display the score from class scoreSheet
    global level
    global tutorial
    #sleep(2)
    level += 1
    tutorial = False
    sheet.drawSheet(strokes)
    pygame.display.update()
    go = True
    while go:  # Wait until user clicks until we move to next level
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                go = False
                setup(level)


def holeInOne():  # If player gets a hole in one display special mesage to screen
    text = myFont.render('Hole in One!', 1, (255,255,255))
    x = (winwidth / 2) - (text.get_width() / 2)
    y = (winheight / 2) - (text.get_height() / 2)
    #Update is necessary to not glitch ball into hole
    #win.blit(text, (x, y))
    pygame.display.update()
    showScore()


def displayScore(stroke, par):  # Using proper golf terminology display score
    #RoundWinner -1 not yet assigned, 1 is player 1, 2 is player 2, 3 is a round tie
    roundWinner = 0
    global player1Round, player2Round
    if(strokes_1 < strokes_2):
        player1Round += 1

    elif(strokes_2 < strokes_1):
        player2Round += 1
    else:
        print("Round is a tie")

    if(player1Round > player2Round):
        text = parFont.render('Wizard 1 is winning!', 1, (255,255,255))
        win.blit(text, (winwidth//2 - 200,100))
    elif(player2Round > player1Round):
        text = parFont.render('Wizard 2 is winning!', 1, (255,255,255))
        win.blit(text, (winwidth//2 - 200,100))
    else:
        #wizards are tied 
        text = parFont.render('Wizards are tied!', 1, (255,255,255))
        win.blit(text, (winwidth//2 - 200,100))

    #Display Rounds
    text = parFont.render('Player 1 rounds won: ' + str(player1Round), 1, (255,255,255))
    win.blit(text, (winwidth//2 - 200,135))
    text = parFont.render('Player 2 rounds won: ' + str(player2Round), 1, (255,255,255))
    win.blit(text, (winwidth//2 - 200,170))


    #label = myFont.render(text, 1, (255,255,255))
    #win.blit(label, ((winwidth//2) - (label.get_width() // 2), (winheight//2) - (label.get_height()//2)))
    
    #Setting the display to zero score
     #Updateand showscore is necessary to not glitch ball into hole
    pygame.display.update()
    showScore()

#Need to Change Parameters
def redrawWindow(ball, ball2, line, shoot=False, update=True):
    global water, par, strokes, flagx

    win.blit(background, (-200, -100))  # REFRESH DISPLAY



    for x in powerUpButtons[1:-1]:  # Draw the power up buttons in top right
        #POWERUPDRAW commented out power up circles
        #DRAWSCROLL
        if(powerUpPlayer1 and player1_turn):
            pygame.draw.circle(win, (0, 0, 0), (x[0], x[1]), x[2] +2)
            pygame.draw.circle(win, x[4], (x[0], x[1]), x[2])
            text = parFont.render("1", 1, (255,255,255))
            win.blit(text, (x[0] - (text.get_width()/2), x[1] - (text.get_height()/2)))
        if(powerUpPlayer2 and (player1_turn == False)):
            pygame.draw.circle(win, (0, 0, 0), (x[0], x[1]), x[2] +2)
            pygame.draw.circle(win, x[4], (x[0], x[1]), x[2])
            text = parFont.render("2", 1, (255,255,255))
            win.blit(text, (x[0] - (text.get_width()/2), x[1] - (text.get_height()/2)))

    #STROKE DRAWING AND POWERUPS
    # Draw information such as strokes, par and powerups left
    #smallFont = pygame.font.SysFont('comicsansms', 20)
    #text = smallFont.render('Left: ' + str(powerUps), 1, (64,64,64))
    #win.blit(text, (920, 55))

    this_turn = 1
    this_stroke = 0
    if(player1_turn):
        this_turn = '1'
        this_stroke = strokes_1

    else:
        this_turn = '2'
        this_stroke = strokes_2

    text = parFont.render('Player Turn: ' + this_turn, 1, (64,64,64))


    win.blit(text, (20,10))
    
    text = parFont.render('Strokes: ' + str(this_stroke), 1, (64,64,64))
    win.blit(text, (18,45))


    #Welcome to the 89,575th annual golf wizarding tournament
    #The tournament was established to determine the most talented golfing wizards in the realm of Samuelia
    #Wizards will compete head to head, vying for the championship throne

    #To enter the tournament, each wizard must provide proof of magic and basic movement training
    #Let's start with player 1, move your mouse on screen to select swing direction
    #Great! Now click to lock in the angle of swing
    #So far so good, hold your casting button on your controller and take a swing to determine shot power
    #Click on screen to send your power to the ball 
    #Woah that was powerful!!
    #Player 2, its your turn, move around!
    #Player 1 try to reach that powerbox, once you aquire it, we can cast on your next turn
    #Player 2, do the same
    #Nice player 1, now click the scroll to cast your powerup.
    #Hold your hand in front of the computer screen in the shape of a fist (to attack) or an open palm (to defend)
    #Now, speak into the microphone the name of the powerup to activate
    #Nice job, used used sticky ball, a powerup which sticks your ball to walls (this will be useful later)
    #Let's get to the hole so we can complete our proof of magic requirement

    #I think we have an array with player 1 and 2 instructions

    #I have competed before or, first tournament if statement
    if(tutorial):

        #Tutorial Dialogue Sequence
        if(tut_seq == 0):
            text = parFont.render('Welcome to the 89,575th annual golf wizarding tournament!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('To enter the tournament, each wizard must prove they', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('are magical by blood.......', 1, (64,64,64))
            win.blit(text, (50,170))
            text = parFont.render('Player 1, click the mouse to lock in your swing angle!', 1, (64,64,64))
            win.blit(text, (50,240))
            text = parFont.render('While holding the wand button, swing to capture your shot power.', 1, (64,64,64))
            win.blit(text, (50,275))
            text = parFont.render('After your swing, press the keyboard again to shoot!', 1, (64,64,64))
            win.blit(text, (50,310))
        if(tut_seq == 1):
            text = parFont.render('Player 2, click the mouse to lock in your swing angle!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('While holding the wand button, swing to capture your shot power.', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('After your swing, press the keyboard again to shoot!', 1, (64,64,64))
            win.blit(text, (50,170))  
        if(tut_seq == 2):
            text = parFont.render('Well done Wizards, but this is only the first step.......', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('To enter the tournament, you each must successfully cast a spell.', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('To cast a spell, sorcerers must have in their posession, a charm.', 1, (64,64,64))
            win.blit(text, (50,170)) 
            text = parFont.render('Shoot your ball through the enchanted-gold to collect the charm!', 1, (64,64,64))
            win.blit(text, (50,205)) 
        if(tut_seq == 3):
            text = parFont.render('Wizard 1, congrats on collecting the charm first!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('For testing purposes, you have both been awarded the sticky-ball charm.', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Casting is a two step process, so listen carefully!', 1, (64,64,64))
            win.blit(text, (50,170)) 
            text = parFont.render('Click the spell icon (top right) to initiate casting.', 1, (64,64,64))
            win.blit(text, (50,205)) 
        if(tut_seq == 4):
            text = parFont.render('Wizard 2, congrats on collecting the charm first!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('For testing purposes, you have both been awarded the sticky-ball charm.', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Casting is a two step process, so listen carefully!', 1, (64,64,64))
            win.blit(text, (50,170)) 
            text = parFont.render('Click the spell icon (top right) to initiate casting.', 1, (64,64,64))
            win.blit(text, (50,205)) 
        if(tut_seq == 5):
            text = parFont.render('As per sorcerers guidelines, spells must be cast at start of each turn', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('Spells can be applied to your opponent or self', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Raise your hand in a fist to apply your powerup to your opponent', 1, (64,64,64))
            win.blit(text, (50,170))
            text = parFont.render('Raise an open facing palm to apply to powerup to self ', 1, (64,64,64))
            win.blit(text, (50,205))
            
        if(tut_seq == 6):
            text = parFont.render('Now speak (into mic) your casting phrase!!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('Player 1 Casting Phrase: Water', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Player 2 Casting Phrase: Fire', 1, (64,64,64))
            win.blit(text, (50,170))
            text = parFont.render('Speech precision is crucial to a successful casting....', 1, (64,64,64))
            win.blit(text, (50,205))
        if(tut_seq == 7):
            text = parFont.render('Congrats on your spell casting player 1!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('The spells within the charms are random, so be careful.....', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Wait for player 2 to prove they are worthy of competition', 1, (64,64,64))
            win.blit(text, (50,170))
            
        if(tut_seq == 8):
            text = parFont.render('Congrats on your spell casting player 2!', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('The spells within the charms are random, so be careful.....', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('Wait for player 1 to prove they are worthy of competition', 1, (64,64,64))
            win.blit(text, (50,170))
           
        if(tut_seq == 9):
            text = parFont.render('Get in the hole to begin the tournament.', 1, (64,64,64))
            win.blit(text, (50,100))
            text = parFont.render('The player with the lowest stroke count wins the hole!', 1, (64,64,64))
            win.blit(text, (50,135))
            text = parFont.render('The player with the most won holes wins the tournament!', 1, (64,64,64))
            win.blit(text, (50,170))
            text = parFont.render('May the luck of Samuelia rest in you both....good luck', 1, (64,64,64))
            win.blit(text, (50,205))


        #text = parFont.render('Spells can either be applied to yourself or your opponent on their next turn', 1, (64,64,64))
        #win.blit(text, (50,100))
        #text = parFont.render('Show your camera your hand in a fist to apply your powerup to your opponent', 1, (64,64,64))
        #win.blit(text, (50,135))
        #text = parFont.render('Show your camera an open facing palm to apply to powerup to self ', 1, (64,64,64))
        #win.blit(text, (50,170))


    #To enter the tournament, each wizard must provide proof of magic and basic movement training
    #Let's start with player 1, move your mouse on screen to select swing direction, and click to lock in angle of swing




    #text = parFont.render('Player 1, move your mouse to select your swing direction, then click to lock the angle', 1, (64,64,64))
    #win.blit(text, (100,130))

    

    # Draw all objects in the level, each object has a specific image and orientation
    for i in objects:
        if i[4] == 'sand':
            for x in range(i[2]//64):
                win.blit(sand, (i[0] + (x * 64), i[1]))
        elif i[4] == 'water':
            for x in range(i[2] // 64):
                water = water.convert()
                water.set_alpha(170)
                win.blit(water, (i[0] + (x * 64), i[1]))
        elif i[4] == 'edge':
            win.blit(edge, (i[0], i[1]))
        elif i[4] == 'bottom':
            for x in range(i[2] // 64):
                win.blit(bottom, (i[0] + (64 * x), i[1]))
        elif i[4] == 'flag':
            win.blit(flag, (i[0], i[1]))
            pygame.draw.circle(win, (0,0,0), (i[0] + 2, i[1] + i[3]), 6)
            flagx = i[0]
        elif i[4] == 'floor':
            for x in range(i[2] // 64):
                if(i[0] != 950 or tut_seq != 9):
                    win.blit(bottom, (i[0] + 64 * x, i[1]))
        elif i[4] == 'green':
            for x in range(i[2] // 64):
                win.blit(green, (i[0] + (64 * x), i[1]))
        elif i[4] == 'wall':
            for x in range(i[3] // 64):
                if(i[0] != 950 or tut_seq != 9):
                    win.blit(edge, (i[0], i[1] + (64 * x)))
                
                #TUTORIAL WALL BLOCKERS
                #if(tutorial):
                    #win.blit(edge, (950, 550))
                    #win.blit(bottom, (950, 550))
                    #win.blit(bottom, (1010, 550))

        elif i[4] == 'laser':
            for x in range(i[3] // 64):
                win.blit(laser, (i[0], i[1] + (64 * x)))
        elif i[4] == 'sticky':
            for x in range(i[3]//64):
                win.blit(sticky, (i[0], i[1] + (64 * x)))
        elif i[4] == 'coin':
        
            if i[5]:
               
                img = coinImg()
            
                if(tut_seq == 2 or tutorial == False):
                    win.blit(img, (i[0], i[1]))

    win.blit(powerMeter, (4, 520))

    if line != None and not (shoot): # If we are not in the process of shooting show the angle line
        if(player1_turn):
            pygame.draw.line(win, (0, 0, 0), ballStationary, line, 2)
        else:
            pygame.draw.line(win, (0, 0, 0), ballStationary2, line, 2)

    # Draw the ball and its outline
    pygame.draw.circle(win, (0, 0, 0), ball, 5)
    pygame.draw.circle(win, ballColor, ball, 4)

    #Multiplayer Initial Draw
    #Player2
    pygame.draw.circle(win, (0, 0, 0), ball2, 5)
    pygame.draw.circle(win, ballColor2, ball2, 4)

    if update:
        powerBar()


def coinImg():  # Animation for spinning coin, coin acts as currency
    global coinTime, coinIndex
    coinTime += 1
    if coinTime == 15:  # We don't want to delay the game so we use a count variable based off the clock speed
        coinIndex += 1
        coinTime = 0
    if coinIndex == 8:
        coinIndex = 0
    #print(coinPics[coinIndex])
    #return pygame.image.load(os.path.join('img', 'box.png'))
    #return "box.png"
#Old Code 
    return coinPics[coinIndex]


def powerBar(moving=False, angle=0):
    if moving:
        # Move the arm on the power meter if we've locked the angle
        redrawWindow(ballStationary, ballStationary2, line, False, False)
        pygame.draw.line(win, (255,255,255), (80, winheight -7), (int(80 + round(math.cos(angle) * 60)), int((winheight - (math.sin(angle) * 60)))), 3)
    
    
    pygame.display.update()



# Find the angle that the ball hits the ground at
def findAngle(pos):
    if(player1_turn):
        sX = ballStationary[0]
        sY = ballStationary[1]
    else:
        sX = ballStationary2[0]
        sY = ballStationary2[1]
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


def onGreen():  # Determine if we are on the green
    global hole

    for i in objects:
        if i[4] == 'green':
            if(player1_turn):
                if ballStationary[1] < i[1] + i[3] and ballStationary[1] > i[1] - 20 and ballStationary[0] > i[0] and ballStationary[0] < i[0] + i[2]:
                    return True
                else:
                    return False
            else:
                if ballStationary2[1] < i[1] + i[3] and ballStationary2[1] > i[1] - 20 and ballStationary2[0] > i[0] and ballStationary2[0] < i[0] + i[2]:
                    return True
                else:
                    return False


def overHole(x,y):  # Determine if we are over top of the hole
    if x > hole[0] - 6 and x < hole[0] + 6:
        if y > hole[1] - 13 and y < hole[1] + 10:
            if((tutorial == True and tut_seq == 9) or tutorial == False):
                
                return True
            else: 
                return False
        else:
            return False
    else:
        return False

#++++++++++++++++++++++++++++++++ START OF THE GAME +++++++++++++++++++++++++++++++++++++++++++
list = courses.getPar(1)
par = list[level - 1]
sheet = scoreSheet(list)

pos = courses.getStart(level, 1)
ballStationary = pos
setup(1)


#We want to edit 



# MAIN GAME LOOP:
# - Collision of ball
# - Locking angle and power
# - Checking if power up buttons are clicked
# - Shooting the ball, uses physics module
# - Keeping track of strokes
# - Calls all functions and uses modules/classes imported and defined above

# Start loop
# Display start screen
hover = False
#**SET STARTING TO TRUE IF WE WANT A START SCREEN**#

starting = True
while starting:
    
    pygame.time.delay(10)
    startScreen.mainScreen(hover)

    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            hover = startScreen.shopClick(pos)
            course = startScreen.click(pos)
            startScreen.mouseOver(course != None)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if startScreen.click(pos) != None:
                starting = False
                break
            if startScreen.shopClick(pos) == True:
                surface = startScreen.drawShop()
                win.blit(surface, (0,0))
                pygame.display.update()
                shop = True
                while shop:
                    for event in pygame.event.get():
                        pygame.time.delay(10)
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if pos[0] > 10 and pos[0] < 100 and pos[1] > 560:
                                shop = False
                                break
                            surface = startScreen.drawShop(pos, True)
                            win.blit(surface, (0,0))
                            pygame.display.update()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        


#######################################
#CREATION OF NETWORK SOCKET AFTER THE START SCREEN
from gameNetwork import *
player2client = Network()

#Helper Funcitons
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5]), int(str[6]), int(str[7]), int(str[8]), int(str[9]), int(str[10])
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," +  str(tup[5]) + "," + str(tup[6]) + "," + str(tup[7]) + "," +  str(tup[8]) + "," + str(tup[9]) + "," + str(int(tup[10]))


#######################################


# Game Loop for levels and collision
while True:
    if stickyPower == False and superPower == False:
        ballColor = startScreen.getBallColor()
        if ballColor == None:
            ballColor = (255,255,255)
    if((player1attacked and player1_turn)):
        player1attacked = False
        #Randomize power up features
        

        if(tutorial == True):
            stickyPower = True
            ballColor = (255,0,255)
        else:
            #Randomly selects a powerup with equal chance
            number = random.randint(1,4)
            if(number == 1):
                stickyPower = True
                ballColor = (255,0,255)
            elif(number == 2):
                moonGravity = True
            elif(number == 3):
                blackHole = True
            elif(number == 4):
                moonGravity = True

        ballColor = (255,0,255)
        #powerUpPlayer1 = False
        if(tutorial):
            #tut_seq = 7
            print("1...DONE WITH TUTORIAL, RACE TO THE FINISH")
            if(tutorial == True):
                powerUps -= 1
            tut_seq = 7
            spell_seq += 1
            if(spell_seq == 2):
                tut_seq = 9
    if((player2attacked and player1_turn == False)):
        if(tutorial == True):
            stickyPower = True
            ballColor = (255,0,255)
        else:
            #Randomly selects a powerup with equal chance
            number = random.randint(1,4)
            if(number == 1):
                stickyPower = True
                ballColor2 = (255,0,255)
            elif(number == 2):
                moonGravity = True
            elif(number == 3):
                blackHole = True
            elif(number == 4):
                moonGravity = True

        player2attacked = False
        #powerUpPlayer1 = False
        if(tutorial):
            #tut_seq = 7
            print("1...DONE WITH TUTORIAL, RACE TO THE FINISH")
            if(tutorial == True):
                powerUps -= 1
            tut_seq = 7
            spell_seq += 1
            if(spell_seq == 2):
                tut_seq = 9

    if(player1_turn):
        ####################################################################
        #SEND CLAUSE
        if (line != None):
            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2,  int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], shoot))
        else:
            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), -1, -1, shoot))
        recData = player2client.send(sendData)
        ####################################################################

        player1data = read_pos(recData)

        #Key Variables (x,y, strokes, h1, player1_turn, player1attacked, player2attacked, powerupplayer1, linex, liney, shoot)
        ballStationary = (player1data[0], player1data[1])
        h1 = player1data[3]

        ##If there is an addition in strokes and you arent in the hole, change turns
        if (strokes_1 < player1data[2] and h2 != 1 and player1data[10] == 0):
            player1_turn = False

        strokes_1 = player1data[2]
        #player1_turn = bool(player1data[4])
        player1attacked = bool(player1data[5])
        player2attacked = bool(player1data[6])
        powerUpPlayer1 = bool(player1data[7])
        if (player1data[8] == -1 and player1data[9] == -1):
            line = None
        else:
            line = (player1data[8], player1data[9])
        shoot = bool(player1data[10])    

        redrawWindow(ballStationary, ballStationary2, line, shoot)

        # Advance to score board
        if (h1 + h2 == 2):
                #hole_seq += 1
            fade()
            displayScore(strokes, par)
            tutorial = False
            strokes = 0
            strokes_1 = 0
            strokes_2 = 0

        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                fade()
                if strokes == 1:
                    holeInOne()
                else:
                    displayScore(strokes, par)

                strokes = 0
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            for x in powerUpButtons:
                if pos[0] < x[0] + x[2] and pos[0] > x[0] - x[2] and pos[1] < x[1] + x[2] and pos[1] > x[1] - x[2]:
                    if x[3] == 'S':
                        x[4] = (255,0,120)
                    elif x[3] == 'M':
                        x[4] = (105,75,75)
                    elif x[3] == 'P':
                        x[4] = (170,69,0)
                else:
                    if x[3] == 'S':
                        x[4] = (255,0,255)
                    elif x[3] == 'M':
                        x[4] = (105,105,105)
                    elif x[3] == 'P':
                        x[4] = (255,69,0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            lock = 0
            pos = pygame.mouse.get_pos()
            # See if power up buttons are clicked
            #Alter to see if sticky ball 


            
            #stickyPower = audio.powerUp()

            #audio.spellCast()
            #powerUpButtons = [[900, 35, 20, 'P', (255,69,0)],[1000, 35, 20, 'S', (255,0,255)], [950, 35, 20, 'M', (105,105,105)]]
            #print(pos[0])
            #print[pos[1]]

            for x in powerUpButtons:
                # Check collision of mouse and button
                if pos[0] < x[0] + x[2] and pos[0] > x[0] - x[2] and pos[1] < x[1] + x[2] and pos[1] > x[1] - x[2]:
                    lock = -1
                    
                    if powerUps == 0:

                        error()
                        break
                    elif x[3] == 'S':  # 'S' Sticky Ball (sticks to any non-hazard) 

                        if stickyPower is False and superPower is False and powerUps > 0:
                            #LOOP THROUGH TO
                            #linker
                            #handGesture = "none"
                            #if(handGesture == "none"):
                            #    handGesture = app.main()
                            #print(app.main())  

                            #CODE FOR LINKING HAND GESTURE SCRIPT  
                            #text = parFont.render('Spells can either be applied to yourself or your opponent on their next turn', 1, (64,64,64))
                            #win.blit(text, (50,100))
                            #text = parFont.render('Show your camera your hand in a fist to apply your powerup to your opponent', 1, (64,64,64))
                            #win.blit(text, (50,135))
                            #text = parFont.render('Show your camera an open facing palm to apply to powerup to self ', 1, (64,64,64))
                            #win.blit(text, (50,170))
                            tut_seq = 5

                            powerup_number = random.randint(1,4)
                            if(powerup_number == 1):
                                text = parFont.render('Sticky Power! Attack or Defend!!!', 1, (255,0,0))
                                win.blit(text, (425,100))
                                pygame.display.update()
                                pygame.time.delay(1500)
                            elif(powerup_number == 2):
                                text = parFont.render('Moon gravity! Attack or Defend!!!', 1, (255,0,0))
                                win.blit(text, (425,100))
                                pygame.display.update()
                                pygame.time.delay(1500)
                            elif(powerup_number == 3):
                                text = parFont.render('Heavy swing! Attack or Defend!!!', 1, (255,0,0))
                                win.blit(text, (425,100))
                                pygame.display.update()
                                pygame.time.delay(1500)
                            elif(powerup_number == 4):
                                text = parFont.render('Stroke division! Attack or Defend!!!', 1, (255,0,0))
                                win.blit(text, (425,100))
                                pygame.display.update()
                                pygame.time.delay(1500)

                            redrawWindow(ballStationary, ballStationary2, line, False, False)
                            pygame.display.update()
                            


                            #APP.main calls the opening of the camera
                            handGesture = app.main()
                            if(handGesture == "open"):
                                print("Defend")
                                
                            elif(handGesture == "close"):
                                print("Attack")

                            tut_seq = 6
                            redrawWindow(ballStationary, ballStationary2, line, False, False)
                            pygame.display.update()
                                
                            #m_spell = audio.spellCast()
                            #debugging to save some time
                            if(player1_turn):
                                m_spell = "water"
                            elif(player1_turn == False):
                                m_spell = "fire"
                            print(m_spell)

                            #Debugging m_spell == "water" or "fire"
                            if(m_spell == "water" or "fire"):
                                print("Audio Linking Successful, Water or Fire is the Magic Word")
                                
                                if(tutorial == False):
                                    powerUps -= 1
                                if((player1_turn and m_spell == "water" and handGesture == "open")):
                                    #player1attacked = False


                                    if(tutorial == True):
                                        stickyPower = True
                                        ballColor = (255,0,255)
                                    else:
                                        number = powerup_number#random.randint(1,4)
                                        if(number == 1):
                                            print("1")
                                            stickyPower = True
                                            ballColor = (255,0,255)
                                            text = parFont.render('Sticky Power Active!', 1, (255,0,0))
                                            win.blit(text, (425,100))
                                            pygame.display.update()
                                            pygame.time.delay(1500)

                                        elif(number == 2):
                                            print("2")
                                            moonGravity = True
                                        elif(number == 3):
                                            print("3")
                                            blackHole = True
                                        elif(number == 4):
                                            print("3")
                                            moonGravity = True

                                    
                                    powerUpPlayer1 = False
                                    if(tutorial):
                                        

                                        print("1...DONE WITH TUTORIAL, RACE TO THE FINISH")
                                        if(tutorial == True):
                                            powerUps -= 1
                                        if(player1_turn):
                                            tut_seq = 7
                                        else:
                                            tut_seq = 8
                                        spell_seq += 1
                                        if(spell_seq == 2):
                                            tut_seq = 9

                                        redrawWindow(ballStationary, ballStationary2, line, False, False)
                                        pygame.display.update()
                                elif((player1_turn == False and m_spell == "fire" and handGesture == "open")):
                                    
                                    
                                    powerUpPlayer2 = False
                                    
                                    if(tutorial == True):
                                        stickyPower = True
                                        ballColor2 = (255,0,255)
                                    else:
                                        number = powerup_number#random.randint(1,4)
                                        if(number == 1):
                                            print("1")
                                            stickyPower = True
                                            ballColor2 = (255,0,255)
                                            text = parFont.render('Sticky Power Active!', 1, (255,0,0))
                                            win.blit(text, (425,100))
                                            pygame.display.update()
                                            pygame.time.delay(1500)

                                            
                                        elif(number == 2):
                                            print("2")
                                            moonGravity = True
                                        elif(number == 3):
                                            print("3")
                                            blackHole = True
                                        elif(number == 4):
                                            print("3")
                                            moonGravity = True
        


                                    
        

                                    if(tutorial):
                                        if(player1_turn):
                                            tut_seq = 7
                                        else:
                                            tut_seq = 8
                                        spell_seq += 1
                                        if(spell_seq == 2):
                                            tut_seq = 9

                                        redrawWindow(ballStationary, ballStationary2, line, False, False)
                                        pygame.display.update()
                                        print("2...DONE WITH TUTORIAL, RACE TO THE FINISH")
                                        if(tutorial == True):
                                            powerUps -= 1
                                elif(player1_turn == False and m_spell == "fire" and handGesture == "close"):
                                    print("Here1")
                                    player1attacked = True
                                    powerUpPlayer2 = False
                                    if(player1_turn and tutorial):
                                            tut_seq = 7
                                    else:
                                        tut_seq = 8
                                elif(player1_turn and m_spell == "water" and handGesture == "close"):
                                    print("Here2")
                                    player2attacked = True
                                    powerUpPlayer1 = False
                                    if(player1_turn and tutorial):
                                            tut_seq = 7
                                    else:
                                        tut_seq = 8
                            else:
                                tut_seq = 4
                                redrawWindow(ballStationary, ballStationary2, line, False, False)
                                pygame.display.update()
                                
                            
                    elif x[3] == 'M':  # 'M' Mullagain, allows you to retry your sot from your previous position, will remove strokes u had on last shot
                        if mullagain is False and powerUps > 0 and strokes >= 1:
                            mullagain = True
                            powerUps -= 1
                            ballStationary = shootPos
                            pos = pygame.mouse.get_pos()
                            angle = findAngle(pos)
                            line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                    round(ballStationary[1] - (math.sin(angle) * 50)))
                            if hazard:
                                strokes -= 2
                            else:
                                strokes -= 1
                            hazard = False
                    elif x[3] == 'P':  # 'P' Power ball, power is multiplied by 1.5x
                        if superPower is False and stickyPower is False and powerUps > 0:
                            superPower = True
                            powerUps -= 1
                            ballColor = (255,69,0)

            # If you click the power up button don't lock angle
            if lock == 0:
                powerAngle = math.pi
                neg = 1
                powerLock = False
                loopTime = 0

                while not powerLock:  # If we haven't locked power stay in this loop until we do
                    loopTime += 1
                    if loopTime == 6:
                        powerAngle -= 0.1 * neg
                        #powerAngle = velocity.getVelocity()
                        #powerBar(True, powerAngle)
                        loopTime = 0
                        if powerAngle < 0 or powerAngle > math.pi:
                            neg = neg * -1
                   # else:
                        #redrawWindow(ballStationary, ballStationary2, line, False, False)


                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if(player1_turn):
                                strokes_1 += 1
                            else:
                                strokes_2 += 1
                            hazard = False
                            if not onGreen():
                                shoot = True
                            else:
                                put = True
                                if SOUND:
                                    puttSound.play()
                            if put:
                                #REPLACE powerAngle with getVelocity()
                                #original has power angle insetead of velocity.getVelocity()
                                
                                power = (math.pi - velocity.getVelocity() ) * 20
                                rollVel = power
                            else:
                                if not superPower:  # Change power if we selected power ball
                                    m_vel1 = velocity.getVelocity()
                                    powerBar(True, m_vel1)
                                    redrawWindow(ballStationary, ballStationary2, line, False, False)
                                    
                                    
                                    
                                    power = (math.pi - m_vel1) * 40 * 4
                                else:
                                    m_vel1 = velocity.getVelocity()
                                    powerBar(True, m_vel1)
                                    redrawWindow(ballStationary, ballStationary2, line, False, False)

                                    

                                    power = (math.pi - m_vel1) * 40 * 4

                            if(player1_turn):
                                shootPos = ballStationary
                            else:
                                shootPos = ballStationary2
                            
                            powerLock = True
                            if(tutorial and tut_seq < 2):
                                tut_seq += 1
                                print(tut_seq)

                            #powerBar(True, 1.5)
                            #redrawWindow(ballStationary, ballStationary2, line, False, False)

                
                    

                            #Good Place to Switch Turns
                            #if(player1_turn):
                                #player1_turn = False
                            #else:
                                #player1_turn = True
                            #break

        if event.type == pygame.MOUSEMOTION:  # Change the position of the angle line
            pos = pygame.mouse.get_pos()
            angle = findAngle(pos)

            if(player1_turn):
                line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
            else:
                line = (round(ballStationary2[0] + (math.cos(angle) * 50)), round(ballStationary2[1] - (math.sin(angle) * 50)))

            if onGreen():  # If we are on green have the angle lin point towards the hole, bc putter cannot chip
                if(player1_turn):
                    if ballStationary[0] > flagx:
                        angle = math.pi
                        line = (ballStationary[0] - 30, ballStationary[1])
                    else:
                        angle = 0
                        line = (ballStationary[0] + 30, ballStationary[1])
                else:
                    if ballStationary2[0] > flagx:
                        angle = math.pi
                        line = (ballStationary2[0] - 30, ballStationary2[1])
                    else:
                        angle = 0
                        line = (ballStationary2[0] + 30, ballStationary2[1])

    redrawWindow(ballStationary, ballStationary2, line)
    hitting = False

    ####################################################################
    #SEND CLAUSE
    if (line != None):
        sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], False))
    else:
        sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), -1, -1, False))
    player2client.send(sendData)
    ####################################################################

    while put and not shoot:  # If we are putting
        # If we aren't in the hole

        if(player1_turn):
            if(  not(overHole(ballStationary[0], ballStationary[1]))  ):
                pygame.time.delay(20)
                rollVel -= 0.5  # Slow down the ball gradually
                if angle == math.pi:
                    ballStationary = (round(ballStationary[0] - rollVel), ballStationary[1])
                else:
                    ballStationary = (round(ballStationary[0] + rollVel), ballStationary[1])
                redrawWindow(ballStationary, ballStationary2, None, True)
                if rollVel < 0.5:  # Stop moving ball if power is low enough
                    
                    time = 0
                    put = False
                    pos = pygame.mouse.get_pos()
                    angle = findAngle(pos)
                    line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))

                    #Determine what way to point the angle line
                    if onGreen():
                        if ballStationary[0] > flagx:
                            angle = math.pi
                            line = (ballStationary[0] - 30, ballStationary[1])
                        else:
                            angle = 0
                            line = (ballStationary[0] + 30, ballStationary[1])
                    

                    if(player1_turn and hole_seq == 0):
                        print("1")
                        player1_turn = False
                    elif(player1_turn == False and hole_seq == 0):
                        print("2")
                        player1_turn = True
                    break
            else:
                tutorial = False
                #player1_turn = False

                hole_seq += 1
                print("hole seq 1")
                
                player1_turn = False

                if(h1 == 0):
                    h1 = 1
                    if SOUND:
                        inHole.play()
                    while True:  # Move ball so it looks like it goes into the hole (increase y value)
                        pygame.time.delay(20)
                        redrawWindow(ballStationary, ballStationary2, None, True)
                        ballStationary = (ballStationary[0], ballStationary[1] + 1)
                        if ballStationary[0] > hole[0]:
                            ballStationary = (ballStationary[0] - 1, ballStationary[1])
                        else:
                            ballStationary = (ballStationary[0] + 1, ballStationary[1])

                        if ballStationary[1] > hole[1] + 5:
                            put = False
                            break

                # Advance to score board
                if (h1 + h2 == 2):
                #hole_seq += 1
                    fade()
                    displayScore(strokes, par)
                    tutorial = False
                    strokes = 0
                    strokes_1 = 0
                    strokes_2 = 0
        else:
            if(  not(overHole(ballStationary2[0], ballStationary2[1]))  ):
                pygame.time.delay(20)
                rollVel -= 0.5  # Slow down the ball gradually
                if angle == math.pi:
                    ballStationary2 = (round(ballStationary2[0] - rollVel), ballStationary2[1])
                else:
                    ballStationary2 = (round(ballStationary2[0] + rollVel), ballStationary2[1])
                redrawWindow(ballStationary, ballStationary2, None, True)

                ####################################################################
                #SEND CLAUSE
                if (line != None):
                    sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], True))
                else:
                    sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, player1_turn, h2, player1attacked, player2attacked, powerUpPlayer2, -1, -1, True))
                player2client.send(sendData)
                #################################################################### 
                   
                if rollVel < 0.5:  # Stop moving ball if power is low enough
                    
                    time = 0
                    put = False
                    pos = pygame.mouse.get_pos()
                    angle = findAngle(pos)
                    line = (round(ballStationary2[0] + (math.cos(angle) * 50)), round(ballStationary2[1] - (math.sin(angle) * 50)))

                    #Determine what way to point the angle line
                    if onGreen():
                        if ballStationary2[0] > flagx:
                            angle = math.pi
                            line = (ballStationary2[0] - 30, ballStationary2[1])
                        else:
                            angle = 0
                            line = (ballStationary2[0] + 30, ballStationary2[1])
                    

                    if(player1_turn and hole_seq == 0):
                            print("1")
                            player1_turn = False
                    elif(player1_turn == False and hole_seq == 0):
                        print("2")
                        player1_turn = True
                    break
            else:
                tutorial = False
                #player1_turn = False

                hole_seq += 1
                print("hole seq 2")
                player1_turn = True
                if(h2 == 0):
                    h2 = 1
                    if SOUND:
                        inHole.play()
                    while True:  # Move ball so it looks like it goes into the hole (increase y value)
                        pygame.time.delay(20)
                        redrawWindow(ballStationary, ballStationary2, None, True)

                        ####################################################################
                        #SEND CLAUSE
                        if (line != None):
                            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], True))
                        else:
                            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), -1, -1, True))
                        player2client.send(sendData)
                        ####################################################################

                        ballStationary2 = (ballStationary2[0], ballStationary2[1] + 1)
                        if ballStationary2[0] > hole[0]:
                            ballStationary2 = (ballStationary2[0] - 1, ballStationary2[1])
                        else:
                            ballStationary2 = (ballStationary2[0] + 1, ballStationary2[1])

                        if ballStationary2[1] > hole[1] + 5:
                            put = False
                            break
                    ####################################################################
                    #SEND CLAUSE
                    if (line != None):
                        sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], False))
                    else:
                        sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), -1, -1, False))
                    player2client.send(sendData)
                    #################################################################### 

                # Advance to score board
                
                if (h1 + h2 == 2):
                #hole_seq += 1
                    fade()
                    displayScore(strokes, par)
                    tutorial = False
                    strokes = 0
                    strokes_1 = 0
                    strokes_2 = 0
                    #shoot = False
            
      
    #Implement Shooting into the hole? Make sure this works
    
    while shoot:  # If we are shooting the ball
        #PLAYER2 IN HOLE
        if ((overHole(ballStationary[0], ballStationary[1]) == False or overHole(ballStationary2[0], ballStationary2[1]) == False) and (h1 + h2 != 2)):  # If we aren't in the hole
            maxT = physics.maxTime(power, angle)
            time += 0.085
            #ballCords = physics.ballPath(ballStationary2[0], ballStationary2[1], power, angle, time)

            
            if(player1_turn):
                ballCords = physics.ballPath(ballStationary[0], ballStationary[1], power, angle, time)
                redrawWindow(ballCords, ballStationary2, None, True)
                #player1_turn = False
            else:
                ballCords = physics.ballPath(ballStationary2[0], ballStationary2[1], power, angle, time)
                redrawWindow(ballStationary, ballCords, None, True)

                ####################################################################
                #SEND CLAUSE
                if (line != None):
                    sendData = make_pos((ballCords[0],ballCords[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), line[0], line[1], True))
                else:
                    sendData = make_pos((ballCords[0],ballCords[1], strokes_2, h2, int(player1_turn), int(player1attacked), int(player2attacked), int(powerUpPlayer2), -1, -1, True))
                player2client.send(sendData)
                #################################################################### 

                #player1_turn = True

            # TO FIX GLITCH WHERE YOU GO THROUGH WALLS AND FLOORS
            if ballCords[1] > 650:
                ballCords = shootPos
                subtract = 0
                hazard = True
                if(player1_turn):
                    ballStationary = ballCords
                else:
                    ballStationary2 = ballCords
                time = 0
                pos = pygame.mouse.get_pos()
                angle = findAngle(pos)

                if(player1_turn):
                    line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
                else:
                    line = (round(ballStationary2[0] + (math.cos(angle) * 50)), round(ballStationary2[1] - (math.sin(angle) * 50)))
    
                power = 1
                powerAnglfe = math.pi
                shoot = False
                #strokes -= 1
                if(player1_turn):
                    strokes_1 -= 1
                else:
                    strokes_2 -= 1


                #USEFUL FOR POWERUP CALL OUTS
                label = myFont.render('Game Glitch, try again', 1, (255, 255, 255))
                if SOUND:
                    splash.play()
                win.blit(label, (winwidth / 2 - label.get_width() / 2, winheight / 2 - label.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(1500)
                #ballColor = (255,255,255)
                #stickyPower = False
                #mullagain = False
                #superPower = False
                break

            # COLLISION LOOP, VERY COMPLEX,
            # - All angles are in radians
            # - Physics are in general real and correct

            for i in objects:  # for every object in the level
                if i[4] == 'coin':  # If the ball hits a coin
                    if i[5]:
                        if(tutorial == False or tut_seq > 1 ):
                            if ballCords[0] < i[0] + i[2] and ballCords[0] > i[0] and ballCords[1] > i[1] and ballCords[1] < i[1] + i[3]:
                                print("Level: ", level)
                                courses.coinHit(level - 1)
                                coins += 1
                                print("HIT COIN")
                                if(player1_turn):
                                    tut_seq = 3
                                    powerUpPlayer1 = True
                                    if(tutorial):
                                        powerUpPlayer2 = True
                                if(player1_turn == False):
                                    tut_seq = 4
                                    powerUpPlayer2 = True
                                    if(tutorial):
                                        powerUpPlayer1 = True

                if i[4] == 'laser':  # if the ball hits the laser hazard
                    if ballCords[0] > i[0] and ballCords[0] < i[0] + i[2] and ballCords[1] > i[1] and ballCords[1] < i[1] + i[3]:
                        ballCords = shootPos
                        hazard = True
                        subtract = 0
                        ballStationary = ballCords
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)

                        
                        line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                round(ballStationary[1] - (math.sin(angle) * 50)))
                        power = 1
                        powerAngle = math.pi
                        shoot = False
                        strokes += 1

                        label = myFont.render('Laser Hazard, +1 stroke', 1, (255, 255, 255))
                        win.blit(label, (winwidth / 2 - label.get_width() / 2, winheight / 2 - label.get_height() / 2))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        ballColor = (255,255,255)

                        stickyPower = False
                        superPower = False
                        mullagain = False
                        break

                elif i[4] == 'water':
                    if ballCords[1] > i[1] - 6 and ballCords[1] < i[1] + 8 and ballCords[0] < i[0] + i[2] and ballCords[0] > i[0] + 2:
                        ballCords = shootPos
                        subtract = 0
                        hazard = True
                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)

                        if(player1_turn):
                            line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
                        else:
                            line = (round(ballStationary2[0] + (math.cos(angle) * 50)), round(ballStationary2[1] - (math.sin(angle) * 50)))
            
                        power = 1
                        powerAngle = math.pi
                        shoot = False
                        strokes += 1

                        #USEFUL FOR POWERUP CALL OUTS
                        label = myFont.render('Water Hazard, +1 stroke', 1, (255, 255, 255))
                        if SOUND:
                            splash.play()
                        win.blit(label, (winwidth / 2 - label.get_width() / 2, winheight / 2 - label.get_height() / 2))
                        pygame.display.update()
                        pygame.time.delay(1500)
                        ballColor = (255,255,255)
                        stickyPower = False
                        mullagain = False
                        superPower = False
                        break

                elif i[4] != 'flag' and i[4] != 'coin':
                    
                    if ballCords[1] > i[1] - 2 and ballCords[1] < i[1] + 7 and ballCords[0] < i[0] + i[2] and ballCords[0] > i[0]:
                        hitting = False
                        #THIS IS THE COLLISION LOOP FOR THE GROUND
                        
                        

                        power = physics.findPower(power, angle, time)
                        if angle > math.pi * (1/2) and angle < math.pi:
                            x = physics.findAngle(power, angle)
                            angle = math.pi - x
                        elif angle < math.pi / 2:
                            angle = physics.findAngle(power, angle)
                        elif angle > math.pi and angle < math.pi * (3/2):
                            x = physics.findAngle(power, angle)
                            angle = math.pi - x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = x

                        power = power * 0.5
                        
                        if time > 0.15:
                            time = 0
                        subtract = 0
                        while True:
                            subtract += 1
                            if ballCords[1] - subtract < i[1]:
                                
                                
                                ballCords = (ballCords[0], ballCords[1] - subtract)
                                break

                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords
                        

                        if i[4] == 'sand':
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[1] - subtract < i[1] - 4:
                                    
                                    ballCords = (ballCords[0], ballCords[1] - subtract)
                                    power = 0
                                    break

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[1] - subtract < i[1] - 4:
                                    
                                    ballCords = (ballCords[0], ballCords[1] - subtract)
                                    power = 0
                                    break


                            if(player1_turn):
                                ballStationary = ballCords
                            else:
                                ballStationary2 = ballCords
                            shoot = False
                            time = 0
                            pos = pygame.mouse.get_pos()
                            angle = findAngle(pos)
                            if(player1_turn):
                                line = (round(ballStationary[0] + (math.cos(angle) * 50)),
                                    round(ballStationary[1] - (math.sin(angle) * 50)))
                            else:
                                line = (round(ballStationary2[0] + (math.cos(angle) * 50)),
                                    round(ballStationary2[1] - (math.sin(angle) * 50)))
                            
                            

                            power = 1
                            powerAngle = math.pi


                    elif ballCords[1] < i[1] + i[3] and ballCords[1] > i[1] and ballCords[0] > i[0] - 2 and ballCords[0] < i[0] + 10:
                        
                        hitting = False
                        power = physics.findPower(power, angle, time)
                        if angle < math.pi / 2:
                            if not(time > maxT):
                                x = physics.findAngle(power, angle)
                                angle = math.pi - x
                            else:
                                x = physics.findAngle(power, angle)
                                angle = math.pi + x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = math.pi + x


                        power = power * 0.5

                        if time > 0.15:
                            time = 0
                        subtract = 0

                        while True:
                            subtract += 1
                            if ballCords[0] - subtract < i[0] - 3:
                                
                                ballCords = (ballCords[0] - subtract, ballCords[1])
                                break
                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] - subtract < i[0] - 3:
                                    
                                    ballCords = (ballCords[0] - subtract, ballCords[1])
                                    power = 0
                                    break

                    elif ballCords[1] < i[1] + i[3] and ballCords[1] > i[1] and ballCords[0] > i[0] + i[2] - 16 and ballCords[0] < i[0] + i[2]:
                        hitting = False

                        power = physics.findPower(power, angle, time)
                        if angle < math.pi:
                            if not (time > maxT):
                                angle = physics.findAngle(power, angle)
                            else:
                                x = physics.findAngle(power, angle)
                                angle = math.pi * 2 - x
                        else:
                            x = physics.findAngle(power, angle)
                            angle = math.pi * 2 - x

                        #Power is divided by 2
                        power = power * 0.5

                        if time > 0.15:
                            time = 0
                        subtract = 0

                        while True:
                            subtract += 1
                            if ballCords[0] + subtract > i[0] + i[2] + 4:
                                
                                ballCords = (ballCords[0] + subtract, ballCords[1])
                                break
                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords

                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] + subtract > i[0] + i[2] + 4:
                                    
                                    ballCords = (ballCords[0] + subtract, ballCords[1])
                                    power = 0
                                    break



                    elif ballCords[1] > i[1] + i[3]and ballCords[0] + 2 > i[0] and ballCords[1] < i[1] + i[3] + 10 and ballCords[0] < i[0] + i[2] + 2:
                        power = physics.findPower(power, angle, time)
                        if not(hitting):
                            hitting = True
                            if angle > math.pi / 2:
                                x = physics.findAngle(power, angle)
                                angle = math.pi + x
                            else:
                                x = physics.findAngle(power, angle)
                                angle = 2 * math.pi - x

                        #Power divided by 2
                        power = power * 0.5
                        if time > 0.04:
                            time = 0

                        subtract = 0
                        while True:
                            subtract += 1
                            if ballCords[1] + subtract > i[1] + i[3] + 8:
                                ballCords = (ballCords[0], ballCords[1] + subtract)
                                break
                        if i[4] == 'sticky' or stickyPower:
                            subtract = 0
                            while True:
                                subtract += 1
                                if ballCords[0] + subtract > i[1] + i[3] + 4:
                                    
                                    ballCords = (ballCords[0], ballCords[1] + subtract)
                                    power = 0
                                    break
                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords
                    if power < 2.5:
                        subtract = 0
                        pygame.display.update()
                        if(player1_turn):
                            ballStationary = ballCords
                        else:
                            ballStationary2 = ballCords
                        shoot = False
                        time = 0
                        pos = pygame.mouse.get_pos()
                        angle = findAngle(pos)

                        if(player1_turn):
                            line = (round(ballStationary[0] + (math.cos(angle) * 50)), round(ballStationary[1] - (math.sin(angle) * 50)))
                        else:
                            line = (round(ballStationary2[0] + (math.cos(angle) * 50)), round(ballStationary2[1] - (math.sin(angle) * 50)))                        
                        
                        
                        power = 1
                        powerAngle = math.pi
                        if(player1_turn):
                            ballColor = (255,255,255)
                        else:
                            ballColor2 = (255,0,0)
                        stickyPower = False
                        mullagain = False
                        superPower = False

                        #Good Place to Switch Turns
                        if(player1_turn and h1 != 1):
                            player1_turn = False

                        elif(player1_turn == False and h2 != 1):
                            player1_turn = True
                        break
                        
        if(overHole(ballStationary[0], ballStationary[1]) == True):
           
            if(player1_turn):
                
                #tutorial = False
                player1_turn = False
                if(h1 == 0):
                    h1 = 1
                    if SOUND:
                        inHole.play()
                    var = True
                    while var:
                        pygame.time.delay(20)
                        redrawWindow(ballStationary, ballStationary2, None, True)
                        ballStationary = (ballStationary[0], ballStationary[1] + 1)
                        if ballStationary[0] > hole[0]:
                            ballStationary = (ballStationary[0] - 1, ballStationary[1])
                        else:
                            ballStationary = (ballStationary[0] + 1, ballStationary[1])

                        if ballStationary[1] > hole[1] + 5:
                            shoot = False
                            var = False

                            
        if(overHole(ballStationary2[0], ballStationary2[1]) == True):
               
            #tutorial = False
            #player1_turn = True
            if(player1_turn == False):
                
                #tutorial = False
                player1_turn = True
                if(h2 == 0):
                    h2 = 1
                    if SOUND:
                        inHole.play()
                    var = True
                    while var:
                        pygame.time.delay(20)
                        redrawWindow(ballStationary, ballStationary2, None, True)

                        ####################################################################
                        #SEND CLAUSE
                        if (line != None):
                            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, player1_turn, h2, player1attacked, player2attacked, powerUpPlayer2, line[0], line[1], True))
                        else:
                            sendData = make_pos((ballStationary2[0],ballStationary2[1], strokes_2, player1_turn, h2, player1attacked, player2attacked, powerUpPlayer2, -1, -1, True))
                        player2client.send(sendData)
                        #################################################################### 

                        ballStationary2 = (ballStationary2[0], ballStationary2[1] + 1)
                        if ballStationary2[0] > hole[0]:
                            ballStationary2 = (ballStationary2[0] - 1, ballStationary2[1])
                        else:
                            ballStationary2 = (ballStationary2[0] + 1, ballStationary2[1])

                        if ballStationary2[1] > hole[1] + 5:
                            shoot = False
                            var = False
            
                    
        if (h1 + h2 == 2):
            #hole_seq += 1
                
                
                fade()
                displayScore(strokes, par)
                tutorial = False
                strokes = 0
                strokes_1 = 0
                strokes_2 = 0
               
           
            

    if onGreen():
        if(player1_turn):
            if ballStationary[0] > flagx:
                angle = math.pi
                line = (ballStationary[0] - 30, ballStationary[1])
            else:
                angle = 0
                line = (ballStationary[0] + 30, ballStationary[1])
        else:
            if ballStationary2[0] > flagx:
                angle = math.pi
                line = (ballStationary2[0] - 30, ballStationary2[1])
            else:
                angle = 0
                line = (ballStationary2[0] + 30, ballStationary2[1])


pygame.quit()
