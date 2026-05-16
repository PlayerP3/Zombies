import pygame,random,json,os,math,sys
from pygame.math import Vector2
from moveableobject import Moveable_Object
from game import engine
from weapon import *
from utils import *
from statemachine import StateMachine
from States.Deck.idle import Idle
from States.Deck.reloading import Reloading
from States.Deck.shooting import Shooting


# load files in
with open('config_suits_and_ranks.json','r') as suit_rank_attributes_file:

    suit_rank_weight_parameters = json.load(suit_rank_attributes_file)

class Card(Bullet):

    # keep start and end point arguments in case i want to give the bullet some quirky pathing when shot
    def __init__(self,
                         
                suit:str="Hearts",rank:str="1",rotation_speed:float=10):

        Bullet.__init__(self)

        self.suit = suit
        self.rank = rank
        self.rotation_speed = rotation_speed
    
        
    def init(self,attributes:dict={}):

        for att,val in attributes.items():

            setattr(self,att,val)
        
        # init sprite variables
        self.init_sprite()

        self.hurtbox.width = self.hurtbox_width
        self.hurtbox.height = self.hurtbox_height
        
        self.timer_init()

        self.original_vars = {k:v for k,v in self.__dict__.items()}



    # rotate card after it has been thrown
    def rotate_card(self):

        self.direction += self.rotation_speed
    
        

    def run_behaviour(self):
        
        # only show the orbital and draw it if it is active
        if self.is_active:
            
            # rotate card
            self.rotate_card()

            # update position
            self.update_position()

            # collision check
            # self.collision_check()

            # update movement vars
            self.update_movement()
            
            # # movement
            # self.move2()
            self.move_and_collide()

            # handle how long bullet is allowed to travel for
            self.travel_time()

            # draw surface
            self.draw_surface(position=self.hurtbox.center)
            # self.draw_mask(position=self.hurtbox.center)
            # self.draw_rect(position=self.hurtbox.center)
            self.draw_rect(position=self.hurtbox.center)


    def create_split_bullets(self):
        pass

    def explode(self):
        pass

    def enemy_collision_rects(self):
        pass

    def handle_damage_and_score(self):
        pass



class DeckStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        if self.state.done:

            self.transition_to_next_state()

            
        self.state.update()

# different decks
# e.g deck of hearts, deck of spades, deck of clubs, deck of fire and ice
# each deck gives the cards a different effect 
# each deck contains the same types of cards 1,2,3,4,5,j,q,k,A. the card number is linked to the probibility of the deck effect triggering + a set chance

class Deck(Weapon,DeckStateMachine):

    def __init__(self,total_cards:int=32,select_fire:str='fullauto',suits:list=['Hearts','Diamonds'],
                ranks:list=['1','2','3','4','5','6','7','8','9','10','J','Q','K','A'],
                   
                ):

        Weapon.__init__(self)

        self.cards_remaining = total_cards
        self.total_cards = total_cards
        self.deck_of_cards = []
        self.used_deck_of_cards = []
        self.current_card = None
    
        self.suits = suits
        self.ranks = ranks

        self.wielded_by = None
        self.is_shooting = False
        self.is_reloading = False
        self.select_fire = select_fire

        # these are endpoints for the bullets
        self.final_endpoints = []
        self.spread_final_endpoints = []


       

    def init(self,attributes:dict={}):

        for att,val in attributes.items():

            setattr(self,att,val)
        
        self.original_vars = {k:v for k,v in self.__dict__.items()}

        # these are very important to synergize the card with wepaon class
        self.bullets_remaining_in_mag = self.magazine_size
        self.total_cards = self.magazine_size

        # set speed for reload timer andf shooring timer
        self.reloading_timer.timer_speed = self.reload_speed
        self.shooting_timer.timer_speed = self.fire_rate

        self.states = {'IDLE':Idle(),
                       'RELOADING':Reloading(),
                       'SHOOTING':Shooting()}

        
        self.state = self.states['IDLE']


        self.create_deck(card_number=self.total_cards)


    # here a deck is a list of suit_rank, which we split to be able to get the suit and rank we will give to the card
    def create_deck(self,card_number:int):

        # we dont need to save card objects ion the deck, jsut what they are soq when we reload it doesnt matter
        # given number, generate a 

        self.deck_of_cards = []

        for i in range(card_number):

            suit = proc_using_weights(ItemWeights={k:suit_rank_weight_parameters['suits'][k] for k in self.suits})

            rank = proc_using_weights(ItemWeights={k:suit_rank_weight_parameters['ranks'][k] for k in self.ranks})
            
            self.deck_of_cards.append(f"{suit}_{rank}")

        self.current_card = self.deck_of_cards[0]

    def add_cards(self,suits:list,ranks:list,card_number:int):

        # update total cards
        self.total_cards += card_number

        for i in card_number:

            self.deck_of_cards.append(f"{suits[i]}_{ranks[i]}")

            

        # self.deck_of_cards.extend()

    # function to handle all the nuansces of using the deck of card with our current weapon class
    def update_deck_of_cards(self):

        # print(f'remaing = {self.bullets_remaining_in_mag}')
        # print(self.deck_of_cards)
        
        self.deck_of_cards.remove(self.current_card)
        self.used_deck_of_cards.append(self.current_card)

        # if deck of cards is empty assign current card to the first element
        if self.deck_of_cards:
            self.current_card = self.deck_of_cards[0]

        # otehrwsie assign current card to None
        elif not self.deck_of_cards:
            self.current_card = None
        


        
    def init_projectiles(self): 

        ## NORMAL CLICK SHOTS
        for bullet_object in self.projectile_attributes:
       
            # loop through where each bullet is being sent to out of all the available end points
            for i in range(len(self.final_endpoints)):

                # set a bullet to be the first thing in the inacitve pool
                bullet = OnShotEffectInactivePools[bullet_object].inactive_pool[i]

                # third conditional means we only ever try to run this code if there is atually a bullet in the inactive pool to use
                if not bullet.is_active and not bullet.fired and OnShotEffectInactivePools[bullet_object].inactive_pool: # second condiitonal prevents bullet being fired twice until reload. this is important because after bullets collided they are sent back to the inactive pool, but we dont want inactive bullets that have already been fired

                    # set projectile manager
                    bullet.projectile_manager = self

                    # set rank and suit
                    bullet.suit,bullet.rank = self.current_card.split('_')

                    # set image path
                    bullet.img_path = f"Sprites/Cards/{bullet.suit}/Back.png"

                    # init the bullet
                    bullet.init(self.projectile_attributes[bullet_object])

                    # update deck of cards
                    self.update_deck_of_cards()

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
                    OnShotEffectInactivePools[bullet_object].inactive_pool.remove(bullet)

                    # remove one from the display ammo because a bullet has been shot
                    self.bullets_remaining_in_mag -= 1
                
             


    # effectively a reload
    def shuffle(self):

        random.shuffle(self.used_deck_of_cards)
                
    # manage ammo count
    def managing_ammo_count(self):

        random.shuffle(self.used_deck_of_cards)
        self.deck_of_cards.extend(self.used_deck_of_cards.copy())
        random.shuffle(self.deck_of_cards)
        self.bullets_remaining_in_mag = self.magazine_size
        self.current_card = self.deck_of_cards[0]
        self.used_deck_of_cards = []

