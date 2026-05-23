import pygame,os,re,sys
from pygame.math import Vector2
from game import engine
from utils import *
import random
import math
import json
import string
import copy
import numpy as np
from moveableobject import Moveable_Object
from interactable import Interactable,Idle,Interacting
from animatedsprite import GameSprites
from item import Item
from gun import guns
# from miscsprites import MiscellaneousMgr

# load in parameters
with open('config_wallbuy.json','r') as wallbuy_attributes_file:

    wallbuy_parameters = json.load(wallbuy_attributes_file)


class Wallbuy(Item):

    def __init__(self,weaponCost:int=500,ammoCost:int=100):

        self.weapon_bought = None
        self.ammoCost = ammoCost
        self.weaponCost = weaponCost

        Item.__init__(self)
     

    def init(self):

        # display item init
        # can use the below because we have set attr already
        for att,val in self.display_item_init.items():
            setattr(self.display_item,att,val)

        
        self.display_item.init_sprite()
        self.display_item.hurtbox.center = self.hurtbox.center

        # display message init
        self.display_message.is_text = True
        self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.weaponCost}]"
        self.display_message.init_sprite()
        self.display_message.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1
        
        

        super().init()

    # stick display item to pedesatal
    def stick_item_to_pedestal(self):

        self.display_item.hurtbox.center = self.hurtbox.center

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            # if player does not have weapon in their inventory, display buy
            if self.name in gameobj.allWeapons:

                # return weapon
                weapon = guns[self.name]

                if weapon.total_ammo_stock < weapon.original_vars["total_ammo_stock"]:

                    gameobj.money -= self.cost
                    weapon.total_ammo_stock = weapon.original_vars["total_ammo_stock"]


            # if player has weapon in their inventory display ammo
            elif self.name not in gameobj.allWeapons:
        
                gameobj.money -= self.cost
                self.give_weapon(gameobj=gameobj)

    def update_data(self):

        # if player does not have weapon in their inventory, display buy
        if self.name in engine.player.allWeapons:
            self.cost = self.ammoCost
            self.display_message.img_path = f"Hold E to buy ammo [Cost:{self.cost}]"


        # if player has weapon in their inventory display ammo
        elif self.name not in engine.player.allWeapons:
            self.cost = self.weaponCost
            self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"

        self.display_message.init_sprite()

    # swap weapon function
    def give_weapon(self,gameobj):

        # first end weapon state
        gameobj.weapon.state.completed()

        # find first element in list which is current weapon
        current_weapon = gameobj.allWeapons[0]
        
        # find second element in list which is next weapon
        weapon_to_give = self.name

        if len(gameobj.allWeapons) < gameobj.weaponCarryLimit:

            # remove current weapon and add to end of list
            gameobj.allWeapons.insert(0,weapon_to_give)


        elif len(gameobj.allWeapons) > gameobj.weaponCarryLimit:

            # remove current weapon and add to end of list
            gameobj.allWeapons.remove(current_weapon)
            gameobj.allWeapons.insert(0,weapon_to_give)

        # set new weapon
        gameobj.weapon = guns[weapon_to_give]
        gameobj.weapon.wielded_by = gameobj

        # enter state
        gameobj.weapon.state = gameobj.weapon.states['PICKUP']
        gameobj.weapon.state.enter()




for wb in wallbuy_parameters:

    wbobj = Wallbuy()

    set_attributes(game_object=wbobj,attributes=wallbuy_parameters[wb])
    wbobj.init()
    store_original_vars(game_object=wbobj)

    wbobj.spawn(pos=wallbuy_parameters[wb]['pos'])

    engine.active_pool.append(wbobj)


