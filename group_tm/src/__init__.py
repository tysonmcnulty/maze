from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple, Type, Optional, Mapping, TypeVar, Iterator, Iterable


class Coordinates(NamedTuple):
    x: int
    y: int


@dataclass
class Maze:
    locations: dict["Coordinates", "Location"] = field(init=False)

    def __post_init__(self):
        self.locations = defaultdict(lambda: None)

    @staticmethod
    def parse(
        data: list[str],
    ) -> tuple["Maze", Optional["Maze.Corridor"], Optional["Maze.Corridor"]]:
        maze = Maze()
        start_location = None
        end_location = None

        for j, line in enumerate(data):
            for i, mark in enumerate(line.strip()):
                coordinates = Coordinates(i, j)
                location = Maze.Location.parse(mark)(maze, coordinates)
                maze.locations[coordinates] = location
                if mark == "S":
                    start_location = location
                elif mark == "E":
                    end_location = location

        return maze, start_location, end_location

    @dataclass
    class Location(ABC):
        maze: "Maze" = field(compare=False, repr=False)
        coordinates: "Coordinates"

        @staticmethod
        def parse(mark: str) -> Type["Maze.Location"]:
            if mark == "S":
                return Maze.Corridor
            elif mark == "E":
                return Maze.Corridor
            elif mark == ".":
                return Maze.Corridor
            elif mark == "#":
                return Maze.Wall
            else:
                raise ValueError(f'value "{mark}" cannot be parsed as a maze location')

    @dataclass
    class Corridor(Location):
        def neighbors(self) -> Iterable["Maze.Corridor"]:
            x, y = self.coordinates
            return list(
                filter(
                    lambda it: isinstance(it, Maze.Corridor),
                    [
                        self.maze.locations[Coordinates(x + 1, y)],
                        self.maze.locations[Coordinates(x - 1, y)],
                        self.maze.locations[Coordinates(x, y + 1)],
                        self.maze.locations[Coordinates(x, y - 1)],
                    ],
                )
            )

    @dataclass
    class Wall(Location):
        ...


T = TypeVar("T")


@dataclass
class PathMapping(Mapping[T, list[T]]):
    start: T
    previous: dict[T, Optional[T]] = field(init=False)

    def __post_init__(self):
        self.previous = {self.start: None}

    def __len__(self) -> int:
        return len(self.previous)

    def __iter__(self) -> Iterator[T]:
        return iter(self.previous)

    def __getitem__(self, key: T) -> list[T]:
        current_item = key
        path = [current_item]
        while True:
            current_item = self.previous[current_item]
            if current_item is None:
                return list(reversed(path))

            path.append(current_item)

    def __iadd__(self, path: Iterable[T]):
        for current_item, next_item in pairwise(path):
            self.previous[next_item] = current_item

        return self


def navigate(
    start: Maze.Corridor, end: Optional[Maze.Corridor] = None
) -> Mapping[Coordinates, list[Coordinates]]:
    paths = PathMapping(start.coordinates)
    unexplored: list[Maze.Corridor] = [start]

    while len(unexplored) > 0:
        current = unexplored.pop()
        for discovered in filter(lambda it: it.coordinates not in paths, current.neighbors()):
            paths += (current.coordinates, discovered.coordinates)
            unexplored.append(discovered)

            if discovered == end:
                break
        else:
            continue

        break

    return paths


def load(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]
