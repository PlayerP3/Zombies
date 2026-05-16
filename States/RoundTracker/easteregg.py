import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from statemachine import State

class EasterEgg(State):

    def __init__(self):
        State.__init__(self)