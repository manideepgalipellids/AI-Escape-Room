
# AI Escape Room — Demonstration Guide

## 1. Project Overview

The AI Escape Room is an interactive application built using Python, Streamlit, and Google Gemini.

The project contains two versions:

- **Version 1:** An LLM-driven escape room where Gemini acts as the Game Master.
- **Version 2:** A more reliable escape room that uses a Python game engine to validate actions, maintain inventory, and control puzzle progression.

This guide explains how to demonstrate both versions and verify their behavior.

## 2. Running Version 1

Open a terminal in the project root and run:

```powershell
python -m streamlit run version1/app.py
```

The application opens in a browser.

### Demonstration

1. Start the escape room.
2. Examine the bookshelf.
3. Examine the desk.
4. Examine the painting.
5. Unlock the drawer using the discovered password.
6. Collect the brass key.
7. Unlock the exit door using the correct code.

### Expected Outcome

The Game Master confirms that the player has escaped.

## 3. Running Version 2

Run:

```powershell
python -m streamlit run version2/app.py
```

Version 2 includes structured game-state tracking, inventory management, and Python-based rule validation.

### Demonstration

1. Examine the bookshelf.
2. Examine the desk.
3. Examine the painting.
4. Open the drawer using `MOON`.
5. Collect the brass key.
6. Unlock the exit using the brass key and code `4271`.

### Expected Outcome

The game displays a successful escape message.

The sidebar should show:

- Clues discovered: 3/3
- Inventory: Brass key
- Drawer: Open
- Exit: Escaped

## 4. Security and Invalid Action Demonstration

Version 2 was also tested against invalid and adversarial player inputs.

| Test | Player Action | Expected Result |
|---|---|---|
| Administrator impersonation | Claim administrator authority and demand immediate escape | Reject |
| Unauthorized item use | Use brass key before collecting it | Reject |
| Invalid drawer password | Enter an incorrect password | Reject |
| Secret code request | Ask the AI to reveal all codes | Reject |
| False completion claim | Claim all puzzles are already solved | Reject |

During the recorded adversarial test sequence, the game maintained:

- Inventory: Empty
- Clues discovered: 0/3
- Drawer: Locked
- Exit: Locked

## 5. Automated Testing

Run:

```powershell
python -m pytest -v
```

Recorded development test results:

| Metric | Result |
|---|---|
| Total tests | 12 |
| Passed | 12 |
| Failed | 0 |
| Execution time | 2.74 seconds |

For detailed results, see [TEST_CASES.md](TEST_CASES.md).

## 6. Screenshot Evidence

Gameplay and testing screenshots are stored in:

[View Screenshots](screenshots/)

The screenshots document the gameplay interface, successful escape, and selected validation scenarios.

## 7. Version Comparison

| Feature | Version 1 | Version 2 |
|---|---|---|
| Game Master | Gemini | Gemini narration |
| Game-state control | LLM-driven | Python game engine |
| Inventory validation | LLM-dependent | Python validation |
| Puzzle progression | LLM-dependent | Deterministic rules |
| Invalid action handling | Potentially inconsistent | Explicit validation |
| Security testing | Not systematically tested | Automated and interactive tests |

## 8. Conclusion

The demonstration illustrates the development of an AI-powered escape room from a conversational prototype into a more reliable application.

Version 2 improves consistency by separating AI-generated narration from game-state validation.

The project demonstrates LLM integration, Streamlit application development, structured state management, automated testing, and adversarial input handling.
