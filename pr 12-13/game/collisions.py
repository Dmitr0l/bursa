import pygame

def move_and_collide(rect, vel_x, vel_y, platforms):
    on_ground = False
    hit_ceiling = False

    rect.x += vel_x
    for p in platforms:
        if rect.colliderect(p):
            if vel_x > 0:
                rect.right = p.left
            if vel_x < 0:
                rect.left = p.right

    rect.y += vel_y
    for p in platforms:
        if rect.colliderect(p):
            if vel_y > 0: 
                rect.bottom = p.top
                on_ground = True
            if vel_y < 0:
                rect.top = p.bottom
                hit_ceiling = True

    return on_ground, hit_ceiling