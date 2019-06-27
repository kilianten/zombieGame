import pygame as pg
vec = pg.math.Vector2

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
PLAYER_HEALTH = 100
playerSpeed = 300
playerImage = "player\\Rich.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_BOX = pg.Rect(0,0,35,40)
PLAYER_SHOOTING = "player\\richShooting.png"


#gun settings
BULLET_IMAGE = "weapons\\bullet.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 100
GUN_SPREAD = 5
GUN_OFFSET = 0
PISTOL_IMAGE = "weapons\\handgun.png"
PISTOL_DAMAGE = 10

#HUD
HEALTH_BAR_OVERLAY = "HUD\\healthBar.png"
BAR_LENGTH = 150
BAR_HEIGHT = 20
WARNING_ANIM = 'hud\\infectedAnim\\'
WARNING_FRAMES = 5
WARNING_DURATION = 6
INFECTED_BANNER = "hud\\infectedBanner.png"


#how far off bullet is from player
BULLET_OFFSET = vec(30, 0)

#mobs
MOB_IMAGE = 'mobs\\zombie01_normal.png'
MOB_SPEEDS = [150, 100, 75, 125, 130, 160, 150, 150, 150]
MOB_HIT_BOX = pg.Rect(0,0,35,40)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 15
INFECTION_CHANCE = 20 #change of player being infected DEFAULT 1/10
INFECTION_TIME = 2000
AVOiD_RADIUS = 50

#items
ANTIDOTE_IMAGE = 'items\\antidote.png'

#DROPS
SPAWN_CHANCE_TOTAL = 100
SPAWN_CHANCE_ANTIDOTE = 5
