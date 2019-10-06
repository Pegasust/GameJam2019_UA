#MAX_FPS = 60
#MAX_UPS = 60
import pygame
from pygame.locals import *
import renderer
import world
import time
import asset_manager

def load_level(level_name):
    pygame.init()
    f_obj = open(asset_manager.get_level_file(level_name))
    return world.World.from_str_map(f_obj.read())
def main():
    pygame.init()
    w0 = load_level("demo.lvl")
    print(w0.get_str_map())
    render_module = renderer.Raw_Renderer()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        w0.update()
        render_module.update(w0)

if __name__ == "__main__":
    main()