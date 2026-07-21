import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State


class Idle(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # set sprite sheet to be idle animation
        self.parent_node.shooting_timer.timer_complete = True
        # self.parent_node.is_shooting = False

    def update(self):

        # submit event processing
        self.submit_event_processing()

        # draw surface
        # self.parent_node.draw_surface(position=self.parent_node.hurtbox.center)
        
        if self.parent_node.is_shooting:

            if self.parent_node.bullets_remaining_in_mag:
                self.emit('SHOOTING')

            elif not self.parent_node.bullets_remaining_in_mag:
                self.emit('RELOADING')

    def handle_event(self, event):

         # handling mouse clicks
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                # if not dual wield or alternating click and dual wield
                if not self.parent_node.is_dual_wield:

                    if (self.parent_node.bullets_remaining_in_mag < self.parent_node.magazine_size):

                        self.emit('RELOADING')

        # handling mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                # handle left clicks differently for semi auto and full aout weapons
                # do a quick check if there the whole magazine size has been fired, if it has then force a reload
                if (self.parent_node.total_ammo_stock > 0 and self.parent_node.bullets_remaining_in_mag == 0): # here bullets being 0 means that all has been fired
                        
                    # if we do have ammo then reload
                    self.emit("RELOADING")


                # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                elif self.parent_node.bullets_remaining_in_mag > 0:#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                    # if the gun is not a dual wiled weapon set the regular shooting to true
                    if not self.parent_node.is_dual_wield:

                        self.emit('SHOOTING')
                        self.parent_node.is_shooting = True


               
        # handling mouse clicks
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == pygame.BUTTON_LEFT:

                self.parent_node.is_shooting = False 


