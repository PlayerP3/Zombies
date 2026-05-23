import pygame,os,re
import pygame.freetype
from pygame.math import Vector2
from game import Game,engine
from gun import guns
# from Drawing_TileMaps import Creative_Mode,AnimatedSprite
import random
import math
import sys
import json
from animatedsprite import AnimatedSprite,GameSprites
import copy
from deck import *
from statemachine import StateMachine
from States.Player.idle import Idle
from States.Player.walking import Walking
from States.Player.running import Running

# from Bullets import Weapons,RightHandWeapons
# from Orbitals import Orbital
from moveableobject import Moveable_Object
# from ItemBench import ItemPools,ItemPoolsReset,remove_from_itempool,add_to_itempool
pygame.font.init()

## USEFUL INFO
# self.current weapon is actual weapon object
# self.current_wepaon_slot is the key used to access the weapon object in the weapon slot dictionary
# self.left_hand_weapon_slots is a dictioanry with the weapon number as key and the weapon object object as a value
# self.left_hand_weapon_slots[self.weapon_choice] returns weapon object if the slot is filled


class PlayerStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        if self.state.done:
            self.transition_to_next_state()

        self.state.update()

        # update position
        self.update_position()

        # self.draw_surface(position=self.hurtbox.center)



class Player(Moveable_Object,PlayerStateMachine):

    def __init__(self):

        Moveable_Object.__init__(self)
        PlayerStateMachine.__init__(self)

        # movement
        self.movementx = [0,0] # index 0 is no movememnt, -1 left, 1 right
        self.movementy = [0,0] # index 0 is no movement, -1 up, 1 down

        self.mouse_pos = (0,0)

        # starting weapon
        self.starting_weapon = 'AssaultRifle'

        # current weapon
        self.weapon = guns[self.starting_weapon]

        # all weapons
        self.allWeapons = [self.starting_weapon]

        # total number of weapons player can carry
        self.weaponCarryLimit = 2

        # list of items
        self.picked_items = []

        # slide variable
        self.slide_friction = 3

        # is interacting
        self.is_interacting = False

        # target position for shooting
        self.shooting_target_position = (0,0)


    # function to link set attirbutes, init and storing original values on obj start
    def start(self,attributes:dict):

        set_attributes(game_object=self,attributes=attributes)
        self.init()
        store_original_vars(game_object=self)

    # reinit
    def init(self):

        # update raycast vars
        self.weapon.wielded_by = self

        self.states = {'IDLE':Idle(),
                       'WALKING':Walking(),
                       'RUNNING':Running()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['IDLE']
        
        self.update_movement_vectors(unique_id='movement',direction_vectorX=0,direction_vectorY=0,acceleration=5,
                                            Xcceleration_rate=0,Xcceleration_rate_change='negative',max_value=0,
                                            reduce_on_wall_collision=False,reset_on_max_value=False)
        super().init()

        
    # handle collision damage etc
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Game':

            if game_object.__class__.__name__ == 'Wall':

                if axis == 'x':
                    if self.movement[0] < 0:
                        self.hurtbox.left = game_object.hurtbox.right

                    elif self.movement[0] > 0:
                        self.hurtbox.right = game_object.hurtbox.left

                elif axis == 'y':
                    if self.movement[1] < 0:
                        self.hurtbox.top = game_object.hurtbox.bottom

                    if self.movement[1] > 0:
                        self.hurtbox.bottom = game_object.hurtbox.top

                
  
    # apply a slow down effect to movement if no keys are being pressed
    def slide_after_stop(self):

        # player is not moving
        if sum(self.movementx) == 0 and sum(self.movementy) == 0:

            if 'movement' in self.movement_vectors:

                # by using this method we use whatever velocity existed before and move that way
                self.movement_vectors['movement']['Xcceleration_rate'] = 3
                

        # player is moving
        else:

            if 'movement' in self.movement_vectors:

                self.movement_vectors['movement']['direction_vectorX'] = sum(self.movementx)
                self.movement_vectors['movement']['direction_vectorY'] = sum(self.movementy)
                self.movement_vectors['movement']['Xcceleration_rate'] = 0
                self.movement_vectors['movement']['acceleration'] = 1

    # update movement vectors each frame
    def update_direction_vector(self):

        self.movement_vectors['movement']['direction_vectorX'] = sum(self.movementx)
        self.movement_vectors['movement']['direction_vectorY'] = sum(self.movementy)

    # update shooting target position
    def update_shooting_target_position(self):

        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # adjust mouse position because of rescaling
        x = mouse_pos[0]/(engine.windows.fullscreen_width/engine.windows.win_width) - engine.camera.bg_offset_x
        y = mouse_pos[1]/(engine.windows.fullscreen_height/engine.windows.win_height) - engine.camera.bg_offset_y

        self.shooting_target_position = (x,y)
        self.weapon.shooting_start_position = self.hurtbox.center

    # swap weapon function
    def swap_weapon(self):

        if len(self.allWeapons) > 1:

            # first end weapon state
            self.weapon.state.completed()

            # find first element in list which is current weapon
            current_weapon = self.allWeapons[0]
            
            # find second element in list which is next weapon
            next_weapon = self.allWeapons[1]

            # remove current weapon and add to end of list
            self.allWeapons.pop(0)
            self.allWeapons.append(current_weapon)

            # set new weapon
            self.weapon = guns[next_weapon]
            self.weapon.wielded_by = self

            # enter state
            self.weapon.state = self.weapon.states['PULLOUT']
            self.weapon.state.enter()
        
    # behaviour function
    def run_behaviour(self):

        if self.is_active:

            self.update_position()

            # self.find_surrounding_game_objects()

            self.update_shooting_target_position()

            self.slide_after_stop()

            # self.move2()
            # draw surface
            
            self.move_and_collide()

            self.movement_raycast.init({'starting_position':self.hurtbox.center,"target_position":self.shooting_target_position})
            self.movement_raycast.apply_fog_of_war()
            
            self.draw_surface(position=self.hurtbox.center)


            # draw rect for debugging 
            self.draw_rect(position=self.hurtbox.center)

            # self.draw_hitbox(position=self.hitbox.center)

