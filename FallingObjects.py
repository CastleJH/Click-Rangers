import numpy as np
import pygame
from UserStat import *
    
gravity = 0.2
fragments_num = 50
fallings_radius = [25.0, 35.0]
falling_objects = {}
ring_images = []
coin_image = None
heal_orb_image = None
trap_image = None
freezer_image = None
chain_lightning_image = None
flame_thrower_image = None


def PrepareImage():
    global ring_images, coin_image, heal_orb_image, trap_image, freezer_image, chain_lightning_image, flame_thrower_image
    image = pygame.image.load("resources/Rings.png")
    size = 130
    big_size = 195
    for i in range(6):
        for j in range(6):
            if len(ring_images) >= 33:
                break
            rect = pygame.Rect(size * j, size * i, size, size)
            cut_image = image.subsurface(rect)
            
            for x in range(size):
                for y in range(size):
                    ori = cut_image.get_at((x, y))
                    if ori == (0, 0, 0, 255):
                        cut_image.set_at((x, y), (255, 255, 255, 0))
                        
            ring_images.append(cut_image)    
    
    image = pygame.image.load("resources/Items.png")
    coin_image = image.subsurface(pygame.Rect(size * 1, size * 1, size, size))
    heal_orb_image = image.subsurface(pygame.Rect(size * 2, size * 0, size, size))
    
    trap_image = image.subsurface(pygame.Rect(size * 0, size * 3, big_size, big_size))
    for x in range(big_size):
        for y in range(big_size):
            ori = trap_image.get_at((x, y))
            if ori[3] == 255:
                trap_image.set_at((x, y), (150, 150, 150, 255))
    
    image = pygame.image.load("resources/Items.png")
    freezer_image = image.subsurface(pygame.Rect(size * 0, size * 3, big_size, big_size))
    for x in range(big_size):
        for y in range(big_size):
            ori = freezer_image.get_at((x, y))
            if ori[3] == 255:
                freezer_image.set_at((x, y), (0, 255, 255, 255))
    
    image = pygame.image.load("resources/Items.png")
    chain_lightning_image = image.subsurface(pygame.Rect(size * 0, size * 3, big_size, big_size))
    for x in range(big_size):
        for y in range(big_size):
            ori = chain_lightning_image.get_at((x, y))
            if ori[3] == 255:
                chain_lightning_image.set_at((x, y), (255, 255, 0, 255))
    
    image = pygame.image.load("resources/Items.png")
    flame_thrower_image = image.subsurface(pygame.Rect(size * 0, size * 3, big_size, big_size))
    for x in range(big_size):
        for y in range(big_size):
            ori = flame_thrower_image.get_at((x, y))
            if ori[3] == 255:
                flame_thrower_image.set_at((x, y), (255, 0, 0, 255))

def GetRandomPixelColor(image):
    width, height = image.get_size()
    passed = False
    while not passed:
        rx = np.random.randint(0, width)
        ry = np.random.randint(0, height)
        color = image.get_at((rx, ry))
        passed = color[0] != 0
        passed = passed and color[1] != 0
        passed = passed and color[2] != 0
        passed = passed and color[3] == 255
    return color

#---------------game classes
class FallingObject():
    def __init__(self, _index, _window_width):
        self.index = _index
        self.radius = 30
        self.line = round(np.interp(self.radius, fallings_radius, [5.0, 9.0]))
        self.x = np.random.uniform(self.radius, _window_width - self.radius)
        self.y = -18
        self.image = ring_images[0]
        self.base_speed = np.random.uniform(2.0, 4.0)
        
        self.is_freezed = False
        self.is_alive = True
        self.del_timer = 0.0
        
        self.fragments_location = [[0, 0] for i in range(fragments_num)]
        self.fragments_color = [(0, 0, 0) for i in range(fragments_num)]
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
                color_list.append((255, 255, 255))
            for i, clr in enumerate(self.fragments_color):
                self.fragments_color[i] = color_list[np.random.randint(0, len(color_list))]
        else:
            for i, clr in enumerate(self.fragments_color):
                self.fragments_color[i] = GetRandomPixelColor(self.image)
        
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
        self.image = pygame.transform.scale(ring_images[np.random.randint(0, len(ring_images))], (self.radius * 2.0, self.radius * 2.0))
        self.score = round(np.interp(self.radius, fallings_radius, [1.0, 5.0]))
        
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
    def OnTouchedLine(self):
        super().OnTouchedLine()
        self.SetFragmentsColor(True, [(255, 50, 50), (255, 0, 0), (200, 0, 0), (150, 0, 0), (100, 0, 0)])
        TryDecreaseHP(self.score)
    
    def OnAttacked(self):
        super().OnAttacked()
        self.SetFragmentsColor(False)
        GetScore(self.score)
                  
    def OnFreezed(self):
        super().OnFreezed()
        self.is_freezed = True
    
    def OnMelted(self):
        super().OnMelted()
        self.is_freezed = False
       
class Coin(FallingObject):  
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.image = pygame.transform.scale(coin_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.image = pygame.transform.scale(heal_orb_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
        self.image = pygame.transform.scale(trap_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.image = pygame.transform.scale(freezer_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.image = pygame.transform.scale(chain_lightning_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
    def __init__(self, _index, _window_width):
        super().__init__(_index, _window_width)
        self.image = pygame.transform.scale(flame_thrower_image, (self.radius * 2.0, self.radius * 2.0))
              
    def DrawAlive(self, screen):
        super().DrawAlive(screen)
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
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
    