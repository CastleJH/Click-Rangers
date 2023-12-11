from GameState import *
import pygame

chain_lightning_used = False

def UpgradeMatchingStatWithKey(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            UpgradeUserStat(GetUserStat(EStat(0)))
        elif event.key == pygame.K_w:
            UpgradeUserStat(GetUserStat(EStat(1)))
        elif event.key == pygame.K_e:
            UpgradeUserStat(GetUserStat(EStat(2)))
        elif event.key == pygame.K_r:
            UpgradeUserStat(GetUserStat(EStat(3)))
        elif event.key == pygame.K_a:
            UpgradeUserStat(GetUserStat(EStat(4)))
        elif event.key == pygame.K_s:
            UpgradeUserStat(GetUserStat(EStat(5)))
        elif event.key == pygame.K_d:
            UpgradeUserStat(GetUserStat(EStat(6)))
        elif event.key == pygame.K_f:
            UpgradeUserStat(GetUserStat(EStat(7)))
            
def AttackWithUserMouseClick(event, mouse_pos):
    global chain_lightning_used
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if GetChaingLightningTimer() > 0.0:
                chain_lightning_used = True
                ChainLightningAttack(mouse_pos)
            else:
                NormalAttack(mouse_pos)
        
def AttackWithUserMousePosition(mouse_pos):
    if GetFlameThrowerTimer() > 0.0:
        NormalAttack(mouse_pos)
        
def GetChainLightningUsed():
    global chain_lightning_used
    return chain_lightning_used
        
def ProcessUserInput():
    global chain_lightning_used
    mouse_pos = pygame.mouse.get_pos()
    done = False
    chain_lightning_used = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True    
        UpgradeMatchingStatWithKey(event)
        AttackWithUserMouseClick(event, mouse_pos)
    AttackWithUserMousePosition(mouse_pos)
    
    return mouse_pos, done
    
        
