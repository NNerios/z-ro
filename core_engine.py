# =====================================================================
# CORE ENGINE: CER-C DECAY, POLARIZATION SPRING & BULK VISCOSITY
# =====================================================================
import math

def calculate_quantum_decay_w(density, rho_max, decay_constant=0.1, w_initial=-1.0):
    """
    TRACKS FORMULA 1: The w Vacuum-to-Matter Decay Equation.
    As density drops, virtual vacuum energy decays exponentially into matter.
    """
    if rho_max <= 0:
        return w_initial
    density_ratio = density / rho_max
    decay_profile = math.exp(-decay_constant * (1.0 - density_ratio))
    w_dynamic = w_initial * density_ratio * decay_profile
    return max(min(w_dynamic, 0.0), -1.0)

def calculate_repulsive_pressure_AE(density, rho_max, polarization_power=2.0):
    """
    TRACKS FORMULA 2: The AE Quantum Repulsive Pressure Formula.
    Saturates at 1.0 at the absolute turn-around point to prevent singularity.
    """
    if rho_max <= 0 or density <= 0:
        return 0.0
    bounce_factor = (density / rho_max) ** polarization_power
    return min(bounce_factor, 1.0)

def calculate_viscous_pressure(density, zeta, h_squared, is_contracting=False):
    """
    TRACKS FORMULA 3: Bulk Viscosity (Zeta).
    Simulates quantum particle production friction.
    Breaks mirror symmetry: acts as stabilizing push in contraction, drag in expansion.
    """
    if h_squared <= 0 or zeta == 0:
        return 0.0
    h_current = math.sqrt(h_squared)
    # H is negative during contraction, positive during expansion
    h_sign = -1.0 if is_contracting else 1.0
    return -3.0 * (h_current * h_sign) * zeta

def calculate_h_squared(density, rho_max, G_eff=1.0, decay_constant=0.1, zeta=0.02, is_contracting=False):
    """
    COMBINED ENGINE MASTER LOGIC WITH VISCOSITY INTERACTION
    """
    # 1. First pass calculation of baseline expansion velocity to feed viscosity loop
    w_val = calculate_quantum_decay_w(density, rho_max, decay_constant)
    AE_val = calculate_repulsive_pressure_AE(density, rho_max)
    
    macro_baseline = G_eff * density
    h2_interim = max(0.0, macro_baseline * (1.0 - AE_val))
    
    # 2. Compute dynamic fluid friction using the interim H value
    p_viscous = calculate_viscous_pressure(density, zeta, h2_interim, is_contracting)
    
    # 3. Apply the viscosity correction to the net energy expansion framework
    # In standard units, viscous pressure modifies effective energy density conversion
    macro_viscous_adjusted = max(0.0, macro_baseline - (p_viscous / max(density, 1e-5)))
    
    h_squared_net = macro_viscous_adjusted * (1.0 - AE_val)
    return max(0.0, h_squared_net)
