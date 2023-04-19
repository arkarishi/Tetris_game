"""
                       Tetris
                         by
               Aditi Saxena & Ajesh Sharma 
          [RA2211026010402]   [RA2211026010383]
                   Section - W2
             Specialisation - AI & ML
  Subject - Programming for problem solving [21CSS101J]
"""
#import modules
import random
from pyray import *

#setting board variable
size = 30
x,y = 30,15

#initialising/creating the screen
set_trace_log_level(LOG_NONE)
init_window(x*size,y*size, "Tetris")

#printing the doc of the file
print(__doc__)

#function to create table
def grid_table(x,y):
    playArea = []
    for i in range(y):
        temp = []
        for j in range(x):
            temp.append(0)
        playArea.append(temp)
    return playArea

#making the board
playGround = grid_table(x, y)

#players score and number of players decider
players =[0,0,0]

#player controls
moves = [[KEY_A,KEY_D,KEY_S],
    [KEY_LEFT,KEY_RIGHT,KEY_DOWN],
    [KEY_I,KEY_P,KEY_O],
    [KEY_B,KEY_M,KEY_N]]

#timer
timer = 0

#function to spawn a new block
def spawn(table,i):
    players[i - 1] += 100

    e = random.randint(1,len(playGround[1]) - 2)
    randomNumber = random.randint(1,6)
    if randomNumber == 1:
        table[2][e] = i
        table[2][e + 1] = i
        table[2][e - 1] = i
    if randomNumber == 2:
        table[2][e] = i
        table[1][e + 1] = i
        table[3][e - 1] = i
    if randomNumber == 3:
        table[2][e] = i
        table[3][e] = i
        table[3][e + 1] = i
        table[3][e - 1] = i
    if randomNumber == 4:
        table[2][e] = i
        table[3][e] = i
        table[2][e+1] = i
        table[3][e+1] = i
    if randomNumber == 5:
        table[2][e + 1] = i
        table[2][e] = i
        table[2][e - 1] = i
        table[3][e - 1] = i
    if randomNumber == 6:
        table[2][e] = i
        table[3][e] = i
        table[3][e + 1] = i
        table[2][e - 1] = i

#spawining the first batch of blocks
for i in range(len(players)):
    spawn(playGround,i + 1)

#function to spawn if a player is not on board
def emptyCheck():
    for p in range(len(players)):
        temp = True
        for i in range(len(playGround)):
            for j in range(len(playGround[1])):
                if playGround[i][j] == p + 1:
                    temp = False
                    break

        if temp:
            spawn(playGround,p + 1)

#function to check if a players can move down, returns true if can move
def checkDown(playNum):
    toReturn = True
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if playGround[i][j] == playNum:
                if i == len(playGround) - 1:
                    toReturn = False
                    break
                if playGround[i + 1][j] == -1:
                    toReturn = False
                    break
        
    return toReturn

#function to check if a players can move right, returns true if can move
def checkRight(playNum):
    toReturn = True
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if playGround[i][j] == playNum:
                if j != len(playGround[0]) - 1:
                    if playGround[i][j + 1] == -1:
                        toReturn = False
                        break
                else:
                    toReturn = False
                    break

    return toReturn
    
#function to check if a players can move left, returns true if can move
def checkLeft(playNum):
    toReturn = True
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if playGround[i][j] == playNum:
                if j != 0:
                    if playGround[i][j - 1] == -1:
                        toReturn = False
                        break
                else:
                    toReturn = False
                    break
        
    return toReturn

#moves player right
def moveRight(playNum):
    temp = playGround
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if temp[i][-j] == playNum:
                playGround[i][-j] = 0
                playGround[i][-j + 1] = playNum

#moves player left
def moveLeft(playNum):
    temp = playGround
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if temp[i][j] == playNum:
                playGround[i][j] = 0
                playGround[i][j - 1] = playNum

#moves player right
def moveDown(playNum):
    temp = playGround
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if temp[-i][j] == playNum:
                playGround[-i][j] = 0
                playGround[-i + 1][j] = playNum

#checks keypressed by player and moves players accordingly
def movement():
    temp = playGround
    for p in range(len(players)):
        if is_key_pressed(moves[p][0]):
            if checkLeft(p + 1):
                moveLeft(p + 1)

        if is_key_pressed(moves[p][1]):
            if checkRight(p + 1):
                moveRight(p + 1)
        
        if is_key_pressed(moves[p][2]):
            if checkDown(p + 1):
                moveDown(p + 1)

#convert player to dead block
def deathConvert(playNum):
    for i in range(len(playGround)):
        for j in range(len(playGround[1])):
            if playGround[i][j] == playNum:
                playGround[i][j] = -1

#check if any players should be dead
def deathCheck():
    for p in range(len(players)):
        if not checkDown(p + 1):
            deathConvert(p + 1)
            players[p] += 100
            spawn(playGround,p + 1)

#draws the player score list
def drawScore():
    draw_text(f"{players}",0,0,20,GRAY)

#moves all player down        
def gravity():
    for p in range(len(players)):
        if checkDown(p + 1):
            moveDown(p + 1)

#if a row is fully dead,clears row and moves all blocks down 
def clearRow():
    clear = []
    temp = []
    for j in range(x):
        temp.append(-1)
        clear.append(0)
    for i in range(len(playGround)):
        if playGround[i] == temp:
            
            playGround[i] = clear
            for j in range(1,len(playGround) - 1):
                playGround[-j] = playGround[-j-1]
            playGround[0] = clear

#draw each player colorwise 
def draw():
    for i in range(len(playGround)):
        for j in range(len(playGround[0])):
            if playGround[i][j] == -1:
                draw_rectangle(j*size,i*size,size,size,GRAY)
            if playGround[i][j] == 1:
                draw_rectangle(j*size,i*size,size,size,RED)
            if playGround[i][j] == 2:
                draw_rectangle(j*size,i*size,size,size,GREEN)
            if playGround[i][j] == 3:
                draw_rectangle(j*size,i*size,size,size,BLUE)
            if playGround[i][j] == 4:
                draw_rectangle(j*size,i*size,size,size,PURPLE)
            if playGround[i][j] == 5:
                draw_rectangle(j*size,i*size,size,size,PINK)
            if playGround[i][j] == 6:
                draw_rectangle(j*size,i*size,size,size,CYAN)



#main working loop
while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    movement()
    emptyCheck()
    draw()
    timer += get_frame_time()
    if timer > 0.5:
        timer = 0
        gravity()
        deathCheck()

    clearRow()
    drawScore()
    end_drawing()
close_window()
