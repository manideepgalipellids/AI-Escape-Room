# 🔐 The Midnight Library — AI Escape Room

An interactive AI-powered escape room built for a Python/LLM course assignment. Two independent implementations illustrate the difference between **LLM-controlled gameplay** and **Python-validated gameplay**.

## Problem and solution

A player is trapped in a library and must investigate objects, discover clues, collect a key, and unlock the exit. **Version 1** uses Gemini as the Game Master and relies on conversation history for memory. **Version 2** stores authoritative game state in Python and validates every action before asking Gemini to narrate the result. It prevents accidental puzzle skips, invented inventory, and prompt-based unlocking.

## Technology

Python 3.10+, Streamlit, Google Gemini API (`google-genai`), `python-dotenv`, pytest, JSON configuration. Gemini's free-tier availability, quotas and model names may change; use a model available to your account.

## Quick start (Windows PowerShell / macOS / Linux)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY` using a key from Google AI Studio. Never commit `.env`. Optionally change `GEMINI_MODEL` to a currently supported Gemini model.

**Version 1 (requires Gemini API key):**

```bash
streamlit run version1/app.py
```

**Version 2 (Gemini narration when key configured):**

```bash
streamlit run version2/app.py
```

**Offline Version 2:** set `OFFLINE_MODE=true` in `.env`. The deterministic game engine works without any API calls; the UI uses fixed narrative text. Version 1 requires an API key by design.

**Tests:**

```bash
python -m pytest -v
```

## How to play

Five objects: bookshelf, desk, painting, drawer and exit door. Discover the three clues (bookshelf word, desk note, painting digits), open the drawer, collect the brass key, and unlock the exit. Commands can be natural-language, but Version 2 uses a deliberately bounded command parser; examples: `examine bookshelf`, `examine desk`, `open drawer with MOON`, `take brass key`, `examine painting`, `unlock door with 4271`. Use `hint` or `inventory` as needed.

## Version comparison

| Area | V1 | V2 |
|---|---|---|
| Game state | Chat history | Python `GameState` |
| Puzzle enforcement | LLM instruction | Deterministic `act()` |
| Item ownership | Model memory | Inventory set |
| Invalid commands | LLM response | Engine refusal |
| Prompt-injection resistance | Not required | Pattern-based rejection + independent engine |
| Escape | Model declares success | `door_open=True` only on valid action |

## Architecture

![V1 architecture](docs/architecture_v1.png)
![V2 architecture](docs/architecture_v2.png)

Source diagrams: [`docs/architecture_v1.mmd`](docs/architecture_v1.mmd), [`docs/architecture_v2.mmd`](docs/architecture_v2.mmd).

## Testing and evidence

See [`docs/TEST_CASES.md`](docs/TEST_CASES.md) for 12 scenarios and [`docs/DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) for screenshots. The 2–3 page report is [`docs/project_report.pdf`](docs/project_report.pdf). Automated tests cover Version 2's engine. Version 1's possible failures are **hypotheses**, not observed results; test them with a live API key before making empirical claims.

## Limitations

- V2 accepts a limited vocabulary rather than arbitrary free-form actions; it is not a general natural-language planner.
- V2 filters known injection phrases but does not guarantee that Gemini's narration is immune to all prompt injection. Crucially, Gemini cannot mutate game state, and the UI always shows the authoritative engine outcome.
- Game state persists only in the current Streamlit session and resets on restart.
- V1 can be inconsistent because game state exists only in the model's context.
- Gemini access requires a working key, network, and available API quota.

## Suggested Git history (make commits as you actually work)

1. `Initialize project and environment templates`
2. `Implement Version 1 Gemini game master`
3. `Add Version 2 structured game state and rules`
4. `Add Streamlit inventory and progress UI`
5. `Add adversarial and gameplay tests`
6. `Document architecture, results, and setup`

Do not fabricate commit history; make genuine incremental commits as you test and improve your work. Never upload credentials.

## Assignment submission

Create a public GitHub repository named `AI-Escape-Room`, push the files, add genuine screenshots to `docs/screenshots/`, and submit the repository URL. Verify the app starts and tests pass on your machine before submitting.
