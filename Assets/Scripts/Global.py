from random import *
from math import *
import pygame
import os
import json
pygame.init()

texts={}
fonts={}
def produce(text="TEXT NOT FOUND",size=20,color=(255,255,255),font="courier new"):
    font_key=str(size)+str(font)
    text_key=str(text)+str(size)+str(color)+str(font)
    if not font_key in fonts:
        fonts[font_key]=pygame.font.SysFont(font,int(size))
    if not text_key in texts:
        texts[text_key]=fonts[font_key].render(str(text),1,color)
    return texts[text_key]
def center(sprite,surface,x,y):
    sprite.set_colorkey((0,0,1))
    surface.blit(sprite,(x-sprite.get_width()/2,y-sprite.get_height()/2))
croll=lambda x:int(-log(random(),x))