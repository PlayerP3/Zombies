import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State


class Reloading(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # set reloading animation stuff
        self.parent_node.reloading_timer.timer_init()
        self.parent_node.reloading_timer.timer_complete = False

    def update(self):

        # submit event processing
        self.submit_event_processing()

        # run timer
        self.parent_node.reloading_ammo()

        if self.parent_node.reloading_timer.timer_complete:

            # we were in the middle of shooting
            # if parent node is shooting
            if self.parent_node.is_shooting:
                self.emit('SHOOTING')
    
            else:
                self.emit('IDLE')

        # draw surface
        ###

    def handle_event(self,event):

        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                # handle left clicks differently for semi auto and full aout weapons
                if self.parent_node.select_fire == 'fullauto':

                    # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                    if (self.parent_node.total_ammo_stock > 0 or self.parent_node.bullets_remaining_in_mag > 0):#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                        # if the gun is not a dual wiled weapon set the regular shooting to true
                        if not self.parent_node.is_dual_wield:

                            # set shooting to be true
                            # self.emit('SHOOTING')
                            # set shooting to be true
                            self.parent_node.is_shooting = True

        # MOUSE BUTTON UP EVENTS
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == pygame.BUTTON_LEFT:

                # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
                # if the gun is not a dual wiled weapon set the regular shooting to true
                if not self.parent_node.is_dual_wield:

                    # set shooting to be true
                    self.parent_node.is_shooting = False
                    


