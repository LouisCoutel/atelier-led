import asyncio
import logging
from functools import reduce
from itertools import chain
from types import FunctionType
from typing import Generator

from PIL import Image

from api.affichage import Affichage
from api.animations import Animation
from api.frames import Frame
from reseau.ddp import stream_ddp


class Player:
    def __init__(self, ip: str) -> None:
        self.affichage = Affichage(ip)
        self.premier_plan: list[tuple[Animation, int]] = []
        self.arriere_plan: list[tuple[Animation, int]] = []

    @property
    def _frames_manquantes(self):
        return (
            (self._duree_totale - self._duree_ap) * 24,
            (self._duree_totale - self._duree_pp) * 24,
        )

    @property
    def _duree_pp(self):
        return _duree(self.premier_plan)

    @property
    def _duree_ap(self):
        return _duree(self.arriere_plan)

    @property
    def _duree_totale(self):
        return (
            self._duree_ap
            if (self._duree_ap >= self._duree_pp)
            else self._duree_pp
        )

    def ajouter_premier_plan(self, animation: Animation, duree):
        self.premier_plan.append((animation, duree))

    def ajouter_arriere_plan(self, animation: Animation, duree):
        self.arriere_plan.append((animation, duree))

    def _tout_generer(self):
        frames_manquantes_ap, frames_manquantes_pp = self._frames_manquantes
        logging.warning(frames_manquantes_ap)

        rendu_arriere_plan = _generer_et_combler(
            self.arriere_plan,
            self.affichage.taille,
            frames_manquantes_ap,
            _generer_noir,
        )
        rendu_premier_plan = _generer_et_combler(
            self.premier_plan,
            self.affichage.taille,
            frames_manquantes_pp,
            _generer_transparent,
        )

        for image1, image2 in zip(rendu_arriere_plan, rendu_premier_plan):
            yield Frame(image1, image2, self.affichage.taille)

    def jouer(self):
        playlist = self._tout_generer()
        asyncio.run(
            stream_ddp(
                playlist=playlist,
                affichage=self.affichage,
            )
        )


def _duree(plan: list[tuple[Animation, int]]) -> int:
    if len(plan) > 0:
        durees = tuple(item[1] for item in plan)
        return reduce(lambda duree_1, duree_2: duree_1 + duree_2, durees)

    return 0


def _transparent(limites: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", limites, "BLACK")
    image.putalpha(0)

    return image


def _generer_transparent(
    n_frames: int, limites: tuple[int, int]
) -> Generator[Image.Image, None, None] | None:
    return (_transparent(limites) for i in range(n_frames))


def _noir(limites: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", limites, "BLACK")

    return image


def _generer_noir(
    n_frames: int, limites: tuple[int, int]
) -> Generator[Image.Image, None, None] | None:
    return (_noir(limites) for i in range(n_frames))


def _generer_plan(
    plan: list[tuple[Animation, int]], limites: tuple[int, int]
) -> Generator[Image.Image, None, None] | None:
    return (
        frame
        for (animation, duree) in plan
        for frame in animation.generer(duree, limites)
    )


def _generer_et_combler(
    plan: list[tuple[Animation, int]],
    limites: tuple[int, int],
    frames_manquantes: int,
    pour_combler: FunctionType,
) -> chain[Image.Image]:
    generateur = _generer_plan(plan, limites)
    return (
        chain(
            generateur,
            pour_combler(frames_manquantes, limites),
        )
        if generateur is not None
        else pour_combler(frames_manquantes, limites)
    )
