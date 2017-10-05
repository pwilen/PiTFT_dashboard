#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author: jeremyblythe, peterwilen
'''
import homeassistant.remote as remote
import sys, pygame
from pygame.locals import *
import os
import locale
import subprocess
import time
import random
from time import sleep
from time import strftime

locale.setlocale(locale.LC_TIME, "sv_SE.utf8") #swedish
os.putenv('SDL_FBDEV', '/dev/fb1')#PiTFT

#set up Home Assistant API
api = remote.API('127.0.0.1', 'PASSWD') #Adress to Home assistant and Password
sleep(60)#without sleep it chrashes
#class pyscope
class pyscope :
    screen = pygame.display.set_mode((320, 240))
    #Set text rectangles
    text_rect1 = pygame.Rect(60, 20, 300, 60)
    text_rect2 = pygame.Rect(60, 80, 300, 60)
    text_rect3 = pygame.Rect(60, 160, 300, 60)
   
    def renderDate(self):
         currentTimeLine2 = strftime("%a  %d  %b", time.localtime())
         font = pygame.font.Font("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 46)
         text_surface2 = font.render(currentTimeLine2, True, (255, 255, 255))
         # Blit the text at 60, 90
         self.screen.blit(text_surface2, self.text_rect1)

    def renderTime(self):
         currentTimeHour = strftime("%H", time.localtime())
         currentTimeMinutes = strftime("%M", time.localtime())
         font = pygame.font.Font("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 60)
         text_surface1 = font.render(currentTimeHour +":" +currentTimeMinutes, True, (255, 255, 255))  # White text
         # Blit the text at 100, 100
         self.screen.blit(text_surface1, self.text_rect2)
        
    def renderTemp_Outside(self):
         outside_temperature = remote.get_state(api, 'sensor.weather_temperature')
         print(outside_temperature.state)
         font = pygame.font.Font("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 46)
         text_surface3 = font.render("Ute: " +str(outside_temperature.state) +" "+u"\u00B0" , True, (255, 255, 255)) #u"u2103" DEGREES CELCIUS
         # Blit the text at 60, 140
         self.screen.blit(text_surface3, self.text_rect3)

    def renderTemp_Inside(self):
         inside_temperature = remote.get_state(api, 'sensor.hall_temperature')
         print(inside_temperature.state)
         font = pygame.font.Font("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 46)
         text_surface3 = font.render("Inne: " +str(inside_temperature.state) +" "+u"\u00B0" , True, (255, 255, 255)) #u"u2103" DEGREES CELCIUS
         # Blit the text at 60, 140
         self.screen.blit(text_surface3, self.text_rect3)
   
pygame.init()
pygame.mouse.set_visible(False)
pygame.font.init()

# Create an instance of the PyScope class
scope = pyscope()
while True:
    t_end = time.time() + 60    # refresh rate in sec 
    ev = pygame.event.poll()    # Look for any event
    if ev.type == pygame.QUIT:  # Window close button clicked?
       break                   #   ... leave game loop
    lcd = pygame.display.set_mode((320, 240))
    lcd.fill((0,0,0))
    scope.renderDate()
    scope.renderTemp_Outside()
    pygame.display.update()
    while time.time() < t_end: #time less than t_end starting with 60 sec
        pygame.draw.rect(scope.screen, (0,0,0), scope.text_rect2)
        scope.renderTime()
        pygame.display.update(scope.text_rect2)
    sleep(60)
    scope.renderTemp_Inside
    pygame.display.update(scope.text_rect3)
pygame.quit()     # Once we leave the loop, close the window.
