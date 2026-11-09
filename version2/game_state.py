"""Authoritative game state; independent of LLM output."""
from dataclasses import dataclass, field

@dataclass
class GameState:
    examined: set[str] = field(default_factory=set)
    inventory: set[str] = field(default_factory=set)
    solved: set[str] = field(default_factory=set)
    drawer_open: bool = False
    door_open: bool = False
    turns: int = 0

    def snapshot(self) -> dict:
        return {"examined": sorted(self.examined), "inventory": sorted(self.inventory),
                "solved": sorted(self.solved), "drawer_open": self.drawer_open,
                "door_open": self.door_open, "turns": self.turns}
