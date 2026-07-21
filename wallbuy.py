import pygame,os,re,sys
from pygame.math import Vector2
from pynaccle.utils import *
from pynaccle.objectsystem import objectManager
import json
import numpy as np
from item import Item
from gun import gun_parameters,Gun
from pynaccle.interactable import Interactable

class Wallbuy(Interactable):

    def __init__(self,weaponCost:int=500,ammoCost:int=100):

        Interactable.__init__(self)

        self.weapon_bought = None
        self.ammoCost = ammoCost
        self.weaponCost = weaponCost

    def init(self):

        super().init()

        # display message init
        self.display_message.update_message(f"Hold E to buy {self.name} [Cost:{self.weaponCost}]")
        self.display_message.init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            # if player does not have weapon in their inventory, display buy
            if self.name in gameobj.inventory.inventory['weapons']:

                # return weapon, can get from cached weapons because it is a reference to actual obj
                weapon = gameobj.cachedWeapons[self.name]

                if weapon.total_ammo_stock < weapon.original_vars["total_ammo_stock"]:

                    gameobj.money -= self.cost
                    weapon.total_ammo_stock = weapon.original_vars["total_ammo_stock"]


            # if player does not have weapon, give it to them
            elif self.name not in gameobj.inventory.inventory['weapons']:
        
                gameobj.money -= self.cost
                give_weapon(gameobj=gameobj,weaponName=self.name,weaponClass=Gun,weaponParams=gun_parameters)

    def update_data(self):

        # if player does not have weapon in their inventory, display buy
        if self.name in objectManager.player.inventory.inventory['weapons']:
            self.cost = self.ammoCost
            self.display_message.update_message(f"Hold E to buy ammo [Cost:{self.cost}]")

        # if player has weapon in their inventory display ammo
        elif self.name not in objectManager.player.inventory.inventory['weapons']:
            self.cost = self.weaponCost
            self.display_message.update_message(f"Hold E to buy {self.name} [Cost:{self.cost}]")

    

