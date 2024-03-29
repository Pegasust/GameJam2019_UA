"""
    Handles small object with rectangular form.
    A big object can consist of many smaller objects.
    There can be many objects of the same type, but each type
    should have unique get_type_id()\

    IMPORTANT: all objects should be implemented in this file
    and added to construct_from_id func
"""
import world_rules
import pygame
import asset_manager
from physics import Rotation
from post_processing import *
import player_input_listener as input_listener

def construct_from_id(type_id = 0, *arg,**kwarg):
    """
    **kwarg only needs "i_x" and "i_y" keys.
    """

    # I am sorry for the switch/case, father of coding.
    if type_id == Object.TYPE_ID:
        return Object(*arg,**kwarg)
    elif type_id == Dynamic_Object.TYPE_ID:
        return Dynamic_Object(*arg,**kwarg)
    elif type_id == Static_Object.TYPE_ID:
        return Static_Object(*arg,**kwarg)
    elif type_id == Player.TYPE_ID:
        return Player(*arg,**kwarg)
    elif type_id == Ultimate_Border.TYPE_ID:
        return Ultimate_Border(*arg,**kwarg)
    else:
        # Should not reach here.
        assert(false)
        
def _assign_current_sprite(self,rot):
    self.current_sprite = (None if self.SPRITES is None else self.SPRITES[rot])

Free_Space = None

def _get_directional_sprites(dir:Rotation=None, surface:pygame.Surface=None):
    if dir is None:
        return None
    dict_ = {dir:surface}
    for i in range(1,4):
        dict_[(dir+i)%4]=pygame.transform.rotate(surface,90*i)
    return dict_

def _static_dict_sprite(file_name, dir = Rotation.UP):
    # Returns a scaled sprite from assets/objs/file_name to 
    # post_processing.Graphical_Specs.VISUAL_PIXELS_RES
    return {dir:pygame.transform.scale(pygame.image.\
        load(asset_manager.get_char_sprite(file_name)),(Graphical_Specs.\
        VISUAL_PIXELS_RES,Graphical_Specs.VISUAL_PIXELS_RES))}

def _load_dynamic_sprites(file):
    tup = tuple(_static_dict_sprite(file).items())[0]
    return _get_directional_sprites(*tup)

class Object:
    """ 
        Const: 
            TYPE_ID
            SPRITES is the dict of Rotation-Sprite
        Vars:
            position: type pygame.math.Vector2 top-right of the object
            rotation: Rotation type
            name: string that represents this obj
            height: height of this obj in physical pixel
            width: width of this obj in physical pixel
            current_sprite: current pointer to sprite obj in SPRITES
    """
    TYPE_ID = 0
    SPRITES = _static_dict_sprite("free_space.png")
    def __init__(self, name = "free_space", i_x = 0, i_y = 0, i_rotation = Rotation.UP\
        ,height = 1, width = 1\
        ):
        self.position = pygame.Vector2()
        self.position.x = i_x
        self.position.y = i_y
        self.rotation = i_rotation
        self.name = name
        self.height = height
        self.width = width
        _assign_current_sprite(self, self.rotation)
        
    def __str__(self):
        return "{}(pos={},rot={},name={},h={},w={})".format(self.__class__.__name__,\
            self.position,self.rotation,self.name,self.height,self.width)
    def update(self,*args, **kwargs):
        return (world_rules.IGNORE,None,None)
