from animations import SpriteAnimee, Strobe
from player import Player


def main():
    mario = SpriteAnimee("mario")
    question = SpriteAnimee("question")
    question.ajouter_serie("QuestionBlock")
    mario.ajouter_serie("mario_marche")
    strobe = Strobe(3, "BLUE", "BLACK")

    player = Player("192.168.1.14")
    player.ajouter_arriere_plan(strobe, 30)

    player.ajouter_premier_plan(mario, 15)
    player.ajouter_premier_plan(question, 15)
    player.jouer()


main()
