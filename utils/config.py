from pathlib import Path

# Base project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

# Default CDR config
DEFAULT_CDR_ROWS = 1000
DEFAULT_CDR_FILE_FORMAT = "csv"
