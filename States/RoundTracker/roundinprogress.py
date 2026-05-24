import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from engine.statemachine import State

class RoundInProgress(State):

    def __init__(self):
        State.__init__(self)


    def enter(self):
        
        # set reloading animation stuff
        self.timer_init()
        self.timer_complete = False
        
        # self.parent_node.connected_hud.text_colour = 'red'
        self.parent_node.connected_hud.alpha = 255

    # keep track of time between rounds
    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run timer
        self.run_timer()

        # update spawners
        self.parent_node.update_spawners()

        # end round condition
        # get total dead and total spawned
        if self.parent_node.totalDeadInRound == self.parent_node.totalSpawnedInRound:

            self.emit("ROUNDEND")
    