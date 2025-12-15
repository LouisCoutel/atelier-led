import colorsys
from abc import ABC, abstractmethod
import logging
from _deformers import WaveDeformer
import numpy as np
from PIL import Image, ImageOps, ImageChops


class Effet(ABC):
    @abstractmethod
    def appliquer(self, image: Image.Image, etape: int):
        pass


class Defilement(Effet):
    def __init__(
        self, duree: int, horizontal: bool, vertical: bool, vitesse: int = 1
    ) -> None:
        """Inverse l'image horizontalement."""

        super().__init__()
        self.duree = duree
        self.horizontal = horizontal
        self.vertical = vertical
        self.vitesse = vitesse

    def appliquer(self, image: Image.Image, etape: int):
        xoffset = self.vitesse * etape if self.horizontal else 0
        yoffset = self.vitesse * etape if self.vertical else 0

        return ImageChops.offset(image, xoffset, yoffset)


class Negatif(Effet):
    def __init__(self, duree: int) -> None:
        """Inverse l'image horizontalement."""

        super().__init__()
        self.duree = duree

    def appliquer(self, image: Image.Image, etape: int):
        image = image.convert("RGB")
        return ImageOps.invert(image)


rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)


class HueShift(Effet):
    def __init__(self, duree: int, vitesse: int = 1) -> None:
        """Inverse l'image horizontalement."""

        super().__init__()
        self.duree = duree
        self.vitesse = vitesse

    def appliquer(self, image: Image.Image, etape: int):
        largeur, hauteur = image.size
        image = image.convert("RGBA")
        donnees = np.array(image.getdata()) / 256
        r, g, b, a = np.rollaxis(donnees, -1)
        h, s, v = rgb_to_hsv(r, g, b)
        shift = (etape + self.vitesse) / 360
        h = h + shift
        h = h % 1

        r, g, b = hsv_to_rgb(h, s, v)
        donnees = np.dstack((r, g, b, a)) * 256
        donnees = donnees.reshape((hauteur, largeur, 4)).astype(np.uint8)

        return Image.fromarray(donnees, "RGBA")


class Mirroir(Effet):
    def __init__(self, duree: int) -> None:
        """Inverse l'image horizontalement."""

        super().__init__()
        self.duree = duree

    def appliquer(self, image: Image.Image, etape: int):
        return ImageOps.mirror(image)


class Redimensionner(Effet):
    def __init__(self, etapes: int, facteur: float, double_sens: bool) -> None:
        """Agrandir ou rapetisser l'image selon un facteur.

        Facteur: nombre par lequel la taille de l'image est multipliée.
        Pour agrandir l'image, il doit être supérieur à 1.
        Pour la rapetisser, inférieur à 1.

        Double_sens: si cette option est activée,
        l'image sera redimensionnée dans un sens (agrandie ou rétrecie)
        puis dans le sens inverse au cours de l'animation.

        Etapes: En combien d'étapes d'animation la déformation maximale est atteinte.
        """

        self.etapes = etapes
        self.facteur = facteur
        self.double_sens = double_sens

    def appliquer(self, image: Image.Image, etape: int = 1):
        nouvelle_hauteur = round(image.width * self.facteur)
        nouvelle_largeur = round(image.height * self.facteur)

        return image.resize(
            (nouvelle_largeur, nouvelle_hauteur), reducing_gap=3.0
        )


class Vague(Effet):
    def __init__(
        self, vertical: bool, horizontal: bool, max: int, etapes: int
    ) -> None:
        """Déformation de l'image en vagues ou ondulations.
        Vertical: active la déformation dans le sens de la hauteur.
        Horizontal: dans le sens de la largeur.
        Max: L'intensité maximale de la déformation
        Etapes: En combien d'étapes d'animation la déformation maximale est atteinte.
        Avec 1, la déformation est instantanée et constante.
        Avec 12, la déformation maximale sera atteinte au bout de 12 frames
        soit 1 seconde.
        """
        self.vertical = vertical
        self.horizontal = horizontal
        self.max = max
        self.etapes = etapes

    def appliquer(self, image: Image.Image, etape: int = 1):
        return ImageOps.deform(
            image, WaveDeformer(x_dir=self.horizontal, y_dir=self.vertical)
        )
