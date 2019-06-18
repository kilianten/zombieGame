import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from map import *

class Game:

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
        self.map = Map (path.join(game_folder, 'map.txt'))
        self.playerImage = pg.image.load(path.join(imageFolder, playerImage)).convert_alpha()
        self.mob_image = pg.image.load(path.join(imageFolder, MOB_IMAGE)).convert_alpha()
        self.wall_image = pg.image.load(path.join(imageFolder, WALL_IMAGE)).convert_alpha()
        #self.kitchenTileImage = pg.image.load(path.join(imageFolder, KITCHEN_TILE_IMAGE)).convert_alpha()


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'Z':
                    self.mob = Mob(self, col, row)
                #if tile == 'K':
                    #self.screen.blit(self.kitchenTileImage, (col, row))
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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.devMode:
                pg.draw.rect(self.screen, GREEN, self.player.hit_box, 2)
                positionText = self.myfont.render('X: ' + '{0:.2f}'.format(self.player.pos.x) + ("     ") + 'Y: ' + '{0:.2f}'.format(self.player.pos.y) , False, (0, 0, 0))
                FPSText = self.myfont.render("{:.2f}".format(self.clock.get_fps()), False, (0, 0, 0))

                self.screen.blit(positionText, (0,0))
                self.screen.blit(FPSText, (0,20))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SLASH:
                    if self.devMode:
                        self.devMode = False
                    else:
                        self.devMode = True

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
