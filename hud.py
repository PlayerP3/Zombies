import pygame,random,os,string,numpy
from animatedsprite import AnimatedSprite,GameSprites
from game import engine
import copy

class HUD():

    def __init__(self):

        self.hud_elements = {}


    def add_element(self,group:str,hud_element:HUD_element):

        if not group in self.hud_elements:

            self.hud_elements[group] = [hud_element]

        elif group in self.hud_elements:

            self.hud_elements[group].append(hud_element)
        

    def display_hud(self):

        for group in self.hud_elements:

            for hud_element in self.hud_elements[group]:

                if hud_element.display:

                    hud_element.draw_surface(position=hud_element.win_pos)




class HUD_element(AnimatedSprite):

    def __init__(self,win_pos:tuple=(0,0)):

        AnimatedSprite.__init__(self)

        # you can give a set of sprite objects to the hud element, and give a zlayer as well, and then it handles how it is drawn by the hud
        # the position is always 
        self.display = True

        # this is the position on the win, not the surface it is drawn on
        self.win_pos = win_pos

        # linked var or object that helps control what is displayed and how
        self.linked_obj = None
        self.linked_var = None

    # reinit
    def init(self,attributes:dict={}):

        for att,val in attributes.items():

            setattr(self,att,val)
        
        # init sprite variables
        self.init_sprite(SpriteCache=GameSprites)

        self.original_vars = {k:v for k,v in self.__dict__.items()}


PlayingCardSprites = {}

# load sprites for all 
for suit in os.listdir('Sprites/Cards'):

    path = f"Sprites/Cards/{suit}"

    # print(path)
    for rank_png in os.listdir(path):
        

        png = f"Sprites/Cards/{suit}/{rank_png}"

        rank = rank_png.rstrip('.png')

        obj = AnimatedSprite(img_path=png,img_width=23,img_height=36,name=f"{rank}_{suit}")
        obj.init_sprite(SpriteCache=PlayingCardSprites)

  


# set hud
engine.hud = HUD()