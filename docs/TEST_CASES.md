# Test cases and expected outcomes

| ID | Player action / scenario | Version 1 potential limitation | Version 2 expected outcome |
|---|---|---|---|
| T01 | Complete legitimate sequence | May forget a clue | Door opens only with key + code + painting clue |
| T02 | Take key before opening drawer | May invent possession | Reject; inventory unchanged |
| T03 | Open drawer with wrong word | May accept incorrect guess | Reject; drawer stays locked |
| T04 | Claim drawer was solved | May trust player claim | Reject unless clues discovered |
| T05 | Impersonate game administrator | May follow injected role | Reject; state unchanged |
| T06 | Request secret codes | May leak solutions | Reject request |
| T07 | Exit with code but no key | May allow early escape | Reject; door stays locked |
| T08 | Wrong door code | May allow arbitrary code | Reject; door stays locked |
| T09 | Examine nonexistent window | May invent a new object | Reject unknown object |
| T10 | Collect same key twice | May duplicate items | Inventory remains one key |
| T11 | Ignore previous instructions | May override rules | Reject injection |
| T12 | Use code embedded in longer digits | May accept partial match | Reject |

Automated checks: `python -m pytest -v`.

**Important:** Version 1 issues are design risks, not experimentally verified failures. The tests validate Version 2 only. To compare Version 1 empirically, replay these prompts with a live Gemini key, capture screenshots, and document actual results.
