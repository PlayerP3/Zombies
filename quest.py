import json,sys
from pynaccle.utils import *
from pynaccle.moveableobject import Moveable_Object
from pynaccle.objectsystem import objectManager
from pynaccle.quest import Quest
from pynaccle.task import Task
from pynaccle.inventory import gameInventory
from enum import Enum
from pynaccle.configs import configData
from pynaccle.tilemap import tilemapProcessor
from pynaccle.quest import questManager

# class TaskType(Enum):
    
#     PLACEHOLDER = 'placeholder'
#     FILLSOULBOX = 'fillSoulBox'
#     PICKUPWEAPON = 'pickUpWeapon'
#     PICKUPPART = 'pickUpPart'
#     PLACEWEAPON = 'placeWeapon'
#     GOTOLOCATION = 'goToLocation'
#     INTERACTWITHITEM = 'interactWithItem'
    
# # Task
# class Task(Tasks):
    
#     def __init__(self, parentNodes = [], linkedNodes = [], targetValue=1, taskType = 'placeholder', description = 'Complete this task.'):
#         super().__init__(parentNodes, linkedNodes, targetValue, taskType, description)
        
#     def update(self):

#         if self.taskType is TaskType.PICKUPPART:
            
#             # check if 
#             pass
        
#         if self.taskType is TaskType.PICKUPWEAPON:
#             pass
        
#         pass

### TASKS
class FillSouls(Task):

    def __init__(self):

        super().__init__(self)

    def activate(self):

        for soulBox in self.linkedNodes:
            soulBox.state.emit('COLLECTING')

    def update(self):

        for soulBox in self.linkedNodes:
            if soulBox.state.name == 'Filled':
                self.currentValue += 1

class FindParts(Task):

    def __init__(self,buildableObject:str):
        
        self.buildableObject = buildableObject
    
        super().__init__(self)
        
    def init(self):

        self.targetValue = configData.loadedConfigs['buildable'][self.buildableObject]['partsNeeded']
        super().init()

    def run(self):

        # check for amount of parts picked for the buildable
        partsFound = gameInventory.get_inventory_item_size('buildable',self.buildableObject)
        
        # update current value
        self.currentValue = partsFound
        
        print(partsFound,'parts found')
        print(self.targetValue,'target val')
        
        # check if all found
        if partsFound == self.targetValue:
            self.state.emit('COMPLETED')

class BuildWeapon(Task):
    
    def __init__(self,buildableObject:str):
        
        self.buildableObject = buildableObject
        
        super().__init__(self)
        
    def init(self):
        
        # get all work benches
        workbenches = tilemapProcessor.get_obejcts(className="Bench")
        
        # find the one for this buildable object
        myWb = [wb for wb in workbenches if wb.buildableObject == self.buildableObject][0]
        
        # add to linked nodes
        self.add_linked_nodes(myWb)
        
        # init tasks
        super().init()

        
    def run(self):
        
        # loop through linked nodes and check if it is in the built stage
        for ln in self.linkedNodes:
            
            if ln.currentState == 'BUILDABLEBUILT':
                self.state.emit('COMPLETED')
        
class PickUpWeapon(Task):
    
    def __init__(self,buildableObject:str):
        
        self.buildableObject = buildableObject
        
        super().__init__(self)
    
    def init(self):
        
        # get all work benches
        workbenches = tilemapProcessor.get_obejcts(className="Bench")
        
        # find the one for this buildable object
        myWb = [wb for wb in workbenches if wb.buildableObject == self.buildableObject][0]
        
        # add to linked nodes
        self.add_linked_nodes(myWb)
        
        # init tasks
        super().init()
    
    def run(self):
        
        # loop through linked nodes and check if it is in the built stage
        for ln in self.linkedNodes:
            
            if ln.currentState == 'BUILDABLETAKEN':
                self.state.emit('COMPLETED')
                

class PlaceWeapon(Task):
    
    def __init__(self):
        pass
    
class GoToLocation(Task):
    
    def __init__(self):
            
        pass

class InteractWithItem(Task):
    
    def __init__(self):
        
        pass
    

### QUESTS
class BuildItem(Quest):
    
    def __init__(self,buildableObject:str):
        
        # set buildable object
        self.buildableObject = buildableObject
        
        super().__init__()
        
        # set tasks
        self.add_task(0,FindParts(buildableObject))
        self.add_task(1,BuildWeapon(buildableObject))
        self.add_task(2,PickUpWeapon(buildableObject))
        
        
        
myQuest = BuildItem(buildableObject='RobotBoy')
myQuest.set_description('Build RoboBoy Wonder Weapon')
myQuest.add_parent_nodes(nodes=objectManager.player)   


questManager.add_quest('Build Robotboy',myQuest)
questManager.start_quest('Build Robotboy')

    
    
    

