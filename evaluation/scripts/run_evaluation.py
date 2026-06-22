import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from evaluation.evaluator import Evaluator

if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.run()