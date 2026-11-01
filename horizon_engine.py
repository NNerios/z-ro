# =====================================================================
# HORIZON ENGINE: CAUSAL BOUNDARIES & COSMIC HORIZONS
# =====================================================================
import math

def calculate_horizon_limit(w_current, baseline_horizon=14.0):
    """
    Calculates the boundary limit of the cosmic horizon.
    The changing fluid state parameter (w) dynamically alters the speed
    at which information propagates through the fluid substrate.
    """
    # In a dark energy/vacuum-dominated era (w close to -1), horizons freeze out.
    # In a matter-dominated era (w close to 0), the horizon opens up steadily.
    fluid_scaling_factor = 1.0 + w_current  # Shifting factor based on state
    
    # Dynamic calculation of causal information depth
    dynamic_horizon = baseline_horizon * math.exp(fluid_scaling_factor)
    
    return max(0.1, dynamic_horizon)

def calculate_hubble_radius(h_squared):
    """
    Computes the instantaneous Hubble Horizon (the speed of light sphere).
    """
    if h_squared <= 0:
        return float('inf')  # At the exact bounce point, the Hubble horizon expands to infinity
        
    h_current = math.sqrt(h_squared)
    c = 3.0e5  # Speed of light constant approximation (km/s)
    
    return c / h_current
