"""
    + Allows conversion from World to line-separated string
    + Allows World init from line-separated string

    - Needs a better implementation of Ultimate_Border. Might get
        expensive in memory if World is large.

    Format:
    <format>
    ; This is a comment
    ##############
    #      #A P  #
    ### ####\## ##
    ## #C##B### ##
    ## #\ #\# # ##
    ##E    \F\\\ # 
    ##############
    ~ ;Asserts the end of the map
    ; # is border (not final)
    ; P is player (not final)
    ; A,B,C,E,F are dummy enemies (not final)
    ; Notice: A,B,C,E,F are top-left of the hitbox of the enemies
    ; ' ' is free-space (final)
    ; '\' is place-holder (for objects that are bigger than 1x1)
    ~ ;Asserts the end of the level

    </format>
    For now, no grouping is needed to produce
"""
import objects
import world_rules
_PLACEHOLDER_CHAR = '\\'
_FREESPACE_CHAR = ' '
_id2char = {
    objects.Free_Space: _FREESPACE_CHAR,
    objects.Dynamic_Object.TYPE_ID: 'D',
    objects.Static_Object.TYPE_ID:'S',
    objects.Player.TYPE_ID:'P',
    objects.Ultimate_Border.TYPE_ID:'#',
}
_char2id = dict()
for key,val in _id2char.items():
    _char2id[val]=key

def _get_char(obj)->str:
    """
    Returns char notation of that object type
    """
    return _FREESPACE_CHAR if obj is objects.Free_Space \
        else _id2char[obj.TYPE_ID]
def _get_id(char):
    """
    Returns id of object type (which can be used with
    objects.construct_from_id() to construct objects in runtime.
    Do not pass in Free_Space or _PLACEHOLDER_CHAR.
    """
    return _char2id[char]
class World:
    """
        consts:
        vars:
            _phys_pixels: 2D (columns of rows) array that stores Object pointers
            _objs: list of objects in the world, excludes player, excludes free_space
            player: the player
            game_over: bool
    """

    def __init__(self, phys_pixels: [[objects.Object]], objs: [objects.Object],\
        player: objects.Player,\
       #free_space: [objects.Free_Space]\
       ):
        self._phys_pixels = phys_pixels
        self._objs = objs
        self.player = player
        self.game_over = False
        #self._free_space = free_space


    @classmethod
    def get_empty_rect(cls, height:int, width:int)-> None:
        """
        ONLY FOR TESTING/DEBUGGING. Creates an empty square World with player at 0,0
        height is the max number of physical pixel in a column
        width is the max number of physical pixel in a row
        """
        # Shouldn't be on Ultimate_Border
        player = objects.Player.get_default(1,1)
        (top,bot,left,right) = objects.Ultimate_Border.\
            get_4_borders(height,width)
        phys_pixels = [[top for x in range(width+2)]]
        phys_pixels += [([left]+[objects.Free_Space for x in range(width)]+[right])\
            for y in range(height)]
        phys_pixels += [[bot for x in range(width+2)]]
        phys_pixels[1][1] = player
        objs = [top,bot,left,right]
        return cls(phys_pixels, objs, player)

    @classmethod
    def from_str_map(cls, str_map:str, username:str="Suc"):
        wid_strs = str_map.splitlines()
        # TODO: Can be optimized to storing pointers of objects larger
        # than 1x1 into a post-processing array, create objs first
        # with top-left of the large obj initialized in phys_pixels.
        # Then, with post-processing array ptrs, initialize the rest
        # parts of the body of the objects.

        # Create Free_Space world first. Allocate the memory.
        phys_pixels = []
        for wid_str in wid_strs:
            phys_pixels.append([objects.Free_Space for x in range(len(wid_str))])
        # Initialize variables
        objs = []
        player = None
        # Loop over again, this time we assign stuff
        for y0 in range(len(wid_strs)):
            for x0 in range(len(wid_strs[y0])):
                # Check if the str should be ignored
                if wid_strs[y0][x0] == _PLACEHOLDER_CHAR or\
                    wid_strs[y0][x0] == _FREESPACE_CHAR:
                    continue
                type_id = _get_id(wid_strs[y0][x0])
                # Arguments to "spawn" the object
                kwargs = dict(i_x=x0, i_y=y0)
                is_player = False
                if type_id == objects.Player.TYPE_ID:
                    # Add name to the argument to spawn obj
                    # because Player needs "name"
                    kwargs["name"]=username
                    is_player = True
                # Spawn the object with kwargs
                obj = objects.construct_from_id(type_id,**kwargs)
                if is_player:
                    player = obj
                    assert(player.TYPE_ID == objects.Player.TYPE_ID)
                else:
                    objs.append(obj)
                # With the width and length of the obj,
                # assign it to phys_pixels.
                for _y in range(obj.height):
                    y = y0 + _y
                    for _x in range(obj.width):
                        x = x0 + _x
                        phys_pixels[y][x] = obj
        return cls(phys_pixels,objs,player)

    def get_str_map(self):
        """
        Create str_map formatted string represents the world
        """
        result = ""
        for y in range(len(self._phys_pixels)):
            wid_str = ""
            for x in range(len(self._phys_pixels[y])):
                wid_str+= _get_char(self._phys_pixels[y][x])
            result += wid_str + '\n'
        return result[:-1]  # voids the last '\n'
    def __str__(self):
        ret_val = self.get_str_map()
        ret_val+=("\nPlayer: {}".format(self.player))
        ret_val+=("\nObjs:")
        for obj in self._objs:
            ret_val+=("\n{}".format(obj))
        return ret_val
    def handle_rule_output(self, rule, obj_req, target_obj):
        if rule == world_rules.KILL:
            self.eliminate(target_obj)
        elif rule == world_rules.KILLED:
            self.eliminate(obj_req)
        elif rule == world_rules.GAME_OVER:
            self.game_over = True
        return None
    def update(self,*args, **kwargs):
        """
            Player is updated first, followed by other dynamic
            objects
        """
        (outcome, player, interacted) = \
            self.player.update({'world':self._phys_pixels,'objs':self._objs})
        self.handle_rule_output(outcome,player,interacted)
        for foreign_obj in self._objs:
            self.handle_rule_output(\
                *foreign_obj.update(world=self._phys_pixels,\
                objs=self._objs))
    
    def eliminate(self, obj):
        self._objs.remove(obj)
        
    pass
if __name__ == "__main__":
    print("World: ")
    w0=World.get_empty_rect(10, 10)
    str_map = w0.get_str_map()
    print(str_map)
    print("World from str: ")
    w = World.from_str_map(str_map)
    print(w.get_str_map())
    print("__w0:")
    print(w0)
    print()
    print("__w:")
    print(w)

