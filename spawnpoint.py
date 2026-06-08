import json,sys
from pynaccle.utils import *
from pynaccle.moveableobject import Moveable_Object
from pynaccle.objectsystem import objectManager


class SpawnPoint(Moveable_Object):

    # keep start and end point arguments in case i want to give the bullet some quirky pathing when shot
    def __init__(self):

        Moveable_Object.__init__(self)
    
        
    def init(self):

        super().init()

    # combines movement and collision function
    def update(self):

        # only show the orbital and draw it if it is active
        if self.is_active:
            # track current tile
            self.update_position()

            self.draw_surface(position=self.hurtbox.topleft)
            self.draw_rect(position=self.hurtbox.topleft)




