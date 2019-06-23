import pygame as pg
from random import uniform
from settings import *
from map import collide_hit_box

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    #checkCollision serpately
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_box.width/2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_box.width/2
            sprite.vel.x = 0
            sprite.hit_box.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_box.height/2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_box.height/2
            sprite.vel.y = 0
            sprite.hit_box.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.playerImage
        self.rect = self.image.get_rect()
        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.shooting = False
        self.gunEquipped = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_DOWN]:
            self.vel = vec(-playerSpeed/2, 0).rotate(-self.rot)
        if keys[pg.K_UP]:
            self.vel = vec(playerSpeed, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1,0).rotate(-self.rot)
                #so bullet spawns from gun not center of player
                pos = self.pos + BULLET_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir, self.rot)
                self.shooting = True
                #kickback
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
        else:
            self.shooting = False;

    def update(self):
        if self.shooting:
            curr_image = self.game.player_shooting
        else:
            curr_image = self.game.playerImage
        #get keys pressed
        self.get_keys()
        #rotate player
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        #rotate image
        self.image = pg.transform.rotate(curr_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_image
        self.rect = self.image.get_rect()
        #copy of once in settings
        self.hit_box = MOB_HIT_BOX.copy()
        self.hit_box_center = self.rect.center
        self.pos = vec(x,y) * TILESIZE
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        #find the angle between player and x axis i.e where zombie needs to look
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel *-1
        self.vel += self.acc * self.game.dt
        #equation of motion
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt**2
        #mob collision
        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        #after collision regular rect set to where hitbox is after collision
        self.rect.center = self.hit_box.center

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.bullet_image, rot)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        #innaccuracy
        spread = uniform (-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
