from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle,Interacting
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager

class Door(Interactable,Wall):

    def __init__(self,connectedChunk:int=0):

        self.hitbox = pygame.FRect(0,0,100,100)

        self.connectedChunk = connectedChunk

        Wall.__init__(self)
        Interactable.__init__(self)
        
        
     

    def init(self):

        # display message init
        self.display_message.is_text = True
        self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"
        self.display_message.init_sprite()
        self.display_message.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1
        
        

        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

            # set to inactive
            self.is_active = False

            objectManager.add_chunk(self.connectedChunk)
           


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
        self.hitbox.center = self.hurtbox.center

# for wb in wallbuy_parameters:

#     wbobj = Wallbuy()

#     set_attributes(game_object=wbobj,attributes=wallbuy_parameters[wb])
#     wbobj.init()
#     store_original_vars(game_object=wbobj)

#     wbobj.spawn(pos=wallbuy_parameters[wb]['pos'])

#     pynaccle.active_pool.append(wbobj)


# print(Door.__mro__)