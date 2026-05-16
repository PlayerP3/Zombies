import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from statemachine import State
import numpy as np

class RoundEnd(State):

    def __init__(self):
        State.__init__(self)

    
    def enter(self):
        
        # set reloading animation stuff
        self.timer_init()
        self.timer_complete = False

        # self.parent_node.connected_hud.text_colour = 'white'
        self.parent_node.connected_hud.alpha = 0
        

    # keep track of time between rounds
    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run timer
        self.run_timer()

        # flicker alpha for connected hud
        self.parent_node.connected_hud.alpha = np.clip(255 * self.map_to_sine_wave(),0,255)

        # if timer complete add number to rounds and move to before round start
        if self.timer_complete:
            self.emit('ROUNDSTART')

    

        


    def completed(self):

        self.done = False
        self.next_state = None