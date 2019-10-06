import pygame
from pygame.locals import *
from physics import Rotation
class Player_Listener:
    """
        Vars:
            
    """
    # Currently mapped to arrow keys
    MOVE_KEYS = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
    def __init__(self, player):
        self._player = player
    def update(self, player_obj):
        pressed = pygame.key.get_pressed()
        for dir in range(len(self.MOVE_KEYS)):
            if not pressed[dir]:
                continue
            if dir == self._player.rotation:
                self._player.move_forward()
            else:
                self._player.turn(dir)

