class Rotation:
    """
        Consts:
            UP, DOWN, LEFT, RIGHT, UNKNOWN
        Vars:
            value: stores either UP, DOWN, LEFT, RIGHT or UNKNOWN (???)
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UNKNOWN = -1 # SHOULD NEVER BE USED. 
                 # IF FOR PLACE-HOLDER, EXPECT UNDEFINED BEHAVIOR.
    def __init__(self, starting_rotation = UNKNOWN):
        self.value = starting_rotation
    def __eq__(self, other):
        return self.value == other.value
    def __str__(self):
        return "Rotation({})"
    def set_rotation(self, new_rot):
        """
            Returns pointer to self
        """
        self.value = new_rot
        return self
    def get_rotation(self):
        return self.value
    def get_next_rotation(self):
        return (self.value + 1)%4
    def rotate_left(self):
        """
            Rotates left relative to current position:
                ex:
                    UP -> LEFT
                    RIGHT -> UP
                    DOWN -> RIGHT
                    LEFT -> DOWN
        """
        # to handle value = 0
        self.value += 4  # note: using {operator}= will micro-optimize this code
        self.value -= 1
        self.value %= 4  # can micro-optimize this should python not optimize % with exponential of 2
        return self
    def rotate_right(self):        
        """
            Rotates left relative to current position:
                ex:
                    UP -> RIGHT
                    RIGHT -> DOWN
                    DOWN -> LEFT
                    LEFT -> UP
        """
        self.value += 1
        self.value %= 4
        return self

