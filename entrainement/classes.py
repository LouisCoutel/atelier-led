MAJORITE = 18


class Personne:
    def __init__(self, nom: str, prenom: str, age: int):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.majeur = self.verifier_si_majeur()

    def verifier_si_majeur(self):
        return self.age >= MAJORITE

    def se_presenter(self):
        message = (
            "Bonjour, je m'appelle "
            + self.prenom
            + " "
            + self.nom
            + ", j'ai "
            + str(self.age)
            + " ans."
        )
        print(message)
