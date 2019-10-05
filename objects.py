"""
    Handles small object with rectangular form.
    A big object can consist of many smaller objects.
    There can be many objects of the same type, but each type
    should have unique get_type_id()\

    IMPORTANT: all objects should be implemented in this file
    and added to construct_from_id func
"""
import pygame
from physics import Rotation

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

Free_Space = None
class Object:
    """ 
        Const: 
            TYPE_ID
            IS_FREE_SPACE: whether this type is a handler for free_space.
                free_space will be ignored on the World if there is a 
                non-free_space occupying in one of its tile.
        Vars:
            position: type pygame.math.Vector2 top-right of the object
            rotation: Rotation type
            name: string that represents this obj
            height: height of this obj in physical pixel
            width: width of this obj in physical pixel
    """
    TYPE_ID = 0
    def __init__(self, name = "free_space", initial_x = 0, initial_y = 0, initial_rotation = Rotation.UP\
        ,height = 1, width = 1\
        ):
        self.position = pygame.Vector2()
        self.position.x = initial_x
        self.position.y = initial_y
        self.rotation = initial_rotation
        self.name = name
        self.height = height
        self.width = width
    def __str__(self):
        return "{}(pos={},rot={},name={},h={},w={})".format(self.__class__,\
            self.position,self.rotation,self.name,self.height,self.width)
class Dynamic_Object(Object):
    """ 
        This object can move and interact
    """
    TYPE_ID = 1
    def __init__(self,name="dynamo", i_x:int=0, i_y:int=0, i_rot = Rotation.UP,
                 height = 1, width = 1)->None:
        super(Dynamic_Object, self).__init__(name,i_x, i_y, i_rot,
                                             height, width)

"""
    To be distinguished. Basically, will have position and rotation
    and might have micro-optimization by not moving
"""
Static_Object = Dynamic_Object

class Player(Dynamic_Object):
    """
    This object should be visually rendered in the back-most (lowest priority)
    """
    TYPE_ID = 2
    def __init__(self,name:str="Suc",i_x:int=0, i_y:int=0, i_rot: Rotation\
        =Rotation.UP) -> None:
        super(Player,self).__init__(name, i_x, i_y, i_rot,1,1)

    @classmethod
    def get_default(cls,i_x:int, i_y:int) -> None:  # cls stands for class
        return cls("Suc", i_x, i_y, Rotation.UP)

class Ultimate_Border(Static_Object):
    """
        A border no object should be on. This should encapsulates the outer border
        of the world
    """
    TYPE_ID = 3
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
