from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any

from pyfedappwrap.learning.run_runfig import (
    AppConfig,
    AppInputConfig,
    AppOutputConfig,
)


@dataclass
class MyAppConfig(AppConfig):
    draws: int = 200
    tune: int = 200
    chains: int = 1
    max_refits: int = 0
    target_accept: float = 0.9
    min_total: int = 5


@dataclass
class MyAppInputConfig(AppInputConfig):
    junction_counts: Any


@dataclass
class MyAppOutputConfig(AppOutputConfig):
    results: Any = None
    scatter_plot: Optional[Path] = None
