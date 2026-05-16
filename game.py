import pygame,random,os,string,numpy,math
from pygame.math import Vector2
from window import Window
from camera import Camera
import sys
pygame.font.init()

class Game():

    def __init__(self):
       
        self.FPS = 60
        self.delta = 1/self.FPS

        self.drawing_queue = {}
 
        # set camera
        self.camera = Camera()

        # set window
        self.windows = Window()

        # position of game objects
        self.object_positions = {}

        # get events
        self.events = None

        # get extra event processing
        self.extra_event_processing = []

        # set player
        self.player = None

        # create hud
        self.hud = None

        # for creating dmg numbers
        self.display_dmg_num = -1

        # astar graph,coors are key, and Node object is value
        self.astar_graph = {}

        # path cache
        self.path_cache = {}
        self.tile_size = 32
        self.tiles = {}
        self.accessible_tiles = []
        view_rect = self.windows.win.get_rect(center = (0,0))

        for x in range(view_rect.left,view_rect.right,32):
            for y in range(view_rect.top,view_rect.bottom,32):

                pos = (x,y)

                if pos in [(32,32)]:
                    continue
                self.accessible_tiles.append(pos)

                
        self.inaccessible_tiles = [(32,32),
            # Top row (y = -320)
            (-544, -320), (-512, -320), (-480, -320), (-448, -320), (-416, -320), (-384, -320), (-352, -320), (-320, -320),
            (-288, -320), (-256, -320), (-224, -320), (-192, -320), (-160, -320), (-128, -320), (-96, -320), (-64, -320),
            (-32, -320), (0, -320), (32, -320), (64, -320), (96, -320), (128, -320), (160, -320), (192, -320),
            (224, -320), (256, -320), (288, -320), (320, -320), (352, -320), (384, -320), (416, -320), (448, -320),
            (480, -320), (512, -320),

            # Bottom row (y = 288)
            (-544, 288), (-512, 288), (-480, 288), (-448, 288), (-416, 288), (-384, 288), (-352, 288), (-320, 288),
            (-288, 288), (-256, 288), (-224, 288), (-192, 288), (-160, 288), (-128, 288), (-96, 288), (-64, 288),
            (-32, 288), (0, 288), (32, 288), (64, 288), (96, 288), (128, 288), (160, 288), (192, 288),
            (224, 288), (256, 288), (288, 288), (320, 288), (352, 288), (384, 288), (416, 288), (448, 288),
            (480, 288), (512, 288),

            # Left column (x = -544, excluding corners)
            (-544, -288), (-544, -256), (-544, -224), (-544, -192), (-544, -160), (-544, -128), (-544, -96), (-544, -64),
            (-544, -32), (-544, 0), (-544, 32), (-544, 64), (-544, 96), (-544, 128), (-544, 160), (-544, 192),
            (-544, 224), (-544, 256),

            # Right column (x = 512, excluding corners)
            (512, -288), (512, -256), (512, -224), (512, -192), (512, -160), (512, -128), (512, -96), (512, -64),
            (512, -32), (512, 0), (512, 32), (512, 64), (512, 96), (512, 128), (512, 160), (512, 192),
            (512, 224), (512, 256)
]

        
        
        # tile display
        self.display_tiles = -1

        # sine wave testing
        self.sinrect = pygame.FRect(-120,0,10,10)
        self.sinrect.center = (-120,0)
        self.sintime = 0

 

        # pen 
        self.pen = pygame.sysfont.SysFont("Arial",10)
        self.damage_number_pen = pygame.sysfont.SysFont("Arial",24)

    # init/set values for certain attributes
    def init(self,player:object,spawn_point:tuple=(0,0)):

        self.player = player
        self.player.spawn(spawn_point)
        self.player.update_movement_vectors(unique_id='movement',direction_vectorX=0,direction_vectorY=0,acceleration=5,
                                            Xcceleration_rate=0,Xcceleration_rate_change='negative',max_value=0,
                                            reduce_on_wall_collision=False,reset_on_max_value=False)
        
    # update mouse pos of player because it i srescaled

    # handle base events
    def process_base_events(self):

        # loop through events
        for event in self.events:

            # if the actual X is clicked to close the tab
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            for processor in self.extra_event_processing:

                processor(event)

        # empty extra event processing
        self.extra_event_processing = []
    
    # update positions of all objects in the game
    def update_object_positions(self,coors:tuple,object_to_add:object):

        # check if the coors are in the object position dict already
        if coors not in self.object_positions:

            # add the coors and add the object
            self.object_positions[coors] = [object_to_add]

        # if the coors are already present we just want to add to the list that is already there
        elif coors in self.object_positions:

            if object_to_add not in self.object_positions[coors]:

                self.object_positions[coors].append(object_to_add)

    # function that handless all drawing
    def draw_objects(self):

        # Z layer list
        # Zombies - 0
        # Boss - 1
        # Boss Projectile - 2
        # Boss Orbital - 3
        # Player - 4
        # Player Projectile - 5
        # Player Orbital - 6
        # Danage Numbers - 7

        # this allows us to resolve z layers
        # meaning if there are multiple of a game object type on a layer
        # we refer to this to see what gets drawn first
        GameObjectPriority = {'Enemy':0,
                            'Player':0,
                            'Boss':0,
                            'Bullet':1,
                            'Orbital':2,
                            'DamageNumbers':3}
        
        # get all different surfaces that could be drawn on, always put winas the last
        surfs = list(set([drawinstruc['surface_to_draw_on'] for objid,drawinstruc in self.drawing_queue.items()]))

        surfs.remove(engine.windows.win)
        surfs.append(engine.windows.win)

        # go through each surface
        for surf in surfs:

            # create dictionary with only items that will be drawn on that surface
            specific_drawing_queue = dict(filter(lambda item: self.drawing_queue[item[0]]['surface_to_draw_on'] == surf, self.drawing_queue.items()))

            # sort drawing queue based on z layer
            # ZlayerSortedDrawingQueue = sorted(Creative_Mode.drawing_queue,key=lambda id:Creative_Mode.drawing_queue[id]['z_layer'],reverse=True)
            ZlayerSortedDrawingQueue = dict(sorted(specific_drawing_queue.items(),key=lambda x:self.drawing_queue[x[0]]['z_layer'],reverse=False))

            # for unique_id in Creative_Mode.drawing_queue:
            for unique_id in ZlayerSortedDrawingQueue:

                # print(ZlayerSortedDrawingQueue['key'])

                # if what we are drawing is going to be a surface
                if ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'surface':

                    adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position_rect'].x + self.camera.bg_offset_x, ZlayerSortedDrawingQueue[unique_id]['position_rect'].y + self.camera.bg_offset_y)

                    if ZlayerSortedDrawingQueue[unique_id]['alpha'] != -1:
                    
                        ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].set_alpha(ZlayerSortedDrawingQueue[unique_id]['alpha'])


                    ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'].blit(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'],adjusted_position)


                # if what we are drawing is going to be a rect
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'rect':

                    adjusted_position_rect = pygame.FRect(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].x + self.camera.bg_offset_x,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].y + self.camera.bg_offset_y,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].width,
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].height)

                    # draw rects
                    pygame.draw.rect(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],ZlayerSortedDrawingQueue[unique_id]['rect_colour'],adjusted_position_rect,1)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'circle':

                    # if inactive schedule deletion
                    if not ZlayerSortedDrawingQueue[unique_id]['game_object'].is_active:
                        ZlayerSortedDrawingQueue[unique_id]['schedule_deletion'] = True
                    # draw rects
                    pygame.draw.circle(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',(ZlayerSortedDrawingQueue[unique_id]['game_object'].centerx+self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['game_object'].centery+self.bg_offset_y),ZlayerSortedDrawingQueue[unique_id]['radius'],2)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'line':

                    adjusted_start =  (ZlayerSortedDrawingQueue[unique_id]['startpos'][0] + self.camera.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['startpos'][1] + self.camera.bg_offset_y)
                    adjusted_end = (ZlayerSortedDrawingQueue[unique_id]['endpos'][0] + self.camera.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['endpos'][1] + self.camera.bg_offset_y)

                    pygame.draw.line(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',adjusted_start,adjusted_end)

                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'lines':

                    points = [(p[0] + self.camera.bg_offset_x, p[1] + self.camera.bg_offset_y) for p in ZlayerSortedDrawingQueue[unique_id]['points']]

                    pygame.draw.lines(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],color='blue',points=points,closed=False)


                # if what we are drawing is going to be a surface
                elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'polygon':

                    adjusted_endpoints = [(e[0]+ engine.camera.bg_offset_x,e[1]+ engine.camera.bg_offset_y) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]

                    pygame.draw.polygon(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],(255,255,255),adjusted_endpoints)



        self.drawing_queue = {k:self.drawing_queue[k] for k in self.drawing_queue if not self.drawing_queue[k]['schedule_deletion']}



    def display_game_tiles(self,tile_size:int=32):

        
        if self.display_tiles == 1:

            # first we need the width and height of the screen
            # then we need ot know where the center is , in future the center can change depending on which room in the map we are in 
            view_rect = self.windows.win.get_rect(center = (0,0))

            for x in range(view_rect.left,view_rect.right,tile_size):
                for y in range(view_rect.top,view_rect.bottom,tile_size):

                    pos = (x,y)
                
                    rect = pygame.FRect(*pos,32,32)


                    engine.drawing_queue[f"{id(rect)}_rect"] = {'game_object':None,
                                                        'asset_to_draw':rect,
                                                        'asset_type':'rect',
                                                        'z_layer':2,
                                                        'surface_to_draw_on':self.windows.win,
                                                        'game_object_origin':'game',
                                                        'is_animated':False,
                                                        'animation_length':0,
                                                        'animation_timer':0,
                                                        'position':pos,
                                                        'position_rect':None,
                                                        'value':0,
                                                        'is_critical':False,
                                                        'sin_waveY':math.radians(90),
                                                        'sin_waveX':0,
                                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                                        'initial_width':2,
                                                        'initial_height':2,
                                                        'scale_factor_timer':1,
                                                        'alpha_value':255,
                                                        'rect_colour':'blue',
                                                        'schedule_deletion':True}
                    
                    # add text
                    # # txt2 = player_Weapon.pen.render(f'Score: {player.score}',True,'blue')
                    txt = self.pen.render(f'({pos[0]},{pos[1]})',True,'blue')

                    txt_rect = txt.get_frect(center=(pos[0]+(tile_size//2),pos[1]+(tile_size//2)))
            
                    engine.drawing_queue[f"{id(txt_rect)}_rect"] = {'game_object':None,
                                                        'asset_to_draw':txt,
                                                        'asset_type':'surface',
                                                        'z_layer':2,
                                                        'surface_to_draw_on':self.windows.win,
                                                        'game_object_origin':'game',
                                                        'is_animated':False,
                                                        'animation_length':0,
                                                        'animation_timer':0,
                                                        'position':txt_rect.center,
                                                        'position_rect':txt_rect,
                                                        'value':0,
                                                        'is_critical':False,
                                                        'sin_waveY':math.radians(90),
                                                        'sin_waveX':0,
                                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                                        'initial_width':2,
                                                        'initial_height':2,
                                                        'scale_factor_timer':1,
                                                        'alpha_value':255,
                                                        'rect_colour':'blue',
                                                        'schedule_deletion':True,
                                                        'alpha':255}
    

    def visualise_sine_wave2(self):

        
        # pos = (0,0)
        
        # ss = 0
        # x = 0
        # pointas = []
        # rectums = []

        # for i in range(180):

        #     y = math.sin(ss) * amp
            
        #     # create rect to recturms
        #     rectums.append(pygame.FRect(x,y,2,2))

        #     x += 1
        #     ss += 1/60
        lol = pygame.Vector2()

        amp = 100
        freq=200
        self.sinrect.centerx += 1
        # self.sinrect.y -= 1

        # setting it like this is literally setting it to a value of -amp to amp
        # self.sinrect.x = math.sin(self.sintime*20) * amp

        # but what i want is that there is an existing x velocity already, ie the bullet is moving in the x direction and the y
        # and i want to add another velocity which makes it keep moving in the main x,y movement but with a sin wave
        self.sinrect.centery = (math.cos(self.sintime*freq) * amp)

        

        self.sintime += 1/60

        for rr in [self.sinrect]:

            
            rect = rr
            pos = (rr.x,rr.y)


            engine.drawing_queue[f"{id(rect)}_rect"] = {'game_object':None,
                                                'asset_to_draw':rect,
                                                'asset_type':'rect',
                                                'z_layer':2,
                                                'surface_to_draw_on':self.windows.win,
                                                'game_object_origin':'game',
                                                'is_animated':False,
                                                'animation_length':0,
                                                'animation_timer':0,
                                                'position':pos,
                                                'position_rect':None,
                                                'value':0,
                                                'is_critical':False,
                                                'sin_waveY':math.radians(90),
                                                'sin_waveX':0,
                                                'sin_waveX_movement':random.choice(['positive','negative']),
                                                'initial_width':2,
                                                'initial_height':2,
                                                'scale_factor_timer':1,
                                                'alpha_value':255,
                                                'rect_colour':'blue',
                                                'schedule_deletion':True}
            


    def visualise_sine_wave3(self):

        
        # pos = (0,0)
        
        # ss = 0
        # x = 0
        # pointas = []
        # rectums = []

        # for i in range(180):

        #     y = math.sin(ss) * amp
            
        #     # create rect to recturms
        #     rectums.append(pygame.FRect(x,y,2,2))

        #     x += 1
        #     ss += 1/60
        lol = pygame.Vector2()

        amp = 1
        freq= 10
        speed = 150
        acceleration= 1

        # self.sinrect.centerx += 1
        # self.sinrect.y -= 1

        # setting it like this is literally setting it to a value of -amp to amp
        # self.sinrect.x = math.sin(self.sintime*20) * amp

        along = Vector2(1,0)

        cross = Vector2(0,-1)

        # but what i want is that there is an existing x velocity already, ie the bullet is moving in the x direction and the y
        # and i want to add another velocity which makes it keep moving in the main x,y movement but with a sin wave
        wiggle = (math.cos(self.sintime*freq) * amp)
        
        crosswiggle = cross*wiggle
        

        dirs = [along]

        for dd in dirs:

            direction_vectorX,direction_vectorY = dd
            movementx = (0,0)
            movementy = (0,0)
            
            # if only xvel or yvel is changed then set the other axis movement to be 0 because we want to move left, then check for a collision, and then move right and do the same
            if direction_vectorX !=0:
                movementx = (Vector2(direction_vectorX,0).normalize()*engine.delta*speed*acceleration)

            if direction_vectorY !=0:
                movementy = (Vector2(0,direction_vectorY).normalize()*engine.delta*speed*acceleration)

            # if both x and y are pressed, normalise the x and y values the player is going to move in.
            # when both x and y are pressed, the normalised value is different from if only one of those was pressed
            if direction_vectorX != 0 and direction_vectorY != 0:

                move = Vector2(direction_vectorX,direction_vectorY).normalize()*engine.delta*speed*acceleration

                # separate into only x movement and only y movement
                movementx = (move[0],0)
                movementy = (0,move[1])


            self.sinrect.centerx += movementx[0]
            self.sinrect.centery += movementy[1]

        dirs = [crosswiggle]

        for dd in dirs:

            direction_vectorX,direction_vectorY = dd
            movementx = (0,0)
            movementy = (0,0)
            
            # if only xvel or yvel is changed then set the other axis movement to be 0 because we want to move left, then check for a collision, and then move right and do the same
            if direction_vectorX !=0:
                movementx = (Vector2(direction_vectorX,0)*engine.delta*speed*acceleration)

            if direction_vectorY !=0:
                movementy = (Vector2(0,direction_vectorY)*engine.delta*speed*acceleration)

            # if both x and y are pressed, normalise the x and y values the player is going to move in.
            # when both x and y are pressed, the normalised value is different from if only one of those was pressed
            if direction_vectorX != 0 and direction_vectorY != 0:

                move = Vector2(direction_vectorX,direction_vectorY)*engine.delta*speed*acceleration

                # separate into only x movement and only y movement
                movementx = (move[0],0)
                movementy = (0,move[1])


            self.sinrect.centerx += movementx[0]
            self.sinrect.centery += movementy[1]
        

        self.sintime += 1/60

        for rr in [self.sinrect]:

            
            rect = rr
            pos = (rr.x,rr.y)


            engine.drawing_queue[f"{id(rect)}_rect"] = {'game_object':None,
                                                'asset_to_draw':rect,
                                                'asset_type':'rect',
                                                'z_layer':2,
                                                'surface_to_draw_on':self.windows.win,
                                                'game_object_origin':'game',
                                                'is_animated':False,
                                                'animation_length':0,
                                                'animation_timer':0,
                                                'position':pos,
                                                'position_rect':None,
                                                'value':0,
                                                'is_critical':False,
                                                'sin_waveY':math.radians(90),
                                                'sin_waveX':0,
                                                'sin_waveX_movement':random.choice(['positive','negative']),
                                                'initial_width':2,
                                                'initial_height':2,
                                                'scale_factor_timer':1,
                                                'alpha_value':255,
                                                'rect_colour':'blue',
                                                'schedule_deletion':True}
            
engine = Game()