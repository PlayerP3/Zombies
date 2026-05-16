import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State


class Gameover(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # set sprite sheet to be idle animation

        # remove movement if it is in movement vectors
        # self.parent_nodemovement_vectors = {}

        # set acceleration to base
        # self.parent_node.acceleration = self.parent_node.original_vars['acceleration']
        self.parent_node.movement_vectors['movement']['Xcceleration_rate'] = self.parent_node.slide_friction

        # change acceleration_timer

        pass

    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run move and collide
        self.parent_node.move_and_collide()

        # update shooting pos
        self.parent_node.update_shooting_target_position()

        # handle stamina
        self.parent_node.update_stamina()

        # movement raycast
        self.parent_node.movement_raycast.init({'starting_position':self.parent_node.hurtbox.center,"target_position":self.parent_node.shooting_target_position})
        self.parent_node.movement_raycast.apply_fog_of_war()

        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.hurtbox.center)
        self.parent_node.draw_rect(position=self.parent_node.hurtbox.center)

        self.end_condition()

    def handle_event(self, event):

        # if the actual X is clicked to close the tab
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
