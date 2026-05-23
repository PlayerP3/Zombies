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


class Door(Interactable):

    def __init__(self):


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

            # remove from game tiles




# for wb in wallbuy_parameters:

#     wbobj = Wallbuy()

#     set_attributes(game_object=wbobj,attributes=wallbuy_parameters[wb])
#     wbobj.init()
#     store_original_vars(game_object=wbobj)

#     wbobj.spawn(pos=wallbuy_parameters[wb]['pos'])

#     engine.active_pool.append(wbobj)


