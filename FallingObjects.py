import numpy as np
import pygame
from UserStat import *
    
gravity = 0.2
fragments_num = 50
fallings_radius = [15.0, 25.0]
falling_objects = {}

#---------------game classes
class FallingObject():
    def __init__(self, _index, _window_width):
        self.index = _index
        self.radius = 20
        self.line = round(np.interp(self.radius, fallings_radius, [5.0, 9.0]))
        self.x = np.random.uniform(self.radius, _window_width - self.radius)
        self.y = -18
        self.base_color = (np.random.randint(100, 256),
                      np.random.randint(100, 256),
                      np.random.randint(100, 256))
        self.current_color = self.base_color
        self.base_speed = np.random.uniform(2.0, 4.0)
        
        self.is_freezed = False
        self.is_alive = True
        self.del_timer = 0.0
        
        self.fragments_location = [[0, 0] for i in range(fragments_num)]
        self.fragments_color = [self.base_color for i in range(fragments_num)]
        self.fragments_velocity = [[np.random.uniform(-1.0, 1.0), np.random.uniform(-3.0, -5.0)] for i in range(fragments_num)]
        
    def update(self, delta_seconds, fall_speed_modifier, bottom_line_y):
        if self.is_alive:
            if ~self.is_freezed:
                self.y += fall_speed_modifier * self.base_speed
                if bottom_line_y + self.radius <= self.y:
                    self.OnTouchedLine() 
        else:
            self.del_timer += delta_seconds
            for i, loc in enumerate(self.fragments_location):
                self.fragments_velocity[i][1] += gravity
                loc[0] += self.fragments_velocity[i][0]
                loc[1] += self.fragments_velocity[i][1]

    
    def CheckOverlappedCircle(self, point, radius = 0):
        if self.is_alive:
            if (self.x - point[0]) ** 2 + (self.y - point[1]) ** 2 <= (self.radius + radius) ** 2:
                return True
        return False
    
    def draw(self, screen):
        if self.is_alive:
            self.DrawAlive(screen)
        else:
            self.DrawDead(screen)
    
    def SetFragmentsColor(self, use_fixed_color_only, color_list = []):
        if use_fixed_color_only:
            if len(color_list) == 0:
                color_list.append(self.current_color)
            for i, clr in enumerate(self.fragments_color):
                self.fragments_color[i] = color_list[np.random.randint(0, len(color_list))]
        else:
            for i, clr in enumerate(self.fragments_color):
                min_val = min(self.current_color)
                adding = np.random.randint(-int(min_val * 0.8), 256 - min_val)
                self.fragments_color[i] = (np.clip(self.current_color[0] + adding, 0, 255),
                                           np.clip(self.current_color[1] + adding, 0, 255),
                                           np.clip(self.current_color[2] + adding, 0, 255))  
        
    def DrawDead(self, screen):
        for i, loc in enumerate(self.fragments_location):
            pygame.draw.circle(screen, self.fragments_color[i], [self.x + loc[0], self.y + loc[1]], 1)
    
    def DrawAlive(self, screen):
        return
    
    def OnTouchedLine(self):
        global falling_objects
        self.is_alive = False
        
    def OnAttacked(self):
        global falling_objects
        self.is_alive = False
    
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return
            

class Drop(FallingObject):
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.radius = np.random.uniform(fallings_radius[0], fallings_radius[1])
        self.score = round(np.interp(self.radius, fallings_radius, [1.0, 5.0]))
        
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, self.current_color, [self.x, self.y], self.radius, self.line)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.current_color = (255, 0, 0)
        self.SetFragmentsColor(True, [(255, 50, 50), (255, 0, 0), (200, 0, 0), (150, 0, 0), (100, 0, 0)])
        TryDecreaseHP(self.score)
    
    def OnAttacked(self):
        super().OnAttacked()
        self.SetFragmentsColor(False)
        GetScore(self.score)
                  
    def OnFreezed(self):
        super().OnFreezed()
        self.is_freezed = True
        if self.is_alive :
            self.current_color = (255, 255, 255)
    
    def OnMelted(self):
        super().OnMelted()
        self.is_freezed = False
        if self.is_alive :
            self.current_color = self.base_color
       
class Coin(FallingObject):        
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, (250, 200, 0), [self.x, self.y], self.radius)
        pygame.draw.circle(screen, (125, 100, 0), [self.x, self.y], self.radius * 0.4)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(250, 200, 0), (125, 100, 0), (50, 50, 0)])
        
    def OnAttacked(self):
        super().OnAttacked()
        AddGold(GetUserStat(EStat.GOLD).stat)
        self.SetFragmentsColor(True, [(250, 200, 0), (125, 100, 0), (50, 50, 0)])
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return
        
class HealOrb(FallingObject):
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, (255, 100, 100), [self.x, self.y], self.radius)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(255, 100, 100), (150, 80, 80)])
        
    def OnAttacked(self):
        super().OnAttacked()
        TryHealHP(GetUserStat(EStat.HEAL_ORB).stat)
        self.SetFragmentsColor(True, [(255, 100, 100), (150, 80, 80)])
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return
        
class Trap(FallingObject):    
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.base_color = (100, 100, 100)
        self.current_color = self.base_color
            
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, self.base_color, [self.x, self.y], self.radius)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(100, 100, 100), (50, 50, 50), (150, 150, 150)])
        
    def OnAttacked(self):
        TryDecreaseHP(10)
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return

class Freezer(FallingObject):
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, (100, 255, 255), [self.x, self.y], self.radius)
        pygame.draw.circle(screen, (255, 255, 255), [self.x, self.y], self.radius * 0.3)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(0, 255, 255), (255, 255, 255)])
        
    def OnAttacked(self):
        super().OnAttacked()
        StartFreezer()
        self.SetFragmentsColor(True, [(0, 255, 255), (255, 255, 255)])
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return

class ChainLightning(FallingObject):
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, (255, 255, 0), [self.x, self.y], self.radius)
        pygame.draw.circle(screen, (255, 255, 255), [self.x, self.y], self.radius * 0.3)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(255, 255, 100), (255, 255, 255)])
        
    def OnAttacked(self):
        super().OnAttacked()
        StartChainLightning()
        self.SetFragmentsColor(True, [(255, 255, 100), (255, 255, 255)])
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return

class FlameThrower(FallingObject):
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        pygame.draw.circle(screen, (255, 0, 0), [self.x, self.y], self.radius)
        pygame.draw.circle(screen, (255, 200, 0), [self.x, self.y], self.radius * 0.3)
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(255, 0, 0), (255, 200, 0)])
        
    def OnAttacked(self):
        super().OnAttacked()
        StartFlameThrower()
        self.SetFragmentsColor(True, [(255, 0, 0), (255, 200, 0)])
                  
    def OnFreezed(self):
        return
    
    def OnMelted(self):
        return
    
def AddFallingObject(index, object):
    falling_objects[index] = object
    
def RemoveFallingObject(index):
    falling_objects.pop(index)
    