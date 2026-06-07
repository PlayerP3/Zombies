import os
from pygame.math import Vector2
from pynaccle.utils import *
import random,json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.objectsystem import objectManager
from pynaccle.interactable import Interactable,Idle,Interacting
# from miscsprites import MiscellaneousMgr

# load in parameters
with open(os.path.join(os.path.dirname(__file__),'configs/config_item.json'),'r') as item_attributes_file:

    item_parameters = json.load(item_attributes_file)

class Item(Interactable):

    def __init__(self):

        self.display_item = Moveable_Object()
        self.display_item_init = {}

        Interactable.__init__(self)
     

    def init(self):

        # display item init
        # can use the below because we have set attr already
        for att,val in self.display_item_init.items():
            setattr(self.display_item,att,val)

        self.display_item.init_sprite()
        self.display_item.hurtbox.center = self.hurtbox.center

        super().init()

       

    # stick display item to pedesatal
    def stick_item_to_pedestal(self):

        self.display_item.hurtbox.center = self.hurtbox.center

    # what happens when a player picks up the item
    def pickup(self):

        pass

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if self.name in gameobj.picked_items:
            return
        
        gameobj.picked_items.append(item_parameters[self.name])

        if item_parameters[self.name]["effect"] == "stat change":
            
            set_attributes(game_object=gameobj,attributes=item_parameters[self.name]["stat_val"])
     



# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
objectManager.inactive_pool["Item"] = [Item() for _ in range(300)]



