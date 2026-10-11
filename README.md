# Draft math

The hole a door gap really makes, how many rolls of weatherstrip to buy, and what the job costs in money and Saturday minutes. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/draftmath/

## The three tools

- **Gap plan** - `gapPlan(gapMm, perimeterM)`: open area and the equivalent round hole.
- **Strip plan** - `stripPlan(doors, windows, doorM, windowM, rollM)`: meters needed, rolls, leftover.
- **Cost plan** - `costPlan(rolls, priceRoll, doors, windows, minEach)`: cost and install minutes.

## Labeled norms (illustrative references, not rules)

- Gap: 3 mm along a 5 m door. Roll: 5 m of foam strip. Install: 15 minutes per frame. Your gaps, frames and rolls decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (45 cases, 126 checks)

Regenerate the oracle expectations: `python3 oracle.py`
