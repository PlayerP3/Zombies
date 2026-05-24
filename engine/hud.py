import pygame,random,os,string,numpy
from .animatedsprite import AnimatedSprite,GameSprites
from .screen import gameScreen

class HUD():

    def __init__(self):

        self.hud_elements = {}
        self.active_elements = []


    def add_element(self,group:str,hud_element:HUD_element):

        if not group in self.hud_elements:

            self.hud_elements[group] = [hud_element]

        elif group in self.hud_elements:

            self.hud_elements[group].append(hud_element)
        

    def display_hud(self):

        # get active elemnets
        self.active_elements = []

        for group in self.hud_elements:

            for hud_element in self.hud_elements[group]:

                

                if hud_element.display:

                    hud_element.update()
                    hud_element.draw_surface(position=hud_element.hurtbox.center)

                    # draw rect for debugging 
                    hud_element.draw_rect()

                    


                    self.active_elements.append(hud_element)

    # give list of hud element groups and they will be turned off
    def deactivate_hud_elements(self,groupNames:list):

        for group in groupNames:

            for hudElement in self.hud_elements[group]:

                hudElement.display = False


    # give list of hud element groups and they will be turned off
    def activate_hud_elements(self,groupNames:list):

        for group in groupNames:

            for hudElement in self.hud_elements[group]:

                hudElement.display = True
        


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

        # list of functions we will execute
        self.extraProcessing = []

    # reinit
    def init(self,attributes:dict={}):

        for att,val in attributes.items():

            setattr(self,att,val)
        
        # init sprite variables
        self.init_sprite(SpriteCache=GameSprites)

        self.hurtbox.width = self.hurtbox_width
        self.hurtbox.height = self.hurtbox_height
        self.hurtbox.center = self.win_pos

        self.original_vars = {k:v for k,v in self.__dict__.items()}

    # function to update some preoprty about the hud
    def update(self):

        if self.extraProcessing:

            for f in self.extraProcessing:

                f(self)


  


# set hud
overlay = HUD()