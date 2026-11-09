"""Deterministic escape room rules. Never executes instructions supplied by player or LLM."""
import json
import re
from pathlib import Path
from dataclasses import dataclass
from game_state import GameState

CONFIG = json.loads((Path(__file__).resolve().parent / "game_config.json").read_text(encoding="utf-8"))

@dataclass(frozen=True)
class Result:
    success: bool
    message: str
    category: str

ALIASES = {"books": "bookshelf", "shelf": "bookshelf", "table": "desk", "picture": "painting",
           "cabinet": "drawer", "exit": "door", "gate": "door"}

def target_of(text: str) -> str | None:
    words = set(re.findall(r"[a-z]+", text.lower()))
    for obj in CONFIG["objects"]:
        if obj in words:
            return obj
    for alias, obj in ALIASES.items():
        if alias in words:
            return obj
    return None

def act(state: GameState, player_text: str) -> Result:
    """Process one player turn; return only approved information for narration."""
    state.turns += 1
    raw = player_text.strip()
    s = raw.lower()
    obj = target_of(s)
    words = set(re.findall(r"[a-z]+", s))
    if not raw:
        return Result(False, "Please describe an action.", "invalid")
    # Never interpret role-play or prompt-injection as game commands.
    if any(term in s for term in ("ignore previous", "ignore all", "system prompt", "developer message", "administrator", "admin override", "reveal all", "secret codes", "you are now", "pretend you", "bypass", "override the rules")):
        return Result(False, "The library does not respond to requests to override its rules. Explore the room normally.", "blocked")
    if ("inventory" in words or "items" in words or "backpack" in words):
        items = ", ".join(sorted(state.inventory)) or "nothing"
        return Result(True, f"You are carrying: {items}.", "inventory")
    if "help" in words or "hint" in words:
        if "bookshelf" not in state.examined:
            msg = "Try examining the bookshelf."
        elif "desk" not in state.examined:
            msg = "Look at the desk for a hint about the drawer."
        elif not state.drawer_open:
            msg = "Combine the bookshelf and desk clues to open the drawer."
        elif "painting" not in state.examined:
            msg = "Study the painting for the exit combination."
        else:
            msg = "Use the brass key and the painting's code on the exit door."
        return Result(True, msg, "hint")
    if any(w in words for w in ("look", "examine", "inspect", "search", "investigate", "read", "study")):
        if obj is None:
            return Result(False, "You see a bookshelf, desk, painting, locked drawer and exit door. Name one to examine.", "invalid")
        state.examined.add(obj)
        if obj == "bookshelf":
            state.solved.add("bookshelf_clue")
            return Result(True, "Four oddly placed book spines spell M-O-O-N.", "clue")
        if obj == "desk":
            state.solved.add("desk_clue")
            return Result(True, "A note on the desk says: 'The word on the shelf unlocks the drawer.'", "clue")
        if obj == "painting":
            state.solved.add("painting_clue")
            return Result(True, "The painting has four stars labelled 4, 2, 7, 1 from left to right.", "clue")
        if obj == "drawer":
            return Result(True, "The drawer is open, revealing its empty velvet lining." if state.drawer_open else "The drawer has a four-letter password lock.", "observation")
        return Result(True, "The exit door has a keyhole and a four-digit keypad. It is open!" if state.door_open else "The exit door has a keyhole and a four-digit keypad.", "observation")
    # Drawer opens only after both clue discoveries and correct password.
    if obj == "drawer" and any(w in words for w in ("open", "unlock", "enter", "type", "try", "use")):
        if state.drawer_open:
            return Result(True, "The drawer is already open.", "observation")
        if not {"bookshelf_clue", "desk_clue"}.issubset(state.solved):
            return Result(False, "You need to discover the bookshelf and desk clues before opening the drawer.", "locked")
        if not re.search(r"\bmoon\b", s, flags=re.I):
            return Result(False, "The drawer does not open. Enter the correct four-letter password.", "locked")
        state.drawer_open = True
        state.solved.add("drawer_puzzle")
        return Result(True, "The drawer clicks open. A brass key rests inside. You can take it.", "unlock")
    if any(w in words for w in ("take", "collect", "pick", "grab")):
        if "key" in words or "brass" in words:
            if not state.drawer_open:
                return Result(False, "You cannot take the brass key: the drawer is still locked.", "locked")
            if "brass key" in state.inventory:
                return Result(True, "You already have the brass key.", "observation")
            state.inventory.add("brass key")
            return Result(True, "You collect the brass key and place it in your inventory.", "inventory")
        return Result(False, "There is no collectible item matching that description.", "invalid")
    if obj == "door" and any(w in words for w in ("open", "unlock", "enter", "type", "try", "use", "escape")):
        if state.door_open:
            return Result(True, "The exit is already open. You escaped!", "win")
        if "brass key" not in state.inventory:
            return Result(False, "The exit stays locked. You must first collect the brass key.", "locked")
        if "painting_clue" not in state.solved:
            return Result(False, "You need to investigate the painting before entering the exit code.", "locked")
        if not re.search(r"(?<!\d)4271(?!\d)", s):
            return Result(False, "The keypad flashes red: incorrect or missing four-digit code.", "locked")
        state.door_open = True
        state.solved.add("exit_puzzle")
        return Result(True, "The key turns and the keypad glows green. The door opens. ESCAPED!", "win")
    if obj is not None:
        return Result(False, f"That action does not work on the {obj}. Try examining it or using an appropriate item.", "invalid")
    return Result(False, "That action is not available here. Try examining one of the five room objects.", "invalid")
