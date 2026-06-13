# %% [markdown]
# # Proton Exchange Membrane Electrolyzer (PEME) Model in Python
# 
# ## Overview
# This notebook provides a high-fidelity Python implementation of a mechanistic Proton Exchange Membrane Electrolyzer (PEME) model. The code simulates the inverse electrochemical process of a fuel cell, mapping water-splitting kinetics under high-precision thermodynamic constraints.
# 
# The model predicts:
# - Cell operating voltage ($V_{\text{cell}}$)
# - Anode and cathode activation overpotentials ($\eta_{\text{act,a}}$, $\eta_{\text{act,c}}$)
# - Integrated membrane ohmic resistance ($R_{\text{ohm}}$)
# - High-purity hydrogen mass flow and annual yields
# - First-law thermal efficiency (LHV basis)
# 
# ## Model Assumptions
# 
# - Steady-state operation
# - Isothermal cell
# - Negligible gas crossover
# - Uniform current density
# - Uniform pressure distribution
# - One-dimensional membrane hydration profile
# - Pure water feed
# - Ideal gas behavior for product gases
# 
# ---
# 
# ## Model Verification
# The present implementation reproduces the PEME operating conditions and results reported in:
# 
# 1. Homayoun Boodaghi, et al.  
#    *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering** (2023). https://doi.org/10.1007/s13369-023-08410-7
# 
# 2. Homayoun Boodaghi, et al.  
#    *"Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework."* **Thermal Science and Engineering Progress** (2026). https://doi.org/10.1016/j.tsep.2026.104773
# 
# ---
# 
# 

# %%
"""
=============================================================================
Proton Exchange Membrane Electrolyzer (PEME) Core Simulation Engine
=============================================================================
Author: Homayoun Boodaghi
Version: 1.1

Description:
  This module resolves multi-phase water splitting transport kinetics. It features
  Butler-Volmer activation mapping via inverse hyperbolic sines and definite 
  numerical integration of local membrane conductivity gradients.
=============================================================================
"""

import numpy as np
import CoolProp.CoolProp as CP
from scipy.integrate import quad

print("--- Step 1: Scientific Computing & Integration Libraries Loaded ---")

# %% [markdown]
# # 1. Input Parameters & Design Constants
# This section initializes all geometric properties, kinetic pre-exponential limits, operating boundaries, and thermochemical conversion constants. All units are standardized to SI base units or cleanly converted to match EES-validated states.

# %%
# =============================================================================
# 1. INPUT PARAMETERS (SI Units & Reference Conversions)
# =============================================================================

# ---------- Fluid Feed Configurations ----------
m_inlet_water = 0.1             # Mass flow rate of incoming fluid water [kg/s]
T_inlet_water = 40.0 + 273.15   # 40 °C converted to absolute Kelvin [K]
P_inlet_water = 100 * 1000      # 100 kPa converted to Pascal [Pa]
P_outlet_H2   = 100 * 1000      # 100 kPa converted to Pascal [Pa]

# ---------- Membrane & Geometry Boundaries ----------
lambda_a      = 14.0            # Dynamic water content at the anode-membrane boundary [-]
lambda_c      = 10.0            # Dynamic water content at the cathode-membrane boundary [-]
D             = 0.0001          # Solid polymer membrane thickness [m] (100 microns)
N_cells       = 1               # Total number of cells connected in the stack series [-]

# ---------- Kinetic Activation Constants ----------
J_ref_a       = 170000.0        # Anode pre-exponential exchange factor [A/m²]
J_ref_c       = 4600.0          # Cathode pre-exponential exchange factor [A/m²]
E_act_a       = 76000.0         # Activation energy barrier for the anode reaction [J/mol]
E_act_c       = 18000.0         # Activation energy barrier for the cathode reaction [J/mol]

# ---------- Target Operating Boundary ----------
J             = 5000.0          # System Operating Current Density [A/m²]

