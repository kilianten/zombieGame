import pygame as pg
from settings import *
from map import collide_hit_box

vec = pg.math.Vector2

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

    def collide_with_walls(self, dir):
        #checkCollision serpately
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_box)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_box.width/2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_box.width/2
                self.vel.x = 0
                self.hit_box.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_box)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_box.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_box.height/2
                self.vel.y = 0
                self.hit_box.centery = self.pos.y


    def update(self):
        #get keys pressed
        self.get_keys()
        #rotate player
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        #rotate image
        self.image = pg.transform.rotate(self.game.playerImage, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_box.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_box.centery = self.pos.y
        self.collide_with_walls('y')


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_image
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        #find the angle between player and x axis i.e where zombie needs to look
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


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
