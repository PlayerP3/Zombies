
import pygame,random,json,os,sys

# set working dir to current game
os.chdir(os.path.dirname(__file__))

# add path to
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pynaccle.engine as Pyn
from States.Game.splash import Splash
from States.Game.paused import Paused
# from States.Game import gameover
from States.Game.gameplay import Gameplay
from States.Game.quit import Quit
from wallbuy import Wallbuy
from pynaccle.animatedsprite import AnimatedSprite
from door import Door
from wall import Wall
from spawnpoint import SpawnPoint
from buildable import Part,Bench
from soulbox import Soulbox,Soul


# init engine
core = Pyn.Engine()

print(os.path.dirname(__file__))

core.init(states={'SPLASH':Splash(),'GAMEPLAY':Gameplay(),'PAUSED':Paused(),'QUIT':Quit()},
          classMappings={'Wallbuy':Wallbuy,'BgTile':AnimatedSprite,'Door':Door,'Wall':Wall,'SpawnPoint':SpawnPoint,'Bench':Bench,'Soulbox':Soulbox},hitboxMetadataJSON='configs/config_hitboxes.json')

# spawn initial bg objects
for chunk in core.tilemapProcessor.openChunks:
    for gameobj in core.tilemapProcessor.chunkObj[chunk]:
        gameobj.init()
        gameobj.spawn(pos=gameobj.spawnLocation,vertice='center')

        if gameobj.inaccessible:
            core.tilemapProcessor.inaccessible_tiles.append(gameobj.spawnLocation)

        elif not gameobj.inaccessible:
            core.tilemapProcessor.accessible_tiles.append(gameobj.spawnLocation)
    
# spawn initial objects
for gameobj in core.objectManager.active_pool:
    gameobj.init()
    gameobj.spawn(pos=gameobj.spawnLocation)


import cProfile
import pstats
import pynaccle.interactable
from roundtracker import round_manager
from player import Player
from item import Item
from pynaccle.enemy import Enemy
import pynaccle.moveableobject
from pynaccle.hud import HUD_element
from pynaccle.objectsystem import objectManager
import wallbuy
from wall import *
from pynaccle.pathfinding import Pathfinding,build_astar_graph,build_true_clearance_graph




# set random seed
random.seed()

# load files in
with open('configs/config_player.json','r') as player_attributes_file, open('configs/config_hud_elements.json','r') as hudelements_attributes_file, \
    open('configs/config_buildable.json','r') as buidlable_attributes_file:

    player_parameters = json.load(player_attributes_file)
    hudelements_parameters = json.load(hudelements_attributes_file)
    buildable_parameters = json.load(buidlable_attributes_file)


# add objects to inactive pool
objectManager.inactive_pool["Enemy"] = [Enemy() for _ in range(500)]
objectManager.inactive_pool["Soul"] = [Soul() for _ in range(200)]


# player
player = Player()
player.start(attributes=player_parameters)
core.objectManager.player = player
core.objectManager.player.spawn((0,0))

def update_health_hud(hud_element:HUD_element):

    hud_element.spriteWidthScale = (core.objectManager.player.health*hud_element.original_vars['spriteWidthScale'])/core.objectManager.player.total_health

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
    # round_manager.connected_hud = [x for x in pynaccle.hud.hud_elements['RoundNumber'] if x.name == 'RoundNumberHUD'][0]

    

    # add objs to active pool
    core.objectManager.active_pool.append(player)
    core.objectManager.active_pool.append(round_manager)

    # load buildables
    buildableData = {}

    for buildable in buildable_parameters:

        # add image path
        buildableData[buildable] = buildable_parameters[buildable]['img_path']

        # add as key in player collected parts
        player.collectedParts[buildable] = []

        for bPart in buildable_parameters[buildable]["Parts"]:

            # init and spawn part
            gameobj = Part()

            set_attributes(game_object=gameobj,attributes=buildable_parameters[buildable]["Parts"][bPart])
            gameobj.init()
            gameobj.spawn(pos=gameobj.spawnLocation)

            # add to tilemap connected chunk
            core.tilemapProcessor.chunkObj[gameobj.connectedChunk].append(gameobj)

    # if there are any work benches inject buildable data into them
    workbenches = core.tilemapProcessor.get_obejcts(className="Bench")
    for wb in workbenches:
        wb.buildableData = buildable_parameters


    
    
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