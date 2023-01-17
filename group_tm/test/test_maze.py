import re
import unittest
from itertools import chain
from pathlib import Path

from ..src import load, Maze, Coordinates


class MazeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maze_data = load(Path(__file__).parent / ".." / ".." / "resources" / "maze.txt")

    def test_load(self):
        self.assertEqual(101, len(self.maze_data))
        self.assertTrue(all(map(lambda row: len(row) == 102, self.maze_data)))
        self.assertTrue(
            all(map(lambda char: re.match(r"[SE.#\n]", char) is not None, chain.from_iterable(self.maze_data))))

    def test_parse_small_maze(self):
        maze, start_location, end_location = Maze.parse(["#S.E\n"])
        self.assertEqual(Maze.Wall, type(maze.locations[Coordinates(0, 0)]))
        self.assertEqual(Maze.Corridor, type(maze.locations[Coordinates(1, 0)]))
        self.assertEqual(Maze.Corridor, type(maze.locations[Coordinates(2, 0)]))
        self.assertEqual(Maze.Corridor, type(maze.locations[Coordinates(3, 0)]))
        self.assertEqual(None, maze.locations[Coordinates(4, 0)])

        self.assertEqual(start_location, maze.locations[Coordinates(1, 0)])
        self.assertEqual(end_location, maze.locations[Coordinates(3, 0)])
