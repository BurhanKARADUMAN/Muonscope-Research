import numpy as np
import pytest
from muonscope.electronics import Pulse, waveform, leading_edges, pair_coincidences


def test_waveform_has_negative_pulse():
    t,v=waveform([Pulse(25,3)],duration_ns=50,step_ns=.05,noise_rms_mv=0)
    assert t.size==v.size
    assert -3.01<np.min(v)<-2.99


def test_threshold_crossings():
    t=np.arange(9.)
    v=np.array([0,0,-2,-2,0,0,-3,0,0],float)
    assert np.allclose(leading_edges(t,v,-1),[1.5,5+1/3])


def test_coincidence_one_to_one():
    matches=pair_coincidences([10,100,200],[13,150,201],window_ns=5,dead_time_ns=0)
    assert len(matches)==2
    assert matches[0][2]==pytest.approx(-3)


def test_dead_time():
    assert len(pair_coincidences([10,20,100],[11,21,101],window_ns=2,dead_time_ns=30))==2


def test_bad_input():
    with pytest.raises(ValueError):waveform([Pulse(0,-1)])
    with pytest.raises(ValueError):pair_coincidences([],[],window_ns=-1)
