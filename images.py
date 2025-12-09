"""Il est possible de créer des affichages à partir d'images.
On peut s'en servir comme textures,
décaler les images pour créer l'illusion d'un déplacement,
faire varier les couleurs ou les distordre."""

import numpy as np
from pathlib import Path

from PIL import Image

from effets import Effet


RESOURCES = Path("./resources")


class Sprite:
    """Une sprite est une image en pixel-art."""

    def __init__(self, fichier):
        self.fichier = fichier
        with Image.open(fichier) as img:
            self.largeur = img.width
            self.hauteur = img.height


def rogner_depuis_centre(
    image: Image.Image, limites: tuple[int, int]
) -> Image.Image:
    img_width, img_height = image.size

    return image.crop(
        (
            (img_width - limites[0]) // 2,
            (img_height - limites[1]) // 2,
            (img_width + limites[0]) // 2,
            (img_height + limites[1]) // 2,
        )
    )


class Frame:
    """Une frame est une image finale prète à être affichée,
    une fois tous les effets appliqués"""

    def __init__(self, image: Image.Image, limites) -> None:
        image_contrainte = self._contraindre(image, limites)
        self.donnees = np.array(
            image_contrainte.convert("RGB").getdata()
        ).astype(np.uint8)

    def decouper(self):
        """On sépare les données en blocs de maximum 480 valeurs,
        pour éviter de saturer la matrice de LED
        en envoyant trop d'informations"""
        return np.array_split(self.donnees, np.ceil(len(self.donnees) / 480))

    def _contraindre(self, image, limites: tuple[int, int]):
        if image.width > limites[0] or image.height > limites[1]:
            return rogner_depuis_centre(image, limites)
        return image


class Animation:
    def __init__(
        self,
        nom: str,
    ):
        """Une animation consiste en une série de sprites à afficher,
        en y appliquant éventuellement des effets.
        Les sprites sont jouées dans l'ordre d'ajout.
        Les effets sont tous appliqués à chaque sprite"""
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
        n_etapes = 12 * duree if duree else None
        etape = 0
        while True:
            if n_etapes is not None:
                if etape == n_etapes:
                    break

            frame = self.appliquer_effets(etape, limites)
            yield frame
            etape += 1

    def appliquer_effets(self, etape: int, limites: tuple[int, int]):
        numero_sprite = etape % len(self.sprites)
        sprite = self.sprites[numero_sprite]

        with Image.open(sprite.fichier) as image:
            nouvelle_image = image
            for effet in self.effets:
                nouvelle_image = effet.appliquer(nouvelle_image, etape)

            return Frame(nouvelle_image, limites)
