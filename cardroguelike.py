import pygame,random,json,os
import cProfile
import pstats
import interactable
from deck import shoot_event
from game import engine
from player import Player
from deck import OnShotEffectMgr
from enemy import EnemyMgr,spawn_enemy_event
from hud import HUD_element
from animatedsprite import GameSprites,AnimatedSprite
from moveableobject import MiscellaneousMgr
from wall import *
from pathfinding import Pathfinding,build_astar_graph,build_true_clearance_graph

# set random seed
random.seed()

# load files in
with open('config_player.json','r') as player_attributes_file, open('config_hud_elements.json','r') as hudelements_attributes_file:

    player_parameters = json.load(player_attributes_file)
    hudelements_parameters = json.load(hudelements_attributes_file)

def update_health_hud(hud_element:HUD_element):

    hud_element.img_width_scale = (engine.player.health*hud_element.original_vars['img_width_scale'])/engine.player.original_vars['health']

def update_health_text_hud(hud_element:HUD_element):

    # create text for current health
    text = f"{int(engine.player.health)}/{engine.player.original_vars['health']}"

    hud_element.img_path = text
    hud_element.init_sprite()

def update_current_card_hud(hud_element:HUD_element):

    # if there is a current card
    if engine.player.deck.current_card:

        # split current card
        suit,rank = engine.player.deck.current_card.split('_')

        hud_element.img_path = f"Sprites/Cards/{suit}/{rank}.png"

        hud_element.display = True

    # if not current card stop displaying the card hud
    elif not engine.player.deck.current_card:
        hud_element.display = False

    # hud_element.init_sprite()
# based on current window rect, get width and height of rect and breakdown into 32 x 32 tiles
# print(engine.windows.win.get_width())    
# print(engine.windows.win.get_height())
# print(853/32)

def run():

    playing = True

    clock = pygame.time.Clock()

    # player
    player = Player()
    player.init(player_parameters)
    
    # create tile map

    # build astar graph
    build_astar_graph()
    build_true_clearance_graph()

    # for z in engine.astar_graph:

    #     print(z,'clearence =',engine.astar_graph[z].clearance)

    # sys.exit()



    # create hud elements
    current_health_hud = HUD_element()
    empty_health_hud = HUD_element()
    current_health_text_hud = HUD_element()
    current_card_hud = HUD_element()
    default_card_hud = HUD_element()

    # change text hud img path
    current_health_hud.init(attributes=hudelements_parameters['CurrentHealthHUD'])
    empty_health_hud.init(attributes=hudelements_parameters['EmptyHealthHUD'])
    current_health_text_hud.init(attributes=hudelements_parameters['CurrentHealthTextHUD'])
    current_card_hud.init(attributes=hudelements_parameters['CurrentCardHUD'])
    default_card_hud.init(attributes=hudelements_parameters['DefaultCardHUD'])

    engine.hud.add_element(group='PlayerHealth',hud_element=current_health_hud)
    engine.hud.add_element(group='PlayerHealth',hud_element=empty_health_hud)
    engine.hud.add_element(group='PlayerHealth',hud_element=current_health_text_hud)
    engine.hud.add_element(group='CurrentCard',hud_element=current_card_hud)
    engine.hud.add_element(group='CurrentCard',hud_element=default_card_hud)
    



    # HUD elements
    # black one first
    # then red one
    # attach width of red one to health bar of player
    # number text
    # HealthHUD = HUD_element(name='HealthHUD',)
    # a hud is an animated sprite, whose value / representation is linked to another objects variable/ that object

    # init game engine
    engine.init(player=player,spawn_point=(0,0))

    # apply alpha/transparency to regular window
    engine.windows.win.convert_alpha()
    engine.windows.win.set_alpha(100)
    engine.windows.fog_of_war_surface.set_colorkey('WHITE')
    # engine.windows.win_copy = engine.windows.win.copy()
    # engine.windows.fog_of_war_surface = engine.windows.win.copy()

    cardog = pygame.image.load("Sprites/Cards/Hearts/A.png")
    # cardog = GameSprites["Sprites/Cards/Hearts/A.png"]['loaded_image']
    x,y = 96,160
    ang = -70

    # update current card hud
    update_current_card_hud(hud_element=current_card_hud)

    cache = {}


    quit_time = 10
    quit_log = 0

    xx = AnimatedSprite() 

    
    

    while playing:

        # quit_log += 1/60
        # print(quit_log)
        # if quit_log >= quit_time:
        #     playing = False


        ang += 1
        # x-=0.5
        # y-=0.5
        # drawing and frames
        clock.tick(engine.FPS)

       

        # fill window
        engine.windows.win.fill((200,0,0))

        engine.windows.win_copy = engine.windows.win.copy()

        engine.extra_event_processing.append(spawn_enemy_event)
        # get all events
        engine.events = pygame.event.get()

        # handle events
        engine.process_base_events()

        # position camera
        engine.camera.track_position(window=engine.windows.win)

        
        # run object behaviour
        # player.run_behaviour()
        player.update()

        # print(player.state)

        # run gun shooting
        # player.deck.run_behaviour()
        player.deck.update()

        # run onshoteffect behaviour
        OnShotEffectMgr.run_behaviour()

        # run enemy behaviour
        EnemyMgr.run_behaviour()

        # run miscellaneous behaviour
        MiscellaneousMgr.run_behaviour()
        

        # display hud
        update_health_hud(hud_element=current_health_hud)
        update_health_text_hud(hud_element=current_health_text_hud)
        update_current_card_hud(hud_element=current_card_hud)
        engine.hud.display_hud()

        engine.display_game_tiles()
        engine.visualise_sine_wave3()

   
        # xx.init_text_sprite(f"{clock.get_fps()}")
        # xx.init_sprite()
        # xx.draw_surface()

        # draw all objects onto the window
        engine.draw_objects()

        # print(engine.accessible_tiles)
        # print(engine.path_cache)

        # scale the window, and blit to display
        pygame.transform.scale(engine.windows.win,(engine.windows.fullscreen_width,engine.windows.fullscreen_height),engine.windows.display)

        # update display
        pygame.display.update()

      
if __name__ == '__main__':

    with cProfile.Profile() as profile:
        run()

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()


# run game
# run()