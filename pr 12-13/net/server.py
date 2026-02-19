import socket
import json
import time
import pygame
from common.constants import *
from game.level import get_colliders, SPAWN_POINTS

class ServerPlayer:
    def __init__(self, id, x, y):
        self.id = id
        self.rect = pygame.Rect(x, y, 32, 48) # Приблизний розмір хітбокса
        self.xvel = 0
        self.yvel = 0
        self.hp = PLAYER_HP
        self.alive = True
        self.state = "idle"
        self.last_attack = 0
        self.death_time = 0

    def update(self, mx, my, jump, attack, platforms):
        if not self.alive: return

        self.xvel = mx * MOVE_SPEED
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if jump and self.on_ground:
            self.yvel = -JUMP_POWER
        
        self.yvel += GRAVITY
        self.on_ground = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        # Оновлення стану
        if abs(self.xvel) > 0: self.state = "run"
        else: self.state = "idle"
        if not self.on_ground: self.state = "jump"

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if self.rect.colliderect(p):
                if xvel > 0: self.rect.right = p.left
                if xvel < 0: self.rect.left = p.right
                if yvel > 0:
                    self.rect.bottom = p.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.bottom
                    self.yvel = 0

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("127.0.0.1", 5555))
    server.setblocking(False)
    
    players = {}
    addrs = {}
    platforms = get_colliders()
    
    print("Сервер запущено...")
    
    while True:
        try:
            data, addr = server.recvfrom(1024)
            msg = json.loads(data.decode())
            
            if msg['type'] == 'join':
                p_id = str(len(players))
                players[p_id] = ServerPlayer(p_id, 100, 100)
                addrs[addr] = p_id
                server.sendto(json.dumps({'type': 'welcome', 'id': p_id}).encode(), addr)
            
            elif msg['type'] == 'input':
                p_id = addrs.get(addr)
                if p_id:
                    players[p_id].update(msg['mx'], msg['my'], msg['jump'], msg['attack'], platforms)
        except: pass

        now = time.time() * 1000
        for p in players.values():
            if not p.alive and now - p.death_time > RESPAWN_DELAY:
                p.alive = True
                p.hp = PLAYER_HP
                p.rect.topleft = SPAWN_POINTS[0]

        snapshot = {
            'type': 'snapshot',
            'players': [{'id': k, 'x': v.rect.x, 'y': v.rect.y, 'hp': v.hp, 'state': v.state, 'alive': v.alive} for k, v in players.items()]
        }
        for addr in addrs:
            server.sendto(json.dumps(snapshot).encode(), addr)
            
        time.sleep(1/SERVER_TICKRATE)

if __name__ == "__main__":
    main()