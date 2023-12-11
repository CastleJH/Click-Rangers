import pygame
import numpy as np
from UserStat import *
from FallingObject import *
from GameState import *
from UserInput import *

#---------------functions to interact game objects
def CheckDropsCollision():
    global mouse_pos, falling_objects
    remove_list = []
    for idx, drop in enumerate(falling_objects):
        print(idx)
        if drop.CheckOverlappedCircle(mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat):
            drop.OnAttacked()
            remove_list.append(idx)
    
    #for idx in reversed(falling_objects):
        #falling_objects.removeat
            
def TrySpawnDrop():
    global base_drop_rate, game_level, falling_objects
    poss = base_drop_rate * np.interp(float(min(game_level, 50)), [1.0, 50.0], [1.0, 5.0])
    if np.random.uniform(0.0, 1.0) < poss:
        falling_objects.append(Drop())
  
#---------------main
def main():
    pygame.init()
    global screen, mouse_pos, falling_objects
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()
    done = False
    falling_objects = [Drop() for i in range(10)]
    
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
                    print("pressed")
            
        screen.fill(0)
        
        for f in falling_objects:
            f.update()
            f.draw(screen)
            
        pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
        pygame.display.flip()
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()