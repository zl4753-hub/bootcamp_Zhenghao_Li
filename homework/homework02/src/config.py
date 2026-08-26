import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def get_key(name: str, default=None):
    """Retrieve an environment variable key."""
    return os.getenv(name, default)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
