import collections
import os
from functools import reduce
from math import gcd

import numpy as np
import pandas as pd
import tqdm

from core import Number, Problem, main


def find_gcd(list):
    x = reduce(gcd, list)
    return x


Input = collections.namedtuple("Input", ["D", "I", "S", "V", "F", "streets", "paths"])
Solution = collections.namedtuple("Solution", ["A", "intersections"])
Street = collections.namedtuple("Street", ["start", "end", "name", "time"])
Intersection = collections.namedtuple(
    "Intersection", ["id", "streets_names", "streets_durations"]
)

PATH_DIR_INPUTS = os.path.join("..", "inputs", "2021_traffic_signaling")
PATH_DIR_OUTPUTS = os.path.join("..", "outputs", "2021_traffic_signaling")


class TemplateProblem(Problem):
    def parse_input(self, path_file_input: str) -> Input:
        with open(path_file_input, "r") as fp:
            lines = fp.readlines()
        D, I, S, V, F = map(int, lines[0].strip("\n").split())
        streets = []
        paths = []
        for line in lines[1 : S + 1]:
            line = line.strip("\n")
            street = line.split(" ")
            street = Street(
                start=int(street[0]),
                end=int(street[1]),
                name=street[2],
                time=int(street[3]),
            )
            streets.append(street)
        for line in lines[S + 1 :]:
            line = line.strip("\n")
            path = line.split(" ")
            path = path[1:]
            paths.append(path)
        return Input(D=D, I=I, S=S, V=V, F=F, streets=streets, paths=paths)

    def score(self, inp: Input, solution: Solution) -> Number:
        pass

    def solve(self, inp: Input):

        intersections = collections.defaultdict(list)

        for s in inp.streets:
            intersections[s.end].append(s.name)

        nodes_start_end = {s.name: s.end for s in inp.streets}

        nodes = pd.DataFrame(
            0, columns=list(intersections.keys()), index=list(nodes_start_end.keys())
        )

        for paths in tqdm.tqdm(inp.paths, position=0):
            for s in paths:
                end = nodes_start_end[s]
                nodes.loc[s, end] += 1

        nodes = nodes.astype(int)

        solution = []

        for id, s in intersections.items():
            if len(s) == 1:
                solution.append(
                    Intersection(id=id, streets_names=s, streets_durations=[inp.D])
                )
            elif len(s) > 1:
                sample = nodes[id].T[nodes[id] > 0]
                solution.append(
                    Intersection(
                        id=id,
                        streets_names=list(sample.index),
                        streets_durations=sample.tolist(),
                    )
                )
        return Solution(A=len(solution), intersections=solution)


def func_convert(solution: Solution) -> str:
    A = 0
    output = "\n"
    for intersection in solution.intersections:
        if len(intersection.streets_names) == 0:
            continue
        A += 1
        output += str(intersection.id) + "\n"
        output += str(len(intersection.streets_names)) + "\n"
        for street_name, street_duration in zip(
            intersection.streets_names, intersection.streets_durations
        ):
            output += street_name + " " + str(street_duration) + "\n"
    return str(A) + output


if __name__ == "__main__":
    main(
        problem_class=TemplateProblem,
        func_convert=func_convert,
        path_dir_inputs=PATH_DIR_INPUTS,
        path_dir_outputs=PATH_DIR_OUTPUTS,
        inputs_to_skip=[],
    )
