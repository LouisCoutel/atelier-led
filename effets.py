from abc import ABC, abstractmethod
from _deformers import WaveDeformer
from PIL import Image, ImageOps


class Effet(ABC):
    @abstractmethod
    def appliquer(self, image: Image.Image, etape: int):
        pass


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
