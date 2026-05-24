import pygame,random,os,string,numpy,json,sys
from pygame.math import Vector2
from .globs import *

# load files in
class Screen():

    def __init__(self):
        
        # the final display which the window is drawn onto
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        # get exact width and height of the full screen once the window has been made full screen, this is needed for centering the player
        self.fullscreen_width = pygame.display.Info().current_w
        self.fullscreen_height = pygame.display.Info().current_h

        # set windows var
        self.windows = {}

        # bg surfaces and the chunks they beloing to
        self.bgSurface = {}

    # function to add window
    def add_window(self,winName:str,width:int,height:int,pos:tuple):

        self.windows[winName] = Window(width=width,height=height,pos=pos)

    def render_windows(self):

        for nom,win in self.windows.items():
            win.render_objects()
        

class Window():
    
    def __init__(self,width:int=1200,height:int=800,pos:tuple=(0,0)):

        # drawing queue for window
        self.drawing_queue = {}

        # get the actual size we want the window to be
        self.win_width = width
        self.win_height = height

        # create window, everything is first drawn onto this surface
        self.win = pygame.Surface((width,height),pygame.SRCALPHA)

        self.hurtbox = pygame.FRect(*pos,width,height)

        self.bg_offset_x = 0
        self.bg_offset_y = 0

        self.extra_offset_x = 0
        self.extra_offset_y = 0

        self.pos = (0,0)
        self.focus = (0,0)
        self.movement = Vector2(0,0)
        self.damping = 0.9 # takes values between 0 and 1, loweer values = dampeningn spring/friction so object doesnt overshoot
        self.spring_stiffness = 0.01 # the inverse of smoothness, higher values is less smooth, loiwer vlaue sis more smooth
        self.zoom = 1

        
    # change camera view based on what is being shown
    def track_position(self):
        self.bg_offset_x = self.win.get_width()//2 - self.focus[0]+ self.extra_offset_x
        self.bg_offset_y = self.win.get_height()//2 - self.focus[1] + self.extra_offset_y


    # change camera based on obj
    def track_object(self,focus):
        
        self.bg_offset_x = self.win.get_width()/2 - focus.hurtbox.centerx
        self.bg_offset_y = self.win.get_height()/2 - focus.hurtbox.centery

    # change camera based on obj
    def track_object_spring(self):

        if ((Vector2(self.focus)*self.zoom) - (Vector2(self.pos))*self.zoom).length() <= 0.01:
            self.movement = Vector2(0,0)
        
        # Direction toward target
        acceleration = ((Vector2(self.focus)*self.zoom) - (Vector2(self.pos)*self.zoom)) * self.spring_stiffness

        # Add force to velocity
        self.movement += acceleration

        # Damping slows it down over time
        self.movement *= self.damping

        # Move object
        self.pos += self.movement

        self.bg_offset_x = self.win.get_width()//2 - self.pos[0]*self.zoom + self.extra_offset_x
        self.bg_offset_y = self.win.get_height()//2 - self.pos[1]*self.zoom + self.extra_offset_y

        

    # function that handless all drawing
    def render_objects(self):

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


        # if self.windows.win in surfs:
        #     surfs.remove(self.windows.win)
        #     surfs.append(self.windows.win)

        # go through each surface
    

        # sort drawing queue based on z layer
        # ZlayerSortedDrawingQueue = sorted(Creative_Mode.drawing_queue,key=lambda id:Creative_Mode.drawing_queue[id]['z_layer'],reverse=True)
        ZlayerSortedDrawingQueue = dict(sorted(self.drawing_queue.items(),key=lambda x:self.drawing_queue[x[0]]['z_layer'],reverse=False))

        # for unique_id in Creative_Mode.drawing_queue:
        for unique_id in ZlayerSortedDrawingQueue:

            # print(ZlayerSortedDrawingQueue['key'])

            # if what we are drawing is going to be a surface
            if ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'surface':

                adjusted_position = (0,0)

                if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                    adjusted_position = ((ZlayerSortedDrawingQueue[unique_id]['position'][0]*self.zoom) + self.bg_offset_x, (ZlayerSortedDrawingQueue[unique_id]['position'][1]*self.zoom) +self.bg_offset_y)

                elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                    adjusted_position = (ZlayerSortedDrawingQueue[unique_id]['position'][0]*self.zoom + self.win.get_width()//2, ZlayerSortedDrawingQueue[unique_id]['position'][1]*self.zoom + self.win.get_height()//2)



                if ZlayerSortedDrawingQueue[unique_id]['alpha'] != -1:
                
                    ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].set_alpha(ZlayerSortedDrawingQueue[unique_id]['alpha'])


                # print(adjusted_position)
                # print(surf)
                # sys.exit()
                # adjusted_position = (int(adjusted_position[0]),int(adjusted_position[1]))
                self.win.blit(ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'],adjusted_position)


            # if what we are drawing is going to be a rect
            elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'rect':

                adjusted_position_rect = pygame.FRect((ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].x*self.zoom)+ self.bg_offset_x ,
                (ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].y *self.zoom )+ self.bg_offset_y,
                ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].width*self.zoom,
                ZlayerSortedDrawingQueue[unique_id]['asset_to_draw'].height*self.zoom)
                

                # draw rects
                pygame.draw.rect(self.win,ZlayerSortedDrawingQueue[unique_id]['rect_colour'],adjusted_position_rect,1)

            # if what we are drawing is going to be a surface
            elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'circle':

                # if inactive schedule deletion
                if not ZlayerSortedDrawingQueue[unique_id]['game_object'].is_active:
                    ZlayerSortedDrawingQueue[unique_id]['schedule_deletion'] = True
                # draw rects
                pygame.draw.circle(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',(ZlayerSortedDrawingQueue[unique_id]['game_object'].centerx+self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['game_object'].centery+self.bg_offset_y),ZlayerSortedDrawingQueue[unique_id]['radius'],2)

            # if what we are drawing is going to be a surface
            elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'line':

                adjusted_start =  (ZlayerSortedDrawingQueue[unique_id]['startpos'][0] +  self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['startpos'][1] +  self.bg_offset_y)
                adjusted_end = (ZlayerSortedDrawingQueue[unique_id]['endpos'][0] +  self.bg_offset_x,ZlayerSortedDrawingQueue[unique_id]['endpos'][1] +  self.bg_offset_y)

                pygame.draw.line(ZlayerSortedDrawingQueue[unique_id]['surface_to_draw_on'],'blue',adjusted_start,adjusted_end)

            # if what we are drawing is going to be a surface
            elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'lines':

                points = [(p[0]*self.zoom + self.bg_offset_x, p[1]*self.zoom +  self.bg_offset_y) for p in ZlayerSortedDrawingQueue[unique_id]['points']]

                pygame.draw.lines(self.win,color='blue',points=points,closed=False)


            # if what we are drawing is going to be a surface
            elif ZlayerSortedDrawingQueue[unique_id]['asset_type'] == 'polygon':

                adjusted_endpoints = []

                if not ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                    adjusted_endpoints = [(e[0]*self.zoom+  self.bg_offset_x,e[1]*self.zoom+ self.bg_offset_y) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]

                elif ZlayerSortedDrawingQueue[unique_id]['ignore_offset']:
                    adjusted_endpoints = [(e[0]*self.zoom+  self.win.get_width()//2,e[1]*self.zoom +  self.win.get_height()//2) for e in ZlayerSortedDrawingQueue[unique_id]['endpoints']]


                pygame.draw.polygon(self.win,(255,255,255),adjusted_endpoints)



        self.drawing_queue = {k:self.drawing_queue[k] for k in self.drawing_queue if not self.drawing_queue[k]['schedule_deletion']}


    def draw_surface(self,asset_to_draw,asset_type:str='surface',game_object_origin:str='game',is_animated:bool=False,schedule_deletion:bool=True,
                       animation_length:int=0,position:tuple=(0,0),value:int=0,is_critical:bool=False,initial_width:int=0,initial_height:int=0,
                       zlayer:int=-1,ignoreCameraOffset:bool=False,alpha:int=255):

        position = (position[0] - (self.win.get_width()/gameScreen.windows['win'].zoom)//2,position[1]- (self.win.get_height()//gameScreen.windows['win'].zoom)//2)

        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))


        self.drawing_queue[random_id] = {'game_object':'obj',
                                        'asset_to_draw':asset_to_draw,
                                        'asset_type':asset_type,
                                        'z_layer':zlayer,
                                        'game_object_origin':game_object_origin,
                                        'is_animated':is_animated,
                                        'animation_length':animation_length,
                                        'animation_timer':animation_length,
                                        'position':position,
                                        'position_rect':0,
                                        'value':value,
                                        'is_critical':is_critical,
                                        'sin_waveY':0,
                                        'sin_waveX':0,
                                        'sin_waveX_movement':random.choice(['positive','negative']),
                                        'initial_width':initial_width,
                                        'initial_height':initial_height,
                                        'scale_factor_timer':1,
                                        'alpha':alpha,
                                        'ignore_offset':ignoreCameraOffset,
                                        'schedule_deletion':schedule_deletion}
    
gameScreen = Screen()
