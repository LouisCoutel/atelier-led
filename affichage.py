import logging
import requests


class AppareilIntrouvable(Exception):
    def __init__(self) -> None:
        super().__init__(
            "L'appareil ne répond pas. Vérifiez que l'IP est correcte."
        )


class Affichage:
    """Les infos de l'appareil LED."""

    def __init__(self, ip):
        res = requests.get(url=f"http://{ip}/json/info")
        if res.status_code == 200:
            infos_matrice = res.json()

            self.ip = infos_matrice["ip"]
            self.largeur = infos_matrice["leds"]["matrix"]["w"]
            self.hauteur = infos_matrice["leds"]["matrix"]["h"]
            self.n_pixels = self.largeur * self.hauteur
            self.taille = (self.largeur, self.hauteur)

            logging.info(f"Infos de l'appareil {ip} récupérées.")
        else:
            raise AppareilIntrouvable()
