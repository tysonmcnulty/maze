import re
import unittest
from itertools import chain
from pathlib import Path

from ..src import load, parse


class MazeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maze = load(Path(__file__).parent / ".." / ".." / "resources" / "maze.txt")

    def test_load(self):
        self.assertEqual(101, len(self.maze))
        self.assertTrue(all(map(lambda row: len(row) == 102, self.maze)))
        self.assertTrue(all(map(lambda char: re.match(r"[SE.#\n]", char) is not None, chain.from_iterable(self.maze))))

    def test_parse_small_maze(self):
        self.assertEqual(
            None,
            parse(["#S.E#"])
        )
