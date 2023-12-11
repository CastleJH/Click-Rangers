from enum import Enum

class EStat(Enum):
    MOUSE_RADIUS = 0
    MAX_HP = 1
    HEAL_ORB = 2
    GOLD = 3
    FALL_SPEED = 4
    FREEZE = 5
    CHAIN_LIGHTNING = 6
    FLAME_THROWER = 7
    
    def __int__(self):
        return self.value

class StatData():
    def __init__(self, _stat_name = "default", _base_stat = 1, _max_level = 5, _cost = 1, _additive_modifier_per_level = 0):
        self.stat_name = _stat_name
        #unchangeable
        self.base_stat = _base_stat
        self.max_level = _max_level
        self.additive_modifier_per_level = _additive_modifier_per_level
        #changed by upgrade
        self.stat = self.base_stat
        self.level = 1
        self.cost = _cost
        self.real_cost = round(self.cost)
        
    def Upgrade(self):
        if self.level < self.max_level:
            self.stat = self.base_stat + (self.additive_modifier_per_level * self.level)
            self.level += 1
            self.cost *= 1.5
            self.real_cost = round(self.cost)
            return True
        else: 
            return False
       
user_stats = [      #stat name,     base stat,  max level,  base cost,  stat modifier
    StatData(       "Mouse Radius", 20,         10,         2,          4),
    StatData(       "Max HP",       100,        999,        1,          10),
    StatData(       "Heal Orb",     10,         5,          2,          2),
    StatData(       "Gold",         1,          5,          2,           1),
    StatData(       "Fall Speed",   1.0,        10,         2,          -0.05),
    StatData(       "Freezer",      3.0,        999,        5,          0.2),
    StatData(       "Chain Lightning", 2,       999,        7,          1),
    StatData(       "Flame Thrower",   5.0,     999,        7,          0.5)
]

score = 0
gold = 0
max_hp = user_stats[int(EStat.MAX_HP)].stat
current_hp = max_hp
freezer_timer = 0
chain_lightning_timer = 0
flame_thrower_timer = 0

def GetUserStat(Index):
    global user_stats
    return user_stats[int(Index)]

def TryDecreaseHP(ammount):
    global current_hp
    current_hp = max(0, current_hp - ammount)
    if current_hp == 0:
        is_gameover = True

def TryHealHP(ammount):
    global current_hp
    current_hp = min(max_hp, current_hp + ammount)
    
def GetScore(ammount):
    global score
    score += ammount
    
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

def UpgradeUserStat(stat):
    global gold
    cost = stat.real_cost
    if cost <= gold and stat.Upgrade():
        TrySpendGold(cost)
        
def StartFreezer():
    global freezer_timer, chain_lightning_timer, flame_thrower_timer
    freezer_timer = GetUserStat(EStat.FREEZE).stat
    chain_lightning_timer = 0.0
    flame_thrower_timer = 0.0
    
def StartChainLightning():
    global freezer_timer, chain_lightning_timer, flame_thrower_timer
    freezer_timer = 0.0
    chain_lightning_timer = 5.0
    flame_thrower_timer = 0.0

def StartFlameThrower():
    global freezer_timer, chain_lightning_timer, flame_thrower_timer
    freezer_timer = 0.0
    chain_lightning_timer = 0.0
    flame_thrower_timer = GetUserStat(EStat.FLAME_THROWER).stat