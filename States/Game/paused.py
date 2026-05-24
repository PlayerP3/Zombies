import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from engine.statemachine import State


class Paused(State):

    def __init__(self):

        State.__init__(self)

        self.option_select = None

    def enter(self):

       # here when in splash can set mouse visibility to off until we get to selections creen
       # but for now splash is selection screen

        self.parent_node.screenManager.windows['win'].pos = (0,0)
        self.parent_node.overlay.activate_hud_elements(['Pause'])
        self.parent_node.overlay.deactivate_hud_elements(['PlayerHealth','RoundNumber','Ammo','Points','Splash'])
        self.parent_node.objectManager.player.movementx[0] = 0 
        self.parent_node.objectManager.player.movementy[0] = 0 
        self.parent_node.objectManager.player.movementx[1] = 0 
        self.parent_node.objectManager.player.movementy[1] = 0 
        self.parent_node.objectManager.player.is_interacting = False
        self.parent_node.objectManager.player.weapon.state.emit('IDLE')

        


    def update(self):

        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        x = mouse_pos[0]/(self.parent_node.screenManager.fullscreen_width/self.parent_node.screenManager.windows['win'].win_width) - self.parent_node.screenManager.windows['win'].bg_offset_x
        y = mouse_pos[1]/(self.parent_node.screenManager.fullscreen_height/self.parent_node.screenManager.windows['win'].win_height) - self.parent_node.screenManager.windows['win'].bg_offset_y

        # submit event processing
        self.submit_event_processing()

        # fill window
        self.parent_node.screenManager.windows['win'].win.fill((0,0,0))

        # subsample circle
        self.parent_node.screenManager.windows['win'].focus = (0,0)
        self.parent_node.screenManager.windows['win'].track_object_spring()

        # display hud
        self.parent_node.overlay.display_hud()

        # check for collision of mouse pos with options
        for hudElement in self.parent_node.overlay.active_elements:

            # check collision
            if hudElement.hurtbox.collidepoint((x,y)):

                self.option_select = hudElement.name


        self.parent_node.screenManager.render_windows()

        # scale the window, and blit to display
        pygame.transform.scale(self.parent_node.screenManager.windows['win'].win,(self.parent_node.screenManager.fullscreen_width,self.parent_node.screenManager.fullscreen_height),self.parent_node.screenManager.screen)

        # update display
        pygame.display.flip()

    def handle_event(self, event):

        # handling mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == pygame.BUTTON_LEFT:

                if self.option_select == 'PauseResumeHUD':
                    self.emit('GAMEPLAY')

                if self.option_select == 'PauseQuitHUD':
                    self.emit('QUIT')

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.emit('GAMEPLAY')