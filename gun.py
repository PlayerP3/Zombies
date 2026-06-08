import pygame,random,json,os,math,sys
from pygame.math import Vector2
from pynaccle.moveableobject import Moveable_Object
from pynaccle.weapon import *
from pynaccle.utils import *
from pynaccle.statemachine import StateMachine
from pynaccle.objectsystem import objectManager
from States.Gun.idle import Idle
from States.Gun.reloading import Reloading
from States.Gun.shooting import Shooting
from States.Gun.pickup import Pickup
from States.Gun.pullout import Pullout
# from States.Gun.racking import Racking
from States.Gun.tbns import Tbns

# load files in
with open(os.path.join(os.path.dirname(__file__),'configs/config_gun.json'),'r') as gun_attributes_file:

    gun_parameters = json.load(gun_attributes_file)

class GunStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        if self.state.done:
            
            self.transition_to_next_state()
            # print(self.state.__class__.__name__)

        
        self.state.update()

# different decks
# e.g deck of hearts, deck of spades, deck of clubs, deck of fire and ice
# each deck gives the cards a different effect 
# each deck contains the same types of cards 1,2,3,4,5,j,q,k,A. the card number is linked to the probibility of the deck effect triggering + a set chance

class Gun(Weapon,GunStateMachine):

    def __init__(self,spreadReduction:float=0.6):

        self.spreadReduction = spreadReduction

        Weapon.__init__(self)
       

    def init(self):

        self.states = {'IDLE':Idle(),
                       'RELOADING':Reloading(),
                       'SHOOTING':Shooting(),
                       'PICKUP':Pickup(),
                       'PULLOUT':Pullout(),
                       'TBNS':Tbns()}
        
        # set pullout time
        self.states['PULLOUT'].timer_limit = self.pullout_time

        # set tbns time
        self.states['TBNS'].timer_limit = self.triggerResetSpeed

        # set parent node for states 
        for x in self.states:
            self.states[x].parent_node = self

        self.state = self.states['IDLE']

        super().init()


    def max_ammo(self):

        self.total_ammo_stock = self.original_vars['total_ammo_stock']
        self.bullets_remaining_in_mag = self.magazine_size
        
        

        
    def init_projectiles(self): 

        ## NORMAL CLICK SHOTS
        for bullet_object in self.projectile_attributes:
       
            # loop through where each bullet is being sent to out of all the available end points
            for i in range(len(self.final_endpoints)):

                # set a bullet to be the first thing in the inacitve pool
                bullet = objectManager.inactive_pool[bullet_object][i]

                # third conditional means we only ever try to run this code if there is atually a bullet in the inactive pool to use
                if not bullet.is_active and not bullet.fired and objectManager.inactive_pool[bullet_object]: # second condiitonal prevents bullet being fired twice until reload. this is important because after bullets collided they are sent back to the inactive pool, but we dont want inactive bullets that have already been fired

                    # set projectile manager
                    bullet.projectile_manager = self

                    # set image path
                    bullet.img_path = f"Sprites/Cards/Hearts/Back.png"

                    set_attributes(game_object=bullet,attributes=self.projectile_attributes[bullet_object])

                    # init the bullet
                    bullet.init()

                    store_original_vars(game_object=bullet)

                    bullet.pathing = 'regular'

                    # setting start and target pos
                    bullet.start_position = self.shooting_start_position
                    bullet.hurtbox.center = self.shooting_start_position
                    bullet.target_position = self.final_endpoints[i]

               
                    # bullet.target_position = bullet.projectile_manager.wielded_by.shooting_target_position


                    bullet.length_to_target = (Vector2(bullet.target_position) - Vector2(bullet.hurtbox.center)).length()

                    # # set bullet direction/current angle
                    # direction_vectorX, direction_vectorY = Vector2(bullet.target_position) - Vector2(bullet.rect.center)

                    # # update movement vector
                    # bullet.update_movement_vectors(unique_id='movement',direction_vectorX=direction_vectorX,direction_vectorY=direction_vectorY,
                    #                                             acceleration=bullet.acceleration,Xcceleration_rate=0,max_value=bullet.acceleration)

                    # set time bullet will wait until in projectile queue before it is sent to active pool
                    bullet.time_until_active = 0 # always 0 so it gets shot immediately

                    # start time until active timer
                    bullet.time_until_active_timer.timer_limit = bullet.time_until_active
                    bullet.time_until_active_timer.timer_init()

                    # # init the bullet
                    # bullet.init(self.projectile_attributes[bullet_object])

                    # determine movement
                    bullet.determine_movement(target=bullet.target_position,start=bullet.hurtbox.center)
                    
                    # add bullet to projectile queue before it is added to active pool
                    self.projectile_queue.append(bullet)
                    
                    # remove bullet obj from inactive pool
                    objectManager.inactive_pool[bullet_object].remove(bullet)

                    # remove one from the display ammo because a bullet has been shot
                    self.bullets_remaining_in_mag -= 1
       
            # spread shots
            if self.shot_spread_number > 0:

                # loop through where each bullet is being sent to out of all the available end points
                for i in range(len(self.spread_final_endpoints)):

                    # set a bullet to be the first thing in the inacitve pool
                    bullet = objectManager.inactive_pool[bullet_object][i]

                    # third conditional means we only ever try to run this code if there is atually a bullet in the inactive pool to use
                    if not bullet.is_active and not bullet.fired and objectManager.inactive_pool[bullet_object]: # second condiitonal prevents bullet being fired twice until reload. this is important because after bullets collided they are sent back to the inactive pool, but we dont want inactive bullets that have already been fired

                        # set projectile manager
                        bullet.projectile_manager = self

                        # set image path
                        bullet.img_path = f"Sprites/Cards/Hearts/Back.png"

                        set_attributes(game_object=bullet,attributes=self.projectile_attributes[bullet_object])

                        # init the bullet
                        bullet.init()

                        store_original_vars(game_object=bullet)

                        # reduce speed travel time, and damager
                        self.apply_spread_reduction(bullet)

                        bullet.pathing = 'regular'

                        # setting start and target pos
                        bullet.start_position = self.shooting_start_position
                        bullet.hurtbox.center = self.shooting_start_position
                        bullet.target_position = self.spread_final_endpoints[i]

                
                        # bullet.target_position = bullet.projectile_manager.wielded_by.shooting_target_position


                        bullet.length_to_target = (Vector2(bullet.target_position) - Vector2(bullet.hurtbox.center)).length()

                        # # set bullet direction/current angle
                        # direction_vectorX, direction_vectorY = Vector2(bullet.target_position) - Vector2(bullet.rect.center)

                        # # update movement vector
                        # bullet.update_movement_vectors(unique_id='movement',direction_vectorX=direction_vectorX,direction_vectorY=direction_vectorY,
                        #                                             acceleration=bullet.acceleration,Xcceleration_rate=0,max_value=bullet.acceleration)

                        # set time bullet will wait until in projectile queue before it is sent to active pool
                        bullet.time_until_active = 0 # always 0 so it gets shot immediately

                        # start time until active timer
                        bullet.time_until_active_timer.timer_limit = bullet.time_until_active
                        bullet.time_until_active_timer.timer_init()

                        # # init the bullet
                        # bullet.init(self.projectile_attributes[bullet_object])

                        # determine movement
                        bullet.determine_movement(target=bullet.target_position,start=bullet.hurtbox.center)
                        
                        # add bullet to projectile queue before it is added to active pool
                        self.projectile_queue.append(bullet)
                        
                        # remove bullet obj from inactive pool
                        objectManager.inactive_pool[bullet_object].remove(bullet)

    # reduce variables for spread objefcts
    def apply_spread_reduction(self,gameobj):

        gameobj.damage *= (self.spreadReduction)
        gameobj.travelTimeTimer.timer_limit *= (self.spreadReduction)
        gameobj.travelTimeTimeLimit *= (self.spreadReduction)
        gameobj.speed *= (self.spreadReduction)

# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
objectManager.inactive_pool["Bullet"] = [Bullet() for _ in range(1500)]


# create a weapon for each gun type and init it
guns = {g:Gun() for g in gun_parameters}

for gn,gun in guns.items():

    set_attributes(game_object=gun,attributes=gun_parameters[gn])
    gun.init()
    store_original_vars(game_object=gun)


