import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106,55,5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN


TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMAGE = 'structures\\wall.png'
KITCHEN_TILE_IMAGE = 'structures\\kitchenTile.png'

#player settings
playerSpeed = 300
playerImage = "player\\Rich.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_BOX = pg.Rect(0,0,35,40)

#mobs
MOB_IMAGE = 'mobs\\zombie01_normal.png'
MOB_SPEED = 150
