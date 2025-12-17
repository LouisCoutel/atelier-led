from api.animations import CouleurUnie, Radial, SpriteAnimee, Strobe
from api.effets import Contour, Mirroir
from api.player import Player
from entrainement.classes import Personne


def main():
    moi = Personne("Louis", "Coutel", 32)
    moi.se_presenter()
    mario = SpriteAnimee("mario_marche")
    print(3 * "12")
    radial = Radial([[255, 128, 32], [0, 0, 0], [123, 211, 128]])
    question = SpriteAnimee("QuestionBlock")
    question.ajouter_effet(Mirroir(10))
    mario.ajouter_effet(Contour([0, 0, 0]))
    strobe = Strobe(3, "BLUE", "BLACK")
    fond_bleu = CouleurUnie("BLUE")

    player = Player("192.168.1.18")
    # player.ajouter_arriere_plan(fond_bleu, 20)
    # player.ajouter_arriere_plan(radial, 50)

    player.ajouter_premier_plan(mario, 20)
    # player.ajouter_premier_plan(question, 10)
    player.jouer()


main()
