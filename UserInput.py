from GameState import *

def CheckDropsCollision(mouse_pos):
    global falling_objects, FPS
    remove_list = []
    print(mouse_pos)
    for key in falling_objects:
        if falling_objects[key].CheckOverlappedCircle(mouse_pos, GetUserStat(EStat.MOUSE_RADIUS).stat):
            falling_objects[key].OnAttacked()
        if falling_objects[key].del_counter > 10 * FPS:
            remove_list.append(key)
    for key in remove_list:
        RemoveFallingObject(key)