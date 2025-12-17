# Atelier LED

## Présentation
Bienvenue dans la partie logicielle de cet atelier.  
Elle a pour but de vous introduire à la programmation et à vous faire découvrir les possibilités qu'elle offre dans les domaines créatifs.
Vous serez amenés à découvrir l'environnement de développement et le language Python, que vous utiliserez pour créer et jouer des animations sur une matrice de LED.

Ce projet contient l'essentiel du code nécessaire, mais ce sera à vous de définir ce que vous attendez du programme et de fournir les bonnes instructions.   Après ça, si vous avez des idées ou des envies particulières nous pourront essayer ensemble de les concrétiser.

Je pars du principe que vous n'avez aucune expérience dans le domaine, mais si vous êtes à l'aise n'hésitez pas à passer directement à la pratique,
sinon je vous recommande de suivre les étapes.  
Vous êtes encouragés à vous entraider, me demander de l'aide ou des explications et à faire des recherches sur internet.

### C'est quoi ce site ?
Vous êtes sur **Github**, une plateforme permettant d'héberger des projets et travailler de manière collaborative.
C'est gratuit (jusqu'à un certain point) et utilisé par de très grosses entreprises pour les projets open-source.
Github va nous permettre de travailler directement depuis le navigateur, sans avoir a installer ou configurer quoi que ce soit.

## I - Découverte de l'environnement de travail

### Ouvrir le projet

Pour ouvrir le projet, cliquez sur le bouton vert Code et allez dans l'onglet Codespaces, puis cliquez sur "Create codespace on main".

<img width="967" height="409" alt="Capture d&#39;écran 2025-12-17 105134" src="https://github.com/user-attachments/assets/d5b2d9c3-d4ca-4952-a28f-57c5e1818e71" />

Github ouvrira **Visual Studio Code**, un éditeur de code gratuit, pré-configuré afin que vous n'ayez rien à installer.

### L'interface de VSCode
<img width="1920" height="1080" alt="vs_code_interface" src="https://github.com/user-attachments/assets/1b89060c-9bc4-46da-ae79-eb8a8271bf1e" />

L'interface de VSCode consiste en plusieurs panneaux.

#### 1 - L'explorateur de fichiers

Le panneau sur la gauche affiche par défaut l'explorateur de fichiers. Cliquez simplement sur un dossier pour afficher son contenu, et sur un fichier pour l'ouvrir dans le panneau central.

#### 2 - Le panneau d'édition

C'est ici que vous pouvez voir et modifier le contenu du fichier sous forme de texte.

Lorsque vous tapez, VSCode vous propose des suggestions que vous pouvez accepter avec la touche tab:

<img width="521" height="372" alt="Capture d&#39;écran 2025-12-17 115053" src="https://github.com/user-attachments/assets/768f3aa4-de06-402a-b95b-cc4ab3853bb0" />


Ainsi que des informations sur un bout de code lorsque vous le survolez avec la souris:

<img width="678" height="184" alt="Capture d&#39;écran 2025-12-17 212157" src="https://github.com/user-attachments/assets/f608eab0-d282-4c36-8477-24a17fbb2d67" />


Les erreurs et les avertissements sont signalés par des lignes rouges ou jaunes:

<img width="894" height="155" alt="Capture d&#39;écran 2025-12-17 212225" src="https://github.com/user-attachments/assets/12c5e205-341e-4177-9d34-c46ea920b1fa" />

#### 3 - Le terminal

Le panneau du bas affiche par défaut le **terminal**. Il permet de donner des instructions à l'ordinateur sous forme de texte (des **commandes**). Vous n'en utiliserez que deux:

1. La première une seule fois, lorsque vous ouvrez le projet:

```bash
source ./venv/bin/activate
```
Sans rentrer dans les détails, ca charge les extensions dont le projet a besoin (les **dépendances**).

2. La deuxième permet de lancer l'exécution du code:

```bash
python main.py
```

***

### Mise en pratique:

Ouvrez le projet et utilisez le terminal pour charger les dépendances.
Assurez vous que la commande à fonctionné: vous devriez voir (atelier-led) s'ajouter au début de la dernière ligne, avant votre nom d'utilisateur en vert.
Ensuite, executez le programme. Vous devriez voir apparaitre un message de bienvenue.

***

## II - Découverte de la programmation

Python est un langage de programmation facile d'accès car proche du langage naturel. Sorti en 1991, il est continuellement enrichi et amélioré, ce qui en fait un langage mature et très complet.
Il est à la fois fortement recommandé aux débutants et très utilisé dans les milieux scientifiques, le traitement de données et l'intelligence artificielle.

### L'indentation

Pour hierarchiser le code en Python, il faut l'**indenter**, c'est à dire décaler le début de ligne de 4 espaces ou d'un **tab**, pour signifier que ce qu'on écrit est à l'intérieur de quelque chose.  
C'est indispensable pour créer des blocs de code indépendants et réutilisables.    
VSCode indente votre code automatiquement, mais il peut se tromper.

