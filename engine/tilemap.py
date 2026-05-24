import pygame,os,json,ast,sys
from .screen import gameScreen
from .objectsystem import objectManager

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

        # add window for chunk
        # set chunk in bg surf
        gameScreen.add_window('Chunk1',width=3200,height=3200,pos=(gameScreen.fullscreen_width//2,gameScreen.fullscreen_height//2))
        gameScreen.windows['Chunk1'].bg_offset_x = 1280//2
        gameScreen.windows['Chunk1'].bg_offset_y = 720//2


        # store all pos and layers
        layerPos = []

        # store layer and pos as kv pair
        for layer,layerData in params.items():

            for pos,metadata in layerData.items():

                layerPos.append((layer,pos))

        # go through kv pair and remove animated sprite class and ad vars you want
        for lp in layerPos:

            buildJSON = {}

            layer = lp[0]
            pos = lp[1]

            # get walls
            if params[layer][pos]['AnimatedSprite']['img_path'].split('/')[-1] == 'Wall.png':
                params[layer][pos]['class'] = 'Wall'


            # get class to convert to
            className = params[layer][pos]['class']
            classConversion = params[layer][pos]['class']
            del params[layer][pos]['class']

            # get sprite obj
            objinit = params[layer][pos]

            buildJSON.update(objinit['AnimatedSprite'])
            del objinit['AnimatedSprite']
            buildJSON.update(objinit)

            # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
            newObj = classMappings[classConversion]()
            for att,val in buildJSON.items():
                setattr(newObj,att,val)

            # sprite.surface_to_draw_on = 'tilemap'
            # sprite.vertice = 'topleft'
            newObj.hurtbox.topleft= ast.literal_eval(pos)
            newObj.zlayer_drawing = int(layer)
            newObj.spawnLocation = ast.literal_eval(pos)

            # start building copy
            if layer not in self.tilemap:
                self.tilemap[layer] = {} 
            
            if pos not in self.tilemap[layer]:
                self.tilemap[layer][pos] = {}

            # add animated sprite info to myCopy
            self.tilemap[layer][pos] = newObj

            
            # determine what happens to different objs
            if className == 'BgTile':

                newObj.surface_to_draw_on = 'Chunk1'
                newObj.init_sprite()

                posss = ast.literal_eval(pos)
                newObj.draw_surface(position=ast.literal_eval(pos),schedule_deletion=False)

                # objectManager.active_pool.append(newObj)
                # gameScreen.bgSurface['Chunk1'].blit(newObj.sprite,pos)
            

            else:

                # if className in ['Door','Wallbuy']:
                #     print(pos)
                #     sys.exit()
                newObj.is_active = True
                objectManager.active_pool.append(newObj)
        # print(self.tilemap)



        gameScreen.windows['Chunk1'].render_objects()



tilemapProcessor = Tilemap()