"""
    Style conventions:
        _{name} is private field
        {UPPERCASED_NAME} is const
    Assumes pygame.init() is called
"""
import pygame
from  pygame.locals import *
class Raw_Renderer:
    """
    Vars:   
            _screen_surface: pointer to surface that pygame.display use to .blit()
            SCREEN_SIZE is the total count of pixels on screen
    """
    # set display to custom resolution
    def __init__(self, width=1024, height=720):
        self._screen_surface = pygame.display.set_mode((width, height))
        self.SCREEN_SIZE = width*height

    def display(self):
        pygame.display.flip()

    def update(self, game_info):
        raise NotImplementedError
