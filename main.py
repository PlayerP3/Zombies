import pygame,random,json,os
from Game import Game
from Player import Player
from Drawing_TileMaps import Creative_Mode
from Game_Clock import Timer

from A_star_search_algorithm import *
from Enemy import *
import numpy as np
import sys
from Event_Manger import Event_Handler
from ItemBench import Item_Bench
from Orbitals import Orbital
# from Round_Trackers import Round_Tracker
import cProfile
import pstats
from Boss import *
from Dummy import Dummy
from Walls import Wall
from Interactable import InteractableMgr
from MoveableObject import Moveable_Object_Manager,Moveable_Object,OnCollisionEffectMgr,SoulObjectMgr
from Bullets import BulletObjectMgr,Weapons
from Status_Effects import StatusEffectMgr
from PowerUp import PowerUpMgr, StatBoostMgr
import random
pygame.mixer.init()

# from Bullets import Weapon,Bullet,Item_Bench

## The premise of A* is that when the entity is not doing normal behaviour, it can track and approach the target using A*
## think about pooling. So we need something to manage all the entities we haveds

#####open jsons

with open("config_windows.json",'r') as window_parameter_files,open('config_tilemap.json','r') as tilemap_coors_andsurface_file, \
    open('config_entity.json','r') as entity_attributes, open('config_bullet.json','r') as bullet_attributes_file, \
    open('config_player.json','r') as player_attributes_file, open('config_tilemap_wall_lines.json','r') as tilemap_wall_lines_attributes_file, \
    open('config_orbitals.json','r') as orbital_attributes_file,open('config_weaponmods.json','r') as weapon_mod_file,open('config_playermods.json') as player_mod_file, \
    open("config_boxes.json",'r') as boxes_attributes_file:

    window_parameters = json.load(window_parameter_files)

    tilemap_coors_andsurface = json.load(tilemap_coors_andsurface_file)

    entity_parameters = json.load(entity_attributes)

    bullet_parameters = json.load(bullet_attributes_file)

    player_parameters = json.load(player_attributes_file)

    wall_line_parameters = json.load(tilemap_wall_lines_attributes_file)

    orbital_parameters = json.load(orbital_attributes_file)

    weapon_mod_parameters = json.load(weapon_mod_file)
    player_mod_parameters = json.load(player_mod_file)

    box_parameters = json.load(boxes_attributes_file)


# # create sound
# WeaponSounds = pygame.mixer.Sound(file="C:\Users\panda\Desktop\Universal_Config_Files\Sounds\Gun\SingleGunshot1.wav")


# dispaly = pygame.display.set_mode((window_parameters['SCREENWIDTH'],window_parameters['SCREENHEIGHT']))
# win = pygame.Surface((window_parameters['SCREENWIDTH']//4,window_parameters['SCREENHEIGHT']//4))

# set the window to be the full screen
# display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)





# Create a surface for the fog of war
fog_of_war_surface = pygame.Surface((Creative_Mode.fullscreen_width/Creative_Mode.resize,Creative_Mode.fullscreen_height/Creative_Mode.resize),pygame.SRCALPHA)
# fog_of_war_surface = pygame.Surface((Creative_Mode.fullscreen_width/Creative_Mode.resize,Creative_Mode.fullscreen_height/Creative_Mode.resize))

# fog_of_war_surface = fog_of_war_surface.convert_alpha()  # Ensure it h)
fog_of_war_surface.set_colorkey('WHITE')
# fog_of_war_surface.set_alpha(200)
# fog_of_war_surface.set_colorkey((0,0,0,200))


# store the size of the window that is regualr sized, and everything is drawn onto it
Creative_Mode.drawing_window_width = win.get_width()
Creative_Mode.drawing_window_height = win.get_height()



box_rect = pygame.FRect(0,0,Creative_Mode.drawing_window_width/2, Creative_Mode.drawing_window_height/2)

# now put the center of the rect as the center of the screen
box_rect.center = (Creative_Mode.drawing_window_width/4, Creative_Mode.drawing_window_height/4)

# intialise the display with the pataemet
# displaaaay = pygame.display.set_mode((big_screen_w,big_screen_h))
# win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)



# win = pygame.display.set_mode((window_parameters['SCREENWIDTH'],window_parameters['SCREENHEIGHT']),pygame.FULLSCREEN)

# win = pygame.display.set_mode((Creative_Mode.fullscreen_width/Creative_Mode.resize,Creative_Mode.fullscreen_height/Creative_Mode.resize))

# create death screen text
DeathText = Creative_Mode.pen.render(f'You are Died',True,'blue')

