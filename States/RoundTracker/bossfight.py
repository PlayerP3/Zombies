import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from engine.statemachine import State

class BossFight(State):

    def __init__(self):
        State.__init__(self)

    
    def enter(self):
        
        # set reloading animation stuff
        self.timer_init()
        self.timer_complete = False

    # keep track of time between rounds
    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run timer
        self.run_timer()

        # if timer complete add number to rounds and move to before round start
        if self.timer_complete:
            self.emit('ROUNDSTART')

    

        


    def completed(self):

        self.parent_node.round_number += 1
        self.done = False
        self.next_state = None