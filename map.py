import pygame as pg
import pytmx
from settings import *

def collide_hit_box(one, two):

    return one.hit_box.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x,y,gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x* self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        #limit mapsize scrolling
        x = min(0,x) #left
        y = min(0,y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x,y, self.height, self.width)

class Level:
    def __init__(self, game, numberOfLevels, zombiesPerLevel):
        self.numberOfLevels = 1
        self.zombiesPerLevel = zombiesPerLevel
        self.startLevel = zombiesPerLevel
        self.game = game

    def update(self):
        if self.zombiesPerLevel <= 0 and len(self.game.mobs) <= 0:
            #display new level
            self.startLevel += LEVEL_ADD #increase number of zombies every level
            self.zombiesPerLevel = self.startLevel
            self.numberOfLevels += 1
            self.game.isNewLevel = True
            self.game.effects_sounds['level_start'].play()
            self.game.levelHUDImage = 0
            for blood in self.game.blood:
                blood.kill()
