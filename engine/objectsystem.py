import pygame,random,os,string,numpy,math,json,copy,ast
pygame.font.init()

class ObjectSystem():

    def __init__(self):

        # position of game objects
        self.object_positions = {}

        # get active pools
        self.active_pool = []
        self.inactive_pool = {}

        # path cache for objs
        self.path_cache = {}

        # set player
        self.player = None
                
    # run update function for all game objects
    def update_game_objects(self):

        if self.active_pool:

            to_remove = []

            for gameobj in self.active_pool:
                gameobj.update()
                if not gameobj.is_active:
                    to_remove.append(gameobj)

            if to_remove:
                for gameobj in to_remove:
                    gameobj.kill(self.active_pool,self.inactive_pool[gameobj.__class__.__name__])


    # def draw_tilemap(self):

    #     if self.tilemap:

    #         # get all the sprites 
    #         sprites = []

    #         for layer,posinfo in self.tilemap.items():

    #             for pos,spriteinfo in posinfo.items():

    #                 sprites.append(spriteinfo['AnimatedSprite'])

    #         for s in sprites:
    #             s.draw_surface(position=s.hurtbox.topleft)

    # def save_tilemap(self):

    #     with open(f'tilemaps/{self.tilemap_name}', 'w') as f:

    #         # mycopy = copy.deepcopy(self.tilemap)

    #         # print(mycopy)
    #         myCopy = {}


    #         # store all pos and layers
    #         layerPos = []

    #         # store layer and pos as kv pair
    #         for layer,layerData in self.tilemap.items():

    #             for pos,metadata in layerData.items():

    #                 layerPos.append((layer,pos))


    #         # go through kv pair and remove animated sprite class and ad vars you want
    #         for lp in layerPos:

    #             updateJSON = {}

    #             layer = lp[0]
    #             pos = lp[1]

    #             # get sprite obj
    #             sprite = self.tilemap[layer][pos]['AnimatedSprite']

    #             # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
    #             updateJSON['hurtbox_width'] = sprite.hurtbox.width
    #             updateJSON['hurtbox_height'] = sprite.hurtbox.height
    #             updateJSON['direction'] = sprite.direction
    #             updateJSON['img_path'] = sprite.img_path

    #              # start building copy
    #             if layer not in myCopy:
    #                 myCopy[layer] = {} 
                
    #             if pos not in myCopy[layer]:
    #                 myCopy[layer][pos] = {}

    #             # add animated sprite info to myCopy
    #             myCopy[layer][pos]['AnimatedSprite'] = updateJSON

    #             # add other info from tilemap
    #             for k,v in self.tilemap[layer][pos].items():

    #                 if k == 'AnimatedSprite':
    #                     continue

    #                 myCopy[layer][pos][k] = v

    #         json.dump(myCopy, f,indent=4)

    # def load_tilemap(self):

    #     with open(f'tilemaps/{self.tilemap_name}', 'r') as f:
            
    #         params = json.load(f)
        

    #     self.tilemap = {}


    #     # store all pos and layers
    #     layerPos = []

    #     # store layer and pos as kv pair
    #     for layer,layerData in params.items():

    #         for pos,metadata in layerData.items():

    #             layerPos.append((layer,pos))

    #     # go through kv pair and remove animated sprite class and ad vars you want
    #     for lp in layerPos:

    #         updateJSON = {}

    #         layer = lp[0]
    #         pos = lp[1]

    #         # get sprite obj
    #         spriteinit = params[layer][pos]['AnimatedSprite']

    #         # add variables of interest from the animated sprite class, can actuall use getattr to be more efficient and have a list of vars you want
    #         sprite = AnimatedSprite()
    #         for att,val in spriteinit.items():
    #             setattr(sprite,att,val)

    #         sprite.surface_to_draw_on = 'tilemap'
    #         sprite.vertice = 'topleft'
    #         sprite.hurtbox.topleft = ast.literal_eval(pos)
    #         sprite.zlayer_drawing = int(layer)

    #         # start building copy
    #         if layer not in self.tilemap:
    #             self.tilemap[layer] = {} 
            
    #         if pos not in self.tilemap[layer]:
    #             self.tilemap[layer][pos] = {}


    #         # now we can delete Animated sprite key val
    #         del params[layer][pos]['AnimatedSprite']

    #         # add animated sprite info to myCopy
    #         self.tilemap[layer][pos] = params[layer][pos]

    #         self.tilemap[layer][pos]['AnimatedSprite'] = sprite

        
            

objectManager = ObjectSystem()
