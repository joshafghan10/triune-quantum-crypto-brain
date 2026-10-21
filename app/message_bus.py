from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class BrainConfig:
    perception_name: str = "perception"
    research_name: str = "research"
    decision_name: str = "decision"
    meta_name: str = "meta"
    message_limit: int = 250
    tick_seconds: float = 1.2
    default_priority: int = 4

CONFIG = BrainConfig()
