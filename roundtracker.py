import pygame,math,random,json
from engine.timer import Timer
from engine.utils import *
from engine.statemachine import StateMachine
from engine.objectsystem import objectManager
from States.RoundTracker.bossfight import BossFight
from States.RoundTracker.easteregg import EasterEgg
from States.RoundTracker.roundinprogress import RoundInProgress
from States.RoundTracker.roundend import RoundEnd
from States.RoundTracker.roundstart import RoundStart
pygame.font.init()

with open('config_roundtracker.json','r') as roundtracker_attributes_file:

    roundtracker_parameters = json.load(roundtracker_attributes_file)

# load in parameters
with open('config_enemy.json','r') as enemy_attributes_file:

    enemy_parameters = json.load(enemy_attributes_file)


# "MANAGER":{
#             "TOTAL_NUMBER_OF_ENTITIES": 1000,
#             "SPAWNLIMIT":500,
#             "TIMEBETWEENSPAWNS":0.2,
#             "ENTITIES_ALLOWED_ON_MAP":100,
#             "TIMEBETWEENROUNDS":10
#         }


# from ItemBench import ItemPools,ItemPoolsReset,remove_from_itempool,add_to_itempool
pygame.font.init()


class RoundTrackerStateMachine(StateMachine):

    def __init__(self):

        StateMachine.__init__(self)

    def update(self):

        self.state.update()

        if self.state.done:
            self.transition_to_next_state()

        

class Round_Tracker(RoundTrackerStateMachine):


    def __init__(self) -> None:

        # keep track of round number
        self.round_number = 0

        # store spawn locations
        self.spawnLocations = [(120,256)]

        # keeps track of the number of entities that have been spawned since the round started
        self.totalSpawnedInRound = 0
        self.totalDeadInRound = 0

        self.total_entities_spawned_in_game = 0

        # variable that keeps track of which entities can be spawned
        self.spawningEnemyTypes = ['Enemy']

        # dict of spawners
        self.spawners = {}

        # create spawners and init them
        for enemy in enemy_parameters:
            self.spawners[enemy] = Spawner(enemyType=enemy)
            self.spawners[enemy].parent_node = self

        self.connected_hud = None

        self.is_active = True

        RoundTrackerStateMachine.__init__(self)

    def init(self):

        # init state machine
        self.states = {'ROUNDSTART':RoundStart(),
                       'ROUNDINPROGRESS':RoundInProgress(),
                       'ROUNDEND':RoundEnd(),
                       'BOSSFIGHT':BossFight(),
                       'EASTEREGG':EasterEgg()}
        
        # set parent node for player states
        for x in self.states:
            self.states[x].parent_node = self
        
        self.state = self.states['ROUNDSTART']
        # self.state.enter()

        # make time between rounds longer
        self.states['ROUNDEND'].timer_limit = 7
        self.states['ROUNDEND'].timer_speed = 2
        self.states['ROUNDSTART'].timer_limit = 9
        self.states['ROUNDSTART'].timer_speed = 2

    # set which eneemies are goign to be allowed to spawn for the round
    def set_enemy_allowed(self):

        if self.round_number % 5 == 0:

            self.spawningEnemyTypes = ['Dogs']

        else:

            self.spawningEnemyTypes = ['Enemy']


            
    def update_spawners(self):

        for enemy in self.spawningEnemyTypes:

            self.spawners[enemy].update()

class Spawner(Timer):

    def __init__(self,enemyType:str='Enemy',timeBetweenSpawns:str=1,totalToSpawn:int=1,maxAllowedAlive:int=1):

        # parent node is the round tracker
        self.parent_node = None
        self.enemyType = enemyType
        self.timeBetweenSpawns = timeBetweenSpawns
        self.numberSpawned = 0
        self.totalToSpawn = totalToSpawn
        self.maxAllowedAlive = maxAllowedAlive
        self.is_spawning = False

        Timer.__init__(self)

    def calculate_metrics_for_round(self):

        if self.parent_node.round_number <= 10:

            self.totalToSpawn = math.ceil(min(0.09*(self.parent_node.round_number**2 -0.0029) * (self.parent_node.round_number + 23.958),100))
            enemy_parameters[self.enemyType]["health"] = 50 + (100 * self.parent_node.round_number)
            self.maxAllowedAlive = 1
            self.timer_limit = max(2*0.5**(self.parent_node.round_number-1),0.1)


        elif self.parent_node.round_number > 10:

            self.totalToSpawn = math.ceil(min(0.09*(self.parent_node.round_number**2 -0.0029) * (self.parent_node.round_number + 23.958),100))
            enemy_parameters[self.enemyType]["health"] = 950 * (1.1 ** (self.parent_node.round_number-9))
            self.maxAllowedAlive = 100
            self.timer_limit = max(2*0.5**(self.parent_node.round_number-1),0.1)

        self.numberSpawned = 0

        # start spawnign enemy as soon as we move into round in progress state
        self.is_spawning = True
        self.timer_complete = True


    def spawn_enemy(self):

        # get enemy type still alive
        enemyTypeAlive = [e for e in objectManager.active_pool if (e.__class__.__name__ == self.enemyType and e.object_of_origin == 'Enemy')]

        # find if all enemies are dead and then add the total number that were spawned to the round tracker
        if (len(enemyTypeAlive) == 0) and (self.numberSpawned == self.totalToSpawn):

            self.parent_node.totalDeadInRound += self.numberSpawned
            self.is_spawning = False

            return


        ## does the spawning
        # if limit for enemy hasnt been reached, or if the amount of enemies in the actie pool is the active enemy limit
        if self.timer_complete and ((self.numberSpawned < self.totalToSpawn) and (len(enemyTypeAlive) < self.maxAllowedAlive)):

            enemy_object = objectManager.inactive_pool[self.enemyType][0]

            # init object
            set_attributes(game_object=enemy_object,attributes=enemy_parameters['Enemy'])
            enemy_object.init()
            store_original_vars(game_object=enemy_object)
            enemy_object.spawn(random.choice(self.parent_node.spawnLocations))

            objectManager.active_pool.append(enemy_object)
            objectManager.inactive_pool[self.enemyType].remove(enemy_object)

            self.numberSpawned += 1

            # reinit timer
            self.timer_init()

        
            

    def update(self):

        if self.is_spawning:

            self.run_timer()

            self.spawn_enemy()

round_manager = Round_Tracker()
round_manager.init()
