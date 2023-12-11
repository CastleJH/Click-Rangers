from GameState import *
import pygame

chain_lightning_used = False

normal_attack_sound = None
flame_sound = None
lightning_sound = None
heal_orb_sound = None
coin_sound = None
coin_spend_sound = None
trap_sound = None

def PrepareSound():
    global normal_attack_sound, flame_sound, lightning_sound, heal_orb_sound, coin_sound, coin_spend_sound, trap_sound
    normal_attack_sound = pygame.mixer.Sound('resources/normal.wav')
    normal_attack_sound.set_volume(GetMasterVolume() * 0.6)
    
    flame_sound = pygame.mixer.Sound('resources/flame.wav')
    flame_sound.set_volume(GetMasterVolume() * 1.5)
    
    lightning_sound = pygame.mixer.Sound('resources/lightning.wav')
    lightning_sound.set_volume(GetMasterVolume() * 1.0)
    
    heal_orb_sound = pygame.mixer.Sound('resources/get_special.wav')
    heal_orb_sound.set_volume(GetMasterVolume() * 2.0)
    
    coin_sound = pygame.mixer.Sound('resources/coin.wav')
    coin_sound.set_volume(GetMasterVolume() * 0.6)
    
    coin_spend_sound = pygame.mixer.Sound('resources/upgrade.wav')
    coin_spend_sound.set_volume(GetMasterVolume() * 2.0)
    
    trap_sound = pygame.mixer.Sound('resources/trap.wav')
    trap_sound.set_volume(GetMasterVolume() * 3.0)

def UpgradeMatchingStatWithKey(event):
    if GetGameOver():
        return
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            if UpgradeUserStat(GetUserStat(EStat(0))):
                coin_spend_sound.play()
        elif event.key == pygame.K_w:
            if UpgradeUserStat(GetUserStat(EStat(1))):
                coin_spend_sound.play()
        elif event.key == pygame.K_e:
            if UpgradeUserStat(GetUserStat(EStat(2))):
                coin_spend_sound.play()
        elif event.key == pygame.K_r:
            if UpgradeUserStat(GetUserStat(EStat(3))):
                coin_spend_sound.play()
        elif event.key == pygame.K_a:
            if UpgradeUserStat(GetUserStat(EStat(4))):
                coin_spend_sound.play()
        elif event.key == pygame.K_s:
            if UpgradeUserStat(GetUserStat(EStat(5))):
                coin_spend_sound.play()
        elif event.key == pygame.K_d:
            if UpgradeUserStat(GetUserStat(EStat(6))):
                coin_spend_sound.play()
        elif event.key == pygame.K_f:
            if UpgradeUserStat(GetUserStat(EStat(7))):
                coin_spend_sound.play()
            
def AttackWithUserMouseClick(event, mouse_pos):
    global chain_lightning_used
    if GetGameOver():
        return
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if GetChaingLightningTimer() > 0.0:
                chain_lightning_used = True
                if ChainLightningAttack(mouse_pos):
                    lightning_sound.play()
            else:
                value = NormalAttack(mouse_pos)
                if value == 1:
                    normal_attack_sound.play()
                elif value == 2:
                    heal_orb_sound.play()
                elif value == 3:
                    coin_sound.play()
                elif value == 4:
                    trap_sound.play()
        
def AttackWithUserMousePosition(mouse_pos):
    if GetGameOver():
        return
    if GetFlameThrowerTimer() > 0.0:
        if FlameAttack(mouse_pos):
            flame_sound.play()
        
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                StartGame()
        UpgradeMatchingStatWithKey(event)
        AttackWithUserMouseClick(event, mouse_pos)
    AttackWithUserMousePosition(mouse_pos)
    
    return mouse_pos, done
    
        
