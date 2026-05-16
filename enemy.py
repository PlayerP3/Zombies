import pygame,os,re
import pygame.freetype
from pygame.math import Vector2
from game import Game,engine
from pathfinding import Pathfinding
# from Drawing_TileMaps import Creative_Mode,AnimatedSprite
import random
import math
import sys
import json
from animatedsprite import AnimatedSprite,GameSprites
import copy
from moveableobject import Moveable_Object
from utils import *
from statemachine import StateMachine
from States.Enemy.idle import Idle
from States.Enemy.chasing import Chasing
from States.Enemy.roaming import Roaming
from States.Enemy.death import Death

# from ItemBench import ItemPools,ItemPoolsReset,remove_from_itempool,add_to_itempool
pygame.font.init()


# load in parameters
with open('config_enemy.json','r') as enemy_attributes_file:

    enemy_parameters = json.load(enemy_attributes_file)

class EnemyStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        self.state.update()

        if self.state.done:
            self.transition_to_next_state()

        

        


class Enemy(Moveable_Object,Pathfinding,EnemyStateMachine):

    def __init__(self):

        Moveable_Object.__init__(self)
        Pathfinding.__init__(self)

        # movement
        self.movementx = [0,0] # index 0 is no movememnt, -1 left, 1 right
        self.movementy = [0,0] # index 0 is no movement, -1 up, 1 down

        # self.starter_deck = {}
        # self.deck = Deck()

        # target position for shooting
        self.shooting_target_position = (0,0)

    # reinit
    def init(self,attributes:dict={},pos:tuple=(0,0)):

        # spawn
        self.spawn(pos)

        for att,val in attributes.items():

            setattr(self,att,val)
        
        # init sprite variables
        self.init_sprite()

        # update hurtbox size
        self.hurtbox.width = self.hurtbox_width
        self.hurtbox.height = self.hurtbox_height

        # update raycast vars
        self.movement_raycast.init(attributes=self.movement_raycast_init)

        # init state machine
        self.states = {'IDLE':Idle(),
                       'CHASING':Chasing(),
                       'DEATH':Death()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['IDLE']

        self.original_vars = {k:v for k,v in self.__dict__.items()}

    # handle collision once the check is confirmed
    def handle_collision(self,game_object:Moveable_Object,axis:str):

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

        if game_object.object_of_origin == 'Enemy':

            if game_object.__class__.__name__ == 'Enemy':

                collision_vectorX,collision_vectorY = Vector2(self.hurtbox.center) - Vector2(game_object.hurtbox.center)

                # collision_vectorX,collision_vectorY = (collision_vector/self.collision_vector_reduction)

                # apply a knockback
                self.update_movement_vectors(unique_id='overlapping_spread_knockback',direction_vectorX=collision_vectorX,direction_vectorY=collision_vectorY,
                                    acceleration=((game_object.overlap_resolution_strength/self.overlap_resolution_resistance)),Xcceleration_rate=self.decceleration_rate,Xcceleration_rate_change='negative',max_value=0,
                                    reduce_on_wall_collision=True,reset_on_max_value=True)


    def run_behaviour(self):
        
        # only show the orbital and draw it if it is active
        if self.is_active:

            # update position
            self.update_position()

            # find game objects
            # self.find_game_objects_in_area()

            # handle collisions with the wall and entities
            # self.enemy_collision_rects()
            # self.pathing_end_position_target = (48,-48)
            self.pathing_end_position_target = engine.player.hurtbox.center


            # determine the pathing the entity is going to be using
            # self.determine_pathing_type()

            # update pathing and cache
            self.update_pathing_and_cache()
            self.draw_pathing()

            # # movement
            self.move_and_collide()

            # draw surface
            self.draw_surface(position=self.hurtbox.center)
            self.draw_rect(position=self.hurtbox.center)


# This will be for storing inactive pools of all bullet-like objects
EnemyInactivePools = {}


# This is a pool of card objects 
class DefaultPool():

    def __init__(self):

        self.inactive_pool = [Enemy() for _ in range(50)]

# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
EnemyInactivePools["Enemy"] = DefaultPool()


# controls all type of shooting objects
class EnemyManager():
    def __init__(self):

        self.active_pool = []

    def run_behaviour(self):

        if self.active_pool:

            to_remove = []

            for gameobj in self.active_pool:

                # gameobj.run_behaviour()
                gameobj.update()

                if not gameobj.is_active:
                    to_remove.append(gameobj)

            if to_remove:

                for gameobj in to_remove:

                    gameobj.kill(self.active_pool,EnemyInactivePools[gameobj.__class__.__name__].inactive_pool)


EnemyMgr = EnemyManager()





# event processing for shooting
def spawn_enemy_event(event:pygame.Event):

    # handling mouse clicks
    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_z:

            enemy_object = EnemyInactivePools['Enemy'].inactive_pool[0]

            # spawns = [(-48,-48),(-220,-100),(100,220),(500,100)]
            spawns = [(120,256)]
            
            enemy_object.init(attributes=enemy_parameters['Enemy'],pos=random.choice(spawns))

            EnemyMgr.active_pool.append(enemy_object)
            EnemyInactivePools['Enemy'].inactive_pool.remove(enemy_object)


engine.extra_event_processing.append(spawn_enemy_event)


enemy_object = EnemyInactivePools['Enemy'].inactive_pool[0]

# spawns = [(-48,-48),(-220,-100),(100,220),(500,100)]
spawns = [(120,256)]

enemy_object.init(attributes=enemy_parameters['Enemy'],pos=random.choice(spawns))

EnemyMgr.active_pool.append(enemy_object)
EnemyInactivePools['Enemy'].inactive_pool.remove(enemy_object)