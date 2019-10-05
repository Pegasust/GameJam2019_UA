import os
ASSETS_FOLDER = os.path.join('assets')
OBJ_FOLDER = os.path.join(ASSETS_FOLDER,'objs')
LEVEL_FOLDER = os.path.join(ASSETS_FOLDER,"levels")

def get_char_sprite(file_name):
    return os.path.join(OBJ_FOLDER,file_name)
def get_level_file(file_name):
    return os.path.join(LEVEL_FOLDER,file_name)