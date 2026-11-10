import numpy as np
from muonscope.physics import Readout, scan_grid


def test_toy_scan_reproducible_and_sample_subset():
    a=scan_grid(size=3,extent_mm=30,primaries_per_point=500,seed=9)
    b=scan_grid(size=3,extent_mm=30,primaries_per_point=500,seed=9)
    for lhs,rhs in zip(a,b):assert np.array_equal(lhs,rhs)
    assert np.all(a[3] <= a[2])


def test_zero_loss_grid_is_one_where_defined():
    _,trans,ref,sample=scan_grid(size=3,primaries_per_point=500,seed=8,
                                 readout=Readout(effective_loss_per_cm=0))
    assert np.array_equal(ref,sample)
    assert np.all(trans[np.isfinite(trans)]==1)
