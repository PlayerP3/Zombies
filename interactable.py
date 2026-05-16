import json,random,sys
from moveableobject import Moveable_Object,MiscellaneousMgr,MiscellaneousInactivePools
from animatedsprite import AnimatedSprite
from game import engine
from pygame.math import Vector2
from statemachine import StateMachine
from States.Interactable.idle import Idle
from States.Interactable.interacting import Interacting


# load in parameters
with open('config_interactable.json','r') as interactable_attributes_file:

    interactable_parameters = json.load(interactable_attributes_file)

class InteractableStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        self.state.update()

        if self.state.done:
            self.transition_to_next_state()

class Interactable(Moveable_Object,InteractableStateMachine):

    def __init__(self,cost:float=0,interact_time_limit:float=1):

        Moveable_Object.__init__(self)
        InteractableStateMachine.__init__(self)


        # things an interactable needs:
        # a separate rect to handle its interaction window
        # a message to blit or not to blit when something is interacting
        # returning true if something has interacted with it in the required way
        self.interact_time_limit = interact_time_limit
        self.display_message = AnimatedSprite()
        self.cost = cost
        self.is_active = False
        # self.progress_bar = ProgressBar(**progressbar_parameters['WallBuy'])
  

    def init(self,attributes:dict={},pos:tuple=(0,0)):

        self.spawn(pos)

        for att,val in attributes.items():

            setattr(self,att,val)

        # display message init
        self.display_message.init_text_sprite(f"E")
        self.display_message.init_sprite()
        self.display_message.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1

        self.init_sprite()
        self.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1

        # update hurtbox size
        self.hurtbox.width = self.hurtbox_width
        self.hurtbox.height = self.hurtbox_height

        # init state machine
        self.states = {'IDLE':Idle(),
                       'INTERACTING':Interacting()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['IDLE']

    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                    
                # display message
                self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))

                # if player is interacting
                if game_object.is_interacting:
                    self.state.emit('INTERACTING')

                # if player is interacting
                elif not game_object.is_interacting:
                    self.state.emit('IDLE')

  
    def run_effect(self,gameobj:object):
        pass

    # paying for interactable
    def pay(self,gameobj:object):

        if gameobj.money >= self.cost:
            gameobj.money -= self.cost

            # run effect depending on interactable
            self.run_effect(gameobj=gameobj)
            sys.exit()

    # what happens when object is within interacting rnage but not colliding with the actual object
    def handle_interaction(self,gameobj:object):

        # if the game obj is interacting
        if gameobj.is_interacting:

            # run timer
            self.run_timer()


            if self.timer_complete:
               
               self.pay()


# for soul boxes chekc if player is colliding AND enemies are in detah state


# This is a pool of card objects 
class InteractablePool():

    def __init__(self):

        self.inactive_pool = [Interactable() for _ in range(300)]



# add the card inactive pool to the object that stores all the pools for different projectiles/on shot effects
MiscellaneousInactivePools["Interactable"] = InteractablePool()

miscobj = MiscellaneousInactivePools['Interactable'].inactive_pool[0]

# spawns = [(-48,-48),(-220,-100),(100,220),(500,100)]
spawns = [(0,0)]

miscobj.init(attributes=interactable_parameters['Interactable'],pos=random.choice(spawns))

MiscellaneousMgr.active_pool.append(miscobj)
MiscellaneousInactivePools['Interactable'].inactive_pool.remove(miscobj)