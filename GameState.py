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
max_game_level = 50
is_playing = True
is_gameover = False
new_falling_idx = 0
level_up_timer = 0.0
spawn_cooltime = 0.0

#---------------function
def GetFallSpeedModifier():
    return np.clip(0.95 + game_level * 0.05, 1.0, 2.0) * GetUserStat(EStat.FALL_SPEED).stat

def SpawnFallingObjects(delta_seconds):
    global new_falling_idx, spawn_cooltime
    
    spawn_cooltime += delta_seconds
    
    if spawn_cooltime < 0.1:
        return
    
    spawn_cooltime = 0.0
    
    base_drop_rate = 0.05
    base_coin_rate = 0.005
    base_heal_orb_rate = 0.005
    base_trap_rate = 0.005
    base_freezer_rate = 0.001
    base_chain_lightning_rate = 0.001
    base_flame_thrower_rate = 0.001

    if np.random.uniform(0.0, 1.0) < base_drop_rate * np.interp(float(game_level), [1.0, 50.0], [1.0, 5.0]):
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
        
    if np.random.uniform(0.0, 1.0) < base_freezer_rate:
        AddFallingObject(new_falling_idx, Freezer(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
        
    if np.random.uniform(0.0, 1.0) < base_chain_lightning_rate:
        AddFallingObject(new_falling_idx, ChainLightning(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
        
    if np.random.uniform(0.0, 1.0) < base_flame_thrower_rate:
        AddFallingObject(new_falling_idx, FlameThrower(new_falling_idx, WINDOW_WIDTH))
        new_falling_idx += 1
    return
    
def UpdateFallingObjects(delta_seconds):
    global falling_objects
    for key in falling_objects:
        falling_objects[key].update(delta_seconds, GetFallSpeedModifier(), bottom_line_y)
        
def DeleteObjectsOutOfGame():
    global falling_objects, FPS
    remove_list = []
    for key in falling_objects:
        if falling_objects[key].del_timer > 10:
            remove_list.append(key)
    for key in remove_list:
        RemoveFallingObject(key)
        
def CheckDropsCollision(mouse_pos):
    global falling_objects, FPS
    remove_list = []
    for key in falling_objects:
        if falling_objects[key].CheckOverlappedCircle(mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat):
            falling_objects[key].OnAttacked()
        if falling_objects[key].del_timer > 10:
            remove_list.append(key)
    for key in remove_list:
        RemoveFallingObject(key)
        
def NormalAttack(mouse_pos):
    CheckDropsCollision(mouse_pos)

def ChainLightningAttack(mouse_pos):
    CheckDropsCollision(mouse_pos)
    
def TryIncreaseGameLevel(delta_seconds):
    global level_up_timer, max_game_level, game_level
    level_up_timer += delta_seconds
    if level_up_timer >= 10.0:
        level_up_timer = 0.0
        game_level = min(max_game_level, game_level + 1)
    
def UpdateGameState(delta_seconds):
    TryIncreaseGameLevel(delta_seconds)
    DecreaseAttackTypeTimer(delta_seconds)
    
    SpawnFallingObjects(delta_seconds)
    UpdateFallingObjects(delta_seconds)
    DeleteObjectsOutOfGame()