# ---------- Fundamental Constants ----------
F             = 96486.0         # Faraday constant [C/mol] (Electron transfer tracking)
R             = 8.3145          # Universal Gas Constant [J/mol-K]
LHV_H2        = 242.847 * 1000  # Lower Heating Value of Hydrogen [J/mol]

# ---------- Temporal Operations Metrics ----------
h_op          = 2072.0          # Total operational hours inside a standard calendar year
s_op          = h_op * 3600.0   # Operational window converted to total seconds [s]

print("--- Step 2: PEME Boundary Conditions & Design Constants Initialized ---")

# %% [markdown]
# # 2. CoolProp Fluid State Calculations
# Utilizes the high-fidelity CoolProp database to extract exact, real-fluid enthalpy ($H$) and entropy ($S$) values for the multi-phase water inlet and gas outlet streams.

# %%
# =============================================================================
# 2. ENTHALPY AND ENTROPY CALCULATIONS (Via CoolProp Real-Fluid Engine)
# =============================================================================

# 1. Incoming Feed Water Properties
H_inlet_water = CP.PropsSI('H', 'T', T_inlet_water, 'P', P_inlet_water, 'Water')
s_inlet_water = CP.PropsSI('S', 'T', T_inlet_water, 'P', P_inlet_water, 'Water')

# 2. Generated Outlet Oxygen Properties (Evaluated at inlet thermal equilibrium)
T_outlet_O2   = T_inlet_water
P_outlet_O2   = P_outlet_H2
H_outlet_O2   = CP.PropsSI('H', 'T', T_outlet_O2, 'P', P_outlet_O2, 'Oxygen')
s_outlet_O2   = CP.PropsSI('S', 'T', T_outlet_O2, 'P', P_outlet_O2, 'Oxygen')

# 3. Generated Outlet Hydrogen Properties 
T_outlet_H2   = T_inlet_water
H_outlet_H2   = CP.PropsSI('H', 'T', T_outlet_H2, 'P', P_outlet_H2, 'Hydrogen')
s_outlet_H2   = CP.PropsSI('S', 'T', T_outlet_H2, 'P', P_outlet_H2, 'Hydrogen')

print("--- Step 3: CoolProp Multi-Phase State Extraction Completed ---")

# %% [markdown]
# # 3. Electrochemical Polarization Loop
# Resolves the true operating cell potential by modeling the thermodynamic reversible Nernst baseline alongside a numerical integration across the localized membrane water-content gradient ($\lambda_x$).

# %%
# =============================================================================
# 3. HYDROGEN SPECIATION & ELECTROCHEMICAL LOSS RESOLUTION
# =============================================================================

# ---------- Faraday Split Molar Fluid Balances ----------
N_dot_H2_out      = N_cells * J / (2.0 * F)       # Hydrogen production rate [mol/s]
N_dot_H2O_reacted = N_cells * N_dot_H2_out        # Water consumption rate [mol/s]
N_dot_O2_out      = N_cells * J / (4.0 * F)       # Oxygen evolution rate [mol/s]
N_dot_H2O_out     = (m_inlet_water * 1000.0 / 18.02) - N_dot_H2O_reacted # Excess water output [mol/s]

# 1. Reversible Cell Potential (Nernst Baseline with Pressure Scaling)
V_0_base  = 1.229 - (8.5e-4 * (T_inlet_water - 298.15))
V_0_press = (R * T_inlet_water / F) * np.log(np.sqrt(P_outlet_H2 * P_outlet_O2) / P_inlet_water)
V_0       = V_0_base + V_0_press

# 2. Ohmic Overpotential via Continuous Integral Across Membrane Water Profile
def dydx_func(x):
    """ Computes the local inverse ionic conductivity [1/sigma] across thickness x """
    lambda_x = (((lambda_a - lambda_c) / D) * x) + lambda_c
    sigma_lambda_x = (0.5139 * lambda_x - 0.326) * np.exp(1268.0 * ((1.0 / 303.0) - (1.0 / T_inlet_water)))
    return 1.0 / sigma_lambda_x

