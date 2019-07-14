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
WARNING_ANIM = ["HUD\\infectedAnim\\Sprite-0002.png", "HUD\\infectedAnim\\Sprite-0003.png", "HUD\\infectedAnim\\Sprite-0004.png", "HUD\\infectedAnim\\Sprite-0005.png", "HUD\\infectedAnim\\Sprite-0006.png", "HUD\\infectedAnim\\Sprite-0007.png", "HUD\\infectedAnim\\Sprite-0008.png"]
WARNING_FRAMES = 5
WARNING_DURATION = 6
INFECTED_BANNER = "hud\\infectedBanner.png"
LEVEL_BANNER = "HUD\\LevelBanner.png"


#how far off bullet is from player
BULLET_OFFSET = vec(30, 0)

#mobs
MOB_IMAGE = 'mobs\\zombie01_normal.png'
MOB_SPEEDS =  [250,290]#[190, 160, 95, 125, 130, 180, 150, 150, 150]
MOB_HIT_BOX = pg.Rect(0,0,35,40)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 15
INFECTION_CHANCE = 20 #change of player being infected DEFAULT 1/10
INFECTION_TIME = 2000
AVOiD_RADIUS = 50

#items
ANTIDOTE_IMAGE = 'items\\antidote.png'
MEDKIT_IMAGE = 'items\\medkit.png'
MEDKIT_BOOST = 50

#DROPS
TOTAL_CHANCE = 20 #total chance, chance of all items - total_chance = chance nothing drops. Must be greated than sum of all items chance
ITEM_DROP_CHANCES = {'antidote': 2, 'medkit': 4}


#Vinyl
VINYL_IMAGES = ["misc\\vinyl\\vinyl1.png", "misc\\vinyl\\vinyl2.png", "misc\\vinyl\\vinyl3.png", "misc\\vinyl\\vinyl4.png", "misc\\vinyl\\vinyl5.png"]
VINYL_DISC_IMAGES = ["misc\\vinylDisc\\strVinyl01.png", "misc\\vinylDisc\\strVinyl09.png", "misc\\vinylDisc\\strVinyl02.png", "misc\\vinylDisc\\strVinyl03.png", "misc\\vinylDisc\\strVinyl04.png","misc\\vinylDisc\\strVinyl07.png","misc\\vinylDisc\\strVinyl10.png", "misc\\vinylDisc\\strVinyl08.png"]
VINYL_DURATION = 2
VINYL_ROTATE_SPEED = 2

#LEVELS
LEVEL_1_STAGES = 5
MAX_ZOMBIES = 70
LEVEL_ADD = 3 #ammount of zombies added every level
LEVEL_1_ZOMBIESAMMOUNT = 10
