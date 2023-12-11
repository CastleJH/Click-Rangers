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
        mouse_pos, done = ProcessUserInput()
            
        UpdateGameState()
        
        DrawGame(screen, mouse_pos)
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()