"""
    Questions: 
    How many vis_pixels are there in a phys_pixel?


    Style conventions:
        _{name} is private field
        {UPPERCASED_NAME} is const
    Assumes pygame.init() is called
"""
import pygame
from pygame.locals import *
import world
import objects
class Raw_Renderer:
    """
    Const:
        VISUAL_PER_PHYSICAL_PIXELS is the number of pixels per object
    Vars:   
            _screen_surface: pointer to surface that pygame.display use to .blit()
            SCREEN_SIZE is the total count of pixels on screen
            _background: clean copy of the default_bg
            _updated_rects: rects updated since the last time this was
                called
    """
    VISUAL_PER_PHYSICAL_PIXELS = 16
    # set display to custom resolution
    def __init__(self, width=1280, height=720, default_bg=pygame.Color(0,0,0)):
        self._screen_surface = pygame.display.set_mode((width, height)\
            # ,flags = pygame.FULLSCREEN|pygame.HWSURFACE\
            )
        pygame.display.set_caption('pygame_test')
        self._updated_rects = []
        if default_bg is not None:
            self._updated_rects.append(self._screen_surface.fill(default_bg))
        self._background = self._screen_surface.copy()
        (self.w,self.h) = self._screen_surface.get_size()
        self.SCREEN_SIZE = self.w*self.h
        self.display()

    def display(self):
        pygame.display.update(self._updated_rects)
        #pygame.display.flip()

    def update(self, world_obj:world.World\
        , x_offset = 32, y_offset = 32):
        bg = self._background.copy()
        _x=x_offset
        _y=y_offset
        game_info = world_obj._phys_pixels
        # self._updated_rects =[]
        for y in range(len(game_info)):
            for x in range(len(game_info[y])):
                spec_obj = objects.Object(i_x=x,i_y=y,\
                    ) if game_info[y][x] is None else game_info[y][x]
                bg.blit(\
                        spec_obj.current_sprite,(_x,_y))

                _x += self.VISUAL_PER_PHYSICAL_PIXELS
            _y += self.VISUAL_PER_PHYSICAL_PIXELS
            _x = x_offset
        self._updated_rects = self._screen_surface.blit(bg,(0,0))
        
        self.display()

if __name__ == "__main__":
    def main():
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            rects = []
            renderer = Raw_Renderer(default_bg=None)
            rects.append(renderer._screen_surface.blit(objects.\
                Dynamic_Object().current_sprite,(10,10)))
            pygame.display.update(rects)
    main()