class Dynamic_Object(Object):
    """ 
        This object can move and interact
    """
    TYPE_ID = 1
    SPRITES = _load_dynamic_sprites("dynamo.png")
    # SPRITES
    def __init__(self,name="dynamo", i_x:int=0, i_y:int=0, i_rot = Rotation.UP,
                 height = 1, width = 1)->None:
        super(Dynamic_Object, self).__init__(name,i_x, i_y, i_rot,
                                             height, width)
    # TODO: IMPLEMENT UPDATES IN POSITION AND ROTATION
    def update(self,*args,**kwargs):
        """
        Dynamic's update should return None, GAME_OVER, or KILLED
        """
        # Some logics that is unique to each object
        # Just moves randomly
        return (world_rules.IGNORE,None, None)
    def interact(self, other:Object):
        """ Suppose dynamo is hostile
            That one-hit kills Player
        """
        if other is Free_Space:
            return world_rules.IGNORE
        elif other.TYPE_ID == Player.TYPE_ID:
            return world_rules.GAME_OVER
        elif other.TYPE_ID == Static_Object.TYPE_ID:
            return world_rules.BLOCKED
        
    def move_forward(self,*args,**kwargs):
        desired_position = pygame.math.Vector2(self.position)
        if self.rotation == Rotation.UP:
            desired_position.y+=1
        elif self.rotation == Rotation.DOWN:
            desired_position.y-=1
        elif self.rotation == Rotation.RIGHT:
            desired_position.x+=1
        else:
            desired_position.x-=1
        phys_pixels=kwargs['world']
        other = detect_collision(phys_pixels,desired_position)
        outcome = self.interact(other)
        return self.handle_outcome_interaction(other,outcome)

    def handle_outcome_interaction(self, other,outcome):        
        if outcome == world_rules.BLOCKED:
            return (outcome,self,other)
        elif outcome ==world_rules.IGNORE:
            self.handle_world_change(phys_pixels,desired_position)
            return (outcome, self, other)
        elif outcome == world_rules.KILL:
            other.perish(phys_pixels)
            return (outcome, self, other)
        elif outcome == world_rules.KILLED:
            self.perish(phys_pixels)
            return (outcome, self, other)
    def perish(self, phys_pixels):
        """
        Does not exist on the map, but the world still
        has reference to the obj
        """
        for y in range(len(self.height)):
            _y = self.position.y+y
            for x in range(len(self.width)):
                _x = self.position.x+x
                phys_pixels = Free_Space

    def handle_world_change(self,phys_pixels, new_pos):
        """
        Sanitizes pointers on occupying lands to Free_Space.
        Transforms new pointers to self
        """
        self.perish(phys_pixels)
        for y in range(len(self.height)):
            _y = new_pos.y
            for x in range(len(self.width)):
                _x = new_pos.x+x
                phys_pixels = self
        self.position = new_pos

    @staticmethod
    def detect_collision(phys_pixels,desired_position):
        """
            Returns None or objects.Free_Space if nothing
            Returns the object otherwise
        """
        return phys_pixels[desired_position.y][desired_position.x]
    def turn(self,rotation):
        self.rotation = rotation
        return (world_rules.IGNORE, self, None)

"""
    To be distinguished. Basically, will have position and rotation
    and might have micro-optimization by not moving
"""
Static_Object = Object

class Player(Dynamic_Object):
    """
    This object should be visually rendered in the back-most (lowest priority)
    Extended vars:
        input_listener: brings control to the object. This obj calls move_forward, turn
            and in the future, abilities upon update().
    """
    TYPE_ID = 2
    SPRITES = _load_dynamic_sprites("player.png")
    def __init__(self,name:str="Suc",i_x:int=0, i_y:int=0, i_rot: Rotation\
        =Rotation.UP) -> None:
        super(Player,self).__init__(name, i_x, i_y, i_rot,1,1)
        self.input_listener = input_listener.Player_Listener(self)

    def update(self,*args, **kwargs):
        self.input_listener.update()


    @classmethod
    def get_default(cls,i_x:int, i_y:int) -> None:  # cls stands for class
        return cls("Suc", i_x, i_y, Rotation.UP)

class Ultimate_Border(Static_Object):
    """
        A border no object should be on. This should encapsulates the outer border
        of the world
    """
    TYPE_ID = 3
    SPRITES = _load_dynamic_sprites("ultimate_barrier.png")
    def __init__(self,i_x:int,i_y:int,i_rot:Rotation=Rotation.UP,\
        h:int=1,w:int=1)->None:
        super(Ultimate_Border,self).__init__("_BORDER_",i_x,i_y,i_rot,h,w)
    @classmethod
    def get_4_borders(cls,h:int, w:int):
        """
        Returns (top, bot, left, right)
        """
        return (cls(0,0,Rotation.UP,1,w+2),cls(0,h+2,Rotation.UP,1,w+2),\
            cls(1,0,Rotation.UP,h,1),cls(1,w+2,Rotation.UP,h,1))
