import pygame
from UserInput import *
        
chain_lightning_trail = []

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
        pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
    
def AddChainLightning(obj_list, mouse_pos):
    global chain_lightning_trail
    spread = [-7.0, 8.0]
    for drop in obj_list:
        chain_lightning_trail.append([0.3, 0, 255, 255, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
        chain_lightning_trail.append([0.3, 0, 255, 255, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
        chain_lightning_trail.append([0.3, 255, 255, 255, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
        chain_lightning_trail.append([0.3, 255, 255, 0, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
        chain_lightning_trail.append([0.3, 255, 255, 0, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
        chain_lightning_trail.append([0.3, 255, 255, 0, mouse_pos[0] + np.random.randint(spread[0], spread[1]), mouse_pos[1] + np.random.randint(spread[0], spread[1]), drop.x + np.random.randint(spread[0], spread[1]), drop.y + np.random.randint(spread[0], spread[1])])
    
def DrawChainLightning(screen, delta_seconds):
    global chain_lightning_trail
    for trail in chain_lightning_trail:
        trail[0] -= delta_seconds
        if trail[0] <= 0:
            chain_lightning_trail.remove(trail)
            continue
        else:
            pygame.draw.line(screen, (trail[1], trail[2], trail[3]), (trail[4], trail[5]), (trail[6], trail[7]))
        
def DrawGame(delta_seconds, screen, mouse_pos):
    DrawBackground(screen)
    if GetChainLightningUsed(): 
        AddChainLightning(GetChainLightningTarget(), mouse_pos)
    DrawChainLightning(screen, delta_seconds)
    DrawFallingObjects(screen)
    DrawBottomline(screen)
    DrawUI(screen)
    DrawUserMouse(screen, mouse_pos)
    pygame.display.flip()