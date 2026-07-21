from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.roulette import Roulette
import sys
from pynaccle.animatedsprite import AnimatedSprite
from States.WeaponBox.cycling import Cycling
from States.WeaponBox.display import Display
from States.WeaponBox.reset import Reset
from States.WeaponBox.idle import Idle
from gun import gun_parameters

class Weaponbox(Roulette):

    def __init__(self):

        Roulette.__init__(self)
        

    def init(self):

        super().init()

        self.options = {k:v for k,v in gun_parameters.items()}

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

            # give item
            self.give_item(gameobj=self.interactingObj)


    # swap weapon function
    def give_item(self,gameobj):
        pass


    # collision check
    def collision_check(self,axis:str='y'):

        self.state.collision_check()
        pass

    def handle_collision(self,axis:str='y'):

        self.state.handle_collision()
        pass

    def update_data(self):

        self.state.update_position()

    # function to get the images we cycle through
    def filter_cycle_options(self):

        self.filteredOptions = {}

        # go through buildable weapons, if
        weaponsToRemove = []

        self.filteredOptions = {k:v for k,v in self.options.items() if k not in weaponsToRemove}

    # function to get what is going to be displayed in the final display
    def choose_final_display(self):
        
        # items to remove
        itemsToRemove = []

        # add guns the player is currently holding
        itemsToRemove.extend(self.purchasingObj.inventory.inventory['weapons'])

        self.filteredOptions = {k:v for k,v in self.filteredOptions.items() if k not in itemsToRemove}

        # pick weapon to give, need to pass dict of item name and its weight only
        self.finalDisplay = proc_using_weights({k:v['weight'] for k,v in self.filteredOptions.items()})

    def pay(self):

        self.finalDisplay = None

    # update the display item
    def update_display_item(self):
        
        pass

     





            



    
