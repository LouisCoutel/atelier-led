from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image
from scipy.ndimage import gaussian_filter
from typing_extensions import Generator

from api.effets import Effet

RESSOURCES = Path("./ressources")
SPRITES = RESSOURCES / "sprites"
TEXTURES = RESSOURCES / "textures"


class Animation(ABC):
    @abstractmethod
    def generer(self, duree, limites) -> Generator[Image.Image, None, None]:
        pass


class CouleurUnie(Animation):
    """Une couleur unie à utiliser en arriere plan"""

    def __init__(self, couleur: str | tuple[int, int, int]):
        self.couleur = couleur

        print("Animation de couleur unie créée.")

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
    """Un clignotement stroboscopique entre deux couleurs"""

    def __init__(
        self,
        vitesse: int,
        couleur_1: str | tuple[int, int, int],
        couleur_2: str | tuple[int, int, int] = "BLACK",
    ):
        self.couleur_1 = couleur_1
        self.couleur_2 = couleur_2
        self.vitesse = vitesse

        print("Animation stroboscopique créée.")

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


class Radial(Animation):
    """Des cercles de couleurs qui s'étendent"""

    def __init__(
        self,
        couleurs: list[tuple[int, int, int]],
        inverse: bool = False,
    ):
        self.inverse = inverse
        self.couleurs = couleurs
        self.couleurs_etendues = _couleurs_etendues(self.couleurs)

        print("Animation radiale créée.")

    def generer(self, duree: int, limites: tuple[int, int]):
        dir = 1 if self.inverse else -1
        matrice_originelle = self._creer_matrice(limites)

        n_etapes = 24 * duree
        etape = 0

        while etape < n_etapes:
            matrice = v_shift(matrice_originelle, dir * (etape / 40), 1.0)
            stops = _stops(self.couleurs)
            pixels = _appliquer_couleurs(
                self.couleurs_etendues, stops, matrice
            )
            image = Image.fromarray(pixels)

            yield image
            etape += 1

    def _creer_matrice(self, limites: tuple[int, int]) -> NDArray:
        y_coords, x_coords = np.ogrid[0 : limites[1], 0 : limites[0]]
        arr = np.sqrt(
            ((x_coords - (limites[0] - 1) / 2) ** 2)
            + ((y_coords - (limites[1] - 1) / 2) ** 2)
        )
        arr /= arr.max()

        arr = gaussian_filter(arr, sigma=3)
        arr = np.power(arr, 0.9)

        return arr.astype(np.float16)


class Sprites(Animation):
    """Une série d'images affichées successivement,
    en y appliquant éventuellement des effets.
    Les effets sont tous appliqués à chaque sprite"""

    def __init__(self, nom_dossier: str):
        self.effets = []

        dossier = SPRITES / nom_dossier
        fichiers = dossier.iterdir()

        self.sprites = [Image.open(fichier) for fichier in fichiers]

        print("Animation de sprites créée")

    def ajouter_effet(self, effet: Effet):
        self.effets.append(effet)

    def generer(self, duree: int, limites: tuple[int, int]):
        """Applique les effets et renvoie l'image finale au player
        pour chaque frame de l'animation."""

        n_etapes = 24 * duree
        etape = 0

        while etape < n_etapes:
            image = self._appliquer_effets(etape)
            etape += 1

            yield image

    def _appliquer_effets(self, etape: int) -> Image.Image:
        numero_sprite = etape % len(self.sprites)
        sprite = self.sprites[numero_sprite]

        for effet in self.effets:
            sprite = effet.appliquer(sprite, etape)

        return sprite


class Texture(Animation):
    def __init__(self, nom_fichier: str, couleurs: list[tuple[int, int, int]]):
        self.effets = []
        self.couleurs = np.array(couleurs)

        fichier = TEXTURES / nom_fichier
        nouvelle_taille = (256, 256)

        texture = Image.open(fichier).convert("L")
        texture = texture.resize(nouvelle_taille)

        matrice = np.array(texture.getdata()) / 100.0

        stops = _exp_stops(self.couleurs, 0.7)

        pixels = _appliquer_couleurs(self.couleurs, stops, matrice)
        pixels = pixels.reshape((nouvelle_taille[0], nouvelle_taille[1], 3))

        self.texture = Image.fromarray(pixels)

        print("Animation de texture créée")

    def ajouter_effet(self, effet: Effet):
        self.effets.append(effet)

    def generer(self, duree: int, limites: tuple[int, int]):
        """Applique les effets et renvoie l'image finale au player
        pour chaque frame de l'animation."""

        n_etapes = 24 * duree
        etape = 0

        while etape < n_etapes:
            image = self._appliquer_effets(etape, limites)

            etape += 1

            yield image

    def _appliquer_effets(
        self, etape: int, limites: tuple[int, int]
    ) -> Image.Image:
        image = self.texture

        for effet in self.effets:
            image = effet.appliquer(image, etape)

        return image


def shift(n: float, x: float, max: float) -> float:
    return (n + x) % max


v_shift = np.vectorize(shift)


def _couleurs_etendues(couleurs) -> NDArray:
    return np.vstack([couleurs, couleurs[0]])


def _stops(couleurs) -> NDArray:
    return np.linspace(0, 1, couleurs.shape[0])


def _exp_stops(couleurs, facteur) -> NDArray:
    return np.power(np.linspace(0, 1, couleurs.shape[0]), facteur)


def _appliquer_couleurs(couleurs, stops, matrice: NDArray) -> NDArray:
    return np.stack(
        [
            np.interp(
                matrice,
                stops,
                couleurs[:, c],
            )
            for c in range(3)
        ],
        axis=-1,
    ).astype(np.uint8)
