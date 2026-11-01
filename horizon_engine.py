# =====================================================================
# HORIZON ENGINE: CAUSAL BOUNDARIES ADJUSTED FOR VISCOUS ENGINES
# =====================================================================
import math

def calculate_horizon_limit(w_current, baseline_horizon=14.0):
    """
    Calculates particle horizon limits scaled by dynamic fluid changes.
    """
    fluid_scaling_factor = 1.0 + w_current
    dynamic_horizon = baseline_horizon * math.exp(fluid_scaling_factor)
    return max(0.1, dynamic_horizon)

def calculate_hubble_radius(h_squared):
    """
    Computes instantaneous Hubble Horizon sphere directly from viscous H^2.
    """
    if h_squared <= 0:
        return float('inf')
    h_current = math.sqrt(h_squared)
    c = 299792.458  # Speed of light (km/s)
    return c / h_current