DTRect = DeathText.get_rect(center=(320,320))

pygame.mouse.set_visible(False)


# default parameters for a wall
default_wall_params = {"object_of_origin":"Map",

        "rect_width":32,"rect_height":32,"health":120,"acceleration":1,
        "decceleration_rate":1,

        "knockback_resistance":2,"knockback_strength":1,

        "speed":0,"damage":20,"health_state":{},"zlayer_drawing":1,"rect_colour":"blue",

        "allowed_collisions":["Enemy"],

        "general_explosion_immunity":False,"self_explosion_immunity":False,

        "x_metres_before_collision_detection":500,"x_metres_before_homing_detection":120,

        "is_immune_to":[],"status_effect_immunity_tracker":{},"can_gain_natural_immunity":False,
        "on_collision_effects":{},

        "is_target_for_homing":True,

        "damage_resistance":1,"is_invincible":False,"on_shot_effects":{},
        "on_damage_taken_effects":{},"status_effects":{},

        "stop_at_target_point":False,"can_ricochet":False,
        "score":0,"score_on_hit":20,"score_on_kill":150,

        "max_acceleration":1,"min_acceleration":0,"invincibility_duration":3,

        "score_multiplier":1,"action_every_X_frames":60,"ranged_dot_effects":[],

        "interactable_radius":500,
        "cost":250,
        "interact_time_limit":0.15,
        "display_message":"Hold E to open wall",
        "spawn_point":[0,0],

        "name":"Walle",
        "img_path":"Universal_Config_Files/Sprites/Environment/Walle.png",
        "img_width":32,
        "img_height":32,
        "animation_delay":2,
        "animation_speed":4,
        "directions":["0"],
        "starting_direction":"0",
        "transform_width":26,
        "transform_height":40,
        "transform":False,

        "draw_sine_wave_speed":5,
        "draw_sine_wave_amplitude":6,
        "shadow_frames":1,
        "shadow_transform_width":10,
        "shadow_transform_height":8,
        "shadow_y_offset":14,
        "shadow_animation_speed":3,
        "shadow_animation_delay":4,
        "has_shadow":False,
        "sprite_movement_type":"none",
        "flip_range":[],

        "is_interactable":False,
        "linked_wall_coors":[]}

