import random,string
import pygame,math
from pygame.math import Vector2

def process_chunks(core,chunk,gameobj):

    # if door attach connected chunk
    if gameobj.__class__.__name__ in ['Door','Wall']:

        core.tilemapProcessor.inaccessible_tiles.append(gameobj.spawnLocation)

    if gameobj.__class__.__name__ == 'Wall':
        gameobj.hurtbox_width = 33
        gameobj.hurtbox_height = 32

    if gameobj.__class__.__name__ == 'Door':
        gameobj.hurtbox_width = 28
        gameobj.hurtbox_height = 32
        gameobj.connectedChunk = "1"

