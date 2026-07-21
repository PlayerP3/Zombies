from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager
from pynaccle.pathfinding import *

class Door(Interactable,Wall):

    def __init__(self):


        Wall.__init__(self)
        Interactable.__init__(self)

        self.name = 'Door'
        
        

    def init(self):

        super().init()

        # display message init
        self.display_message.init()
        self.display_message.update_message(f"Hold E to buy {self.name} [Cost:{self.cost}]")        

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

            # set to inactive
            self.is_active = False

            tilemapProcessor.add_chunk("1")

            if self.current_tile_position in tilemapProcessor.inaccessible_tiles:
                tilemapProcessor.inaccessible_tiles.remove(self.current_tile_position)
                build_astar_graph()
                build_true_clearance_graph()
           


    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                    
                # display message
                # self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))
                self.display_message.hurtbox.center = (self.hurtbox.topright[0] + 5, self.hurtbox.topright[1] - 5)
                self.display_message.submit_to_render()

                # if player is interacting
                if game_object.is_interacting:
                    self.state.emit('INTERACTING')

                # if player is interacting
                elif not game_object.is_interacting:
                    self.state.emit('IDLE')

    def update_data(self):

        self.update_position()

# for wb in wallbuy_parameters:

#     wbobj = Wallbuy()

#     set_attributes(game_object=wbobj,attributes=wallbuy_parameters[wb])
#     wbobj.init()
#     store_original_vars(game_object=wbobj)

#     wbobj.spawn(pos=wallbuy_parameters[wb]['pos'])

#     pynaccle.active_pool.append(wbobj)


# print(Door.__mro__)