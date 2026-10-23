"""Turn indicator conditions into positions. A position decided at bar t is held from the close of t."""
import numpy as np
import pandas as pd


def cross_above(a, b):
    """True on the bar where a moves from <= b to > b."""
    return (a > b) & (a.shift(1) <= b.shift(1))


def cross_below(a, b):
    return (a < b) & (a.shift(1) >= b.shift(1))


def positions_from_signals(long_entry, long_exit=None, short_entry=None, short_exit=None):
    """Stateful position in {-1, 0, 1} from boolean entry/exit Series.

    An entry in the opposite direction reverses the position. Exits only close their own side.
    If an entry and an exit fire on the same bar, the entry wins.
    """
    idx = long_entry.index
    false = pd.Series(False, index=idx)
    le = long_entry.fillna(False).to_numpy(bool)
    lx = (long_exit if long_exit is not None else false).fillna(False).to_numpy(bool)
    se = (short_entry if short_entry is not None else false).fillna(False).to_numpy(bool)
    sx = (short_exit if short_exit is not None else false).fillna(False).to_numpy(bool)

    pos = np.zeros(len(idx), dtype=int)
    current = 0
    for i in range(len(idx)):
        if current == 1 and lx[i]:
            current = 0
        elif current == -1 and sx[i]:
            current = 0
        if le[i]:
            current = 1
        elif se[i]:
            current = -1
        pos[i] = current
    return pd.Series(pos, index=idx, name='position')
