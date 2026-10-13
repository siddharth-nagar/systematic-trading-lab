# Research hypotheses — neutral pre-registration template

**Status: exploratory baseline.** No calendar month, sign, transition or trading outcome is privileged in advance.

## Primary questions

1. Are average NIFTY 50 monthly returns distinguishable across the twelve calendar months, after accounting for uncertainty and multiple comparisons?
2. Are month-specific positive-return frequencies distinguishable from the unconditional frequency?
3. How stable are month-level return distributions across non-overlapping historical periods?
4. Do calendar effects survive comparison against broad-market drift, return volatility and economic regimes defined using information available at the time?
5. Do apparent effects generalise to genuinely held-out observations?

## Exploratory (not pre-registered)

- All twelve monthly means, medians, positive frequencies, standard deviations and tails.
- Month-to-month return transitions examined **symmetrically across all months**, not a previously selected pair.
- Ex-ante trend and volatility regime splits applied with a consistent rule to all months.
- Rolling-window seasonal estimates and change-point sensitivity.

## Rules to prevent confirmation bias

- Never privilege individual months or patterns based on prior discretionary observations.
- Distinguish exploratory discoveries from confirmatory tests.
- Apply corrections for the twelve month-level comparisons and any additional tested variants.
- Preserve losing years and outliers; report sensitivity instead of deleting them.
- Freeze training/validation/test periods before inspecting model performance.
- Never use year-end classifications or revisions that were unknowable on the decision date.
- Report all tests conducted, including null and negative findings.
- Assess effect size, uncertainty, stability and practical tradability separately.
- Do not optimise a calendar trade while constructing the descriptive baseline.

## Protocol metadata (to fill before confirmatory work)

- Data source and version:
- Official source verification:
- Sample and missing-month rules:
- Hypothesis family / multiplicity correction:
- Training period:
- Validation period:
- Untouched test period:
- Statistic and confidence interval:
- Bootstrap design (if relevant):
- Costs and execution assumption (only for later trading tests):
- Decision:
