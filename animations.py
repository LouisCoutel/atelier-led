from abc import ABC, abstractmethod
import logging
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

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

    def generer(self, duree: int, limites: tuple[int, int]):
        """Crée une nouvelle image et la donne au player
        pour chaque frame de l'animation.
        """

        image = Image.new(mode="RGBA", size=limites, color=self.couleur)
        n_etapes = 24 * duree
        etape = 0

        while etape < n_etapes:
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

    def generer(self, duree: int, limites: tuple[int, int]):
        image_1 = Image.new(mode="RGBA", size=limites, color=self.couleur_1)
        image_2 = Image.new(mode="RGBA", size=limites, color=self.couleur_2)
        n_etapes = 24 * duree
        etape = 0
        while etape < n_etapes:
            a_afficher = (
                image_1
                if (etape % self.vitesse) < self.vitesse / 2
                else image_2
            )
            yield a_afficher
            etape += 1


def shift(n: float, x: float, max: float) -> float:
    return (n + x) % max


v_shift = np.vectorize(shift)


class Radial(Animation):
    def __init__(self, couleurs):
        self.couleurs = couleurs

    @property
    def couleurs_etendues(self):
        return np.vstack([self.couleurs, self.couleurs[0]])

    @property
    def division_couleurs(self):
        return np.linspace(0, 1, self.couleurs_etendues.shape[0])

    def generer(self, duree: int, limites: tuple[int, int]):
        matrice_originelle = self._creer_matrice(limites)

        n_etapes = 24 * duree
        logging.warning(n_etapes)
        etape = 0

        while etape < n_etapes:
            matrice = v_shift(matrice_originelle, etape / 40, 1.0)
            pixels = self._appliquer_couleurs(matrice)
            image = Image.fromarray(pixels, "RGB")
            logging.warning(etape)

            yield image
            etape += 1

    def _appliquer_couleurs(self, matrice):
        return np.stack(
            [
                np.interp(
                    matrice,
                    self.division_couleurs,
                    self.couleurs_etendues[:, c],
                )
                for c in range(3)
            ],
            axis=-1,
        ).astype(np.uint8)

    def _creer_matrice(self, limites: tuple[int, int]):
        y_coords, x_coords = np.ogrid[0 : limites[1], 0 : limites[0]]
        arr = np.sqrt(
            ((x_coords - (limites[0] - 1) / 2) ** 2)
            + ((y_coords - (limites[1] - 1) / 2) ** 2)
        )
        arr /= arr.max()

        arr = gaussian_filter(arr, sigma=3)
        arr = np.power(arr, 0.9)

        return arr.astype(np.float16)


class TextureAnimee(Animation):
    def __init__(self, nom: str, couleurs) -> None:
        self.nom = nom
        self.effets = []
        self.couleurs = couleurs


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

    def generer(self, duree: int, limites: tuple[int, int]):
        """Applique les effets et renvoie l'image finale au player
        pour chaque frame de l'animation."""

        n_etapes = 24 * duree
        etape = 0
        while etape < n_etapes:
            image = self._appliquer_effets(etape)

            etape += 1
            logging.warning(etape)
            logging.warning(etape < n_etapes)
            yield image

    def _appliquer_effets(self, etape: int):
        numero_sprite = etape % len(self.sprites)
        sprite = self.sprites[numero_sprite]

        image = Image.open(sprite.fichier)
        for effet in self.effets:
            image = effet.appliquer(image, etape)

        return image
