"""Vectorized geometry and transparent *toy* transmission model.

NOT a substitute for Geant4 multiple scattering / energy-loss transport.
The effective loss coefficient is dimensionless per cm, user-configured,
not a measured lead attenuation coefficient.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Geometry:
    panel_width_mm: float = 100.0
    panel_height_mm: float = 100.0
    scintillator_thickness_mm: float = 10.0
    cube_side_mm: float = 50.0
    upper_clearance_mm: float = 50.0
    lower_clearance_mm: float = 50.0

    def __post_init__(self):
        if min(self.panel_width_mm, self.panel_height_mm, self.scintillator_thickness_mm,
               self.cube_side_mm, self.upper_clearance_mm, self.lower_clearance_mm) <= 0:
            raise ValueError("All dimensions and clearances must be positive")

    @property
    def upper_z_mm(self):
        return self.cube_side_mm / 2 + self.upper_clearance_mm + self.scintillator_thickness_mm / 2

    @property
    def lower_z_mm(self):
        return -self.cube_side_mm / 2 - self.lower_clearance_mm - self.scintillator_thickness_mm / 2


@dataclass(frozen=True)
class Readout:
    panel_efficiency: float = 0.90
    effective_loss_per_cm: float = 0.025

    def __post_init__(self):
        if not 0 <= self.panel_efficiency <= 1:
            raise ValueError("panel_efficiency must be between 0 and 1")
        if self.effective_loss_per_cm < 0:
            raise ValueError("effective_loss_per_cm must be non-negative")


def segment_in_box_length_mm(start, end, center, side_mm):
    """Compute distance inside an axis-aligned cube for segments (N,3)."""
    start, end = np.asarray(start), np.asarray(end)
    if start.shape != end.shape or start.ndim != 2 or start.shape[1] != 3:
        raise ValueError("start/end must be equal-size (N,3) arrays")
    center = np.asarray(center, dtype=float)
    lower, upper = center - side_mm / 2, center + side_mm / 2
    delta = end - start
    lo = np.zeros(len(start))
    hi = np.ones(len(start))
    alive = np.ones(len(start), dtype=bool)
    for axis in range(3):
        d = delta[:, axis]
        static = np.abs(d) < 1e-12
        alive &= ~static | ((start[:, axis] >= lower[axis]) & (start[:, axis] <= upper[axis]))
        a = np.divide(lower[axis] - start[:, axis], d,
                      out=np.full(len(start), -np.inf), where=~static)
        b = np.divide(upper[axis] - start[:, axis], d,
                      out=np.full(len(start), np.inf), where=~static)
        amin, bmax = np.minimum(a,b), np.maximum(a,b)
        amin[static] = -np.inf
        bmax[static] = np.inf
        lo = np.maximum(lo, amin)
        hi = np.minimum(hi, bmax)
    return np.where(alive & (hi > lo), (hi - lo) * np.linalg.norm(delta, axis=1), 0.0)


def simulate_pair(n_primaries=50_000, seed=2026, geometry=None, readout=None,
                  scan_x_mm=0.0, scan_y_mm=0.0):
    """Use shared incoming tracks to create paired empty/sample coincidence counts.

    Zenith model is cos²(theta) intensity, projected onto a horizontal area.
    Conditional survival is an illustrative effective exponential loss.
    This is a deterministic, fast geometry surrogate, NOT a Geant4 run.
    """
    if n_primaries < 1:
        raise ValueError("n_primaries must be >= 1")
    g = geometry or Geometry()
    r = readout or Readout()
    rng = np.random.default_rng(seed)
    # Horizontal-plane event rate dN/dOmega ~ cos^3(theta), CDF(cos theta)=cos^4 theta.
    cos_theta = rng.random(n_primaries) ** 0.25
    phi = rng.uniform(0, 2*np.pi, n_primaries)
    tan_theta = np.sqrt(1 - cos_theta**2) / np.maximum(cos_theta, 1e-10)
    dx_dz = tan_theta * np.cos(phi)
    dy_dz = tan_theta * np.sin(phi)
    x0 = rng.uniform(-g.panel_width_mm/2, g.panel_width_mm/2, n_primaries)
    y0 = rng.uniform(-g.panel_height_mm/2, g.panel_height_mm/2, n_primaries)
    travel_z = g.upper_z_mm - g.lower_z_mm
    x1 = x0 + travel_z * dx_dz
    y1 = y0 + travel_z * dy_dz
    inside = (np.abs(x1) < g.panel_width_mm / 2) & (np.abs(y1) < g.panel_height_mm / 2)
    start = np.column_stack((x0,y0,np.full(n_primaries,g.upper_z_mm)))
    end = np.column_stack((x1,y1,np.full(n_primaries,g.lower_z_mm)))
    # Scanning panels relative to a fixed phantom is equivalent to moving phantom by -scan.
    length_mm = segment_in_box_length_mm(start, end,
                                         center=[-scan_x_mm, -scan_y_mm, 0],
                                         side_mm=g.cube_side_mm)
    acceptance_rng = rng.random(n_primaries) < r.panel_efficiency**2
    reference = inside & acceptance_rng
    loss_probability = -np.expm1(-r.effective_loss_per_cm * length_mm / 10.0)
    lost = rng.random(n_primaries) < loss_probability
    with_cube = reference & ~lost
    return {
        "primaries": int(n_primaries),
        "top_intercepts": int(n_primaries),
        "bottom_geometric": int(np.count_nonzero(inside)),
        "intersects_cube": int(np.count_nonzero(length_mm > 0)),
        "reference_coincidences": int(np.count_nonzero(reference)),
        "sample_coincidences": int(np.count_nonzero(with_cube)),
        "scan_x_mm": float(scan_x_mm), "scan_y_mm": float(scan_y_mm),
        "seed": int(seed),
    }


def wilson_interval(successes, trials, z=1.959963984540054):
    """Wilson binomial 95% interval for conditional paired survival."""
    if not 0 <= successes <= trials:
        raise ValueError("Invalid binomial counts")
    if trials == 0:
        return (float("nan"), float("nan"))
    if successes == 0:
        return 0.0, float(z*z/(trials+z*z))
    if successes == trials:
        return float(trials/(trials+z*z)), 1.0
    p = successes / trials
    denom = 1 + z*z/trials
    center = (p + z*z/(2*trials)) / denom
    radius = z/denom * np.sqrt(p*(1-p)/trials + z*z/(4*trials**2))
    return float(max(0,center-radius)), float(min(1,center+radius))


def summarize(result):
    n, k = result["reference_coincidences"], result["sample_coincidences"]
    lo, hi = wilson_interval(k, n)
    return {**result, "conditional_transmission": k/n if n else None,
            "conditional_transmission_ci95": [lo,hi],
            "contrast_pct": 100*(1-k/n) if n else None}


def scan_grid(size=11, extent_mm=75, primaries_per_point=15_000, seed=2026,
              geometry=None, readout=None):
    if size < 2:
        raise ValueError("size must be >= 2")
    coords = np.linspace(-extent_mm, extent_mm, size)
    transmission = np.zeros((size,size))
    count_ref = np.zeros((size,size), dtype=int)
    count_obj = np.zeros((size,size), dtype=int)
    for iy,y in enumerate(coords):
        for ix,x in enumerate(coords):
            o = simulate_pair(primaries_per_point, seed + iy*size + ix,
                              geometry, readout, x, y)
            count_ref[iy,ix] = o["reference_coincidences"]
            count_obj[iy,ix] = o["sample_coincidences"]
            transmission[iy,ix] = (count_obj[iy,ix]/count_ref[iy,ix]
                                   if count_ref[iy,ix] else np.nan)
    return coords, transmission, count_ref, count_obj
