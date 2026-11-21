"""Press Run in PyCharm to check this project's physics and geometry."""
from pathlib import Path
import unittest
import sys

if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.discover(str(Path(__file__).parent/"tests")))
    sys.exit(0 if result.wasSuccessful() else 1)
