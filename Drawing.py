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
    if GetFlameThrowerTimer() > 0.0:
        pygame.draw.circle(screen, (255, 0, 0), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
    elif GetChaingLightningTimer() > 0.0:
        pygame.draw.circle(screen, (255, 255, 0), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
    else:
        pygame.draw.circle(screen, (0, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
        
def DrawGame(screen, mouse_pos):
    DrawBackground(screen)
    DrawFallingObjects(screen)
    DrawBottomline(screen)
    DrawUI(screen)
    DrawUserMouse(screen, mouse_pos)
    pygame.display.flip()