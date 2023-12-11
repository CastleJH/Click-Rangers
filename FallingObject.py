import numpy as np
import pygame
from GameState import *
    
falling_objects = {}
new_falling_idx = 0
gravity = 0.2
fragments_num = 50
fallings_radius = [15.0, 25.0]

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
        
    def draw(self, screen):
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
    
    def CheckOverlappedCircle(self, point, radius = 0):
        if (self.x - point[0]) ** 2 + (self.y - point[1]) ** 2 <= (self.radius + radius) ** 2:
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