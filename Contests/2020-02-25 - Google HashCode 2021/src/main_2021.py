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

from tqdm import tqdm

from core import Problem, Number, main

Input = collections.namedtuple("Input", ['D', 'I', 'S', 'V', 'F', 'streets', 'paths'])
Solution = collections.namedtuple("Solution", ['A', 'intersections'])
Street = collections.namedtuple("Street", ['start', 'end', 'name', 'time'])
Intersection = collections.namedtuple("Intersection", ['id', 'streets_names', 'streets_durations'])

PATH_DIR_INPUTS = os.path.join("..", "inputs", "2021_traffic_signaling")
PATH_DIR_OUTPUTS = os.path.join("..", "outputs", "2021_traffic_signaling")


class TemplateProblem(Problem):
    def parse_input(self, path_file_input: str) -> Input:
        with open(path_file_input, 'r') as fp:
            lines = fp.readlines()
        D, I, S, V, F = map(int, lines[0].strip("\n").split())
        streets = []
        paths = []
        for line in lines[1:S + 1]:
            line = line.strip("\n")
            street = line.split(' ')
            street = Street(start=int(street[0]), end=int(street[1]), name=street[2], time=int(street[3]))
            streets.append(street)
        for line in lines[S + 1:]:
            line = line.strip("\n")
            path = line.split(" ")
            path = path[1:]
            paths.append(path)
        return Input(D=D, I=I, S=S, V=V, F=F, streets=streets, paths=paths)

    def score(self, inp: Input, solution: Solution) -> Number:
        # simulation = Simulation(inp=inp, solution=solution)
        # return simulation.run()
        pass

    def solve(self, inp: Input) -> Solution:
        intersections = self.solve_percent_frequentation(inp)

        return Solution(A=len(intersections), intersections=intersections)

    def solve_1_partout(self, inp: Input):
        all_intersections = dict()
        for street in inp.streets:
            try:
                all_intersections[street.end].append(street.name)
            except KeyError:
                all_intersections[street.end] = [street.name]
        intersections = []
        for inter_id, inter_streets in all_intersections.items():
            intersections.append(
                Intersection(id=inter_id, streets_names=inter_streets, streets_durations=[1] * len(inter_streets))
            )
        return intersections

    def solve_percent_frequentation(self, inp: Input):
        all_intersections = dict()
        for street in inp.streets:
            try:
                all_intersections[street.end].append(street.name)
            except KeyError:
                all_intersections[street.end] = [street.name]

        distrib_streets = dict()
        for path in inp.paths:
            for street in path:
                try:
                    distrib_streets[street] += 1
                except KeyError:
                    distrib_streets[street] = 1
        nb_epochs = inp.D
        intersections = []
        for inter_id, inter_streets in tqdm(all_intersections.items()):
            if len(inter_streets) == 1:
                inter_streets = inter_streets
                streets_durations = [nb_epochs]
            else:
                streets_durations = normalize_list([distrib_streets[street] / nb_epochs for street in distrib_streets.keys()])
                streets_durations = [max(int(dur * nb_epochs), 1) for dur in streets_durations]
            intersections.append(
                Intersection(id=inter_id, streets_names=inter_streets, streets_durations=streets_durations)
            )
        return intersections


def func_convert(solution: Solution) -> str:
    A = 0
    output = '\n'
    for intersection in solution.intersections:
        if len(intersection.streets_names) == 0:
            continue
        A += 1
        output += str(intersection.id) + '\n'
        output += str(len(intersection.streets_names)) + '\n'
        for street_name, street_duration in zip(intersection.streets_names, intersection.streets_durations):
            output += street_name + ' ' + str(street_duration) + '\n'
    return str(A) + output


def normalize_list(lst):
    s = sum(lst)
    norm = [float(i) / s for i in lst]
    return norm


if __name__ == "__main__":
    main(
        problem_class=TemplateProblem,
        func_convert=func_convert,
        path_dir_inputs=PATH_DIR_INPUTS,
        path_dir_outputs=PATH_DIR_OUTPUTS,
        inputs_to_skip=["a", "b", "c", "e", "f"],
    )
