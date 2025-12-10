from affichage import Affichage

from ddp import stream_ddp
from images import Frame
from animations import Animation


class Player:
    def __init__(self, ip: str) -> None:
        self.affichage = Affichage(ip)
        self.premier_plan: list[tuple[Animation, int]] = []
        self.arriere_plan: list[tuple[Animation, int]] = []

    def ajouter_premier_plan(self, animation: Animation, duree):
        self.premier_plan.append((animation, duree))

    def ajouter_arriere_plan(self, animation: Animation, duree):
        self.arriere_plan.append((animation, duree))

    def _tout_generer(self):
        rendu_arriere_plan = (
            animation.generer(duree, self.affichage.taille)
            for (animation, duree) in self.arriere_plan
        )

        rendu_premier_plan = (
            frame
            for (animation, duree) in self.premier_plan
            for frame in animation.generer(duree, self.affichage.taille)
        )
        rendu_arriere_plan = (
            frame
            for (animation, duree) in self.arriere_plan
            for frame in animation.generer(duree, self.affichage.taille)
        )

        for image1, image2 in zip(rendu_arriere_plan, rendu_premier_plan):
            yield Frame(image1, image2, self.affichage.taille)

    def jouer(self):
        playlist = self._tout_generer()
        stream_ddp(
            playlist=playlist,
            affichage=self.affichage,
        )
