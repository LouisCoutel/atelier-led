"""Il est possible de créer des affichages à partir d'images.
On peut s'en servir comme textures,
décaler les images pour créer l'illusion d'un déplacement,
faire varier les couleurs ou les distordre."""

import numpy as np

from PIL import Image


class Sprite:
    """Une sprite est une image en pixel-art."""

    def __init__(self, fichier):
        self.fichier = fichier

        with Image.open(fichier) as img:
            self.largeur = img.width
            self.hauteur = img.height


def _rogner_depuis_centre(
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


def _combiner(
    image1: Image.Image | None, image2: Image.Image, limites: tuple[int, int]
) -> Image.Image:
    image1 = (
        image1.convert("RGBA")
        if image1
        else Image.new("RGBA", limites, color="Black")
    )
    image2 = image2.convert("RGBA")

    image1.paste(image2, box=None, mask=image2)

    return image1.convert("RGB")


def _contraindre(image: Image.Image, limites: tuple[int, int]) -> Image.Image:
    if image.width > limites[0] or image.height > limites[1]:
        return _rogner_depuis_centre(image, limites)

    return image


class Frame:
    """Une frame contient les données à afficher
    une fois le premier et l'arrière plan combinés."""

    def __init__(
        self, image1: Image.Image | None, image2: Image.Image, limites
    ) -> None:
        nouvelle_image = _combiner(image1, image2, limites)
        nouvelle_image = _contraindre(nouvelle_image, limites)

        self.donnees = np.array(nouvelle_image.getdata()).astype(np.uint8)

        image2.close()
        nouvelle_image.close()

    @property
    def blocs(self):
        """On sépare les données en blocs de maximum 480 valeurs,
        pour éviter de saturer la matrice de LED
        en envoyant trop d'informations"""
        return np.array_split(self.donnees, np.ceil(len(self.donnees) / 480))
