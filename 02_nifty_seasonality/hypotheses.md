# NIFTY seasonality — hypothesis register

Research hypotheses are **not findings**. Do not promote a claim to 'validated' until the test protocol, data, costs and temporal validation are documented.

| ID | Idea | Outcome | Conditioning info available by | Status |
|---|---|---|---|---|
| H01 | July has an above-baseline monthly return | July close-to-close % return | June close for prospective forecast | Not tested inferentially |
| H02 | November has an above-baseline monthly return | November % return | October close | Not tested inferentially |
| H03 | September weakness influences October direction | October return | September close | Not tested |
| H04 | September negative, October trades below September low, then October closes up → November positive | November % return and binary positive | October close | Not tested (requires daily bars) |
| H05 | September negative, October closes negative → November rebounds | November % return and binary positive | October close | Not tested |
| H06 | Seasonality strength differs by ex-ante index regime | Next month return | Previous month close | Not tested |

Protocol:
1. Freeze definitions and sample.
2. Calculate unconditional baseline.
3. Check counts and uncertainty for each conditional sample.
4. Evaluate out-of-sample and subperiod robustness.
5. Account for the fact that multiple seasonal hypotheses were considered.
6. Only later evaluate futures or options trading P&L with costs.
