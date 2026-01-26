"""
The Elder Models V: LLMRIM
A Skyrim-style character creator for LLM architectures.

Usage:
    python -m creator
"""

from .config import ModelConfig
from .presets import PRESETS

__all__ = ["ModelConfig", "PRESETS"]