def main():

    playing = True

    clock = pygame.time.Clock()
    true_game_clock = Timer()

    bgs = Creative_Mode.get_sprites(bgpaths=('Sprites','Environment'),tile_size_height=window_parameters['TILE_SIZE'],tile_size_width=window_parameters['TILE_SIZE'],PALETTESCREENWIDTH=window_parameters['PALETTESCREENWIDTH'],
                         SCREENWIDTH=window_parameters['SCREENWIDTH'])

    # bgs2 = Creative_Mode.get_background_2(bgpaths=('Assets_Platformer','Background'),item_trap_paths=('Assets_Platformer','Traps'),tile_size_height=window_parameters['TILE_SIZE'],tile_size_width=window_parameters['TILE_SIZE'],PALETTESCREENWIDTH=window_parameters['PALETTESCREENWIDTH'],
    #                      SCREENWIDTH=window_parameters['SCREENWIDTH'])

    # create circle
    # new_circ = Circles(circle_type=dddddddd,object_of_origin='Boss',health=200,circle_center=(220,220),radius=50,movement_speed=50,radius_fluctuate_type='out-in',fluctuate_radius_change_speed=2000,
    #                    regular_radius_change_speed=100,max_radius=75,min_radius=10)

    # add circle to
    # Creative_Mode.circular_walls.append(new_circ) # when setting a circle to active we need to call this, and when inactive we remove it from this lista

    # set delta time for creative nmode fps variable
    Creative_Mode.delta_time = 1/window_parameters['FPS']

    # print(Creative_Mode.delta_time)p
    # sys.exit()

    # JUST FOR THIS ADD THE THIRD LAYER TO THE FIRST LAYER IN THE JSON
    tilemap_coors_andsurface['layer_1'].update(tilemap_coors_andsurface['layer_3'])

    # convert json to have keys that are actual tuples and nto strings that have to be manipulated
    Creative_Mode.convert_json_to_dict(tilemap = tilemap_coors_andsurface)

    # get different spawn points
    Creative_Mode.get_spawn_points(tilemap=tilemap_coors_andsurface,specific_layer='layer_3')

    # get all tile information
    all_rects_masks_surfaces_scalefactor = Creative_Mode.get_all_rects_masks_fixed_range(jsondata = tilemap_coors_andsurface, key_surface=bgs)

    # get all tiles for Astar, layer 1 is considered the layer for walking
    Creative_Mode.all_tiles_for_astar,Creative_Mode.all_empty_tiles = get_all_tiles_fixed_range(tilemap_layer=tilemap_coors_andsurface,specific_layer='layer_1')


    # get all the rects for the walls, the key in the dictionary will be the wall coordinates and the value will be the rect. we can chang the value fromm just the rect and to the scale factor and surface by changing
    # this value in the dictionary rect_mask_scalefactor[0]
    Creative_Mode.all_walls = {(rect_mask_scalefactor[0].x,rect_mask_scalefactor[0].y):rect_mask_scalefactor[0] for key, rect_mask_scalefactor in all_rects_masks_surfaces_scalefactor['layer_2'].items()}
    # Creative_Mode.all_walls = {(rect_mask_scalefactor[0].x,rect_mask_scalefactor[0].y):Wall() for key, rect_mask_scalefactor in all_rects_masks_surfaces_scalefactor['layer_2'].items()}

    # for coor,wall in Creative_Mode.all_walls.items():

    #     # reintialise walls
    #     wall.reinitialise(**default_wall_params)
    #     wall.rect.topleft = coor



    # add a key entry dwa`for bounding rects
    # Creative_Mode.all_walls["Bounding_Boxes"] = []
    # Creative_Mode.all_walls = {(rect_mask_scalefactor[0].x,rect_mask_scalefactor[0].y):Wall(rect_mask_scalefactor[0]) for key, rect_mask_scalefactor in all_rects_masks_surfaces_scalefactor['layer_2'].items()}

    # # go through all the walls in the game
    # for coor,wall in Creative_Mode.all_walls.items():

    #     # find surrounding coors in all 8 direction and store those coors in the surrounding game objects var
    #     surrounding_rects = Creative_Mode.find_surrounding_walls(center_coors=wall.rect.topleft,tile_width=Creative_Mode.tile_size,tile_height=Creative_Mode.tile_size)

    #     wall.surrounding_game_objects = [Creative_Mode.all_walls[c] for c in surrounding_rects if c in Creative_Mode.all_walls and c != coor]


    ########wwddww
    # i think the issue here is that we need to add 25 to the x and y points for the start point so we are at the centerddaaaaaa
    # enemy_manager = Enemy_Manager(number_of_entities=5,name='pony',x=550,y=0,width=50,height=50,start_point=(550,0),end_point=(450,a0),tilemap_layer=tilemap_coors_andsurface)
    # enemy_manager = Enemy_Manager(number_of_entities=entity_parameters['REGULAR']["MANAGER"]["TOTAL_NUMBER_OF_ENTITIES"], name='pony', x_y=Creative_Mode.spawn_points, width=entity_parameters['REGULAR']["WIDTH"],
    #                                height=entity_parameters['REGULAR']["HEIGHT"], start_point=(0,0), end_point=(320,320),
    #                                health = entity_parameters['REGULAR']["HEALTH"], speed=entity_parameters['REGULAR']["SPEED"],
    #                                spawn_limit=entity_parameters['REGULAR']["MANAGER"]["SPAWNLIMIT"], fov_depth_movement=entity_parameters['REGULAR']["fov_depth_movement"],
    #                                fov_rays_movement=entity_parameters['REGULAR']["fov_rays_movement"],fov_width_movement = entity_parameters['REGULAR']["fov_width_movement"],
    #                                entities_allowed_on_map = entity_parameters['REGULAR']["MANAGER"]["ENTITIES_ALLOWED_ON_MAP"],time_between_spawns = entity_parameters['REGULAR']["MANAGER"]["TIMEBETWEENSPAWNS"],
    #                                time_between_rounds=entity_parameters['REGULAR']["MANAGER"]["TIMEBETWEENROUNDS"],
    #                                attack_rect_width = entity_parameters['REGULAR']["attack_rect_width"],attack_rect_height = entity_parameters['REGULAR']["attack_rect_height"],
    #                                hit_detection_extra_width_and_height = entity_parameters['REGULAR']["hit_detection_extra_width_and_height"],
    #                                attack_speed = entity_parameters['REGULAR']["attack_speed"], attack_damage = entity_parameters['REGULAR']["attack_damage"],
    #                                fov_depth_attack = entity_parameters['REGULAR']["fov_depth_attack"],fov_width_attack = entity_parameters['REGULAR']["fov_width_attack"],
    #                                fov_rays_attack= entity_parameters['REGULAR']["fov_rays_attack"],time_between_attacks = entity_parameters['REGULAR']["time_between_attacks"],
    #                                tick_rate = entity_parameters['REGULAR']["tick_rate"],time_between_ticks = entity_parameters['REGULAR']["time_between_ticks"],
    #                                is_piercing = entity_parameters['REGULAR']["is_piercing"], enemy_type = entity_parameters['REGULAR']["enemy_type"],
    #                                object_of_origin=entity_parameters['REGULAR']["object_of_origin"],is_target_for_homing=entity_parameters['REGULAR']["is_target_for_homing"])
    enemy_manager = []

    ## initialise event managers
    # start player at the center of the window
    # add all weapons to player parameters
    player_parameters["all_weapons"] = bullet_parameters
    player = Player()
    player.reinitialise(**player_parameters)
    player.rect.center = (200,400)

    # create dummy
    # dum = Dummy()sd ps da

    # boss manager
    boss_controller = Boss_Manager()

    # round tracker
    round_tracker = Round_Tracker()

    # item pool manager
    # item_bench_manager = Item_Bench2(all_weapons = Weapons,player_mods=player_mod_parameters,weapon_mods=weapon_mod_parameters,number_of_item_pedestals=3)

    # controls how events are handled for different groups in the game
    event_control = Event_Handler()



    # win.fill(window_parameters['DEFAULT_WINFILL'])

    # drawing static background before game loop so it doesnt have to be rendered every frame, as in blitted every frame
    # the surface must start at 0,0
    background = Creative_Mode.draw_jsondata_fixed_range_return_surface(jsondata=tilemap_coors_andsurface,key_surface=bgs,win=win,player=player)

    # apply alpha/transparency to regular window
    win.convert_alpha()
    win.set_alpha(window_parameters['ALPHA'])

    # create knife

    knife = pygame.FRect(200,200,10,10)

    stove = pygame.FRect(200,400,10,10)
    stove_timer = 0

    # can you see me?

    start_end_pos = player.knifing_path(win=win,knife=knife,fov_width=180)
    reset_shot = player.knifing_path(win=win,knife=knife,fov_width=180)

    # change knfe start point
    # knife.centerx = start_end_pos[0][0]
    # knife.centery = start_end_pos[0][1]


    # knife.centerx = player.rect.centerx + 100
    # knife.centery = player.rect.centery + 150

    angle = math.radians(220)

    anchorY = 100
    anchorX = 200
    frequency = 3
    amplitude = 20 # this makes the wave more hilly
    timer = math.radians(180)





    theta = math.radians(270)  # For example, 45 degrees, change this for different angles
    # theta = 180

    # Speed along the line. this increases the width of the wave, ie it stretches it out
    speed = 0.8
    # Sine wave frequency
    wave_frequency = 0.3
    wave_amplitude = 20

    a = 1    # Linear movement multiplier
    b = 10  # Exponential decay rate
    c = 2    # Frequency of sine oscillationa
    x = 0
    t = 0

    x1,y1 = 300,300

    # myhole = BlackHole(320,320,30,30,100,2,0,0,100 ,'in',1)
    # myhole.spawn(240,240)

    player.update_movement_vectors(unique_id='movement',direction_vectorX=sum(player.movementx),direction_vectorY=sum(player.movementy),acceleration=0,
                                         Xcceleration_rate=12,Xcceleration_rate_change='positive',max_value=1,
                                         reduce_on_wall_collision=False,reset_on_max_value=False)


    quit_time = 3
    quit_log = 0

    # create bounding box
     # create a rect for the window
    bounding_rect = pygame.FRect(0,0,win.get_width()+200,win.get_height()+200)

    # center it so the it always has the player at the center
    bounding_rect.center = player.rect.center

    while playing:

        # quit_log += 1/60
        # print(quit_log)
        # if quit_log >= quit_time:
        #     playing = False


        # drawing and frames
        clock.tick(window_parameters['FPS'])

        # change camera  focus based on where the player isaa
        Creative_Mode.camera_crew_centered(focus=player)

        # find positions in frame
        Creative_Mode.find_positions_in_frame(player=player,win=win)

        win.fill('black')

        # blit background onto surface
        win.blit(background,(0+Creative_Mode.bg_offset_x,0+Creative_Mode.bg_offset_y))

        # create copy of windowd
        win_copy = win.copy()

        # track rounds
        # round_tracker.track_enemy_spawning(enemy_spawners=[enemy_manager],player=player)


        # get events currently in progress
        all_events = pygame.event.get()

        # event_control.player_events(all_events=all_events,player=player,player_Weapon=player_Weapon)
        event_control.player_events(all_events=all_events,player=player,item_bench_manager=None)
        event_control.entity_events(all_events=all_events,enemy_manager=enemy_manager,player=player)
        event_control.game_events(all_events=all_events,boss_controller=boss_controller,player=player)

        ### ITEM BENCH STUFF ###ddddddddddddda
        # item_bench_manager.draw_rect(win=win)
        # item_bench_manager.draw(player=player)
        # item_bench_manager.cycle_through_weapons_and_display(current_player_mods=player.all_player_mods,current_weapon_mods=player.all_weapon_mods,current_weapons=[wpn.name for wpn in player.left_hand_weapon_slots.values() if wpn])

        # need to get entity positions before the plkayer code is ran
        # get entity position dictionary
        # enemy_manager.get_entity_positions()
        player.track_player_position()

        PowerUpMgr.run_behaviour()

        # run wall buy Mhr
        # WallBuyMgr.run_behaviour()


        # box activitypdddddddddd
        # Boxes.get_object_positions()
        # Boxes.run_behaviour()

         # for both weapons in the inventory run bullet behavuour, and draw it
        # for name,weapon in player.left_hand_weapon_slots.items():

        #       # if there is a weapon in the slot then run the beahviour
        #     if weapon:

        #         weapon.get_zombie_positions()
        # dum.get_dummy_pos() # get dummy posiitonp

        if boss_controller.current_boss: # zombies position gets updated here in this code

            # print(boss_controller.current_boss.current_boss_activity)
            # print(boss_controller.current_boss.current_attack)
            # print(boss_controller.current_boss.movement_vectors)
            # print(boss_controller.current_boss.time_in_boss_activity)w
            boss_controller.current_boss.player = player # set player va    r
            boss_controller.current_boss.determine_boss_activity()
            boss_controller.current_boss.run_boss_behaviour(win=win,player=player,enemy_manager=enemy_manager,boss_manager=boss_controller,targets='Player')
            boss_controller.despawn_boss()




            # circ.track_position()
        # myhole.run_behaviour(win=win)

        ### PLAYER STUFF ###
        # track player mouse pos
        player.tracking_mouse_pos()
        # player.movement_and_wall_collision_topdown(win=win,enemy_manager=enemy_manager)
        player.move2()

        player.shooting_target = player.mouse_pos

        player.crosshair.rect.center = player.mouse_pos
        player.crosshair.anchor_pos = player.mouse_pos
        player.crosshair.run_behaviour()


        # player.draw_rect(win=win)s
        player.draw_rect(game_obj=player,asset_to_draw=player.rect,asset_type='rect',
                        surface_to_draw_on='win',game_object_origin=player.object_of_origin,
                         is_animated=False,animation_length=0,position=None,value=None,
                         is_critical=None,z_layer=player.zlayer_drawing,rect_colour='red')
        # player.track_player_position()

        # print(f'Player position is {player.current_tile_position}')

        # handle shooting based on what the players current weapon issswzaaaaaaaAaaaaaaaaaaaaa
        # we only care if the current weapon has been shot, but if theres a bullet for the other wweapon we still want it to carry on as normal even if we switch weapons
        player.left_hand_weapon.can_shot_be_fired(win=win,player=player)

        if player.right_hand_weapon:
            player.right_hand_weapon.can_shot_be_fired(win=win,player=player)

        player.find_game_objects_in_area()
        player.enemy_collision_rects()
        player.run_on_collision_effects()
        player.apply_status_effects()
        # print(f'statyus effect = {player.status_effects}')
        player.track_immunity_to_status_effects()

        print(player.current_tile_position)

        # print(player.running_on_collision_effects)
        # print(player.is_active)


        # print(f'Player effects = {player.status_effects}')
        # StatusEffectManagers['DMG']
        # print(f'effects = {player.applied_on_collision_effects}')

        # player.left_hand_weapon.can_shot_be_fired_left_gun(win=win,player=player)
        # player.left_hand_weapon.can_shot_be_fired_right_gun(win=win,player=player)
        # pl,.ayer.left_hand_weapon.run_bullet_behaviour(win=win,player=player,tilemap=all_rects_masks_surfaces_scalefactor,enemy_manager=enemy_manager) # this should run regardless of what current weapon is being used
        # player.current_wea  on.draw_bullet_rect(win)dddda


        ### uncheck
        # enemy_manager.run_entity_behaviour(win=win,player=player,tilemap=all_rects_masks_surfaces_scalefactor,Weapon=player.left_hand_weapon,
        #                                     empty_tiles=Creative_Mode.all_walls)
        # enemy_manager.draw_entities_rect(win)

         # handle everythign to do with the boss
        # if boss_controller.current_boss: # zombies position gets updated here in this code

        #     # print(boss_controller.current_boss.current_boss_activity)
        #     # print(boss_controller.current_boss.current_attack)
        #     # print(boss_controller.current_boss.movement_vectors)
        #     # print(boss_controller.current_boss.time_in_boss_activity)w
        #     boss_controller.current_boss.player = player # set player va    r
        #     boss_controller.current_boss.determine_boss_activity()
        #     boss_controller.current_boss.run_boss_behaviour(win=win,player=player,enemy_manager=enemy_manager,boss_manager=boss_controller,targets='Player')
        #     boss_controller.despawn_boss()


        # fwor both weapons in the inventory run bullet behavuour, and draw it
        for name,weapon in player.left_hand_weapon_slots.items():

            # if there is a weapon in the slot then run the beahviour
            if weapon:
                weapon.run_behaviour(win=win,player=player,boss_manager=boss_controller,targets=['Boss','Enemy','dummy']) # this should run regardless of what current weapon is being used
                # weapon.draw_bullet_rect(win)

                # fpool = weapon.inactive_pool + weapon.active_pool
                # for b in fpool:
                #     b.apply_status_effects()
                # weapon.adjust_dual_wield_position(player=player,win=win)

        # print(player.right_hand_weapon_slots)
        # sys.exit()
        for name,weapon in player.right_hand_weapon_slots.items():



            # if there is a weapon in the slot then run the beahviour
            if weapon:
                weapon.run_bullet_behaviour(win=win,player=player,enemy_manager=enemy_manager,boss_manager=boss_controller,targets=['Boss','Enemy','dummy']) # this should run regardless of what current weapon is being used
                weapon.draw_bullet_rect(win)
                # weapon.adjust_dual_wield_position(player=player,win=win)


        # game clockdddddddddddddddds
        true_game_clock.track_time_and_draw(win=win)

        # player.tracking_mouse_pos()

        # player.movement_and_wall_collision_topdown(win=win,enemy_manager=enemy_manager)
        # player.draw_rect(win=win)
        # player.track_player_position()

        bounding_rect.center = player.rect.center
        player.find_walls_in_frame(bounding_rect=bounding_rect)

        #player.bresenham_raycast(fog_surface=fog_of_war_surface,win_copy=win_copy,win=win,start_pos=player.rect.center,target_pos=player.mouse_pos)

        EnemyObjectMgr.player = player

        # run round tracker
        round_tracker.run_behaviour()

        # run enemy object mgr
        EnemyObjectMgr.run_behaviour()

        # run bullet objects
        BulletObjectMgr.run_behaviour()

        # run status effect objects
        StatusEffectMgr.run_behaviour()

        # run on collision effects
        OnCollisionEffectMgr.run_behaviour()

        # run any stat boost
        StatBoostMgr.run_behaviour()

        # run interactable objects liek soul box, and in the future wall buy
        InteractableMgr.run_behaviour()

        # run soul objects, in future this should jsut be for generic moveable objects
        SoulObjectMgr.run_behaviour()

        # print(list(Creative_Mode.all_walls.keys()))

        # sys.exit()

        # print(player.left_hand_weapon.bullets_remaining_in_mag)

        # for bullet in BulletObjectMgr.active_pool:
        #     bullet.draw_rect(game_obj=bullet,asset_to_draw=bullet.rect,asset_type='rect',
        #                 surface_to_draw_on='win',game_object_origin=bullet.object_of_origin,
        #                  is_animated=False,animation_length=0,position=None,value=None,
        #                  is_critical=None,z_layer=bullet.zlayer_drawing,rect_colour='red')
        # if BulletObjectMgr.active_pool:
        #     for bullet in BulletObjectMgr.active_pool:
        #         bullet.draw_rect2(win=win)
        # handle regen after all damage has been checked
        # player.regen()

        # writing text to screendddaaaaaaaaaaaaWWWWWWaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # txdt = player.left_hand_weapon.pen.render(f"{player.left_hand_weapon.bullets_remaining_in_mag}/{player.left_hand_weapon.total_ammo_stock}",True,'red')

        # ##make it appear at top corner of screen
        # rect = txt.get_rect(topleft=(40,40))

        # win.blit(txt,rect)



        # # txt0 = player.left_hand_weapon.pen.render(f"{player.left_hand_weapon.bullets_remaining_in_mag_left_gun}/{player.left_hand_weapon.bullets_remaining_in_mag_right_gun}/{player.left_hand_weapon.total_ammo_stock}",True,'red')
        txt0 = Creative_Mode.pen.render(f"Left Gun Ammo:{player.left_hand_weapon.bullets_remaining_in_mag}/{player.left_hand_weapon.total_ammo_stock}",True,'green')


        # ##make it appear at top corner of screen
        rect0 = txt0.get_rect(topleft=(10,100))

        win.blit(txt0,rect0)

        if player.right_hand_weapon:
            txt1 = Creative_Mode.pen.render(f"Right Gun Ammo:{player.right_hand_weapon.bullets_remaining_in_mag}/{player.right_hand_weapon.total_ammo_stock}",True,'red')


            # ##make it appear at top corner of screend
            rect1 = txt1.get_rect(topleft=(10,120))


            win.blit(txt1,rect1)

        # # txt2 = player_Weapon.pen.render(f'Score: {player.score}',True,'blue')
        txt2 = Creative_Mode.pen.render(f'Score:{player.score}',True,'blue')

        rect2 = txt2.get_rect(topleft=(10,40))
        win.blit(txt2,rect2)

        # print(player.left_hand_weapon.is_homing)
        # # txt3 = player_bullet_ma nager.pen.render(f'{round(player.sprint_time,2)}/{player.reset_sprint_time}',True,'blue')
        # txt3 = player.left_hand_weapon.pen.render(f'{round(player.sprint_time,2)}/{player.reset_sprint_time}',True,'blue')

        # rect3 = txt3.get_rect(topleft=(100,190))
        # win.blit(txt3,rect3)

        # txt5 = player.left_hand_weapon.pen.render(f'{round(player.time_between_rolls,2)}/{player.reset_time_between_rolls}',True,'green')

        # rect5 = txt5.get_rect(topleft=(100,240))
        # win.blit(txt5,rect5)

        # txt4 = player.left_hand_weapon.pen.render(f'{player.health}/{player.max_health}',True,'red')

        # rect4 = txt4.get_rect(topleft=(100,290))
        # win.blit(txt4,rect4)

        txt6 = Creative_Mode.pen.render(f'round:{round_tracker.round_number}',True,'red')

        rect6 = txt6.get_rect(topleft=(450,350))
        win.blit(txt6,rect6)

        # txt7 = player.left_hand_weapon.pen.render(f'roundT:{round_tracker.time_before_round_start}',True,'red')

        # rect7 = txt7.get_rect(topleft=(250,90))
        # win.blit(txt7,rect7)

        # txt8 = player.left_hand_weapon.pen.render(f'killed:{round_tracker.time_between_spawns["regular"]}',True,'red')

        # rect8 = txt8.get_rect(topleft=(250,40))
        # win.blit(txt8,rect8)

        # txt9 = player.left_hand_weapon.pen.render(f'{player.invincibility_timer}/{player.invincibility_time_limit}',True,'yellow')

        # rect9 = txt9.get_rect(topleft=(200,140))

        # win.blit(txt9,rect9)
        # zombie.spawn()
        # spawn zombie 2


        txt10 = Creative_Mode.pen.render(f'Health: {player.health}',True,'yellow')

        rect10 = txt10.get_rect(topleft=(20,350))

        win.blit(txt10,rect10)



        txt11 = Creative_Mode.pen.render(f'Current weapon:{player.left_hand_weapon.name}',True,'yellow')

        rect11 = txt11.get_rect(topleft=(10,85))

        win.blit(txt11,rect11)
        # print(Creative_Mode.object_positions)w
        # start_end_pos = player.knifing_path(win=win,knife=knife)

        # # change knfe start point
        # knife.centerx = start_end_pos[0][0]
        # knife.centery = start_end_pos[0][1]

        # for point in start_end_pos:s
        # angle += 1
        # knife.centerx += (math.cos(timer*0.04)*2)
        # knife.centery += (math.sin(timer*0.04)*2)

        # knife.centerx = knife.centerx + math.cos(angle + math.cos(timer*0.4)*0.03)
        # knife.centery = knife.centery + math.sin(angle + math.cos(timer*0.4)*0.03)


        # higher timer * means wider width
        # higher amplitude menas higher height

        # knife.centery += 1.2
        # knife.centerx += (math.sin(timer*0.02)*1.2)

        # # knife.centerx -= (math.sin(timer*0.02)*1.2)
        # # knife.centery += (math.sin(timer*0.02)*1.2)

        # this creates a circle motion
        # this is what you can use for orbitals, here anchorY will be the players center
        # amplitude makes the circle bigger, frequency increases how fast the object
        knife.centery = anchorY + math.cos(timer)*100
        knife.centerx = anchorX + math.cos(timer)*100

        # print(knife.centerx)
        # print(timer)
        # # knife center - anchorx/100
        # x = math.acos((knife.centerx - anchorX)/100)
        # print(x)
        # print(anchorX + math.cos(x*frequency)*100)
        # sys.exit()


        # print(f'sin:{math.degrees(math.sin(timer*frequency))}\n cos:{math.degrees(math.cos(timer*frequency))} \n add:{math.degrees(math.sin(timer*frequency)) + math.degrees(math.cos(timer*frequency))}')
        if timer >= 7.2:
            # print(knife.centerx)
            # print(timer)
            # # knife center - anchorx/100
            # x = math.acos((knife.centerx - anchorX)/100)/frequency
            # print(x)
            # print(anchorX + math.cos(x*frequency)*100)
            # sys.exit()
            timer = 7.2

        # Creative_Mode.subdivide_bezier_curve(number_of_points=2)aaaaaaaaa

        timer+=((1/60)*frequency)

        knife_to_draw = pygame.FRect(knife[0]+Creative_Mode.bg_offset_x,knife[1]+Creative_Mode.bg_offset_y,knife.width,knife.height)
        # pygame.draw.rect(win,'orange',knife_to_draw)
        # fish = player.knifing_path(win=win,knife=knife,fov_width=180)
        # make everything that has been drawn on the surface biggerd

        # line going to rect center
        line = [(anchorX+Creative_Mode.bg_offset_x,anchorY+Creative_Mode.bg_offset_y),(knife.centerx+Creative_Mode.bg_offset_x,knife.centery+Creative_Mode.bg_offset_y)]

        # pygame.draw.line(win,'blue',*line)

        # _,_ = player.using_melee_weapons(win=win,fov_depth=50,fov_width=50)

        # stove_timer = Creative_Mode.sine_wave_bounce(x1=x1,y1=y1,win=win,rect_to_move=stove,timer=stove_timer,frequency=3,amplitude=30,anchor_for_movement_Y=300)

        # x1 += 1
        # y1 += 1
        # orbs.move_orbital(player=player)

        # orbs.draw(win=win)
         # create the line to draw
         # calculate distance from mouse to player center, on the left is where the rays are pointing to, on the right is where the rays orgininate from
        # direction_vector_x = player.mouse_pos[0] - player.left_hand_weapon.start_point[0]
        # direction_vector_y = player.mouse_pos[1] - player.left_hand_weapon.start_point[1]
        # direction_vector = (direction_vector_x,direction_vector_y)

        # # the problem now that we need to change is the player angle, we need it to be lower

        # # get the angle of the line going from the player center to the mouse
        # player_angle = math.atan2(*direction_vector)
        # mouse_pos_depth = (player.mouse_pos[0] - player.left_hand_weapon.start_point[0])/math.sin(player_angle)
        # drawing_line_x = player.left_hand_weapon.start_point[0] + Creative_Mode.bg_offset_x +  math.sin(player_angle)*mouse_pos_depth
        # drawing_line_y = player.left_hand_weapon.start_point[1] + Creative_Mode.bg_offset_y + math.cos(player_angle)*mouse_pos_depth

        # # draw the line
        # pygame.draw.line(win,'blue',(player.left_hand_weapon.start_point[0]+Creative_Mode.bg_offset_x,player.left_hand_weapon.start_point[1]+Creative_Mode.bg_offset_y),
        #             (drawing_line_x,drawing_line_y))

        # use the player items
        player.run_player_items(win=win,player=player,targets=['Boss','Enemy'],boss_manager=boss_controller)


        # draw dummy and handle if it exsit

        # dum.manage_dummy(win=win)

        # handle regen after all damage has been checked
        player.regen()
        player.track_invincibility()


        # reset collisions
        # enemy_manager.entity_positions = {}
        Game.object_positions = {}


        Game.draw_objects(win=win)

        # this is for drawing cross hairs from the gun for the player
        # player.draw_360_raycast(win=win,start_pos=player.rect.center,target_pos=player.mouse_pos)



        pygame.transform.scale(Game.win,(Game.fullscreen_width,Game.fullscreen_height),Creative_Mode.display)


        # print(all_rects_masks_surfaces_scalefactor)wwwwwwwwwwww
        pygame.display.update()


      

if __name__ == '__main__':

    with cProfile.Profile() as profile:
        main()

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
