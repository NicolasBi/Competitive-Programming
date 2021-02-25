from typing import List


class Simulation:
    def __init__(self, inp, solution):
        self.epochs = inp.D
        self.intersections = []
        self.vehicules = []
        self._current_vehicules = dict()

        for intersection in solution.intersections:
            print(intersection)
            intersection = Intersection(id=intersection.id, streets=intersection.streets_names,
                                        durations=intersection.streets_durations)
            self.intersections.append(intersection)

        for id_path, path in enumerate(inp.paths):
            print(id_path, path)
            vehicule = Vehicule(id=id, path=path)
            self.vehicules.append(vehicule)

        for vehicule in self.vehicules:
            self._current_vehicules

    def run(self) -> int:
        for epoch in range(self.epochs):
            for intersection in self.intersections:
                pass


class Street:
    def __init__(self, start: int, stop: int, name: str, duration: int):
        self.start = start
        self.stop = stop
        self.name = name
        self.duration = duration
        self._current_vehicules = []


class Intersection:
    def __init__(self, id: int,  streets: List[str], durations: List[int]):
        self.id = id
        self.streets = streets
        self.durations = durations
        self._current_street = None
        self._current_duration = None
        self._current_idx = None

    def step_epoch(self):
        if self._current_duration == 0:
            # Switching street's green light
            self._current_idx = (self._current_idx + 1) % len(self.streets)
            self._current_street = self.streets[self._current_idx]
            self._current_duration = self.durations[self._current_idx]
        else:
            self._current_duration -= 1

    def is_greenlighted(self, street: Street) -> bool:
        return self._current_street.name == street.name


class Vehicule:
    def __init__(self, path: List[str], id: int):
        self.path = path
        self.id = id
        self._current_idx = 0
        self._current_street = self.path[self._current_idx]
        self._arrived = False
        self._time_arrived = 0

    def move(self):
        self._current_idx += 1
        self._time_arrived += 1
        try:
            self._current_street = self.path[self._current_idx]
        except IndexError:
            self._arrived = True

    def arrived(self):
        return self._arrived


if __name__ == "__main__":
    pass
