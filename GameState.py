import numpy as np
from FallingObjects import *

#---------------game settings(unchangeable)
FPS = 60
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
screen = 0
bottom_line_y = WINDOW_HEIGHT - 150
max_game_level = 50
master_volume = 0.5

#---------------game state(changed over game)
game_level = 1
is_playing = False
is_gameover = False
new_falling_idx = 0
level_up_timer = 0.0
spawn_cooltime = 0.0
chain_lightning_targets = []

#---------------function
def GetMasterVolume():
    global master_volume
    return master_volume

def GetGameLevel():
    global game_level
    return game_level

def GetGamePlaying():
    global is_playing
    return is_playing

def GetGameOver():
    global is_gameover
    return is_gameover

def SetGameOver(over):
    global is_gameover
    is_gameover = over

def GetFallSpeedModifier():
    freeze_mult = 1.0
    if GetFreezerTimer() > 0.0:
        freeze_mult = 0.5
    return np.clip(0.98 + game_level * 0.02, 1.0, 2.0) * GetUserStat(EStat.FALL_SPEED).stat * freeze_mult

def SpawnFallingObjects(delta_seconds):
    global new_falling_idx, spawn_cooltime
    spawn_cooltime += delta_seconds
    
    if spawn_cooltime < 0.1:
        return
    
    spawn_cooltime = 0.0
    
    base_drop_rate = 0.05
    base_coin_rate = 0.01
    base_heal_orb_rate = 0.01
    base_trap_rate = 0.02
    base_freezer_rate = 0.01
    base_chain_lightning_rate = 0.01
    base_flame_thrower_rate = 0.01

    if np.random.uniform(0.0, 1.0) < base_drop_rate * np.interp(float(game_level), [1.0, 50.0], [1.0, 20.0]):
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
        
def NormalAttack(mouse_pos):
    global falling_objects
    remove_list = []
    attacked = 0
    for key in falling_objects:
        if falling_objects[key].CheckOverlappedCircle(mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat):
            falling_objects[key].OnAttacked()
            if isinstance(falling_objects[key], Drop) or isinstance(falling_objects[key], ChainLightning) or isinstance(falling_objects[key], FlameThrower) or isinstance(falling_objects[key], Freezer):
                attacked = 1
            elif isinstance(falling_objects[key], HealOrb):
                attacked = 2
            elif isinstance(falling_objects[key], Coin):
                attacked = 3
            elif isinstance(falling_objects[key], Trap):
                attacked = 4
        if falling_objects[key].del_timer > 10:
            remove_list.append(key)
    for key in remove_list:
        RemoveFallingObject(key)
    return attacked
        
        
def FlameAttack(mouse_pos):
    global falling_objects
    remove_list = []
    attacked = False
    for key in falling_objects:
        if (falling_objects[key].immune_to_flame == False) and falling_objects[key].CheckOverlappedCircle(mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat):
            falling_objects[key].OnAttacked()
            attacked = True
        if falling_objects[key].del_timer > 10:
            remove_list.append(key)
    for key in remove_list:
        RemoveFallingObject(key)
    return attacked

def custom_sort(FallingObj, mouse_pos):
    return (FallingObj.x - mouse_pos[0]) ** 2 + (FallingObj.y - mouse_pos[1]) ** 2

def CalcChainLigtningTarget(mouse_pos):
    global falling_objects
    ret_list = []
    obj_list = list(falling_objects.values())
    sorted_objects = sorted(obj_list, key=lambda obj: custom_sort(obj, mouse_pos))
    index = 0
    count = GetUserStat(EStat.CHAIN_LIGHTNING).stat
    while count != 0 and index < len(sorted_objects):
        if isinstance(sorted_objects[index], Drop) and sorted_objects[index].is_alive:
            count -= 1
            ret_list.append(sorted_objects[index])
        index += 1
    return ret_list
    
def GetChainLightningTarget():
    global chain_lightning_targets
    return chain_lightning_targets
    
def ChainLightningAttack(mouse_pos):
    global chain_lightning_targets
    attacked = False
    chain_lightning_targets = CalcChainLigtningTarget(mouse_pos)
    for drop in chain_lightning_targets:
        drop.OnAttacked()
        attacked = True
    return attacked
    
def TryIncreaseGameLevel(delta_seconds):
    global level_up_timer, max_game_level, game_level
    level_up_timer += delta_seconds
    if level_up_timer >= 5.0:
        level_up_timer = 0.0
        game_level = min(max_game_level, game_level + 1)
    
def UpdateGameState(delta_seconds):
    global is_playing
    if is_playing:        
        TryIncreaseGameLevel(delta_seconds)
        DecreaseAttackTypeTimer(delta_seconds)
        
        SpawnFallingObjects(delta_seconds)
        UpdateFallingObjects(delta_seconds)
        DeleteObjectsOutOfGame()
        
        if GetCurrentHP() <= 0.0:
            SetGameOver(True)
        
def StartGame():
    global is_playing, game_level, is_gameover, new_falling_idx, level_up_timer, spawn_cooltime, chain_lightning_targets
    if not is_playing or is_gameover:
        print("start!")
        is_playing = True
        game_level = 1
        is_playing = True
        is_gameover = False
        new_falling_idx = 0
        level_up_timer = 0.0
        spawn_cooltime = 0.0
        chain_lightning_targets = []
        
        ResetUserStat()
        ResetFallingObjects()