from animations import CouleurUnie, Radial, SpriteAnimee, Strobe
from effets import Contour, Mirroir
from player import Player


def main():
    mario = SpriteAnimee("mario")
    radial = Radial([[255, 128, 32], [0, 0, 0], [123, 211, 128]])
    question = SpriteAnimee("question")
    question.ajouter_serie("QuestionBlock")
    question.ajouter_effet(Mirroir(10))
    mario.ajouter_serie("mario_marche")
    mario.ajouter_effet(Contour([0, 0, 0]))
    strobe = Strobe(3, "BLUE", "BLACK")
    fond_bleu = CouleurUnie("BLUE")

    player = Player("192.168.1.14")
    player.ajouter_arriere_plan(fond_bleu, 20)
    # player.ajouter_arriere_plan(radial, 50)

    player.ajouter_premier_plan(mario, 20)
    # player.ajouter_premier_plan(question, 10)
    player.jouer()


main()
