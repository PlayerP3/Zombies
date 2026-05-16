import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from game import engine
from statemachine import State


class Reloading(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # set reloading animation stuff
        self.parent_node.deck.reloading_timer.timer_init()
        self.parent_node.deck.reloading_timer.timer_complete = False

    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run timer
        self.parent_node.deck.reloading_ammo2()

        if self.parent_node.deck.reloading_timer.timer_complete:

            # we were in the middle of shooting
            if not self.parent_node.deck.shooting_timer.timer_complete:
                self.emit('SHOOTING')
            else:
                self.emit('IDLE')

        # draw surface
        ###

    def handle_event(self, event):

        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                # handle left clicks differently for semi auto and full aout weapons
                if self.parent_node.deck.select_fire == 'fullauto':

                    # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                    if (self.parent_node.deck.total_ammo_stock > 0 or self.parent_node.deck.bullets_remaining_in_mag > 0):#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                        # if the gun is not a dual wiled weapon set the regular shooting to true
                        if not self.parent_node.deck.is_dual_wield:

                            # set shooting to be true
                            self.emit('SHOOTING')

                    


