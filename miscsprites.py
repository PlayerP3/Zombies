import pygame

from moveableobject import Moveable_Object
from game import engine

# This will be for storing inactive pools of all bullet-like objects
MiscellaneousInactivePools = {}

# controls all type of shooting objects
class MiscellaneousManager():
    def __init__(self):

        self.active_pool = []

    def run_behaviour(self):

        if self.active_pool:

            to_remove = []

            for gameobj in self.active_pool:

                gameobj.run_behaviour()

                if not gameobj.is_active:
                    to_remove.append(gameobj)

            if to_remove:

                for gameobj in to_remove:

                    self.active_pool.remove(gameobj)

                    # add appropriate on shot effect manager
                    MiscellaneousInactivePools[gameobj.__class__.__name__].inactive_pool.append(gameobj)


MiscellaneousMgr = MiscellaneousManager()




# create damage number
class DamageNumber(Moveable_Object):

    def __init__(self):

        Moveable_Object.__init__(self)
        
    def init(self,text:str='1'):

        self.init_text_sprite(f"{text}")
        self.init_sprite()
        self.alpha = 255
        self.is_active = True
        self.hurtbox.center = (0,0)
        self.timer_speed = 4
        self.timer_limit = 6
        self.timer_init()
        

    def run_behaviour(self):

        self.reduce_alpha()

        # draw surface
        self.draw_surface(position=self.hurtbox.center)
        
# This is a pool of card objects 
class DamageNumberPool():

    def __init__(self):

        self.inactive_pool = [DamageNumber() for _ in range(300)]



# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
MiscellaneousInactivePools["DamageNumber"] = DamageNumberPool()


# code to show damage numbers
# event processing for shooting
def display_dmg_num_event(event:pygame.Event):

    # handling mouse clicks
    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_c:

           engine.display_dmg_num *= -1

engine.extra_event_processing.append(display_dmg_num_event)
