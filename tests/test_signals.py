import pandas as pd

from lib import signals


def test_cross_above_and_below():
    a = pd.Series([1, 2, 3, 2, 1])
    b = pd.Series([2, 2, 2, 2, 2])
    assert signals.cross_above(a, b).tolist() == [False, False, True, False, False]
    assert signals.cross_below(a, b).tolist() == [False, False, False, False, True]


def test_positions_from_signals_state_machine():
    f, t = False, True
    le = pd.Series([f, t, f, f, f, f, t])
    lx = pd.Series([f, f, f, t, f, f, f])
    se = pd.Series([f, f, f, f, t, f, f])
    pos = signals.positions_from_signals(le, lx, se)
    # flat, long, long, exit, short, short, reverse to long
    assert pos.tolist() == [0, 1, 1, 0, -1, -1, 1]
