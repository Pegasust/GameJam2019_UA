"""
CURRENTLY DEPRECATED. OPTIMIZATION LATER.
    Visual Loop core that handles the Visual Thread.
"""
import pygame
import threading
class Visual_Core:
    """
    consts:
        TARGET_FRAMETIME: the time it should (at least) take per frame
        TARGET_FRAMERATE: the max framerate
        GAME_INFO_POINTER_ADDRESS: the pointer address we can rely to be updated
    vars:
        clock is pygame.time.Clock used for waiting in each core iteration
        thread is the thread that the core is operating

    """
    def visual_update(self, game_info):
            raise NotImplementedError
    def __init__(self,framerate=(60)):
        """
        frametime is the amount of time (ms) before the core continues the loop
        """
        self.TARGET_FRAMERATE = framerate
        self.TARGET_FRAMETIME = 1/framerate
        self.clock = pygame.time.Clock()
    def get_fps(self):
        return self.clock.get_fps()
    def get_frametime(self):
        return self.clock.get_time()
