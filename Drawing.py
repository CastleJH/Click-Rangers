import pygame
from UserInput import *
        
chain_lightning_trail = []
f_b_30 = None
f_l_30 = None
f_b_20 = None
f_l_20 = None
f_b_15 = None
f_l_15 = None
background_image = None

def PrepareFont():
    global f_b_30, f_l_30, f_b_20, f_l_20, f_b_15, f_l_15
    f_b_30 = pygame.font.Font("resources/Stardust B.ttf", 30)
    f_l_30 = pygame.font.Font("resources/Stardust.ttf", 30)
    f_b_20 = pygame.font.Font("resources/Stardust B.ttf", 20)
    f_l_20 = pygame.font.Font("resources/Stardust.ttf", 20)
    f_b_15 = pygame.font.Font("resources/Stardust B.ttf", 15)
    f_l_15 = pygame.font.Font("resources/Stardust.ttf", 15)

def PrepareBackgroundImage():
    global background_image, WINDOW_WIDTH, WINDOW_HEIGHT
    background_image = pygame.image.load('resources/background.png')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, background_image.get_height() / background_image.get_width() * WINDOW_WIDTH))

def DrawText(screen, font, loc, text, color = (255, 255, 255), align = "l"):
    target = font.render(text, True, color)
    if align == 'l':
        screen.blit(target, (loc[0], loc[1] - target.get_height() // 2))
    elif align == 'c':
        screen.blit(target, (loc[0] - target.get_width() // 2, loc[1] - target.get_height() // 2))
    elif align == 'r':
        screen.blit(target, (loc[0] - target.get_width(), loc[1] - target.get_height() // 2))
    
    
def DrawBackground(screen):
    #screen.fill(0)
    if background_image == None:
        PrepareBackgroundImage()
    screen.blit(background_image, (0, -WINDOW_HEIGHT // 3))
    #screen.fill((0, 0, 0, 250))
    return

def DrawFallingObjects(screen):
    for key in falling_objects:
        falling_objects[key].draw(screen)

def DrawBottomline(screen):
    global bottom_line_y, WINDOW_WIDTH
    pygame.draw.rect(screen, (0, 0, 0, 30), (0, bottom_line_y, WINDOW_WIDTH, 500))
    pygame.draw.line(screen, (255, 0, 0), (0, bottom_line_y), (WINDOW_WIDTH, bottom_line_y), 5)
    
    return 

def DrawUpgradeInfo(screen):
    global bottom_line_y, WINDOW_WIDTH
    render_count = 0
    n_row = 2
    n_col = 4
    x_off = 20
    y_off = bottom_line_y + 50
    x_diff = WINDOW_WIDTH // 4
    y_diff = 50
    for i in range(n_row):
        for j in range(n_col):
            if render_count >= 8:
                break
            render_count += 1
            stat = GetUserStat(EStat(i * n_col + j))
            DrawText(screen, f_l_15, ( + x_off + x_diff * j, y_off + y_diff * i), "[{}]:".format(stat.upgrade_key), (50, 255, 150))
            level_text = "m"
            if stat.level != stat.max_level:
                level_text = str(stat.level)
            DrawText(screen, f_l_15, (30 + x_off + x_diff * j, y_off + y_diff * i), "lv.{}".format(level_text), (50, 150, 255))
            color = (255, 255, 255)
            if stat.real_cost <= GetGold():
                color = (255, 200, 0)    
            DrawText(screen, f_l_15, (80 + x_off + x_diff * j, y_off + y_diff * i), "{}".format(stat.stat_name), color)
            DrawText(screen, f_l_15, (x_diff - 40 + x_off + x_diff * j, y_off + y_diff * i), "{}G".format(stat.real_cost), (255, 200, 0), 'r')
        

def DrawHPBar(screen):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    size_x = 150
    size_y = 12
    loc_x = WINDOW_WIDTH - 180
    loc_y = 70
    pygame.draw.rect(screen, (255, 255, 255), (loc_x, loc_y, size_x, size_y))
    pygame.draw.rect(screen, (255, 50, 50), (loc_x, loc_y, np.interp(GetCurrentHP(), [0, GetUserStat(EStat.MAX_HP).stat], [0, size_x]), size_y))

def DrawUI(screen):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    DrawText(screen, f_b_30, (WINDOW_WIDTH // 2, 50), "Level: {}".format(GetGameLevel()), align="c")
    DrawText(screen, f_b_20, (50, 50), "Score: {}".format(GetScore()), (0, 255, 255))
    DrawText(screen, f_b_20, (50, 80), "Gold: {}".format(GetGold()), (255, 200, 0))
    DrawText(screen, f_b_15, (WINDOW_WIDTH - 30, 50), "{0}/{1}".format(GetCurrentHP(), GetUserStat(EStat.MAX_HP).stat), align = "r")
    DrawHPBar(screen)
    DrawUpgradeInfo(screen)

def DrawUserMouse(screen, mouse_pos):
    if GetFlameThrowerTimer() > 0.0:
        pygame.draw.circle(screen, (255, 0, 0), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat * 0.6, 5)
    if GetChaingLightningTimer() > 0.0:
        pygame.draw.circle(screen, (255, 255, 0), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat * 0.8, 3)
    pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat, 3)
    
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
        
def DrawGameOver(screen):
    global is_gameover, WINDOW_WIDTH, WINDOW_HEIGHT
    if GetGameOver():
        DrawText(screen, f_b_30, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 70), "GAME OVER!", (255, 50, 50), 'c')
        DrawText(screen, f_b_20, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20), "Press [SpaceBar] to restart", (255, 255, 255), 'c')

def DrawStartGame(screen):
    global is_playing, WINDOW_WIDTH, WINDOW_HEIGHT
    if not GetGamePlaying():
        DrawText(screen, f_b_30, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), "Press [SpaceBar] to start", (255, 255, 255), 'c')
        
def DrawGame(delta_seconds, screen, mouse_pos):
    DrawBackground(screen)
    if GetChainLightningUsed(): 
        AddChainLightning(GetChainLightningTarget(), mouse_pos)
    DrawChainLightning(screen, delta_seconds)
    DrawFallingObjects(screen)
    DrawBottomline(screen)
    DrawUI(screen)
    DrawGameOver(screen)
    DrawStartGame(screen)
    DrawUserMouse(screen, mouse_pos)
    pygame.display.flip()