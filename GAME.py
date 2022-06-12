import pygame
from player import Player
from enemies import *
import tkinter
from tkinter import messagebox
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# définit les couleurs du jeux
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Game(object):
    def __int__(self):
        self.font = pygame.font.Font(None, 40)
        self.about = False
        self.game_over = True
        # crée la variable pour le score
        self.score = 0
        # crée la police d'affichage du score à l'écran
        self.font = pygame.font.Font(None, 35)
        # crée le menu du jeu
        self.menu = Menu(("Start", "A propos", "Exit"), font_color=WHITE, font_size=60)
        # crée le personnage du joueur
        self.player = Player(32, 128, "player.png")
        # crée les blocs qui définiront les chemins où le joueur peut aller
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # crée un groupe de points à l'écran
        self.dots_group = pygame.sprite.Group()
        # définit l'environnement
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))
        # création des fantômes
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Fantome(288, 96, 0, 2))
        self.enemies.add(Fantome(288, 320, 0, -2))
        self.enemies.add(Fantome(544, 128, 0, 2))
        self.enemies.add(Fantome(32, 224, 0, 2))
        self.enemies.add(Fantome(160, 64, 2, 0))
        self.enemies.add(Fantome(448, 64, -2, 2))
        self.enemies.add(Fantome(640, 448, 2, 0))
        self.enemies.add(Fantome(448, 320, 2, 0))
        # ajoute des points sur le terrain de jeu
        for i, row in enumerate(enviroment()):
            for j in item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12, i*32+12, WHITE, 8, 8))
        # charge les effets sonores
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.pacman_sound = pygame.mixer.Sound("game_over_sound.ogg")

    def process_event(self):
        for event in pygame.event.get():
            # detections des actions du joueur
            if event.type == pygame.QUIT:
                # si le joueur a cliqué sur quitter proposer le choix entre START, A PROPOS, QUITTER
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START --------
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- A PROPOS ------
                            self.about = True
                        elif self.menu.state == 2:
                            # --- QUITTER -------
                            # User Clicked exit
                            return True
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False
            elif event.type






