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
    delta_seconds = 0.0
    
    while not done:
        mouse_pos, done = ProcessUserInput()
            
        UpdateGameState(delta_seconds)
        
        DrawGame(screen, mouse_pos)
        delta_seconds = clock.tick(FPS) / 1000.0
        
if __name__ == "__main__":
    main()