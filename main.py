import pygame
import numpy as np
from enum import Enum

#---------------game settings(unchangeable)
FPS = 60
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
screen = 0
gravity = 0.2
fragments_num = 50
fallings_radius = [15.0, 25.0]
bottom_line_y = WINDOW_HEIGHT - 100
base_drop_rate = 0.05
base_gold_rate = 0.005
base_heal_orb_rate = 0.005
base_trap_rate = 0.005

#---------------user upgradable stat
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
            if TrySpendGold(self.real_cost):
                self.stat = self.base_stat + (self.additive_modifier_per_level * self.level)
                self.level += 1
                self.cost *= 1.5
                self.real_cost = round(self.cost)
                return True
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

#---------------functions to get user stat
def GetUserStat(Index):
    global user_stats
    return user_stats[int(Index)]


#---------------game state(changed over game)
game_level = 1
is_playing = True
is_gameover = False
mouse_pos = (0, 0)
score = 0
gold = 0
max_hp = GetUserStat(EStat.MAX_HP)
current_hp = max_hp

#---------------functions to get/set game state
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

#---------------game classes
class FallingObject():
    def __init__(self):
        self.radius = np.random.uniform(fallings_radius[0], fallings_radius[1])
        self.line = round(np.interp(self.radius, fallings_radius, [5.0, 9.0]))
        self.x = np.random.uniform(self.radius, WINDOW_WIDTH - self.radius)
        self.y = -18
        self.base_color = (np.random.randint(100, 256),
                      np.random.randint(100, 256),
                      np.random.randint(100, 256))
        self.current_color = self.base_color
        self.base_speed = np.random.uniform(2.0, 4.0)
        
        self.is_freezed = False
        self.is_alive = True
        self.del_counter = 0
        
        self.fragments_location = [[0, 0] for i in range(fragments_num)]
        self.fragments_velocity = [[np.random.uniform(-1.0, 1.0), np.random.uniform(-3.0, -5.0)] for i in range(fragments_num)]
        
    def update(self):
        if self.is_alive:
            if ~self.is_freezed:
                self.y += GetFallSpeedModifier() * self.base_speed
                if bottom_line_y + self.radius <= self.y:
                    self.OnTouchedLine() 
        else:
            self.del_counter += 1
            for i, loc in enumerate(self.fragments_location):
                self.fragments_velocity[i][1] += gravity
                loc[0] += self.fragments_velocity[i][0]
                loc[1] += self.fragments_velocity[i][1]
        
    def draw(self):
        if self.is_alive:
            pygame.draw.circle(screen, self.current_color, [self.x, self.y], self.radius, self.line)
        else:
            for loc in self.fragments_location:
                pygame.draw.circle(screen, self.current_color, [self.x + loc[0], self.y + loc[1]], 1)
    
    def OnTouchedLine(self):
        self.is_alive = False
        self.current_color = (255, 0, 0)
        
    def OnAttacked(self):
        self.is_alive = False
        #self.current_color = (0, 255, 255)
    
    def OnFreezed(self):
        self.is_freezed = True
        if self.is_alive :
            self.current_color = (255, 255, 255)
    
    def OnMelted(self):
        self.is_freezed = False
        if self.is_alive :
            self.current_color = self.base_color
    
    def CheckOverlappedMouse(self):
        if (self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2 <= (self.radius + GetUserStat(EStat.MOUSE_RADIUS).stat) ** 2:
            return True
        return False
            
class Drop(FallingObject):
    def __init__(self):
        super().__init__()
        self.score = round(np.interp(self.radius, fallings_radius, [1.0, 5.0]))
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        TryDecreaseHP(self.score)
    
    def OnAttacked(self):
        super().OnAttacked()
        GetScore(self.score)
    
#class GoldOrb(FallingObject):
    
falling_objects = {}
new_falling_idx = 0

#---------------functions to interact game objects
def CheckDropsCollision():
    global mouse_pos
    remove_list = []
    for idx, drop in enumerate(falling_objects):
        if drop.CheckOverlappedMouse():
            drop.OnAttacked()
            remove_list.append(idx)
    
    for idx in reversed(falling_objects):
        falling_objects.removeat
            
def TrySpawnDrop():
    global base_drop_rate, game_level
    poss = base_drop_rate * np.interp(float(min(game_level, 50)), [1.0, 50.0], [1.0, 5.0])
    if np.random.uniform(0.0, 1.0) < poss:
        falling_objects.append(Drop())

#---------------functions mapped to user input
        
#---------------main
def main():
    pygame.init()
    
    global screen, mouse_pos, mouse_radius, drops
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()
    done = False
    drops = [Drop() for i in range(10)]
    
    while not done:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if 0x31 <= event.key & event.key <= 0x36:
                    print('hello')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    CheckDropsCollision()
            
        screen.fill(0)
        
        for f in drops:
            f.update()
            f.draw()
            
        pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
        pygame.display.flip()
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()