```python
ville = "Paris"
 pays = "France"
```

L'exemple ci-dessus causera une erreur, car la ligne ou le pays est défini est décalé d'un espace qui ne devrait pas être là.

### Les types

Les opérations possibles sur une valeur dépendent de son **type**. Utiliser le mauvais type cause une erreur ou un résultat inattendu.
Pour aujourd'hui, vous aurez besoin de connaitre les suivants:

#### Les nombres entiers, *int*

```python
12
```

On peut les additionner avec `+`, les soustraire avec `-`, les multiplier (`*`), diviser (`/`), faire un modulo (`%`), les comparer (`>`,`<`,`>=`, `<=`).

#### Les chaînes de caractères, *str*

```python
"Jean-Paul"
```

Du texte entre guillemets. On peut les coller ensemble (**concaténer**) avec `+`.

#### Les booléens
```Python
True
False
```
Vrai ou faux. "True" ou "False" sans oublier la majuscule. Quand on compare deux nombres, ça donne un booléen.

```python
20 > -2 # Cette comparaison vaut True
```

On peut aussi vérifier si deux valeurs sont identiques avec `==`

```python
21 == 21 # c'est vrai (True)
"12" == 12 # c'est faux (False), pas le même type
```

VSCode essaiera au mieux de nous renseigner sur le type d'une variable ou ceux attendus par une fonction.

### Variables et fonctions

#### Variables

Une variable sert à stocker une valeur: un chiffre, du texte ou des données plus complexes. 

Définissons deux variables pour stocker un prénom et un age.

```python
prenom = "Jean-Paul"
age = 12
```

Cette valeur peut être modifiée, d'ou le nom:

```python
age = 12
age = 13
# age contient maintenant la valeur 13
```
***

### Mise en pratique:

Naviguez dans le fichier *main.py*. A l'intérieur de la fonction `main`, changez le contenu du message afin qu'il s'adresse à vous par votre prénom. vérifiez le résultat dans le terminal.

***

#### Fonctions

Les fonctions sont des blocs de code réutilisables.
Elle prennent généralement des valeurs en entrée (on parle de **paramètres**), et retournent des valeurs en sortie, mais ce n'est pas obligatoire. Une fonction peut faire appel à d'autres fonctions.
Une fonction doit être définie avec la syntaxe suivante:

```python
def nom_de_la_fonction(parametre_1, parametre_2):
    # ... notre code
    # n'oubliez pas l'indentation
    return "valeur de retour" # la valeur peut être n'importe quoi
```

Ici, on définit une fonction `est_majeur` qui a pour paramètre `age`, et retourne `True` ou `False` si l'âge est supérieur ou égal à 18.

```python
def verifier_si_majeur(age):
    return age >= 18
```

On peut ensuite l'utiliser directement.

```python
verifier_si_majeur(21)
# la fonction renverra True
```

Ou lui passer une variable définie au préalable:

```python
age = 12
verifier_si_majeur(age)
# la fonction renverra False
```

Et même enregistrer sa valeur de retour dans une variable:

```python
age = 18
est_majeur = verifier_si_majeur(age)
```

Pour afficher le résultat, on va utiliser la fonction `print` qui est fournie de base par Python.

```python
age = 18
majeur = verifier_si_majeur(age)
print(est_majeur)
# Le terminal affichera False
```

### En résumé:

- Les **variables** stockent les valeurs qu'on leur assigne, qui peuvent être de différents **types**.
- On peut réaliser des opérations simples sur des valeurs ou des variables, comme des additions ou des comparaisons, selon leur type.
- Pour pouvoir réutiliser une ou plusieurs opérations, on les englobe dans une fonction.
- Les fonctions peuvent prendre des **paramètres** en entrée et renvoyer une **valeur de retour** en sortie

***

### Mise en pratique:

Toujours dans *main.py*, créez une fonction qui renvoie un message personnalisé selon le prénom qu'on lui donne. Pour rappel, on peut mettre des chaînes de caractères bout à bout avec `+`. Vérifiez le résultat dans le terminal. 

***

## III - Fonctionnement de l'application et manipulation

### Importer des modules

Le code de l'application est réparti dans différents fichiers. On parle de **modules**.
Pour accèder au variables et aux fonctions d'un module, il faut les importer.
La syntaxe est simple et utilise la notation à point:

```python
from dossier.module import variable, fonction
```

On peut aussi importer le module en lui-même et accèder aux variables et aux fonctions dans le code, toujours avec la notation à point:

```python
import module

# ...
module.fonction()
```

On place toujours les imports dans les premières lignes d'un fichier, avant le reste du code.

***

### Mise en pratique:

