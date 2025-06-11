import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import greet, add


def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(10, 20) == 30