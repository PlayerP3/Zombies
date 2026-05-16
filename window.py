import pygame,random,os,string,numpy,json

# load files in
with open('config_window.json','r') as window_attributes_file:

    window_parameters = json.load(window_attributes_file)

class Window():
    
    def __init__(self):

        # the final display which the window is drawn onto
        self.display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        # get exact width and height of the full screen once the window has been made full screen, this is needed for centering the player
        self.fullscreen_width = pygame.display.Info().current_w
        self.fullscreen_height = pygame.display.Info().current_h

        # get the actual size we want the window to be
        self.win_width = window_parameters['win_width']
        self.win_height = window_parameters['win_height']
        self.resize_win = window_parameters['resize']

        # create window, everything is first drawn onto this surface
        self.win = pygame.Surface((self.win_width/self.resize_win,self.win_height/self.resize_win),pygame.SRCALPHA)
        self.win_copy = pygame.Surface((self.win_width/self.resize_win,self.win_height/self.resize_win),pygame.SRCALPHA)
        self.fog_of_war_surface = pygame.Surface((self.win_width/self.resize_win,self.win_height/self.resize_win),pygame.SRCALPHA)