import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State

class Splash(State):

    def __init__(self):

        State.__init__(self)

        self.option_select = None

    def enter(self):

       # here when in splash can set mouse visibility to off until we get to selections creen
       # but for now splash is selection screen

        self.parent_node.screenManager.windows['win'].pos = (0,0)
        self.parent_node.screenManager.windows['win'].zoom = self.parent_node.screenManager.windows['win'].stateZoom[self.__class__.__name__.upper()]
        self.parent_node.overlay.activate_hud_elements(['Splash'])
        self.parent_node.overlay.deactivate_hud_elements(['PlayerHealth','RoundNumber','Ammo','Points','Pause'])
        # self.parent_node.screenManager.windows['win'].zoom = 1

        


    def update(self):

        self.option_select = None

         # self.parent_node.screenManager.windows['win']focus = self.parent_node.objectManager.player.hurtbox.center
        self.parent_node.screenManager.windows['win'].focus = (0,0)

        # self.parent_node.screenManager.windows['win'].track_position()

        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        x = (mouse_pos[0]/(self.parent_node.screenManager.fullscreen_width/self.parent_node.screenManager.windows['win'].win_width)) - (self.parent_node.screenManager.windows['win'].win_width//2) 
        y = (mouse_pos[1]/(self.parent_node.screenManager.fullscreen_height/self.parent_node.screenManager.windows['win'].win_height)) - (self.parent_node.screenManager.windows['win'].win_height//2)
        
        # print(x,y)

        # submit event processing
        self.submit_event_processing()

        # display hud
        self.parent_node.overlay.display_hud()

        # check for collision of mouse pos with options
        for hudElement in self.parent_node.overlay.active_elements:

            # check collision
            if hudElement.hurtbox.collidepoint((x,y)):

                self.option_select = hudElement.name
                print(hudElement.hurtbox.center,hudElement.hurtbox.width,hudElement.hurtbox.height)



        self.parent_node.screenManager.render_windows()

        # scale the window, and blit to display
        # pygame.transform.scale(self.parent_node.screenManager.windows['win'].win,(self.parent_node.screenManager.fullscreen_width,self.parent_node.screenManager.fullscreen_height),self.parent_node.screenManager.screen)
        # self.parent_node.screenManager.screen.blit(self.parent_node.screenManager.windows['win'].win,(0,0))

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

            if event.key == pygame.K_RETURN:
                self.emit('GAMEPLAY')