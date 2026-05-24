
import pygame,random,json,os,sys
import engine.pynaccle as Pyn
from States.Game.splash import Splash
from States.Game.paused import Paused
# from States.Game import gameover
from States.Game.gameplay import Gameplay
from States.Game.quit import Quit

pygame.init()

# init engine
core = Pyn.Pynaccle()

core.init(states={'SPLASH':Splash(),'GAMEPLAY':Gameplay(),'PAUSED':Paused(),'QUIT':Quit()})

# add screens

core.screenManager.add_window('wincopy',1280,720,(core.screenManager.fullscreen_width//2,core.screenManager.fullscreen_height//2))
core.screenManager.add_window('fog_of_war',1280,720,(core.screenManager.fullscreen_width//2,core.screenManager.fullscreen_height//2))
core.screenManager.add_window('playeroverlay',1280,720,(core.screenManager.fullscreen_width//2,core.screenManager.fullscreen_height//2))
core.screenManager.add_window('win',1280,720,(core.screenManager.fullscreen_width//2,core.screenManager.fullscreen_height//2))
core.screenManager.windows['win'].zoom = 1.4
core.screenManager.windows['wincopy'].zoom = 1.4
core.screenManager.windows['fog_of_war'].zoom = 1.4

import cProfile
import pstats
import interactable
from roundtracker import round_manager
from player import Player
from item import Item
import enemy
import engine.moveableobject
from engine.hud import HUD_element
from engine.objectsystem import objectManager
import wallbuy
from wall import *
from pathfinding import Pathfinding,build_astar_graph,build_true_clearance_graph



# set random seed
random.seed()

# load files in
with open('config_player.json','r') as player_attributes_file, open('config_hud_elements.json','r') as hudelements_attributes_file:

    player_parameters = json.load(player_attributes_file)
    hudelements_parameters = json.load(hudelements_attributes_file)




# player
player = Player()
player.start(attributes=player_parameters)
core.objectManager.player = player
core.objectManager.player.spawn((0,0))

def update_health_hud(hud_element:HUD_element):

    hud_element.img_width_scale = (core.objectManager.player.health*hud_element.original_vars['img_width_scale'])/core.objectManager.player.total_health

def update_health_text_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{int(core.objectManager.player.health)}/{core.objectManager.player.total_health}"

    hud_element.img_path = text


def update_round_number_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{round_manager.round_number}"

    hud_element.img_path = text


def update_ammo_text_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{core.objectManager.player.weapon.bullets_remaining_in_mag}/{core.objectManager.player.weapon.total_ammo_stock}"

    hud_element.img_path = text


def update_points_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{core.objectManager.player.money}"

    hud_element.img_path = text


def run():

    

    # create tile map
    # build astar graph
    build_astar_graph()
    build_true_clearance_graph()

    # create hud elements
    current_health_hud = HUD_element()
    empty_health_hud = HUD_element()
    current_health_text_hud = HUD_element()
    round_number_hud = HUD_element()
    ammo_text_hud = HUD_element()
    points_hud = HUD_element()
    splashStartHud = HUD_element()
    splashQuitHud = HUD_element()
    pauseResumeHud = HUD_element()
    pauseQuitHud = HUD_element()

    # change text hud img path
    current_health_hud.init(attributes=hudelements_parameters['CurrentHealthHUD'])
    empty_health_hud.init(attributes=hudelements_parameters['EmptyHealthHUD'])
    current_health_text_hud.init(attributes=hudelements_parameters['CurrentHealthTextHUD'])
    round_number_hud.init(attributes=hudelements_parameters['RoundNumberHUD'])
    ammo_text_hud.init(attributes=hudelements_parameters['AmmoTextHUD'])
    points_hud.init(attributes=hudelements_parameters['PointsHUD'])
    splashStartHud.init(attributes=hudelements_parameters['SplashStartHUD'])
    splashQuitHud.init(attributes=hudelements_parameters['SplashQuitHUD'])
    pauseResumeHud.init(attributes=hudelements_parameters['PauseResumeHUD'])
    pauseQuitHud.init(attributes=hudelements_parameters['PauseQuitHUD'])

    # add any extra processing
    current_health_hud.extraProcessing.append(update_health_hud)
    current_health_text_hud.extraProcessing.append(update_health_text_hud)
    round_number_hud.extraProcessing.append(update_round_number_hud)
    ammo_text_hud.extraProcessing.append(update_ammo_text_hud)
    points_hud.extraProcessing.append(update_points_hud)
    

    # add to hud element group
    core.overlay.add_element(group='PlayerHealth',hud_element=current_health_hud)
    core.overlay.add_element(group='PlayerHealth',hud_element=empty_health_hud)
    core.overlay.add_element(group='PlayerHealth',hud_element=current_health_text_hud)
    core.overlay.add_element(group='RoundNumber',hud_element=round_number_hud)
    core.overlay.add_element(group='Ammo',hud_element=ammo_text_hud)
    core.overlay.add_element(group='Points',hud_element=points_hud)
    core.overlay.add_element(group='Splash',hud_element=splashStartHud)
    core.overlay.add_element(group='Splash',hud_element=splashQuitHud)
    core.overlay.add_element(group='Pause',hud_element=pauseResumeHud)
    core.overlay.add_element(group='Pause',hud_element=pauseQuitHud)

    # apply alpha/transparency to regular window
    core.screenManager.windows['win'].win.convert_alpha()
    core.screenManager.windows['win'].win.set_alpha(100)
    core.screenManager.windows['fog_of_war'].win.set_colorkey('WHITE')

    # connect huds to parent objects
    round_manager.connected_hud = round_number_hud
     
    # now that everything is loaded enter roun start state
    round_manager.state.enter()
    # round_manager.connected_hud = [x for x in engine.hud.hud_elements['RoundNumber'] if x.name == 'RoundNumberHUD'][0]

    

    # add objs to active pool
    core.objectManager.active_pool.append(player)
    # engine.active_pool.append(player.weapon)
    core.objectManager.active_pool.append(round_manager)
    
    
    core.state.enter()

    while core.playing:

        core.update()

        # quit_log += 1/60
        # print(quit_log)
        # if quit_log >= quit_time:
        #     playing = False

       
      
if __name__ == '__main__':

    run()
    # with cProfile.Profile() as profile:
    #     run()

    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()


# run game
# run()win2