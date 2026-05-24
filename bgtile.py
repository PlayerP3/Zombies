import json,sys
from engine.utils import *
from engine.animatedsprite import AnimatedSprite
from engine.objectsystem import objectManager

with open('config_wall.json','r') as wall_attributes_file:

    wall_parameters = json.load(wall_attributes_file)

class BgTile(AnimatedSprite):

    # keep start and end point arguments in case i want to give the bullet some quirky pathing when shot
    def __init__(self):

        AnimatedSprite.__init__(self)
    
        
    def init(self):

        self.init_sprite()


    # combines movement and collision function
    def update(self):

        # only show the orbital and draw it if it is active
        if self.is_active:

            # draw surface
            self.draw_surface(position=self.hurtbox.topleft)