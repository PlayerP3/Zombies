import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from engine.statemachine import State

pass

class Gameplay(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.overlay.activate_hud_elements(['PlayerHealth','RoundNumber','Ammo','Points'])
        self.parent_node.overlay.deactivate_hud_elements(['Splash','Pause'])

        self.parent_node.screenManager.windows['win'].pos = self.parent_node.objectManager.player.hurtbox.center
        self.parent_node.screenManager.windows['win'].focus = self.parent_node.objectManager.player.hurtbox.center
        self.parent_node.screenManager.windows['win'].track_object_spring()

        self.parent_node.screenManager.windows['fog_of_war'].bg_offset_x = self.parent_node.screenManager.windows['win'].bg_offset_x
        self.parent_node.screenManager.windows['fog_of_war'].bg_offset_y = self.parent_node.screenManager.windows['win'].bg_offset_y
        self.parent_node.screenManager.windows['wincopy'].bg_offset_x = self.parent_node.screenManager.windows['win'].bg_offset_x
        self.parent_node.screenManager.windows['wincopy'].bg_offset_y = self.parent_node.screenManager.windows['win'].bg_offset_y
        # self.parent_node.screenManager.windows['fog_of_war'].track_object_spring()


    def update(self):
        
        self.submit_event_processing()

        # fill window
        self.parent_node.screenManager.windows['win'].win.fill((200,0,0))

        # self.parent_node.screenManager.windows['win'].win_copy = self.parent_node.screenManager.windows['win']

        # engine.camera.track_position(window=engine.windows.win)
        self.parent_node.screenManager.windows['win'].focus = self.parent_node.objectManager.player.hurtbox.center
        self.parent_node.screenManager.windows['win'].track_object_spring()
        self.parent_node.screenManager.windows['fog_of_war'].bg_offset_x = self.parent_node.screenManager.windows['win'].bg_offset_x
        self.parent_node.screenManager.windows['fog_of_war'].bg_offset_y = self.parent_node.screenManager.windows['win'].bg_offset_y
        self.parent_node.screenManager.windows['wincopy'].bg_offset_x = self.parent_node.screenManager.windows['win'].bg_offset_x
        self.parent_node.screenManager.windows['wincopy'].bg_offset_y = self.parent_node.screenManager.windows['win'].bg_offset_y

        self.parent_node.screenManager.windows['playeroverlay'].win.fill((0,0,0,0))
        

        # run game object behaviour
        self.parent_node.objectManager.update_game_objects()

        # display hud
        self.parent_node.overlay.display_hud()

        # self.parent_node.display_game_tiles()

        # draw all objects onto the window
        self.parent_node.screenManager.render_windows()
        self.parent_node.screenManager.windows['win'].win.blit(self.parent_node.screenManager.windows['playeroverlay'].win,(0,0))

        # scale the window, and blit to display
        pygame.transform.scale(self.parent_node.screenManager.windows['win'].win,(self.parent_node.screenManager.fullscreen_width,self.parent_node.screenManager.fullscreen_height),self.parent_node.screenManager.screen)

        # update display
        pygame.display.flip()

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('PAUSED')