import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from game import engine
from statemachine import State
import sys

class Shooting(State):

    def __init__(self):
        State.__init__(self)

    def enter(self):

        # init the shooting timer
        self.parent_node.shooting_timer.timer_init()
        self.parent_node.shooting_timer.timer_complete = True
        self.parent_node.is_shooting = True
            
    def update(self):

        # submit event processing
        self.submit_event_processing()

        # check if bullets can be fired
        self.parent_node.can_shot_be_fired2()

        # if there is a projectile in the queue
        if self.parent_node.projectile_queue:

            to_remove = []

            # go through each bullet in the projectile queue
            for bullet in self.parent_node.projectile_queue:


                # if bullet.adjust_final_target:

                #     bullet.target_position = self.wielded_by.shooting_target

                if bullet.ready_to_be_shot():

                    to_remove.append(bullet)

            # remove bullets ready to be shot
            if to_remove:

                for blt in to_remove:

                    # remove from queue and add to acitve pool
                    engine.active_pool.append(blt)
                    self.parent_node.projectile_queue.remove(blt)

            # if empty start burst countdown to prevent shooting
            if not self.parent_node.projectile_queue:
                self.burst_countdown_active = True
                

        # do a quick check if there the whole magazine size has been fired, if it has then force a reload
        if self.parent_node.bullets_remaining_in_mag == 0: # here bullets being 0 means that all has been fired
                
            # if we do have ammo then reload
            self.emit("RELOADING")

    def completed(self):

        self.parent_node.projectile_queue = []
        self.done = False
        self.next_state = None
        

    def handle_event(self, event):

        # handling mouse clicks
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                # if not dual wield or alternating click and dual wield
                if not self.parent_node.is_dual_wield:

                    if (self.parent_node.bullets_remaining_in_mag < self.parent_node.magazine_size):

                        self.emit('RELOADING')
                            
        # MOUSE BUTTON UP EVENTS
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == pygame.BUTTON_LEFT:

                # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
                # if the gun is not a dual wiled weapon set the regular shooting to true
                if not self.parent_node.is_dual_wield:

                    # set shooting to be true
                    self.emit('IDLE')

            
        