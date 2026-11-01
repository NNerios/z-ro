# =====================================================================
# CORE ENGINE: CER-C CYCLICAL QUANTUM FLUID DYNAMICS
# =====================================================================
import math

def calculate_fluid_state(density, rho_max, w_initial=-1.0):
    """
    Tracks Variable 1 (w) as virtual energy converts to real matter.
    As density drops during expansion, w transitions smoothly from -1 toward 0.
    """
    if rho_max <= 0:
        return w_initial
        
    density_ratio = density / rho_max
    
    # Smooth logistic transition of the state equation parameter
    w_dynamic = w_initial * density_ratio + 0.0 * (1.0 - density_ratio)
    
    # Enforce physical bounds: cannot be more negative than a pure vacuum (-1)
    return max(min(w_dynamic, 0.0), -1.0)

def calculate_bounce_modifier(density, rho_max):
    """
    Tracks Variable 2 (The AE Bounce Variable).
    Represents the shared denominator of quantum vacuum oscillations.
    Spikes to 1.0 when the universe reaches its maximum allowable density.
    """
    if rho_max <= 0 or density <= 0:
        return 0.0
        
    # Quadratic scaling model for quantum repulsion near the turnaround
    bounce_factor = (density / rho_max) ** 2
    
    # Cap at 1.0 to prevent mathematical divergence at the exact bounce point
    return min(bounce_factor, 1.0)

def calculate_h_squared(density, rho_max, G_eff=1.0):
    """
    Combines both fluid variables to calculate the net cosmic expansion rate (H^2).
    """
    # 1. Get the current state values from the variables
    w_val = calculate_fluid_state(density, rho_max)
    bounce_val = calculate_bounce_modifier(density, rho_max)
    
    # 2. Compute the macroscopic fluid expansion baseline
    fluid_expansion = G_eff * density
    
    # 3. Apply the microscopic quantum bounce correction modifier
    # As bounce_val approaches 1.0, (1.0 - bounce_val) goes to 0, stopping contraction
    h_squared_net = fluid_expansion * (1.0 - bounce_val)
    
    return max(0.0, h_squared_net)
