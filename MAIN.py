# Cette section contient le module principale du programme et fait le lien avec le reste des modules
import pygame

import GAME
from GAME import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


def main():
    # initialisation de tous les modules pygame importés
    pygame.init()
    # definit la largeur et la hauteur de l'écran [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # définit le titre de la fenètre du jeu
    pygame.display.set_caption("PACMAN")
    # Boucle jusqu'à ce que le joueur clique sur le bouton de fermeture
    done = False
    # Utilise pour gérer la vitesse de la mise à jour de l'écran
    clock = pygame.time.Clock()
    # crée un élément du jeu
    game = Game()
    # ------ Boucle de jeu principale -------
    while not done:
        # traite les évènements (frappe du clavier, clics de souris, etc.)
        done = game.process_event()
        # la logique du jeu vient ici
        game.run_logic()
        # dessine l'écran du jeu
        game.display_frame(screen)
        # limite la vitesse d'affichage à 30 images par seconde
        clock.tick(30)
        # tkMessageBox.showinfo("GAME OVER!", "Score final = " + str(GAME.Score))
        # ferme la fenêtre et quitte
        # Si vous oubliez cette ligne le programme se bloquera
        # A la sortie si vous exécutez el programme à partir de l'IDLE
        pygame.quit()
        if __name__ == '__main__':
            main()
