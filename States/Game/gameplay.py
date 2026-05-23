import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State
from eventsystem import eventprocessor

pass

class Gameplay(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.hud.activate_hud_elements(['PlayerHealth','RoundNumber','Ammo','Points'])
        self.parent_node.hud.deactivate_hud_elements(['Splash','Pause'])

        self.parent_node.camera.pos = self.parent_node.player.hurtbox.center
        self.parent_node.camera.focus = self.parent_node.player.hurtbox.center
        self.parent_node.camera.track_object_spring(window=self.parent_node.windows.win)


    def update(self):
        
        self.submit_event_processing()

        # fill window
        self.parent_node.windows.win.fill((200,0,0))

        self.parent_node.windows.win_copy = self.parent_node.windows.win.copy()

        # engine.camera.track_position(window=engine.windows.win)
        self.parent_node.camera.focus = self.parent_node.player.hurtbox.center
        self.parent_node.camera.track_object_spring(window=self.parent_node.windows.win)

        # run game object behaviour
        self.parent_node.update_game_objects()

        # display hud
        self.parent_node.hud.display_hud()

        # self.parent_node.display_game_tiles()

        # draw all objects onto the window
        self.parent_node.draw_objects()

        # scale the window, and blit to display
        pygame.transform.scale(self.parent_node.windows.win,(self.parent_node.windows.fullscreen_width,self.parent_node.windows.fullscreen_height),self.parent_node.windows.screen)

        # update display
        pygame.display.flip()

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('PAUSED')