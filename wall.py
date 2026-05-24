import json,sys
from engine.utils import *
from engine.moveableobject import Moveable_Object
from engine.objectsystem import objectManager

with open('config_wall.json','r') as wall_attributes_file:

    wall_parameters = json.load(wall_attributes_file)

class Wall(Moveable_Object):

    # keep start and end point arguments in case i want to give the bullet some quirky pathing when shot
    def __init__(self):

        Moveable_Object.__init__(self)
    
        
    def init(self):

        super().init()

    
    # handle collision damage etc
    def handle_collision(self,game_object:object):

        # set damage variable by checking if there was a crit
        damage = 0
        crit = proc(self.critical_chance)

        if crit:
            damage = self.damage*self.critical_multiplier

        elif not crit:
            damage = self.damage

        # FOR PLAYER BULLETS
        if game_object.object_of_origin == 'Player':

  

            if game_object.movement[0] < 0:
                game_object.rect.left = self.hurtbox.right

            if game_object.movement[0] > 0:
                game_object.rect.right = self.hurtbox.left

           # dpeendong on which direction they are moving in on the y axis set the player to be at the top or bottom of that rect
            if game_object.movement[1] < 0:
                game_object.rect.top = self.hurtbox.bottom

            if game_object.movement[1] > 0:
                game_object.rect.bottom = self.hurtbox.top


    # def check for a collision
    def collision_check(self):

        # find surrounding objects
        self.find_surrounding_game_objects()        

        # go through all possible game objects
        for game_object in self.surrounding_game_objects:

            # rect collision check
            if self.hitbox.colliderect(game_object.hitbox):

                # sprite collision check
                if self.mask.overlap(game_object.mask,(game_object.hitbox.left-self.hitbox.left,game_object.hitbox.top-self.hitbox.top)):

                    # handle collision
                    self.handle_collision(game_object=game_object)

    # combines movement and collision function
    def update(self):

        # only show the orbital and draw it if it is active
        if self.is_active:

            # track current tile
            self.update_position()

            # find game objects
            # self.find_game_objects_in_area()

            # handle collisions with the wall and entities
            # self.enemy_collision_rects()

            # # movement
            # self.move2()

            # collision check
            # self.collision_check()

            # run on collisioin effects
            # self.run_on_collision_effects()

            # apply status effects
            # self.apply_status_effects()

            # draw surface
            self.draw_surface(position=self.hurtbox.center)
            # self.draw_hitbox(position=self.hitbox.center)


# walle = Wall()

# set_attributes(game_object=walle,attributes=wall_parameters['Generic'])
# walle.init()
# store_original_vars(game_object=walle)

# walle.spawn((48,48))

# objectManager.active_pool.append(walle)


