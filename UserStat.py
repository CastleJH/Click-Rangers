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
    def __init__(self, _stat_name = "default", _base_stat = 1, _max_level = 5, _cost = 1, _additive_modifier_per_level = 0, _upgrade_key = 'Q'):
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
        self.upgrade_key = _upgrade_key
        
    def Upgrade(self):
        if self.level < self.max_level:
            self.stat = self.base_stat + (self.additive_modifier_per_level * self.level)
            self.level += 1
            self.cost *= 1.5
            self.real_cost = round(self.cost)
            return True
        else: 
            return False
       
user_stats = [      #stat name,     base stat,  max level,  base cost,  stat modifier,  uprade key
    StatData(       "Radius",       20,         10,         2,          5,          'Q'),
    StatData(       "Max HP",       100,        999,        1,          10,         'W'),
    StatData(       "Heal Orb",     10,         5,          2,          2,          'E'),
    StatData(       "Gold",         5,          5,          2,          1,          'R'),
    StatData(       "Fall Speed",   1.0,        10,         2,          -0.05,      'A'),
    StatData(       "Blizzard",     3.0,        999,        5,          0.2,        'S'),
    StatData(       "Lightning", 2,       999,        7,          1,          'D'),
    StatData(       "Flame",   5.0,     999,        7,          0.5,        'F')
]

score = 0
gold = 0
max_hp = user_stats[int(EStat.MAX_HP)].stat
current_hp = max_hp
freezer_timer = 0
chain_lightning_timer = 0
flame_thrower_timer = 0

def ResetUserStat():
    global user_stats, score, gold, max_hp, current_hp, freezer_timer, chain_lightning_timer, flame_thrower_timer
    user_stats = [      #stat name,     base stat,  max level,  base cost,  stat modifier,  uprade key
        StatData(       "Radius",       20,         10,         2,          5,          'Q'),
        StatData(       "Max HP",       100,        999,        1,          10,         'W'),
        StatData(       "Heal Orb",     10,         5,          2,          2,          'E'),
        StatData(       "Gold",         5,          5,          2,          1,          'R'),
        StatData(       "Fall Speed",   1.0,        10,         2,          -0.05,      'A'),
        StatData(       "Blizzard",     3.0,        999,        5,          0.2,        'S'),
        StatData(       "Lightning", 2,       999,        7,          1,          'D'),
        StatData(       "Flame",   5.0,     999,        7,          0.5,        'F')
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
    global current_hp, is_gameover
    current_hp = max(0, current_hp - ammount)

def TryHealHP(ammount):
    global current_hp
    current_hp = min(max_hp, current_hp + ammount)

def GetScore():
    global score
    return score

def GetCurrentHP():
    global current_hp
    return current_hp

def GetGold():
    global gold
    return gold

def AddScore(ammount):
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
        return TrySpendGold(cost)
    return False
        
def StartFreezer():
    global freezer_timer
    freezer_timer = GetUserStat(EStat.FREEZE).stat
    
def StartChainLightning():
    global chain_lightning_timer
    chain_lightning_timer = 0.5

def StartFlameThrower():
    global flame_thrower_timer
    flame_thrower_timer = GetUserStat(EStat.FLAME_THROWER).stat
    
def GetFreezerTimer():
    global freezer_timer
    return freezer_timer

def GetChaingLightningTimer():
    global chain_lightning_timer
    return chain_lightning_timer

def GetFlameThrowerTimer():
    global flame_thrower_timer
    return flame_thrower_timer

def DecreaseAttackTypeTimer(delta_seconds):
    global freezer_timer, chain_lightning_timer, flame_thrower_timer
    freezer_timer = max(0.0, freezer_timer - delta_seconds)
    chain_lightning_timer = max(0.0, chain_lightning_timer - delta_seconds)
    flame_thrower_timer = max(0.0, flame_thrower_timer - delta_seconds)