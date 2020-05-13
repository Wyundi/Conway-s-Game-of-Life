# !/usr/bin/env python
# -  *  - coding:utf-8 -  *  - 

import numpy as np
import random

import pygame
from pygame.locals import *
from sys import exit
import time

np.set_printoptions(threshold=np.nan)       #改变阈值 使numpy可以完整打印

#参数
Game_colom = 25                             #宽度
Game_row = 15                               #高度
times = 16                                  #倍数
Pixel_colom = Game_colom * times            #像素宽度
Pixel_row = Game_row * times                #像素高度
Block_size = times - 5                      #块大小
Sleep_Time = 0.05                           #刷新速度
Pause = False                               #暂停计数器

matrix = np.zeros([Game_colom,Game_row], dtype = int)
matrix_temp = np.zeros([Game_colom,Game_row], dtype = int)

# 颜色
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)

#初始化pygame
pygame.init()
screen = pygame.display.set_mode((Pixel_colom, Pixel_row))
pygame.display.set_caption('''Conway's Game of Life''')

def init_matrix(n = 1):
    for j in range(Game_row):
        for i in range(Game_colom):
            if n == 1:
                matrix[i,j] = random.randint(0,1)
            else:
                matrix[i,j] = 0

def init_screen():
    screen.fill(WHITE)

    for m in range(Game_colom + 1):
        pygame.draw.line(screen, BLACK, 
                        [times*m, 0], [times*m, Pixel_row], 1)

    for n in range(Game_row + 1):
        pygame.draw.line(screen, BLACK, 
                        [0, times*n], [Pixel_colom, times*n], 1)

    for i in range(Game_colom):
        matrix[i,0] = 0
        matrix[i,Game_row-1] = 0
    
    for j in range(Game_row):
        matrix[0,j] = 0
        matrix[Game_colom-1,j] = 0                          #初始化屏幕

def Calculate():
    for j in range(Game_row):
        for i in range(Game_colom):
            if i != 0 and j != 0 and \
            i != Game_colom - 1 and j != Game_row - 1:
                data = sum([matrix[i-1,j-1],matrix[i-1,j],matrix[i-1,j+1],
                    matrix[ i ,j-1],              matrix[ i ,j+1],
                    matrix[i+1,j-1],matrix[i+1,j],matrix[i+1,j+1]])

                matrix_temp = matrix

                #rules
                if matrix[i,j] == 1 and data < 2:
                    matrix_temp[i,j] = 0
                elif matrix[i,j] == 1 and data == 2:
                    matrix_temp[i,j] = 1
                elif matrix[i,j] == 1 and data == 3:
                    matrix_temp[i,j] = 1
                elif matrix[i,j] == 1 and data > 3:
                    matrix_temp[i,j] =0
                elif matrix[i,j] == 0 and data == 3:
                    matrix_temp[i,j] = 1
                elif matrix[i,j] == 0 and data == 2:
                    matrix_temp[i,j] = 0
                else:
                    matrix_temp[i,j] = 0

    return matrix_temp                  #刷新矩阵

def Print_block():
    for j in range(Game_row):
        for i in range(Game_colom):
            #time.sleep(Sleep_Time)
            #pygame.display.update()
            if matrix[i,j] == 0:
                pygame.draw.rect(screen, WHITE, 
                                [times*i+3, times*j+3, 
                                Block_size, Block_size])
            else:
                pygame.draw.rect(screen, BLACK, 
                                [times*i+3, times*j+3, 
                                Block_size, Block_size])       #打印矩阵

init_matrix()

init_screen()

while True:
    if Pause == False:
        matrix = Calculate()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Pause = not Pause
            if event.key == K_s:
                init_matrix(0)
                Print_block()
                pygame.display.update()
            if event.key == K_r:
                init_matrix(1)
                Print_block()
                pygame.display.update()
        if event.type == MOUSEBUTTONDOWN:
            i = int(event.pos[0]/times)
            j = int(event.pos[1]/times)
            
            matrix[i,j] = not matrix[i,j]

            Print_block()
            pygame.display.update()

    time.sleep(Sleep_Time)

    Print_block()        
    pygame.display.update()
