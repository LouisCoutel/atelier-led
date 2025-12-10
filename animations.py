from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from effets import Effet
from images import Sprite


RESOURCES = Path("./resources")


class Animation(ABC):
    @abstractmethod
    def generer(self, duree, limites):
        pass


class CouleurUnie(Animation):
    """Une couleur unie à utiliser en arriere plan"""

    def __init__(self, couleur: str | tuple[int, int, int]):
        self.couleur = couleur

    def generer(self, duree: int | None, limites: tuple[int, int]):
        """Crée une nouvelle image et la donne au player
        pour chaque frame de l'animation.
        """

        image = Image.new(mode="RGBA", size=limites, color=self.couleur)
        n_etapes = 24 * duree if duree else None
        etape = 0
        while True:
            if n_etapes is not None:
                if etape == n_etapes:
                    break
            yield image
            etape += 1


class Strobe(Animation):
    def __init__(
        self,
        vitesse: int,
        couleur_1,
        couleur_2: str | tuple[int, int, int] = "BLACK",
    ):
        self.couleur_1 = couleur_1
        self.couleur_2 = couleur_2
        self.vitesse = vitesse

    def generer(self, duree: int | None, limites: tuple[int, int]):
        image_1 = Image.new(mode="RGBA", size=limites, color=self.couleur_1)
        image_2 = Image.new(mode="RGBA", size=limites, color=self.couleur_2)
        n_etapes = 24 * duree if duree else None
        etape = 0
        while True:
            if n_etapes is not None:
                if etape == n_etapes:
                    break
            a_afficher = (
                image_1
                if (etape % self.vitesse) < self.vitesse / 2
                else image_2
            )
            yield a_afficher
            etape += 1


class SpriteAnimee(Animation):
    """Une animation consiste en une série de sprites à afficher,
    en y appliquant éventuellement des effets.
    Les sprites sont jouées dans l'ordre d'ajout.
    Les effets sont tous appliqués à chaque sprite"""

    def __init__(
        self,
        nom: str,
    ):
        self.nom = nom
        self.effets = []
        self.sprites = []
        self.frames = []

    def ajouter_effet(self, effet: Effet):
        self.effets.append(effet)

    def ajouter_sprite(self, sprite: Sprite):
        self.sprites.append(sprite)

    def ajouter_serie(self, nom_dossier: str):
        """Ajouter toutes les sprites d'un dossier correspondant à un mouvement
        (courir, sauter...)"""
        dossier = RESOURCES / nom_dossier
        fichiers = dossier.iterdir()

        self.sprites = [Sprite(fichier) for fichier in fichiers]

    def generer(self, duree: int | None, limites: tuple[int, int]):
        """Applique les effets et renvoie l'image finale au player
        pour chaque frame de l'animation."""

        n_etapes = 24 * duree if duree else None
        etape = 0
        while True:
            if n_etapes is not None:
                if etape == n_etapes:
                    break

            image = self._appliquer_effets(etape)
            yield image
            etape += 1

    def _appliquer_effets(self, etape: int):
        numero_sprite = etape % len(self.sprites)
        sprite = self.sprites[numero_sprite]

        image = Image.open(sprite.fichier)
        for effet in self.effets:
            image = effet.appliquer(image, etape)

        return image
