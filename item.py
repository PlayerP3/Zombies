
from pygame.math import Vector2
from engine.utils import *
import random,json
from engine.moveableobject import Moveable_Object
from engine.objectsystem import objectManager
from interactable import Interactable,Idle,Interacting
# from miscsprites import MiscellaneousMgr

# load in parameters
with open('config_item.json','r') as item_attributes_file:

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

miscobj = objectManager.inactive_pool['Item'][0]

# spawns = [(-48,-48),(-220,-100),(100,220),(500,100)]
spawns = [(-224,100)]

set_attributes(game_object=miscobj,attributes=item_parameters['HealthUp'])
miscobj.init()
store_original_vars(game_object=miscobj)

miscobj.spawn(random.choice(spawns))

objectManager.active_pool.append(miscobj)
objectManager.inactive_pool['Item'].remove(miscobj)


