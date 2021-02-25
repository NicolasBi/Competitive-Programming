""" Template de solution générale pour résoudre un problème d'optimisation type "Google Hashcode".

Les modifications suivantes doivent être apportées au template pour pouvoir être utilisé :
  1) Donner les attributs attendus dans les named-tuples Input et Solution. Ces attributs correspondent aux noms des
     variables accessibles depuis ces tuples et seront utilisés dans votre fonction de parsing d'input, de production
     d'output ainsi que votre solveur.
  2) Implémenter la fonction `parse_input` qui prend en entrée le chemin vers un fichier à lire et qui retourne un
     named-tuple contenant les variables représentant le problème à résoudre.
  3) Implémenter la fonction `func_convert` qui prend en entrée la solution au problème et qui retourne une chaîne de
     caractères attendue en tant que fichier de sortie.
  4) Implémenter la fonction `score` qui prend en entrée les named-tuples d'input et de solution, et renvoie un nombre
     correspondant au score attribué à la solution.
  5) Enfin, implémenter la fonction `solve` qui prend en entrée un named-tuple Input et produit un named-tuple
     Solution. Vous pouvez définir autant de méthodes que vous le souhaitez dans la classe, pourvu que la méthode
     "solve" soit correctement définie.

Une proposition d'organisation d'équipe (de minimum 3 personnes) pour les premières 30 minutes est la suivante :
  * Un membre de l'équipe ne lit même pas le sujet, il s'intéresse seulement aux parties en rapport avec les inputs et
    outputs. Il écrit les fonctions en conséquence. Après test de leur bon fonctionnement, il peut lire le sujet.
  * Un membre de l'équipe lit le sujet mais ne cherche pas de solution et s'attarde à correctement écrire la fonction
    de coût. Une fois la fonction écrite et testée, il commence à réfléchir à des pistes.
  * Un membre de l'équipe (de préférence le plus fort en algorithmique) se concentre sur le sujet et essaye de trouver
    le plus de pistes différentes possibles.
"""

import os
import collections

from core import Problem, Number, main


Input = collections.namedtuple("Input", [...])
Solution = collections.namedtuple("Solution", [...])

PATH_DIR_INPUTS = os.path.join("..", "inputs")
PATH_DIR_OUTPUTS = os.path.join("..", "outputs")


class TemplateProblem(Problem):
    def parse_input(self, path_file_input: str) -> Input:
        with open(path_file_input, 'r') as fp:
            lines = fp.readlines()

        ...

        return Input(...)

    def score(self, inp: Input, solution: Solution) -> Number:
        pass

    def solve(self, inp: Input) -> Solution:
        return Solution(...)


def func_convert(solution: Solution) -> str:
    ...


if __name__ == "__main__":
    main(
        problem_class=TemplateProblem,
        func_convert=func_convert,
        path_dir_inputs=PATH_DIR_INPUTS,
        path_dir_outputs=PATH_DIR_OUTPUTS,
        inputs_to_skip=[],
    )
