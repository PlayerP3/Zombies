import pygame,os,re,math,random,string
import json
from pygame.math import Vector2
from engine.statemachine import State

class Running(State):

    def __init__(self):
        State.__init__(self)

    def enter(self):

        # set acceleration to base value
        self.parent_node.acceleration = 2
        self.parent_node.movement_vectors['movement']['acceleration'] = 2
        self.parent_node.update_direction_vector()
        self.parent_node.movement_vectors['movement']['Xcceleration_rate'] = 0
       
        # init timer
        self.timer_init()

    def completed(self):
        
        # reutrn acceleration to normal
        self.parent_node.movement_vectors['movement']['acceleration'] = 1
        self.parent_node.acceleration = 1

        # if something then set new state
        self.next_state = None

        # set done to false
        self.done = False
        
    def update(self):
        
        # track how long we have been in the state 
        self.run_timer()

        # submit event processing
        self.submit_event_processing()

        # update direction vector
        self.parent_node.update_direction_vector()

        # run move and collide
        self.parent_node.move_and_collide()

        # handle stamina
        self.parent_node.update_stamina()

        # update shooting pos
        self.parent_node.update_shooting_target_position()

        # movement raycast
        self.parent_node.movement_raycast.init({'starting_position':self.parent_node.hurtbox.center,"target_position":self.parent_node.shooting_target_position})
        self.parent_node.movement_raycast.apply_fog_of_war()

        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.hurtbox.center)

        self.parent_node.weapon.update()

        # end condition
        if sum(self.parent_node.movementx) == 0 and sum(self.parent_node.movementy) == 0:

            self.emit('IDLE')

        elif self.parent_node.stamina <= 0:
            
            self.emit('WALKING')

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # default player events
            if event.key == pygame.K_a:
                self.parent_node.movementx[0] = -1

            if event.key == pygame.K_d:      
                self.parent_node.movementx[1] = 1

            if event.key == pygame.K_w:     
                self.parent_node.movementy[0] = -1

            if event.key == pygame.K_s:
                self.parent_node.movementy[1] = 1   

            if event.key == pygame.K_e:
                self.parent_node.is_interacting = True

            if event.key == pygame.K_1:
                self.parent_node.swap_weapon()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                self.parent_node.movementx[0] = 0                

            if event.key == pygame.K_d:
                self.parent_node.movementx[1] = 0
                
            if event.key == pygame.K_w:
                self.parent_node.movementy[0] = 0
            
            if event.key == pygame.K_s:
                self.parent_node.movementy[1] = 0

            if event.key == pygame.K_LSHIFT:
                self.emit('WALKING')

            if event.key == pygame.K_e:
                self.parent_node.is_interacting = False
    