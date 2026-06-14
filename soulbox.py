from pynaccle.utils import *
import json,os
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle,Interacting
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager
from pynaccle.pathfinding import *
from pynaccle.animatedsprite import AnimatedSprite

# load soul config data

with open(os.path.join(os.path.dirname(__file__),'configs','config_souls.json'),'r') as soulbox_attributes_file:

    soulbox_parameters = json.load(soulbox_attributes_file)


class Soul(Moveable_Object):

    def __init__(self,attachedSoulbox:object=None):

        Moveable_Object.__init__(self)
        
        self.attachedSoulbox = attachedSoulbox

    def init(self):

        super().init()

    # collision check
    def collision_check(self,axis:str='y'):

        # find surrounding objects
        self.find_surrounding_game_objects()   

        # go through all possible game objects
        for game_object in self.surrounding_game_objects:

            if game_object != self.attachedSoulbox:
                continue

            collision,hitbox = self.hitbox_collision(game_object=game_object)

            if collision:

                self.handle_collision(game_object=game_object,axis=axis)

    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # add to soul box
        self.attachedSoulbox.soulsCollected += 1

        # reset obj
        self.attachedSoulbox = None
        self.is_active = False


    # combines movement and collision function
    def update(self):

        # only show the orbital and draw it if it is active
        if self.is_active:

            # update position
            self.update_position()

            # draw surface
            self.draw_surface(position=self.hurtbox.center)

            self.draw_hitbox()

            # update movement vars
            self.update_movement()

            # movement
            self.move_and_collide()


class Soulbox(Interactable):

    def __init__(self,soulsToCollect:int=6):
        
        Interactable.__init__(self)

        self.nearbyObjs = []

        self.soulsCollected = 0
        self.soulsToCollect = soulsToCollect
        
    def init(self):
       
        self.cost = 0
        
        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

    # collision check
    def collision_check(self,axis:str='y'):

        # find surrounding objects
        self.find_surrounding_game_objects()  

        # go through all possible game objects
        for game_object in self.surrounding_game_objects:

            # skip collision if game object exists already
            if game_object in self.nearbyObjs:
                continue

            collision,hitbox = self.hitbox_collision(game_object=game_object)

            if collision:

                self.handle_collision(game_object=game_object,axis=axis)
                

    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return
        
        if self.soulsCollected < self.soulsToCollect:

            if game_object.object_of_origin == 'Enemy':

                if game_object.__class__.__name__ == 'Enemy':

                    if game_object not in self.nearbyObjs:

                        self.nearbyObjs.append(game_object)


        elif self.soulsCollected >= self.soulsToCollect:
                
            if game_object.object_of_origin == 'Player':

                if game_object.__class__.__name__ == 'Player':

                    if game_object.is_interacting:
                        self.state.emit('INTERACTING')

                    elif not game_object.is_interacting:
                        self.state.emit('IDLE')
                
                
    def update_data(self):

        self.update_position()

        self.process_interactions()

        self.draw_hitbox()

        


    def process_interactions(self):

        for game_object in self.nearbyObjs:

            collision,hitbox = self.hitbox_collision(game_object=game_object)

            # if collision then remove it
            if not collision:

                self.nearbyObjs.remove(game_object)

                continue
            
            # if there is a collision check if the obj is still active
            elif collision:

                if not game_object.is_active:


                    # create soul
                    soulObj = objectManager.inactive_pool['Soul'][0]
                    soulObj.attachedSoulbox = self

                    # init soul
                    set_attributes(game_object=soulObj,attributes=soulbox_parameters[self.name]['SoulInit'])
                    soulObj.init()
                    soulObj.spawn(pos=game_object.hurtbox.center)
                    soulObj.determine_movement(target=self.hurtbox.center,start=game_object.hurtbox.center)
                    objectManager.active_pool.append(soulObj)
                    self.nearbyObjs.remove(game_object)

                   





