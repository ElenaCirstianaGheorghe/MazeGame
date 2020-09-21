import msvcrt
import os
import time
import sys
from time import *
import threading
import random

def clear():
    ''' It clears the screen.'''

    os.system('cls')

def RemainingTime():
    ''' It displays the time left until the begining of the game.'''

    print(f"Level {level} starts in: \n")
    for remaining in range(3, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d}".format(remaining))
        sys.stdout.flush()
        sleep(1)
    clear()

def Countdown():
    ''' It initializes a timer for the player to check the time left for the
    current level.'''

    global my_timer
    my_timer = time_level
    for x in range(my_timer):
        my_timer = my_timer - 1
        sleep(1)

def InitMatrix():
    '''It initializes the board game (matrix) that includes the level elements from
    the adequate text file.'''

    elem_list = []
    for line in level_read:
        for chr in line:
            if chr != "\n":
                elem_list.append(chr)

    elem_list = [int(elem) for elem in elem_list]

    m = [[0 for i in range(24)] for j in range(24)]

    x = 0
    for i in range(24):
        for j in range(24):
            m[i][j] = elem_list[x]
            x += 1

    return m

def ShowMatrix():
    '''It displays the matrix.'''

    for i in range(24):
        for j in range(24):
            if m[i][j] == 0:
                print(" ", end = " ")
            elif m[i][j] == 1:
                print("=", end = " ")
            elif m[i][j] == 9:
                print(" ", end = " ")
            else:
                print("@", end = " ")
        print("")

def FindPlayer():
    ''' It finds the player (digit 6) and returns its position.'''

    for i in range(24):
        for j in range(24):
            if m[i][j] == 6:
                lin = i
                col = j
                break

    return lin, col

def FindExit():
    ''' It finds the maze exit point (digit 0) and returns its position.'''

    for i in range(24):
        for j in range(24):
            if m[i][j] == 9:
                final_lin = i
                final_col = j
                break

    return final_lin, final_col

def MoveLeft():
    ''' It moves the "@" element to the left when left key is pressed.'''

    global col
    if ((col-1) != -1) and (m[lin][col-1] != 1):
        m[lin][col-1] = 6
        m[lin][col] = 0
        col -= 1

def MoveRight():
    ''' It moves the "@" element to the right when right key is pressed.'''

    global col
    if ((col + 1) != 24) and (m[lin][col+1] != 1):
        m[lin][col+1] = 6
        m[lin][col] = 0
        col += 1

def MoveUp():
    ''' It moves the "@" element to the upper side when up key is pressed.'''

    global lin
    if ((lin - 1) != -1) and (m[lin-1][col] != 1):
        m[lin-1][col] = 6
        m[lin][col] = 0
        lin -= 1

def MoveDown():
    ''' It moves the "@" element to the bottom when left dowm is pressed.'''

    global lin
    if ((lin + 1) != 24) and (m[lin+1][col] != 1):
        m[lin+1][col] = 6
        m[lin][col] = 0
        lin += 1

def PlayMaze():
    ''' It reads the keys that are pressed and executes the specific function and if
    the player reaches the exit point displays the level completed message.'''

    global my_timer, points, points_level, y, z

    while my_timer >= 0:

        clear()
        ShowMatrix()
        print("\nTIMER\n")
        print(f"{my_timer} sec")

        keypress = ord(msvcrt.getch())
        if keypress == 224:
            keypress = ord(msvcrt.getch())

        if keypress == 75:
            MoveLeft()
        if keypress == 72:
            MoveUp()
        if keypress == 77:
            MoveRight()
        if keypress == 80:
            MoveDown()
        if keypress == 27: # ESC
            quit()
        if my_timer == 0:
            break

        if (lin == lin_final) and (col == col_final):
            my_timer = -1
            points = points + points_level
            clear()
            print(f"LEVEL COMPLETED!\n\nSCORE:{points}")

def TimeIsUp():
    ''' If the time expires, the game ends, the score is saved in a text file and
    the high score from the text file is displayed on the screen.'''

    global my_timer, points
    if (my_timer == 0):
        print(f"TIME IS UP!\n\nFINAL SCORE: {points}")
        with open("Score.txt", "a") as scorefile: #don't forget to write the path for the directory where the Score file is stored 
            scorefile.write(f" {str(max_value)}")
        with open("Score.txt", "r") as scorefile2: #don't forget to write the path for the directory where the Score file is stored 
            score_read = scorefile2.read()
            list_score = score_read.split()
            list_score = [int(elem) for elem in list_score]
            print(f"\nHigh score: {max(list_score)}")
        quit()

def FinalLevel():
    ''' It displays a congratulation massage if the player accomplishes the last level,
    saves the score in a text file and shows the high score from the text file.'''

    global my_timer, points
    if my_timer < 0 and points == 2800:
        clear()
        print(f"YOU HAVE WON!\n\nFINAL SCORE: {points}")
        with open("Score.txt", "a") as scorefile: #don't forget to write the path for the directory where the Score file is stored 
            scorefile.write(f" {str(max_value)}")
        with open("Score.txt", "r") as scorefile2: #don't forget to write the path for the directory where the Score file is stored 
            score_read = scorefile2.read()
            list_score = score_read.split()
            list_score = [int(elem) for elem in list_score]
            print(f"\nHigh score: {max(list_score)}")
        quit()



#==================================================================

points = 0
points_level = 100
time_level = 40

for i in range(7):

    level = i + 1

    with open(f"D:/Work/PROJECTS/Jocuri/Labirint/Level {str(level)}.txt", "r") as level_file:
        level_read = level_file.readlines()

    m = InitMatrix()
    lin, col = FindPlayer()
    lin_final, col_final = FindExit()

    print(f"Level {level}\n\nTime: {time_level} sec\n\nLevel score: {points_level}")
    sleep(3)
    clear()
    RemainingTime()

    countdown_thread = threading.Thread(target = Countdown)
    countdown_thread.start() 

    PlayMaze()
    TimeIsUp()
    FinalLevel()
    sleep(3)
    clear()

    # points_level and time_level increase when a level is completed 
    points_level += 100 
    time_level += 10
