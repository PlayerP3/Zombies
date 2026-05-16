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
# from miscsprites import MiscellaneousMgr

class Item(Moveable_Object):

    def __init__(self):

        self.display_item = Moveable_Object()

        
        Moveable_Object.__init__(self)
     


    # what happens when a player picks up the item
    def pickup(self):

        pass

    # what happens when pickup is done like changing stats etc
    def give(self):

        engine.player.picked_items.append(self.name)

        pass

# different types of items on pickup
# exmaple
# item that gives familiar, on pickup run create_familiar function
# item that gives you access to DOT attacks, run add_status_effect_to_cards functino
# item that gives allows your DOT effects to evolve after reaching a certain number, turns on can_evolve signal, so when a bullet hits, triggers a status effect application, and in that
# application function we might chose an evolution, evolvced state always does twice the damage of the base
# each frame status effects look thropugh the immunity list for the entity it is attached to and it will notdo damage if the immunity si on 