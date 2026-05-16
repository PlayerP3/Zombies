import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from game import engine
from statemachine import State


class Interacting(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # change display message spirte


        # set sprite sheet to be idle animation

        self.timer_limit = 2
        self.timer_init()
        

    def update(self):

        # run interaction timer
        self.run_timer()

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()


        # check if player is in colliding objects
        # if engine.player in self.parent_node.surrounding_game_objects:
        #     pass
            # display message
            # self.parent_node.display_message.draw_surface(position=(self.parent_node.hurtbox.topright[0]+3,self.parent_node.hurtbox.topright[1]-3))

        
        if self.timer_complete:

            self.parent_node.pay(gameobj=engine.player)
            self.emit('IDLE')

        elif not engine.player.is_interacting:
            self.emit('IDLE')


        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.hurtbox.center)
        self.parent_node.draw_rect(position=self.parent_node.hurtbox.center)



        

