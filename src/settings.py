from pathlib import Path as Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / 'data'
FIGURES_DIR = ROOT_DIR / 'reports' / 'figures'

RANDOM_SEED = 42