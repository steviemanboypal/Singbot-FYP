from __future__ import print_function
import numpy as np
import tensorflow as tf
import pygame
import pygame.midi
from pygame.locals import *
from pygame import midi
from pygame.midi import Input
import sample
from sys import exit
import os

pygame.font.init()

background_colour = (255,255,255)
(width, height) = (1280, 720)
search = ""
img = pygame.image.load('musicbackground.bmp')
myfont1 = pygame.font.SysFont("arial", 80)
myfont2 = pygame.font.SysFont("arial", 60)
myfont3 = pygame.font.SysFont("arial", 30)
menu1 = myfont1.render("Write Song", 1, (0,0,255))
menu2 = myfont2.render("Train Machine", 1, (0,0,255))
menu3 = myfont2.render("Build Database", 1, (0,0,255))


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Singbot')
screen.fill(background_colour)


running = True
while running:
    xylaphone = search
    cirColA = (255,0,0)
    cirColB = (255,0,0)
    cirColC = (255,0,0)
    (mouseX, mouseY) = pygame.mouse.get_pos()
    if 900 > mouseX > 570 and 180 > mouseY > 100:
        cirColA = (255,255,0)
    if 900 > mouseX > 570 and 280 > mouseY > 220:
        cirColB = (255,255,0)
    if 900 > mouseX > 570 and 385 > mouseY > 325:
        cirColC = (255,255,0)

    screen.blit(img, (0,0))
    screen.blit(menu1, (600, 100))
    pygame.draw.circle(screen, cirColA, (580, 125), 10, 0)
    screen.blit(menu2, (600, 215))
    pygame.draw.circle(screen, cirColB, (580, 235), 10, 0)
    screen.blit(menu3, (600, 325))
    pygame.draw.circle(screen, cirColC, (580, 345), 10, 0)
    menu4 = myfont3.render("Search:" + " " + search, 1, (50,150,50))
    screen.blit(menu4, (620, 370))
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            if 900 > mouseX > 570 and 180 > mouseY > 100:
                os.system('python sample.py')
            if 900 > mouseX > 570 and 275 > mouseY > 215:
                os.system('python train.py')
            if 900 > mouseX > 570 and 385 > mouseY > 325:
                os.system('python learn.py '+ search)
        if event.type == pygame.KEYDOWN:
            search = search + event.unicode
            if pygame.key.get_pressed()[K_BACKSPACE]:
                search = ""



