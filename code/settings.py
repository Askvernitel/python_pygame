import pygame 
from os.path import join
from os import walk
from math import atan2, degrees
from random import randint
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

MAX_FRAMERATE = 60

GROUND_Y_COORDINATE=SCREEN_HEIGHT - 45