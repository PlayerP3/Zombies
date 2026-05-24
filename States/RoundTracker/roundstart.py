import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from engine.statemachine import State
import numpy as np

class RoundStart(State):

    def __init__(self):
        State.__init__(self)

    
    def enter(self):
        
        # set reloading animation stuff
        self.timer_init()
        self.timer_complete = False
        
        # add 1 to round
        self.parent_node.round_number += 1
        self.parent_node.totalDeadInRound = 0 
        self.parent_node.totalSpawnedInRound = 0

        self.parent_node.set_enemy_allowed()

        # calculate metrics for round
        for enemy in self.parent_node.spawningEnemyTypes:

            self.parent_node.spawners[enemy].calculate_metrics_for_round()
            
            self.parent_node.totalSpawnedInRound += self.parent_node.spawners[enemy].totalToSpawn
            # print(self.parent_node.spawners[enemy].totalToSpawn)
            # print(self.parent_node.totalSpawnedInRound)

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
            self.emit('ROUNDINPROGRESS')