from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager
from pynaccle.pathfinding import *
from pynaccle.inventory import gameInventory
from pynaccle.animatedsprite import AnimatedSprite
from gun import gun_parameters,Gun
from States.Bench.buildablebuilt import BuildableBuilt
from States.Bench.buildabletaken import BuildableTaken
from States.Bench.idle import Idle


class Part(Interactable):

    def __init__(self,buildableObject:str='RobotBoy'):
        
        Interactable.__init__(self)

        self.buildableObject = buildableObject
        self.can_collide = False

    def init(self):

        # display message init
        self.display_message.init()
        
        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

            # set to inactive
            self.is_active = False

            # add to collected parts foir game obj
            # objectManager.player.collectedParts.append(self.name)
            objectManager.player.collectedParts[self.buildableObject].append(self.name)

            gameInventory.add_item(k1='buildable',k2=self.buildableObject,v=self.name)


    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):
        

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                    
                # display message
                self.display_message.hurtbox.center = (self.hurtbox.topright[0] + 5, self.hurtbox.topright[1] - 5)
                self.display_message.submit_to_render()

                # if player is interacting
                if game_object.is_interacting:
                    self.state.emit('INTERACTING')

                # if player is interacting
                elif not game_object.is_interacting:
                    self.state.emit('IDLE')

    



class Bench(Interactable):

    def __init__(self,partsNeeded:int=3,buildableObject:str='',canBeReplaced:bool=False,buildingTimer:float=1.5,pickupTimer:float=0.2,replaceTimer:float=0.2):

        Interactable.__init__(self)

        # parts needed to buidl and name of what the bench builds
        self.partsNeeded = partsNeeded
        self.buildableObject = buildableObject
        self.buildableData = {}
        self.buildableBuilt = False
        self.buildableTaken = False
        self.canBeReplaced = canBeReplaced

        # hard set variables
        self.buildingTimer = buildingTimer
        self.pickupTimer = pickupTimer
        self.replaceTimer = replaceTimer

        # create dict that stores the state as key and the interaction time when in the state 
        self.stateInteractTimeLimit = {'IDLE':self.buildingTimer,
                                       'BUILDABLEBUILT':self.pickupTimer,
                                       'BUILDABLETAKEN':self.replaceTimer}
        
        self.stateTimeLimit = {'IDLE':1,
                                'BUILDABLEBUILT':1,
                                'BUILDABLETAKEN':1}
        
    def init(self):

        super().init()

        clear_states(self.states)

        self.buildableSprite = AnimatedSprite()
        self.buildableSprite.zlayer_drawing = self.zlayer_drawing + 1
        
        # set states
         # init state machine
        self.states = {'IDLE':Idle(),
                       'BUILDABLEBUILT':BuildableBuilt(),
                       'BUILDABLETAKEN':BuildableTaken()}                  
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
            self.states[x].timer_limit = self.stateTimeLimit[x]
        
        self.state = self.states['IDLE']
    

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        self.state.pay()


    # swap weapon function
    def give_weapon(self,gameobj):

        give_weapon(gameobj=gameobj,weaponName=self.buildableObject,weaponClass=Gun,weaponParams=gun_parameters)

    # collision check
    def collision_check(self,axis:str='y'):

        self.state.collision_check()
        pass

    def handle_collision(self,axis:str='y'):

        self.state.handle_collision()
        pass

            
