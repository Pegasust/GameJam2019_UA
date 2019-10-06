import pygame
from pygame.locals import *
from physics import Rotation
class Player_Listener:
    """
        Vars:
            _player: reference to player object
    """
    # Currently mapped to arrow keys
    MOVE_KEYS = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
    def __init__(self, player):
        self._player = player
    def update(self):
        pressed = pygame.key.get_pressed()
        for dir in range(len(self.MOVE_KEYS)):
            if not pressed[self.MOVE_KEYS[dir]]:
                continue
            print("ping!")
            if dir == self._player.rotation:
                return self._player.move_forward()
            else:
                self._player.turn(dir)
