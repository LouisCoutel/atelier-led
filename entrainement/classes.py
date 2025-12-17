MAJORITE = 18


class Personne:
    def __init__(self, prenom: str, nom: str, age: int):
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.majeur = self.verifier_si_majeur()

    def verifier_si_majeur(self):
        return self.age >= MAJORITE

    def se_presenter(self):
        print(f"Je m'appelle {self.prenom} {self.nom} et j'ai {self.age} ans.")