# This is a pool of card objects 
class CardPool():

    def __init__(self):

        self.inactive_pool = [Card() for _ in range(300)]



# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
OnShotEffectInactivePools["Card"] = CardPool()



# event processing for shooting
def shoot_event(event:pygame.Event):

    # handling mouse clicks
    if event.type == pygame.MOUSEBUTTONDOWN:

        if event.button == pygame.BUTTON_LEFT:

            # handle left clicks differently for semi auto and full aout weapons
            if engine.player.deck.select_fire == 'fullauto':

                # only allow shoointg if there are ammo reserrves or ammo in the current magazine
                if (engine.player.deck.total_ammo_stock > 0 or engine.player.deck.bullets_remaining_in_mag > 0):#and not player_bullet_manager.is_reloading, this prevents shooting if theyre using auto weapons and try to hold shoot whilskt reloading

                    # if the gun is not a dual wiled weapon set the regular shooting to true
                    if not engine.player.deck.is_dual_wield:

                        # set shooting to be true
                        engine.player.deck.is_shooting = True

                        # init the shooting timer
                        engine.player.deck.shooting_timer.timer_init()
                        
                        engine.player.deck.shooting_timer.timer_complete = True
                        
    # MOUSE BUTTON UP EVENTS
    if event.type == pygame.MOUSEBUTTONUP:

        if event.button == pygame.BUTTON_LEFT:

            # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
            # if the gun is not a dual wiled weapon set the regular shooting to true
            if not engine.player.deck.is_dual_wield:

                # set shooting to be true
                engine.player.deck.is_shooting = False
              
# event processing for shooting
def reload_event(event:pygame.Event):

    # handling mouse clicks
    if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_r:

            # if not dual wield or alternating click and dual wield
            if not engine.player.deck.is_dual_wield:

                if (engine.player.deck.bullets_remaining_in_mag < engine.player.deck.magazine_size):
                    engine.player.deck.is_reloading = True
                    engine.player.deck.reloading_timer.timer_init()
                        
    # MOUSE BUTTON UP EVENTS
    if event.type == pygame.MOUSEBUTTONUP:

        if event.button == pygame.BUTTON_LEFT:

            # if mouse is taken off the trigger then let shooting be False and reset the player bullet manager variables that need to be reset
            # if the gun is not a dual wiled weapon set the regular shooting to true
            if not engine.player.deck.is_dual_wield:

                # set shooting to be true
                engine.player.deck.is_shooting = False

# engine.extra_event_processing.append(shoot_event)
# engine.extra_event_processing.append(reload_event)