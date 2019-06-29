import pygame as pg
import sys
import glob
import random
from os import path
from settings import *
from sprites import *
from map import *


#HUD display
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    #change color depending on health status
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:

    def load_Anim(self, imageFolder, images):
        animation = []
        images = sorted(images) #make sure list is in alphabetic order
        for frame in images:
            loadedImage = pg.image.load(path.join(imageFolder, frame))
            animation.append(loadedImage)
        #imageFiles = glob.glob(path.join(imageFolder, image_path) + "*")
        #for frame in imageFiles:
            #animation.append(pg.image.load(frame).convert_alpha())
        return animation

    def __init__(self):
        pg.init()
        pg.font.init()
        self.myfont = pg.font.SysFont('Arial Header', 25)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.devMode = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        imageFolder = path.join(game_folder, 'images')
        mapFolder = path.join(game_folder, 'maps')
        self.map = TiledMap (path.join(mapFolder, 'basicLevel.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.playerImage = pg.image.load(path.join(imageFolder, playerImage)).convert_alpha()
        self.bullet_image = pg.image.load(path.join(imageFolder, BULLET_IMAGE)).convert_alpha()
        self.mob_image = pg.image.load(path.join(imageFolder, MOB_IMAGE)).convert_alpha()
        self.wall_image = pg.image.load(path.join(imageFolder, WALL_IMAGE)).convert_alpha()
        self.player_shooting = pg.image.load(path.join(imageFolder, PLAYER_SHOOTING)).convert_alpha()
        self.health_overlay = pg.image.load(path.join(imageFolder, HEALTH_BAR_OVERLAY)).convert_alpha()
        self.antidote_image = pg.image.load(path.join(imageFolder, ANTIDOTE_IMAGE)).convert_alpha()
        self.infected_anim = self.load_Anim(imageFolder, WARNING_ANIM)
        self.infected_banner = pg.image.load(path.join(imageFolder, INFECTED_BANNER)).convert_alpha()
        self.medkit_image = pg.image.load(path.join(imageFolder, MEDKIT_IMAGE)).convert_alpha()
        self.vinyl_anim = self.load_Anim(imageFolder, VINYL_IMAGES)
        self.vinyl_disc_anim = self.load_Anim(imageFolder, VINYL_DISC_IMAGES)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.warningAnim = Animation(self, WARNING_FRAMES, WARNING_DURATION)
        for tile_object in  self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wallVinyl':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.vinyl = Vinyl(self, (tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2), VINYL_DURATION * 10)
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        #mobs hit  player collide
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_box)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
            randomNumber = randint(0, INFECTION_CHANCE)
            if randomNumber == INFECTION_CHANCE: #if from 0 - NUMBER = NUMBER, then infect
                self.player.infected = True
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        #bullet hits mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= PISTOL_DAMAGE
            hit.vel = vec(0,0)

        #PlayVINYL
        collisionHappened = pg.sprite.collide_rect(self.player, self.vinyl)
        if collisionHappened:
            self.vinyl.isPlayingVinyl = True
        #if player hits item
        hits = pg.sprite.spritecollide(self.player, self.items, True, collide_hit_box)
        for hit in hits:
            if hit.type == 'antidote':
                self.player.infected = False
                self.player.infection_time = 0
            if hit.type == 'medkit':
                if self.player.health + MEDKIT_BOOST > PLAYER_HEALTH:
                    self.player.health = PLAYER_HEALTH
                else:
                    self.player.health += MEDKIT_BOOST

        if self.player.infected == True:
            self.warningAnim.update()
            if self.player.infection_time == INFECTION_TIME:
                print("infected: game over")
                self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.screen.fill(BGCOLOR)
        #self.draw_grid()          
        for sprite in self.all_sprites:
            if isinstance(sprite, Vinyl) and sprite.playedVinyl:
                self.screen.blit(sprite.image_vinyl, self.camera.apply(sprite))
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.devMode:
                if isinstance(sprite, Player):
                    pg.draw.rect(self.screen, GREEN, self.camera.apply_rect(sprite.hit_box),1)
                elif isinstance(sprite, Mob):
                    pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_box), 1)
                elif isinstance(sprite, Bullet):
                    pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(sprite.hit_box), 1)
        #devmode
        if self.devMode:
            positionText = self.myfont.render('X: ' + '{0:.2f}'.format(self.player.pos.x) + ("     ") + 'Y: ' + '{0:.2f}'.format(self.player.pos.y) , False, (0, 0, 0))
            FPSText = self.myfont.render("{:.2f}".format(self.clock.get_fps()), False, (0, 0, 0))
            playerHealthText = self.myfont.render("{:.2f}".format(self.player.health/PLAYER_HEALTH), False, (0, 0, 0))
            infectionText = self.myfont.render('Infection Level: ' + '{}'.format(self.player.infection_time) , False, (0, 0, 0))

            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)

            self.screen.blit(positionText, (0,0))
            self.screen.blit(FPSText, (0,20))
            self.screen.blit(playerHealthText, (0,40))
            self.screen.blit(infectionText, (0,60))
        #HUD FUNCTIoNS
        #if player is infected, draw infected warning
        if self.player.infected == True:
            self.screen.blit(self.warningAnim.animation, (100,10))
            self.screen.blit(self.infected_banner, (170, 10))
        draw_player_health(self.screen, WIDTH - BAR_LENGTH - 10, 10, self.player.health/PLAYER_HEALTH)
        self.screen.blit(self.health_overlay, (WIDTH - BAR_LENGTH - 10, 10))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SLASH:
                    self.devMode = not self.devMode

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
