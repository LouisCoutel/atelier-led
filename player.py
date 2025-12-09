import logging
from affichage import Affichage

from ddp import stream_ddp
from images import Animation


class Player:
    def __init__(self, ip: str) -> None:
        self.affichage = Affichage(ip)
        logging.warning(self.affichage.largeur)
        logging.warning(self.affichage.hauteur)

    def jouer(self, animation: Animation):
        playlist = animation.generer(
            30, (self.affichage.largeur, self.affichage.hauteur)
        )
        stream_ddp(
            playlist=playlist,
            affichage=self.affichage,
        )
