# TODO: Faire un test QUI MARCHE sur une des annales du hashcode
# TODO: Coder une solution algo genetique.
# TODO: Voir si splitter Problem en une seconde classe (Solver?) (qui gère parsing + output) est pas plus pratique. C'est surement plus lisible.

import glob
import os
import collections
import ntpath

from typing import Union


Number = Union[int, float]


PATH_DIR_INPUTS = os.path.join("..", "inputs")
PATH_DIR_OUTPUTS = os.path.join("..", "outputs")

Input = collections.namedtuple("Input", [])
Solution = collections.namedtuple("Problem", [])


class Problem:
    def parse_input(self, path_file_input: str) -> Input:
        raise NotImplementedError()

    def solve(self, inp: Input) -> Solution:
        raise NotImplementedError()

    def score(self, inp: Input, solution: Solution) -> Number:
        raise NotImplementedError()

    def write_output(self, solution: Solution, func_convert: callable, score: Number, id_problem: str,
                     zfill_score: int = 9, path_dir_outputs: str = PATH_DIR_OUTPUTS):
        # Create outputs directory if it does not exists
        os.makedirs(path_dir_outputs, exist_ok=True)

        if score is None:
            score = 0

        path_file_output = os.path.join(path_dir_outputs, id_problem + '_' + str(score).zfill(zfill_score)) + ".out"
        string = func_convert(solution)
        with open(path_file_output, 'w') as fp:
            fp.write(string)


def iter_path_files_input(extension: str = ".in", path_dir_inputs: str = PATH_DIR_INPUTS):
    """ Iterate through all files located at `path_dir_inputs`.
    :param extension: Suffix matching desired files. Empty string to match everything.
    """
    for file_input in glob.glob(os.path.join(path_dir_inputs, "*" + extension)):
        yield file_input


def get_id_problem(path_file_input: str) -> str:
    """ Return the ID of a problem given its filename. """
    return ntpath.basename(path_file_input)[0]


def main(problem_class: Problem, func_convert: callable, path_dir_inputs: str, path_dir_outputs: str,
         inputs_to_skip=[]):
    problem = problem_class()
    for path_file_input in iter_path_files_input(path_dir_inputs=path_dir_inputs):
        id_problem = get_id_problem(path_file_input)
        print("Classe :", id_problem)
        if id_problem in inputs_to_skip:
            continue
        inp = problem.parse_input(path_file_input)
        solution = problem.solve(inp)
        score = problem.score(inp=inp, solution=solution)
        problem.write_output(
            solution=solution,
            func_convert=func_convert,
            score=score,
            id_problem=id_problem,
            path_dir_outputs=path_dir_outputs
        )


if __name__ == "__main__":
    main()
