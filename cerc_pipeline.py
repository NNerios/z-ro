# =====================================================================
# MASTER PIPELINE: CER-C CYCLICAL SIMULATION WITH 32 CC DATA & BIC
# =====================================================================
import math
import core_engine
import horizon_engine

# --- 32 COSMIC CHRONOMETER EXPERIMENTAL DATA SET (0.07 <= z <= 1.965) ---
# Format: (redshift_z, H_observed, error_sigma)
# Group A: 17 Independent data points (No shared systematics)
CC_17_INDEPENDENT = [
    (0.070, 69.0, 19.6), (0.090, 69.0, 12.0), (0.120, 68.6, 26.2),
    (0.170, 83.0, 8.0),  (0.179, 75.0, 4.0),  (0.199, 75.0, 5.0),
    (0.200, 72.9, 29.6), (0.270, 77.0, 14.0), (0.280, 88.8, 36.6),
    (0.352, 83.0, 14.0), (0.380, 83.0, 13.5), (0.400, 95.0, 17.0),
    (0.444, 93.0, 8.5),  (0.478, 110.9, 11.2), (0.480, 97.0, 62.0),
    (0.593, 104.0, 13.0), (0.680, 92.0, 8.0)
]

# Group B: 15 Covariance data points (Correlated systematics)
CC_15_CORRELATED = [
    (0.781, 105.0, 12.0), (0.875, 125.0, 17.0), (0.880, 101.0, 10.0),
    (0.900, 117.0, 23.0), (1.037, 154.0, 20.0), (1.300, 168.0, 17.0),
    (1.363, 160.0, 33.6), (1.430, 177.0, 18.0), (1.530, 140.0, 14.0),
    (1.750, 202.0, 40.0), (1.965, 186.5, 50.4), (0.350, 82.7, 9.1),
    (0.570, 96.8, 6.4),  (1.260, 135.0, 11.0), (1.100, 120.0, 15.0)
]

def generate_mock_inverse_covariance(points):
    """
    Simulates the inverse covariance matrix (C^-1) for the 15 systematic points.
    In real astrophysics, this is imported from a file.
    """
    n = len(points)
    inv_cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        # Diagonal elements are 1 / sigma^2
        inv_cov[i][i] = 1.0 / (points[i][2] ** 2)
        # Off-diagonal elements represent correlated systematic cross-talk
        for j in range(n):
            if i != j:
                inv_cov[i][j] = 0.05 / (points[i][2] * points[j][2])
    return inv_cov

def run_bic_evaluation():
    print("--- STARTING CER-C COVARIANCE PIPELINE ---")
    
    # 1. Initialize Free Parameters for the Cyclical Model
    rho_max = 1000.0  # Maximum quantum density scale
    G_eff = 50.0      # Effective gravitational coupling parameter
    num_params = 2    # Free parameters tuned (rho_max, G_eff)
    num_data_points = len(CC_17_INDEPENDENT) + len(CC_15_CORRELATED)
    
    chi2_total = 0.0
    
    # 2. Compute Chi-Squared for the 17 Independent Data Points
    print("Processing independent cosmic chronometers...")
    for z, h_obs, sigma in CC_17_INDEPENDENT:
        # Simulate density scaling down as a function of redshift (early universe)
        simulated_density = rho_max / (1.0 + z)**3
        
        # Pull expansion calculations directly from your core_engine
        h2_predicted = core_engine.calculate_h_squared(simulated_density, rho_max, G_eff)
        h_predicted = math.sqrt(h2_predicted)
        
        # Standard chi-squared step
        chi2_total += ((h_predicted - h_obs) / sigma) ** 2
        
    # 3. Compute Chi-Squared for the 15 Correlated Covariance Data Points
    print("Processing correlated systematic covariance matrix...")
    residuals = []
    for z, h_obs, sigma in CC_15_CORRELATED:
        simulated_density = rho_max / (1.0 + z)**3
        h2_predicted = core_engine.calculate_h_squared(simulated_density, rho_max, G_eff)
        h_predicted = math.sqrt(h2_predicted)
        residuals.append(h_predicted - h_obs)
        
    # Apply matrix algebra: Delta_H^T * C^-1 * Delta_H
    inv_cov = generate_mock_inverse_covariance(CC_15_CORRELATED)
    chi2_sys = 0.0
    for i in range(len(residuals)):
        for j in range(len(residuals)):
            chi2_sys += residuals[i] * inv_cov[i][j] * residuals[j]
            
    chi2_total += chi2_sys
    
    # 4. Calculate the Bayesian Information Criterion (BIC)
    # Formula: BIC = chi^2 + k * ln(n)
    # Penalizes models for adding too many arbitrary variables!
    bic_score = chi2_total + num_params * math.log(num_data_points)
    
    # 5. Output metrics to Pydroid Terminal
    print("\n==============================")
    print("📊 MODEL EVALUATION COMPLETE")
    print("==============================")
    print(f"Total Combined Data Points (n): {num_data_points}")
    print(f"Model Parameters Tuned (k):    {num_params}")
    print(f"Total Calculated Chi-Square:   {chi2_total:.4f}")
    print(f"🔵 CYCLICAL MODEL BIC SCORE:  {bic_score:.4f}")
    print("==============================")
    print("💡 Ready for statistical comparison against Lambda-CDM.")

if __name__ == "__main__":
    run_bic_evaluation()