Dans *main.py* importez la fonction `calculer_vitesse_moyenne` située dans le module `importation`, dans le dossier `entrainement`.
Utilisez la fonction une première fois avec les paramètres que vous voulez, en stockant le résultat dans une variable.
Répétez l'opération dans une autre variable avec des paramètres différents, puis vérifiez si votre première vitesse est plus rapide que la seconde avec la fonction `plus_rapide`, dont vous afficherez la valeur de retour avec `print`.

Essayez de créer une nouvelle fonction qui utilise les deux précédentes et prends deux temps de trajet et deux distances en paramètres pour indiquer si le premier est plus rapide que le second.

***

## Classes

Parfois on aimerait regrouper des variables entre elles, par exemple associer un nom à un prénom, et pourquoi pas à un âge ou une adresse.
On peut aussi avoir besoin de fonctions spécifiques a ce groupe de variables (dans cet exemple, une personne). Une des façons d'y parvenir, c'est d'utiliser des **classes** pour créer des **objets**.  
On parle de "programmation orientée objet", c'est un style de programmation qui a ses avantages et ses inconvénients.

### Principe et définition

Une classe regroupe des variables (qu'on appelle **attributs**) et des fonctions (des **méthodes**) pour créer des objets bien définis. Chaque objet créé de cette façon est une **instance** de la classe.
On signale les classes avec le mot clé `class` et une majuscule à la première lettre.

On doit les définir en amont, avec la méthode `__init__` qui décrit comment les objets sont créés. Tous les attributs et les méthodes d'un objet lui sont attachés grace au mot clé `self`.

```python
class Personne:
    def __init__(self, nom, prenom, age): # se lance à chaque fois qu'on crée une nouvelle instance
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.majeur = self.verifier_si_majeur()
    
    def verifier_si_majeur(self):
        return self.age >= 18

    def se_presenter(self):
        message = "Bonjour, je m'appelle " + self.prenom + " " + self.nom + ", j'ai " + str(self.age) + " ans." # On convertit l'âge en chaîne de caractères avec str()
        print(message)
```

Comme la méthode `verifier_si_majeur` est définie à l'intérieur de la classe, elle est utilisée directement pour renseigner l'attribut `majeur` sans qu'on ait besoin de demander.
Pareil pour `se_presenter`

Attention au mot-clé `self`: on s'en sert pour définir la classe, pas quand on crée ou utilise une instance: l'instance sait "qui" elle est, vous n'avez pas besoin de lui dire.

### Utilisation

Pour créer une instance, on utilise la classe comme une fonction, en ouvrant des parenthèses après le nom.
Ici, pour créer une nouvelle instance de Personne, on doit fournir le prénom et l'age.
Pour accèder aux attributs et méthodes de l'instance, on utilise la notation à point:

```python
utilisateur = Personne("Jean-Paul", 12)

print(utilisateur.majeur)
# La console affichera True
```

Les classes dont vous allez vous servir sont rangées dans le dossier `api/`.

### En résumé:
- Pour créer mon programme, j'importe les **classes** dont j'ai besoin depuis les **modules** rangés dans le dossier `api/`.
- Pour utiliser une classe, je crée une **instance** en lui fournissant les paramètres requis, et je la stocke dans une **variable**.
- Pour utiliser les **méthodes** d'une instance, j'utilise la notation à point.

***

### Mise en pratique:
Importez la classe `Personne` depuis le module `classes.py` du dossier `entrainement` et créez une nouvelle instance en renseignant vos informations, puis vérifiez en utilisant la méthode `se_presenter`.

***

## Utilisation de l'API
Une fois le dispositif LED en fonctionnement, vous allez pouvoir commencer à génerer des animations.
Pour cela, il faut procéder par étapes:

1. Je choisi une ou plusieurs classes d'animations dans le module du même nom (elles sont toutes décrites plus bas), je les importe et je crée des instances en fournissant les paramètres requis
3. Si le type d'animation choisi accepte des effets, je peux en importer depuis le module `effets` et créer des instances que j'ajoute à l'animation avec la méthode `animation.ajouter_effet`
4. J'importe et je crée un `Player`, depuis le module du même nom, en lui fournissant l'adresse IP du dispositif LED.
5. J'ajoute chaque animation à la playlist, soit au premier plan soit à l'arrière plan, avec les méthodes `player.ajouter_premier_plan` et `player.ajouter_arriere_plan`, en renseignant la durée. Je peux en ajouter autant que je veux, elle joueront à la suite
6. Je lance avec `player.jouer`

```python
from api.animations import CouleurUnie, Strobe
from api.player import Player
from api.effets import Negatif

def main():
    anim_1 = SpriteAnimee("Mario")
    anim_2 = CouleurUnie("BLUE")
    anim_3 = Strobe("RED","BLACK")

    effet = Negatif()

    anim_1.ajouter_effet(effet)

    player = Player("192.168.XXX.XXX")

    player.ajouter_premier_plan(anim_1, 30)
    player.ajouter_arriere_plan(anim_2, 15)
    player.ajouter_arriere_plan(anim_3, 15)

    player.jouer()



```
