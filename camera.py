import pygame,random,os,string,numpy
from window import Window

class Camera():

    def __init__(self):
        
        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.focus = (0,0)

    # change camera view based on what is being shown
    def track_position(self,window:Window):
        self.bg_offset_x = window.get_width()//2 - self.focus[0]
        self.bg_offset_y = window.get_height()//2 - self.focus[1]

    # change camera based on obj
    def track_object(self,focus,window:Window):
        
        self.bg_offset_x = window.get_width()/2 - focus.rect.centerx
        self.bg_offset_y = window.get_height()/2 - focus.rect.centery