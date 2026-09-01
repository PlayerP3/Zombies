import json,sys
from pynaccle.utils import *
from pynaccle.moveableobject import Moveable_Object
from pynaccle.objectsystem import objectManager
from pynaccle.quest import Quest,Task

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

    pass






### QUESTS
class UpgradeWeapon():
    pass