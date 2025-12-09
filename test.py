from images import Animation
from player import Player


def main():
    animation = Animation("Mario")
    animation.ajouter_serie("mario_marche")
    player = Player("192.168.1.14")
    player.jouer(animation=animation)


main()
