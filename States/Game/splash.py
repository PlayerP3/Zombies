import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from statemachine import State

class Splash(State):

    def __init__(self):

        State.__init__(self)

        self.option_select = None

    def enter(self):

       # here when in splash can set mouse visibility to off until we get to selections creen
       # but for now splash is selection screen

        self.parent_node.camera.pos = (0,0)
        self.parent_node.hud.activate_hud_elements(['Splash'])
        self.parent_node.hud.deactivate_hud_elements(['PlayerHealth','RoundNumber','Ammo','Points','Pause'])

        


    def update(self):

        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        x = mouse_pos[0]/(self.parent_node.windows.fullscreen_width/self.parent_node.windows.win_width) - self.parent_node.camera.bg_offset_x
        y = mouse_pos[1]/(self.parent_node.windows.fullscreen_height/self.parent_node.windows.win_height) - self.parent_node.camera.bg_offset_y

        # submit event processing
        self.submit_event_processing()

        # fill window
        self.parent_node.windows.win.fill((0,0,0))

        # self.parent_node.camera.focus = self.parent_node.player.hurtbox.center
        self.parent_node.camera.focus = (0,0)

        self.parent_node.camera.track_object_spring(window=self.parent_node.windows.win)

        # display hud
        self.parent_node.hud.display_hud()

        # check for collision of mouse pos with options
        for hudElement in self.parent_node.hud.active_elements:

            # check collision
            if hudElement.hurtbox.collidepoint((x,y)):

                self.option_select = hudElement.name


        self.parent_node.draw_objects()

        # scale the window, and blit to display
        pygame.transform.scale(self.parent_node.windows.win,(self.parent_node.windows.fullscreen_width,self.parent_node.windows.fullscreen_height),self.parent_node.windows.screen)

        # update display
        pygame.display.flip()

    def handle_event(self, event):

        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                if self.option_select == 'SplashStartHUD':
                    self.emit('GAMEPLAY')

                if self.option_select == 'SplashQuitHUD':
                    self.emit('QUIT')

        # if the actual X is clicked to close the tab
        if event.type == pygame.QUIT:
            self.emit('QUIT')

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('QUIT')