# Execute exact definite numerical integration from x = 0 to x = D
R_ohm, _ = quad(dydx_func, 0, D)
V_ohm    = J * R_ohm

# 3. Activation Overpotential (Butler-Volmer Deconvolution via arcsinh)
J_0_a   = J_ref_a * np.exp(-E_act_a / (R * T_inlet_water))  # Anode exchange current density
J_0_c   = J_ref_c * np.exp(-E_act_c / (R * T_inlet_water))  # Cathode exchange current density

V_act_a = (R * T_inlet_water / F) * np.arcsinh(J / (2.0 * J_0_a))
V_act_c = (R * T_inlet_water / F) * np.arcsinh(J / (2.0 * J_0_c))

# 4. Total Operating Core Voltage Summation
V_cell  = V_0 + V_act_a + V_act_c + V_ohm
V_stack = V_cell * N_cells

print("--- Step 4: Multi-Physics Polarization Curve Losses Fully Resolved ---")

# %% [markdown]
# # 4. System Mass Balances & Annual Yield Metrics
# Computes the final fluid mass splits, real-world hydrogen yield configurations over an operating year, and first-law energy efficiencies.

# %%
# =============================================================================
# 4. VOLUMETRIC SYSTEM BALANCES & PERFORMANCE SUMMARY
# =============================================================================

# ---------- Absolute Mass Flow Rates [kg/s] ----------
m_H2_out           = 2.016 * N_dot_H2_out * 0.001
m_dot_H2O_out      = 18.016 * N_dot_H2O_out * 0.001
m_O2_out           = 32.000 * N_dot_O2_out * 0.001
m_O2_H2O_out       = m_O2_out + m_dot_H2O_out
m_dot_H2O_reacted  = 18.016 * N_dot_H2O_reacted * 0.001

# ---------- System Power & Energetic Efficiency ----------
W_dot_elec = (J * V_stack) / 1000.0   # Net Stack Power Input [kW]
eta_th_H2  = (LHV_H2 * N_dot_H2_out) / (W_dot_elec * 1000.0) # LHV Efficiency [-]

# ---------- Annual Production Yield Quantities [kg/year] ----------
m_dot_H2_prod = m_H2_out * s_op
m_dot_O2_prod = m_O2_out * s_op

# =============================================================================
# 5. EXPANDED PORTFOLIO REPRODUCIBILITY SUMMARY PRINTER
# =============================================================================
print(f"==================================================")
print(f"      PEME SYSTEM CONVERGENCE SUMMARY             ")
print(f"==================================================")
print(f"Reversible Potential (V_0)     : {V_0:.4f} V")
print(f"Anode Activation Loss (V_act,a): {V_act_a:.4f} V")
print(f"Cathode Activation Loss(V_act,c): {V_act_c:.4f} V")
print(f"Membrane Ohmic Loss (V_ohm)    : {V_ohm:.4f} V")
print(f"--------------------------------------------------")
print(f"Cell Operating Voltage (V_cell): {V_cell:.3f} V  ")
print(f"Stack Operating Voltage (V_stack): {V_stack:.3f} V  ")
print(f"Total Power Input (W_dot_elec) : {W_dot_elec:.2f} kW ")
print(f"Thermal LHV Efficiency         : {eta_th_H2 * 100:.2f} % ")
print(f"--------------------------------------------------")
print(f"H2 Mass Flow Output Rate       : {m_H2_out:.8f} kg/s")
print(f"Annual Hydrogen Yield          : {m_dot_H2_prod:.2f} kg/year")
print(f"==================================================")

# %% [markdown]
# # References
# 
# If this model is used in academic work, please cite:
# 
# 1. Homayoun Boodaghi, et al.  
#    *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering** (2023). https://doi.org/10.1007/s13369-023-08410-7
# 
# 2. Homayoun Boodaghi, et al.  
#    *"Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework."* **Thermal Science and Engineering Progress** (2026). https://doi.org/10.1016/j.tsep.2026.104773


