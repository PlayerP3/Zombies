from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle,Interacting
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager
from pynaccle.pathfinding import *
from pynaccle.animatedsprite import AnimatedSprite
from gun import guns

class Part(Interactable):

    def __init__(self,buildableObject:str='RobotBoy'):
        
        self.buildableObject = buildableObject
       
        
        Interactable.__init__(self)
        

    def init(self):

        # display message init
        self.display_message.is_text = True
        self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"
        self.display_message.init_sprite()
        self.display_message.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1
        self.can_collide = False
        self.cost = 0
        

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


    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):
        

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                    
                # display message
                self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))

                # if player is interacting
                if game_object.is_interacting:
                    self.state.emit('INTERACTING')

                # if player is interacting
                elif not game_object.is_interacting:
                    self.state.emit('IDLE')

    def update_data(self):

        self.update_position()


class Bench(Interactable):

    

    def __init__(self,partsNeeded:int=3,buildableObject:str=''):

        # parts needed to buidl and name of what the bench builds
        self.partsNeeded = partsNeeded
        self.buildableObject = buildableObject
        self.buildableData = {}
        self.buildableBuilt = False
        self.buildableTaken = False

        Interactable.__init__(self)
        
    def init(self):

        # display message init
        # self.display_message.is_text = True
        # self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"
        # self.display_message.init_sprite()
        # self.display_message.hurtbox.center = (0,0)
        # self.display_message.timer_limit = 1

        self.display_item = AnimatedSprite()
        self.display_item.zlayer_drawing = self.zlayer_drawing + 1
       
        self.cost = 0
        
        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost


            # make buildable
            if not self.buildableBuilt:

                # init item sprite
                self.display_item.init_sprite()
                self.display_item.hurtbox.center = (self.hurtbox.centerx,self.hurtbox.centery - 14)

                self.buildableBuilt = True
                
                self.display_message.img_path = 'Hold E to equip'

                self.interactingObj.is_interacting = False
            
            # give to player
            elif not self.buildableTaken:

                self.display_item.is_active = False
                self.display_message.img_path = ' '
                
                # run effect depending on interactable
                self.give_weapon(gameobj=self.interactingObj)
              
                self.buildableTaken = True


    # swap weapon function
    def give_weapon(self,gameobj):

        # first end weapon state
        gameobj.weapon.state.completed()

        # find first element in list which is current weapon
        current_weapon = gameobj.allWeapons[0]
        
        # set weapon to give to player
        weapon_to_give = self.buildableObject

        if len(gameobj.allWeapons) < gameobj.weaponCarryLimit:

            # remove current weapon and add to end of list
            gameobj.allWeapons.insert(0,weapon_to_give)


        elif len(gameobj.allWeapons) >= gameobj.weaponCarryLimit:

            # remove current weapon and add to end of list
            gameobj.allWeapons.remove(current_weapon)
            gameobj.allWeapons.insert(0,weapon_to_give)

        # set new weapon
        gameobj.weapon = guns[weapon_to_give]
        gameobj.weapon.wielded_by = gameobj

        # enter state
        gameobj.weapon.state = gameobj.weapon.states['PICKUP']
        gameobj.weapon.state.enter()


            
    # wall collision check
    def collision_check(self,axis:str='y'):

        # if it has been built and taken just continue
        if self.interactingObj:
            pass


        if not self.interactingObj:

            if self.__class__.__name__ == "Wall":
                return

            # find surrounding objects
            self.find_surrounding_game_objects()  

            # separate self objects from different objects
            self_origin_surrounding_objects  = [x for x in self.surrounding_game_objects if x.object_of_origin == self.object_of_origin]  
            different_origin_surrounding_objets = [x for x in self.surrounding_game_objects if x.object_of_origin != self.object_of_origin]  

            
            # print(objectManager.object_positions[(-224.0, -160.0)])
            # sys.exit()
            # go through all possible game objects
            for game_object in self.surrounding_game_objects:

                if not game_object.can_collide:
                    continue

                # if wall/door use hirtbox collision instead of hitbox
                if array_is_in_array(get_mro(gameObject=game_object),['Wall','Interactable']): 

    
                    # rect collision check
                    if self.hurtbox.colliderect(game_object.hurtbox):

                        # handle collision
                        self.handle_collision(game_object=game_object,axis=axis)


                else:
                   
                    collision,hitbox = self.hitbox_collision(game_object=game_object)

                    if collision:

                        self.handle_collision(game_object=game_object,axis=axis)
                        self.interactingObj = game_object

        # if something is interacting already
        elif self.interactingObj:

            collision,hitbox = self.hitbox_collision(game_object=self.interactingObj)

            if collision:

                self.handle_collision(game_object=self.interactingObj,axis=axis)

            elif not collision:

                # remove interacting obj
                self.interactingObj.is_interacting = False
                self.interactingObj = None
                


        
    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':

                if not self.buildableBuilt:

                    # only if we have bench specific things to build
                    if self.buildableObject:

                        # check if the player has the buildable object and the right amouint
                        if self.buildableObject not in game_object.collectedParts:
                            self.display_message.img_path = f"Wrong work bench"
                    
                        
                        elif self.buildableObject in game_object.collectedParts:
                            
                            if len(game_object.collectedParts[self.buildableObject]) != self.buildableData[self.buildableObject]['partsNeeded']:
                                self.display_message.img_path = f"Not enough parts"
                                
                            
                            elif len(game_object.collectedParts[self.buildableObject]) == self.buildableData[self.buildableObject]['partsNeeded']:
                            
                                # set display message and item image path
                                self.display_message.img_path = f"Hold E to interact"
                                self.display_item.img_path = self.buildableData[self.buildableObject]['img_path']

                                # if player is interacting
                                if game_object.is_interacting:
                                    self.state.emit('INTERACTING')

                                # if player is interacting
                                elif not game_object.is_interacting:
                                    self.state.emit('IDLE')

                    # if theres nothing specific that goes 
                    elif not self.buildableObject:

                        if not game_object.collectedParts:
                            self.display_message.img_path = f"Not enough parts"
                    

                        elif game_object.collectedParts:

                            # go through all possible buildable objs
                            for buildable in game_object.collectedParts:

                                if len(game_object.collectedParts[buildable]) != self.buildableData[buildable]['partsNeeded']:
                                    self.display_message.img_path = f"Not enough parts"
                                    continue
                                    
                                elif len(game_object.collectedParts[buildable]) == self.buildableData[buildable]['partsNeeded']:

                                    # set message and img path
                                    self.display_message.img_path = f"Hold E to interact"
                                    self.display_item.img_path = self.buildableData[buildable]['img_path']

                                    # if player is interacting
                                    if game_object.is_interacting:
                                        
                                        self.buildableObject = buildable
                                        self.state.emit('INTERACTING')

                                    # if player is interacting
                                    elif not game_object.is_interacting:
                                        self.state.emit('IDLE')

                elif not self.buildableTaken:

                    # if player is interacting
                    if game_object.is_interacting:
                        self.state.emit('INTERACTING')

                    # if player is interacting
                    elif not game_object.is_interacting:
                        self.state.emit('IDLE')

                
                # init sprite
                self.display_message.init_sprite()

                # display message
                self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))

                


    def update_data(self):

        self.update_position()

        # if object built then diplsay it
        if self.buildableBuilt and not self.buildableTaken:

            # display message
            self.display_item.draw_surface(position=self.display_item.hurtbox.center)




