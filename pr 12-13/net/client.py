import pygame
import socket
import json
from game.player import Player
from game.level import level_map
from game.blocks import Platform 
from common.constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ("127.0.0.1", 5555)
    
    client.sendto(json.dumps({'type': 'join'}).encode(), server_addr)
    
    my_id = None
    players_sprites = {}
    platforms = pygame.sprite.Group()
    
    for y, row in enumerate(level_map):
        for x, col in enumerate(row):
            if col == "-": platforms.add(Platform(x*32, y*32))

    running = True
    while running:
        keys = pygame.key.get_pressed()
        mx = (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0)
        input_data = {
            'type': 'input',
            'mx': mx, 'my': 0, 
            'jump': keys[pygame.K_w], 
            'attack': keys[pygame.K_SPACE]
        }
        client.sendto(json.dumps(input_data).encode(), server_addr)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False

        try:
            client.settimeout(0.01)
            data, _ = client.recvfrom(2048)
            msg = json.loads(data.decode())
            if msg['type'] == 'welcome': my_id = msg['id']
            if msg['type'] == 'snapshot':
                for p_data in msg['players']:
                    pid = p_data['id']
                    if pid not in players_sprites:
                        players_sprites[pid] = Player(p_data['x'], p_data['y'])
                    
                    players_sprites[pid].rect.x = p_data['x']
                    players_sprites[pid].rect.y = p_data['y']
                    players_sprites[pid].state = p_data['state']
                    players_sprites[pid].animate()
        except: pass

        screen.fill((0, 0, 0))
        platforms.draw(screen)
        for p in players_sprites.values():
            screen.blit(p.image, p.rect)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()