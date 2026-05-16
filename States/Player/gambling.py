import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from game import engine
from statemachine import State

class Gambling(State):

    def __init__(self):
        State.__init__()

    def enter(self):

        # set acceleration to base value

        pass

    def update(self):
        
        # run move and collide
        self.move_and_collide()
        
        pass

    def completed(self):
        return super().completed()