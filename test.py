from animations import CouleurUnie, SpriteAnimee, Strobe
from effets import Defilement, HueShift, Mirroir
from player import Player


def main():
    mario = SpriteAnimee("mario")
    question = SpriteAnimee("question")
    question.ajouter_serie("QuestionBlock")
    question.ajouter_effet(Mirroir(10))
    mario.ajouter_effet(Defilement(10, True, False))
    mario.ajouter_serie("mario_marche")
    mario.ajouter_effet(HueShift(10))
    strobe = Strobe(3, "BLUE", "BLACK")
    fond_bleu = CouleurUnie("BLACK")

    player = Player("192.168.1.14")
    # player.ajouter_arriere_plan(strobe, 10)
    player.ajouter_arriere_plan(fond_bleu, 20)

    player.ajouter_premier_plan(mario, 20)
    # player.ajouter_premier_plan(question, 10)
    player.jouer()


main()
