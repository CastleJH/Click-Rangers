from GameState import *

def DrawFallingObjects(screen):
    print(len(falling_objects))
    for key in falling_objects:
        falling_objects[key].draw(screen)