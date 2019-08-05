import pygame as pg
from random import *
from settings import *
from map import collide_hit_box
import pytweening as tween;

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    #checkCollision serpately
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if hits[0].rect.centerx > sprite.hit_box.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_box.width/2
            if hits[0].rect.centerx < sprite.hit_box.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_box.width/2
            sprite.vel.x = 0
            sprite.hit_box.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if hits[0].rect.centery > sprite.hit_box.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_box.height/2
            if hits[0].rect.centery < sprite.hit_box.centery:
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
        self.rect.center = (x,y)
        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        self.rot = 0
        self.last_shot = 0
        self.shooting = False
        self.gunEquipped = 0
        self.health = PLAYER_HEALTH
        self.infected = False
        self.infection_time = 0
        self.itemSelected = "trap"
        self.inventory = {"trap": 2}
        self.isPlacing = False #to check if player has released placing key

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
                choice(self.game.weapon_sounds['gunshot']).play()
                self.shooting = True
                #kickback
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
        else:
            self.shooting = False;
        if keys[pg.K_q]:
            self.isPlacing = True #playing is trying to place
        if keys[pg.K_q] == False and self.isPlacing == True:
            dir = vec(1,0).rotate(-self.rot)
            #so bullet spawns from gun not center of player
            pos = self.pos + ITEM_SPAWN_OFFSET.rotate(-self.rot)
            self.isPlacing = False
            self.game.canPlace(self.game, self.game.trap_image, pos, dir, self.rot)





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
        if self.infected:
            self.infection_time += 1

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #copy of once in settings
        self.hit_box = MOB_HIT_BOX.copy()
        self.hit_box_center = self.rect.center
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH + randint(-20,20)
        self.speed =  choice(MOB_SPEEDS)
        self.isTrapped = False;

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self: #dont count self
                dist = self.pos - mob.pos #distance betweem two mobs
                if 0 < dist.length() < AVOiD_RADIUS:
                    self.acc += dist.normalize()

    def drop_items(self, game, pos): #decides what/if item drops
        counter = 1
        rand = randint(1, TOTAL_CHANCE) #random number from 0 - total chance
        for key, value in ITEM_DROP_CHANCES.items():
            if value >= rand:
                print(key)
                print(rand)
                Item(game, pos, key)
                return

    def update(self):
        if random() < 0.0004:
            choice(self.game.zombie_grunt_sounds).play()
        if not self.isTrapped: #if not trapped move
            #find the angle between player and x axis i.e where zombie needs to look
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.mob_image, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            #avoid fellow MOB_SPEED
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
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

        if self.health <= 0:
            self.kill()
            self.drop_items(self.game, self.pos)
            self.game.zombieSplat.play()
            BloodSplat(self.game, self.pos)
            '''fromTotal = randint(0,SPAWN_CHANCE_TOTAL)
            if SPAWN_CHANCE_ANTIDOTE >= fromTotal:
                Item(self.game, self.pos, 'antidote')'''

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.bullet_image, rot)
        self.rect = self.image.get_rect()
        self.hit_box = self.rect
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
        self.groups = game.all_sprites, game.walls, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if type == "antidote":
            self.image = game.antidote_image
        elif type == "medkit":
            self.image= game.medkit_image
        elif type == "traps":
            self.image= game.trap_icon_image
        self.type = type
        self.rect = self.image.get_rect()
        self.hit_box = self.rect
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine; #tweening import
        self.step = 0
        self.dir = 1 #direction of bob

    def update(self):
        #bob motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Animation():
    def __init__(self, game, frames, duration):
        self.limit = frames
        self.current_Frame = 0
        self.animations = game.infected_anim
        self.animation = self.animations[0]
        self.counter = 0
        self.duration = duration

    def update(self):
        if self.counter == self.duration:
            self.current_Frame += 1
            self.animation = self.animations[self.current_Frame]
            if self.current_Frame >= self.limit:
                self.current_Frame = 0
            self.counter = 0
        else:
            self.counter += 1

class Vinyl(pg.sprite.Sprite):
    def __init__(self, game, pos, duration):
        self.groups = game.all_sprites, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.vinyl_anim[0]
        self.animation = game.vinyl_anim
        self.disc_image_num = 0
        self.image_vinyl = game.vinyl_disc_anim[self.disc_image_num]
        #self.secondImage = game.vinyl_one
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.hit_box = self.rect
        self.pos = vec(pos)
        self.isPlayingVinyl = False
        self.counter = 0
        self.curr_image = 0
        self.duration = 200
        self.game = game
        self.playedVinyl = False


    def update(self):
        if self.playedVinyl == True:
            self.counter += 2
            if self.counter % (VINYL_ROTATE_SPEED * 10) == 0:
                if self.disc_image_num == len(self.game.vinyl_disc_anim):
                    self.disc_image_num = 0
                self.image_vinyl = self.game.vinyl_disc_anim[self.disc_image_num]
                self.disc_image_num += 1
        if self.isPlayingVinyl:
            self.playedVinyl = True
            if self.counter == self.duration:
                if self.curr_image < len(self.animation):
                    self.curr_image = 3
                self.curr_image += 1
                self.image = self.animation[self.curr_image]
                self.counter = 0
                if self.curr_image == len(self.animation) - 2:
                    self.isPlayingVinyl = False

class Spacer(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self.game = game
        self.image = pg.transform.rotate(game.trap_image, rot)
        self.rect = self.image.get_rect()
        self.hit_box = self.rect
        self.pos = vec(pos)
        self.rect.center = pos

class BearTrap(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self.groups = game.all_sprites, game.traps, game.notPlacable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.trap_image, rot)
        self.rect = pg.Rect(pos.x, pos.y, 2 , 2) #hitbox at center of trap
        self.hit_box = self.rect
        self.pos = vec(pos)
        self.rect.center = pos

class BloodSplat(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.blood
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_blood
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
