
import pygame,random,json,os
pygame.init()
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
# win =  pygame.Surface((2400,2200),pygame.SRCALPHA)
import cProfile
import pstats
import interactable
from deck import shoot_event
from game import engine
from eventsystem import eventprocessor
from roundtracker import round_manager
from player import Player
from item import Item
import deck
import enemy
from hud import HUD_element
from animatedsprite import GameSprites,AnimatedSprite
import moveableobject
import wallbuy
from wall import *
from pathfinding import Pathfinding,build_astar_graph,build_true_clearance_graph

# set random seed
random.seed()

# load files in
with open('config_player.json','r') as player_attributes_file, open('config_hud_elements.json','r') as hudelements_attributes_file:

    player_parameters = json.load(player_attributes_file)
    hudelements_parameters = json.load(hudelements_attributes_file)




def update_health_hud(hud_element:HUD_element):

    hud_element.img_width_scale = (engine.player.health*hud_element.original_vars['img_width_scale'])/engine.player.total_health

def update_health_text_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{int(engine.player.health)}/{engine.player.total_health}"

    hud_element.img_path = text


def update_round_number_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{round_manager.round_number}"

    hud_element.img_path = text


def update_ammo_text_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{engine.player.weapon.bullets_remaining_in_mag}/{engine.player.weapon.total_ammo_stock}"

    hud_element.img_path = text


def update_points_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{engine.player.money}"

    hud_element.img_path = text


def run():

    playing = True

    engine.clock = pygame.time.Clock()

    # player
    player = Player()
    player.start(attributes=player_parameters)
    engine.player = player
    engine.player.spawn((0,0))

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
    engine.hud.add_element(group='PlayerHealth',hud_element=current_health_hud)
    engine.hud.add_element(group='PlayerHealth',hud_element=empty_health_hud)
    engine.hud.add_element(group='PlayerHealth',hud_element=current_health_text_hud)
    engine.hud.add_element(group='RoundNumber',hud_element=round_number_hud)
    engine.hud.add_element(group='Ammo',hud_element=ammo_text_hud)
    engine.hud.add_element(group='Points',hud_element=points_hud)
    engine.hud.add_element(group='Splash',hud_element=splashStartHud)
    engine.hud.add_element(group='Splash',hud_element=splashQuitHud)
    engine.hud.add_element(group='Pause',hud_element=pauseResumeHud)
    engine.hud.add_element(group='Pause',hud_element=pauseQuitHud)

    # apply alpha/transparency to regular window
    engine.windows.win.convert_alpha()
    engine.windows.win.set_alpha(100)
    engine.windows.fog_of_war_surface.set_colorkey('WHITE')

    # connect huds to parent objects
    round_manager.connected_hud = round_number_hud
     
    # now that everything is loaded enter roun start state
    round_manager.state.enter()
    # round_manager.connected_hud = [x for x in engine.hud.hud_elements['RoundNumber'] if x.name == 'RoundNumberHUD'][0]

    

    # add objs to active pool
    engine.active_pool.append(player)
    # engine.active_pool.append(player.weapon)
    engine.active_pool.append(round_manager)
    
    
    engine.state.enter()

    while engine.playing:

        engine.update()

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