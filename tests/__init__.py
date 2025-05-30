"""Test package configuration."""

from pathlib import Path
import sys

# Ensure src/ is on the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
