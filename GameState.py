import numpy as np
from UserStat import GetUserStat, EStat

FPS = 60
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
screen = 0

#---------------game settings(unchangeable)
bottom_line_y = WINDOW_HEIGHT - 100
base_drop_rate = 0.05
base_gold_rate = 0.005
base_heal_orb_rate = 0.005
base_trap_rate = 0.005

#---------------game state(changed over game)
game_level = 1
is_playing = True
is_gameover = False
mouse_pos = (0, 0)
score = 0
gold = 0
max_hp = GetUserStat(EStat.MAX_HP).stat
current_hp = max_hp
        
def TryDecreaseHP(ammount):
    global current_hp
    current_hp = max(0, current_hp - ammount)
    if current_hp == 0:
        is_gameover = True
    print(current_hp)

def TryHealHP(ammount):
    global current_hp
    current_hp = min(max_hp, current_hp + ammount)
    
def GetScore(ammount):
    global score
    score += ammount
    print(score)
    
def AddGold(ammount):
    global gold
    gold += ammount
    
def TrySpendGold(ammount):
    global gold
    if gold < ammount:
        return False
    else:
        gold -= ammount
        return True

def GetFallSpeedModifier():
    return np.clip(0.95 + game_level * 0.05, 1.0, 2.0) * GetUserStat(EStat.FALL_SPEED).stat


def UpgradeUserStat(stat):
    global gold
    cost = stat.real_cost
    if cost <= gold and stat.Upgrade():
        TrySpendGold(cost)

