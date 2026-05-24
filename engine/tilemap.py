import pygame,os,json,ast
from .screen import gameScreen

class Tilemap():
    def __init__(self):


        self.accessible_tiles = []
        self.inacessible_tiles = []
        self.tilemap = {}
        self.astar_graph = {}

        pass


    def load_tilemap(self,tileampJSON:str,classMappings:dict):

        with open(tileampJSON, 'r') as f:
            
            params = json.load(f)

        # store all pos and layers
        layerPos = []

        # store layer and pos as kv pair
        for layer,layerData in params.items():

            for pos,metadata in layerData.items():

                layerPos.append((layer,pos))

        # go through kv pair and remove animated sprite class and ad vars you want
        for lp in layerPos:

            updateJSON = {}

            layer = lp[0]
            pos = lp[1]

            # get class to convert to
            classConversion = params[layer][pos]['class']
            del params[layer][pos]['class']

            # get sprite obj
            objinit = params[layer][pos]

            # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
            newObj = classMappings[classConversion]()
            for att,val in objinit.items():
                setattr(newObj,att,val)

            # sprite.surface_to_draw_on = 'tilemap'
            # sprite.vertice = 'topleft'
            newObj.hurtbox.center = ast.literal_eval(pos)
            newObj.zlayer_drawing = int(layer)

            # start building copy
            if layer not in self.tilemap:
                self.tilemap[layer] = {} 
            
            if pos not in self.tilemap[layer]:
                self.tilemap[layer][pos] = {}

            # add animated sprite info to myCopy
            self.tilemap[layer][pos] = newObj


tilemapProcessor = Tilemap()