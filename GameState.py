import numpy as np
from FallingObjects import *

#---------------game settings(unchangeable)
FPS = 60
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
screen = 0
bottom_line_y = WINDOW_HEIGHT - 100

#---------------game state(changed over game)
game_level = 1
is_playing = True
is_gameover = False

#---------------falling objects(changed over game)
new_falling_idx = 0

#---------------function
def GetFallSpeedModifier():
    return np.clip(0.95 + game_level * 0.05, 1.0, 2.0) * GetUserStat(EStat.FALL_SPEED).stat

def SpawnFallingObjects():
    global new_falling_idx
    
    base_drop_rate = 0.05
    base_coin_rate = 0.005
    base_heal_orb_rate = 0.005
    base_trap_rate = 0.005

    if np.random.uniform(0.0, 1.0) < base_drop_rate * np.interp(float(min(game_level, 50)), [1.0, 50.0], [1.0, 5.0]):
        AddFallingObject(new_falling_idx, Drop(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
        
    if np.random.uniform(0.0, 1.0) < base_coin_rate:
        AddFallingObject(new_falling_idx, Coin(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
        
    if np.random.uniform(0.0, 1.0) < base_heal_orb_rate:
        AddFallingObject(new_falling_idx, HealOrb(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
        
    if np.random.uniform(0.0, 1.0) < base_trap_rate:
        AddFallingObject(new_falling_idx, Trap(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
    return
    
def DeleteObjectsOutOfGame():
    global falling_objects, FPS
    remove_list = []
    for key in falling_objects:
        if falling_objects[key].del_counter > 10 * FPS:
            remove_list.append(key)
    for key in remove_list:
        print("removed:", key)
        RemoveFallingObject(key)
        
def UpdateFallingObjects():
    global falling_objects
    for key in falling_objects:
        falling_objects[key].update(GetFallSpeedModifier(), bottom_line_y)