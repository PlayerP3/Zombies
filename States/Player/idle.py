import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from game import engine
from statemachine import State


class Idle(State):

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

        self.parent_node.weapon.update()

        self.end_condition()

    def handle_event(self, event):

        # if the actual X is clicked to close the tab
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

            # default player events
            if event.key == pygame.K_a:
                self.parent_node.movementx[0] = -1
                self.parent_node.apply_damage(self.parent_node,0.2)


            if event.key == pygame.K_d:      
                self.parent_node.movementx[1] = 1

            if event.key == pygame.K_w:     
                self.parent_node.movementy[0] = -1

            if event.key == pygame.K_s:
                self.parent_node.movementy[1] = 1   

            if event.key == pygame.K_RETURN:
                engine.display_tiles *= -1

            if event.key == pygame.K_e:
                self.parent_node.is_interacting = True

            if event.key == pygame.K_1:
                self.parent_node.swap_weapon()

            # if event.key == pygame.K_m:
            #     engine.camera.change_focus = True
    
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                self.parent_node.movementx[0] = 0                

            if event.key == pygame.K_d:
                self.parent_node.movementx[1] = 0
                
            if event.key == pygame.K_w:
                self.parent_node.movementy[0] = 0
            
            if event.key == pygame.K_s:
                self.parent_node.movementy[1] = 0

            if event.key == pygame.K_e:
                self.parent_node.is_interacting = False

    def end_condition(self):
        
        # if something happens send signal to transition to other state here by setting done to True and setting next state
        # if 'movement' in self.parent_node.movement_vectors:
        #     self.parent_node.emit('WALKING')

        if sum(self.parent_node.movementx) != 0 or sum(self.parent_node.movementy) != 0:

            self.emit('WALKING')

