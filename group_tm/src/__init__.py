from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple, Type, Optional


class Coordinates(NamedTuple):
    x: int
    y: int


@dataclass
class Maze:
    locations: dict["Coordinates", "Location"] = field(init=False)

    def __post_init__(self):
        self.locations = defaultdict(lambda: None)
        print(self.locations)

    @staticmethod
    def parse(data: list[str]) -> tuple["Maze", Optional["Maze.Corridor"], Optional["Maze.Corridor"]]:
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
                raise ValueError(f"value \"{mark}\" cannot be parsed as a maze location")

    @dataclass
    class Corridor(Location):

        def neighbors(self) -> set["Maze.Corridor"]:
            x, y = self.coordinates
            return set(filter(lambda it: it is not None, [
                self.maze.locations[Coordinates(x + 1, y)],
                self.maze.locations[Coordinates(x - 1, y)],
                self.maze.locations[Coordinates(x, y + 1)],
                self.maze.locations[Coordinates(x, y - 1)],
            ]))

    @dataclass
    class Wall(Location):
        ...


def load(data_file: Path) -> list[str]:
    with open(data_file) as data:
        return [*data]
