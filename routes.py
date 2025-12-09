import json
import logging

import requests
from numpy._typing import NDArray
from PIL import Image


def image_to_grid(image: Image.Image) -> NDArray:
    """Utilisez les méthodes exposées par une instance d'Image
    pour la convertir en un tableau de valeurs RGB
    Vous devrez sans doute la redimensionner au préalable"""


def create_grid(width: int, height: int) -> NDArray:
    """A partir des dimensions de la matrice LED, créez une grille
    afin de pouvoir insérer des valeurs à des positions (x, y) précises"""


def grid_to_sequence(grid: NDArray) -> NDArray:
    """Déroulez ou aplatissez une grille afin
    de récupérer une séquence continue correspondant
    à la façon dont les LED sont indexées sur la matrice"""


def create_json_message(sequence: NDArray | list) -> str:
    """Formate la séquence afin de pouvoir l'envoyer au dispositif WLED
    Exemples de séquences valides:
    ["FF0000","00FF00","0000FF"] ou [[255,0,0],[0,255,0],[0,0,255]]"""

    message = {"seg": {"i": sequence}}

    return json.dumps(message)


def send_json(device_ip: str, message: str):
    """Envoie des instructions à la carte WLED via son API JSON et récupère la réponse"""
    res = requests.post(url=f"http://{device_ip}/json/state", data=message)
    if res.status_code == 200:
        return res.json()
    logging.error(res.status_code)


msg = create_json_message(["FF0000", "00FF00", "0000FF", "FF0000"])
send_json("192.168.1.23", msg)
