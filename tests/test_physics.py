import numpy as np
import pytest
from muonscope.physics import Geometry, Readout, simulate_pair, summarize, segment_in_box_length_mm, wilson_interval


def test_segment_crossing():
    a=np.array([[0.,0.,10.],[10,10,10.]])
    b=np.array([[0.,0.,-10.],[10,10,-10.]])
    length=segment_in_box_length_mm(a,b,[0,0,0],10)
    assert length[0]==pytest.approx(10)
    assert length[1]==pytest.approx(0)


def test_statistics_bounds():
    assert wilson_interval(0,100)[0]==0
    assert wilson_interval(100,100)[1]==1
    with pytest.raises(ValueError):wilson_interval(11,10)


def test_zero_loss_preserves_all_references():
    result=simulate_pair(5000,seed=3,readout=Readout(effective_loss_per_cm=0))
    assert result['reference_coincidences']==result['sample_coincidences']
    assert result['bottom_geometric']<=result['primaries']
    assert summarize(result)['contrast_pct']==0


def test_reproducible():
    r1=simulate_pair(1000,seed=5)
    r2=simulate_pair(1000,seed=5)
    assert r1==r2


def test_invalid_geometry():
    with pytest.raises(ValueError):Geometry(upper_clearance_mm=0)
