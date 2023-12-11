from GameState import *
import pygame
        
def DrawBackground(screen):
    screen.fill(0)
    return

def DrawFallingObjects(screen):
    for key in falling_objects:
        falling_objects[key].draw(screen)

def DrawBottomline(screen):
    return 

def DrawUI(screen):
    return

def DrawUserMouse(screen, mouse_pos):
    pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
        
def DrawGame(screen, mouse_pos):
    DrawBackground(screen)
    DrawFallingObjects(screen)
    DrawBottomline(screen)
    DrawUI(screen)
    DrawUserMouse(screen, mouse_pos)
    pygame.display.flip()