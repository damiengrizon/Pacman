# Cette section contient les nombreux modules de fonction qui font partie du jeu.

import pygame

from JOUEUR import Player
from FANTOMES import *

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
                    self.horizontal_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
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
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))
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

            elif event.type == pygame.K_UP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            # Lorsque le block_hit_list contient un sprite, cela signifie que le joueur à touché un point
            if len(block_hit_list) > 0:
                # declenchement de l'effet sonor
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)
            # tkMessageBox.showinfo("GAME OVER!", "Score final = " + str(Game.score))

    def display_frame(self, screen):
        # Tout d'abord effacez l'écran. N'y mettez pas d'autres commandes de dessins
        screen.fill(BLACK)
        # --- Le code pour dessiner le terrain de jeu vient ici
        if self.game_over:
            if self.about:
                self.display_message(screen, "C'est un jeu d'arcade"
                                             "un labyrinthe contenant divers points,\n"
                                             "connu sous le nom de Pac-Dots, et quatre fantômes.\n"
                                             "les quatre fantômes parcourent le labyrinthe, essayant de tuer Pac-Man.\n"
                                             "Si l'un des fantômes frappe Pac-Man, il perd une vie ;\n"
                                             "le jeu est terminé.\n")
            else:
                self.menu.display_frame(screen)
        else:
            # --- Dessin du terrain de jeu ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            text = self.font.render("Score : " + str(self.score), True, RED)
            screen.blit(text, (30, 650))
            # affiche le texte du score
            text = self.font.render("Score : " + str(self.score), True, GREEN)
            # dessine le texte à l'écran
            screen.blit(text, [120, 20])
        # --- met à jour ce que nous avons dessiné.
        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 0, 5)):
        label = self.font.render(message, True, color)
        # obtenir la largeur de l'étiquette
        width = label.get_width()
        height = label.get_height()
        # détermine la position de l'étiquette
        pos_x = (SCREEN_WIDTH / 2)(width / 2)
        pos_y = (SCREEN_HEIGHT / 2)(height / 2)
        # dessine l'étiquette à l'écran
        screen.blit(label, (pos_x, pos_y))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)
            width = label.get_width()
            height = label.get_height()
            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h : total height of text block
            t_h = len(self.items) * height
            pos_y = (SCREEN_HEIGHT / 2) - (t_h / 2) + index * height
            screen.blit(label, (pos_x, pos_y))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.KEYDOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
