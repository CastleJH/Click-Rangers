import pygame
from GameState import *
from UserInput import *
from Drawing import *

#---------------main
def main():
    pygame.init()
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()
    done = False
    
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
                    CheckDropsCollision(mouse_pos)
            
        SpawnFallingObjects()
        
        UpdateFallingObjects()
        
        DeleteObjectsOutOfGame()
        
        screen.fill(0)
        DrawFallingObjects(screen)
        pygame.draw.circle(screen, (255, 255, 255), mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).base_stat)
        pygame.display.flip()
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()