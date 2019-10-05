"""
   This module will need to be consulted to the designers.
   For now, it takes arrow keys to move and no additional interactions.
"""
import pygame
from pygame.locals import *
from physics import Rotation
import threading
import queue

INPUT_CHECK_FREQUENCY = 5000  #Hz

class Player_Command:
    """
    Stores list of available commands to the player.
    """
    MOVE_UP =       0b1000
    MOVE_RIGHT =    0b1001
    MOVE_DOWN =     0b1010
    MOVE_LEFT =     0b1011
    TURN_UP =       0b0100
    TURN_RIGHT =    0b0101
    TURN_DOWN =     0b0110
    TURN_LEFT =     0b0111
    
    def get_opposite_dir_if(condition, move_action):
        return move_action ^ (condition<<1)
    def is_move(input):
        x = (input & 0b11)
        return (input>>3 & 1,x)
    def is_turn(input):
        x = (input & 0b11)
        return (input>>2 & 1,x)

class Move_Turn_Handler:
    """
    Const:
        MOVE_DEADZONE: The amount of time in millisecond before
            arrow input is considered a movement.
    Vars:
        
    """
    MOVE_DEADZONE = 100
    def __init__(self):
        self.time_held = [0 ,0, 0, 0]
    def _registers(self,axis):
        return abs(axis)>self.MOVE_DEADZONE
    def get_command(self)->[int]:
        cmd_list = []
        y_axis = self.time_held[Rotation.UP]-self.time_held[Rotation.DOWN]
        if self._registers(y_axis):
            cmd_list.append(Player_Command.get_opposite_dir_if(y_axis<0,MOVE_UP))
        else:
            cmd_list.append(Player_Command.get_opposite_dir_if(y_axis<0,TURN_UP))
        x_axis = self.time_held[Rotation.RIGHT]-self.time_held[ROTATION.LEFT]
        if self._registers(x_axis):
            cmd_list.append(Player_Command.get_opposite_dir_if(x_axis<0,MOVE_RIGHT))
        else:
            cmd_list.append(Player_Command.get_opposite_dir_if(x_axis<0,TURN_RIGHT))
        return cmd_list
    def calculate_time_held(self, bool_arr, delta_time):
        for i in range(len(bool_arr)):
            if(bool_arr[i]):
                self.time_held[i] = min(1000,self.time_held[i]+delta_time)
            else:
                self.time_held[i] = max(0, self.time_held[i]-delta_time)


class Input_Module:
    """
    Vars:
        input_buffer is efficient multi-producer/multi-consumer
            queue of Player_Command
    """
    def input_loop(self,frequency=INPUT_CHECK_FREQUENCY):
        while not exit:
            pressed = pygame.key.get_pressed()
            # Trim the list down to four
            bool_arr = [pressed[K_UP], pressed[K_RIGHT], pressed[K_DOWN]\
                , pressed[K_LEFT]]
            # Input processing
            self.move_turn_handler.calculate_time_held(bool_arr,\
                self.clock.get_time())
            cmds = self.move_turn_handler.get_command()
            for cmd in cmds:
                self.input_buffer.put(cmd)
                print("put {}_{}".format("MOVE" if ))
            self.clock.tick(frequency)
    def __init__(self):
        self.input_buffer = queue.Queue(256)
        self.exit = False
        self.move_turn_handler = Move_Turn_Handler()
        self.thread = threading.Thread(target=input_loop,args=(self,INPUT_CHECK_FREQUENCY))
        self.clock = pygame.time.Clock()
        self.thread.start()
    def try_sync(self):
        self.exit = True
        self.thread.join()

if __name__ == "__main__":
    dir = 0
    print(Player_Command.is_move(Player_Command.TURN_DOWN))
    print(Player_Command.is_move(Player_Command.MOVE_UP))
    print(Player_Command.is_turn(Player_Command.MOVE_DOWN))
    print(Player_Command.is_turn(Player_Command.TURN_LEFT))