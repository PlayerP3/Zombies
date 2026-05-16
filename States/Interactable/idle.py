import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from game import engine
from statemachine import State


class Idle(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        
        

        pass

    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.hurtbox.center)
        self.parent_node.draw_rect(position=self.parent_node.hurtbox.center)

        

