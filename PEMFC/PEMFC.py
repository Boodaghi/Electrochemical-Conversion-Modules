# %% [markdown]
# # Proton Exchange Membrane Fuel Cell (PEMFC) Model in Python
# 
# ## Overview
# 
# This repository provides a Python implementation of a semi-empirical Proton Exchange Membrane Fuel Cell (PEMFC) model that has been employed and validated in multiple peer-reviewed journal publications.
# 
# The model predicts:
# 
# - Cell voltage
# - Stack voltage
# - Power output
# - Current density
# - Hydrogen consumption
# - Oxygen consumption
# - Electrical efficiency
# 
# under specified operating conditions.
# 
# The implementation follows the same governing equations and assumptions used in the published studies listed below.
# 
# ---
# 
# ## Associated Publications
# 
# 1. Homayoun Boodaghi et al.
# 
#    "Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses.". Arabian Journal for Science and Engineering (2023). https://doi.org/10.1007/s13369-023-08410-7
# 
# 2. Homayoun Boodaghi et al.
# 
#    "Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework". Thermal Science and Engineering Progress (2026). https://doi.org/10.1016/j.tsep.2026.104773
# 
# ---
# 
# ## Model Characteristics
# 
# Type:
# Semi-empirical PEMFC model
# 
# Operating regime:
# Steady-state
# 
# Fuel:
# Pure hydrogen
# 
# Oxidant:
# Pure oxygen
# 
# Outputs:
# 
# - Reversible voltage
# - Activation overpotential
# - Ohmic overpotential
# - Cell voltage
# - Stack voltage
# - Electrical power
# - Reactant consumption rates
# - Electrical efficiency
# 
# ---
# 
# ## Purpose
# 
# This notebook aims to provide a transparent, reproducible, and open-source implementation of the PEMFC model used throughout the author's published research.
# 
# The code can be used independently or integrated into larger renewable-energy, hydrogen, and sustainability assessment frameworks.

# %%
"""
PEMFC Python Model

Author: Homayoun Boodaghi
Version: 1.0

This notebook reproduces the electrochemical
performance of a PEMFC stack using the
"""

import numpy as np

print("Libraries imported successfully.")

# %% [markdown]
# # Input Parameters
# 
# This section contains all operating and design parameters.
# 
# Units:
# 
# - Temperature → K
# - Pressure → bar
# - Area → cm²
# - Thickness → cm
# - Current → A

# %%
# ==========================================================
# INPUT PARAMETERS
# ==========================================================

# ---------- Stack Configuration ----------

N_cells = 100          # Number of cells

# ---------- Membrane Properties ----------

A_PEM = 232.0          # Active membrane area [cm²]
t_PEM = 0.018          # Membrane thickness [cm]

# ---------- Empirical Coefficient ----------

gamma = 1.2

# ---------- Operating Conditions ----------

I_FC = 100.0           # Stack current [A]

T_stack = 333.7        # Stack temperature [K]

p_a_in = 3.041         # Anode pressure [bar]
p_c_in = 3.041         # Cathode pressure [bar]

# ---------- Physical Constants ----------

F = 96487              # Faraday constant [C/mol]

print("Input parameters loaded.")

# %% [markdown]
# # Gas Partial Pressures
# 
# The hydrogen and oxygen partial pressures are calculated using the empirical relationships.
# 
# These equations account for pressure losses caused by electrochemical consumption.
# 
# The oxygen concentration is then calculated and used in the activation overpotential correlation.

# %%
# ==========================================================
# PARTIAL PRESSURES
# ==========================================================

# Saturation pressure correlation
# Valid near PEMFC operating temperatures

p_H2O_sat = (
    25.7
    - 1.615e-1 * T_stack
    + 2.55e-4 * T_stack**2
)

# Hydrogen partial pressure [bar]

p_H2 = (
    p_a_in
    * np.exp(
        (-1.653 * I_FC)
        / (A_PEM * T_stack**1.334)
    )
    - 0.5 * p_H2O_sat
)

# Oxygen partial pressure [bar]

p_O2 = (
    p_c_in
    * np.exp(
        (-4.192 * I_FC)
        / (A_PEM * T_stack**1.334)
    )
    - p_H2O_sat
)

# Oxygen concentration

c_O2 = (
    1.969e-7
    * np.exp(498 / T_stack)
    * p_O2
)

print("Hydrogen partial pressure =", round(p_H2, 4), "bar")
print("Oxygen partial pressure   =", round(p_O2, 4), "bar")
print("Oxygen concentration      =", f"{c_O2:.4e}")

# %% [markdown]
# # Electrochemical Model
# 
# The cell voltage is computed as:
# 
# Vcell = E + ηact + ηohmic
# 
# where:
# 
# - E = reversible voltage
# - ηact = activation loss
# - ηohmic = ohmic loss
# 
# All equations are directly inherited from the original EES implementation.

# %%
# ==========================================================
# REVERSIBLE VOLTAGE
# ==========================================================

E = (
    1.23
    - 8.5e-4 * (T_stack - 298)
    + 4.31e-5 * T_stack
      * np.log(
          p_H2 * np.sqrt(p_O2)
      )
)

# ==========================================================
# ACTIVATION OVERPOTENTIAL
# ==========================================================

eta_act = (
    -0.95
    + 2.43e-3 * T_stack
    + 1.92e-4 * T_stack * np.log(A_PEM)
    - 1.92e-4 * T_stack * np.log(I_FC)
    + 7.6e-5 * T_stack * np.log(c_O2)
)

# ==========================================================
# OHMIC OVERPOTENTIAL
# ==========================================================

eta_ohmic = (
    (-I_FC * t_PEM / A_PEM)
    * (
        8 /
        np.exp(
            3.6 * (T_stack - 353)
            / T_stack
        )
    )
    * (
        1
        + 1.64 * I_FC / A_PEM
        + gamma * (I_FC / A_PEM)**3
    )
)

# ==========================================================
# CELL AND STACK VOLTAGE
# ==========================================================

U_cell = E + eta_act + eta_ohmic

U_stack = N_cells * U_cell

print("Reversible voltage     =", round(E, 4), "V")
print("Activation loss        =", round(eta_act, 4), "V")
print("Ohmic loss             =", round(eta_ohmic, 4), "V")
print("Cell voltage           =", round(U_cell, 4), "V")
print("Stack voltage          =", round(U_stack, 2), "V")

# %% [markdown]
# # Power Output
# 
# Electrical power is calculated from:
# 
# P = V × I
# 
# Both cell and stack powers are reported.

# %%
# ==========================================================
# POWER CALCULATIONS
# ==========================================================

P_cell = U_cell * I_FC

P_stack = U_stack * I_FC

i_density = (
    I_FC / A_PEM
) * 1000

i_density_ASF = (
    I_FC /
    (A_PEM / 929.0304)
)

print("Cell power            =", round(P_cell, 2), "W")
print("Stack power           =", round(P_stack, 2), "W")
print("Current density       =", round(i_density, 1), "mA/cm²")
print("Current density ASF   =", round(i_density_ASF, 1))

# %% [markdown]
# # Energy Efficiency
# 
# The electrical (first-law) efficiency of the PEMFC is calculated using the thermoneutral voltage:
# 
# ηₑ = Ucell / Utn
# 
# where:
# 
# - ηₑ = electrical efficiency [-]
# - Ucell = operating cell voltage [V]
# - Utn = thermoneutral voltage [V]
# 
# The thermoneutral voltage represents the maximum voltage obtainable if the entire enthalpy change of the electrochemical reaction were converted into useful work.
# 
# For hydrogen fuel cells, a commonly accepted value is:
# 
# Utn = 1.475 V
# 
# This metric quantifies the fraction of the fuel's energy that is converted into electrical power.

# %%
# ==========================================================
# ENERGY EFFICIENCY
# ==========================================================

# Thermoneutral voltage for hydrogen fuel cell
# Based on the higher heating value (HHV)

U_tn = 1.475  # [V]

# Electrical efficiency (first-law efficiency)

ETA_e = U_cell / U_tn

print("----- ENERGY EFFICIENCY -----")
print(f"Thermoneutral voltage = {U_tn:.3f} V")
print(f"Electrical efficiency = {ETA_e:.4f} (-)")
print(f"Electrical efficiency = {ETA_e*100:.2f} %")

# %% [markdown]
# # Reactant Consumption
# 
# Hydrogen and oxygen consumptions are calculated using Faraday's law.
# 
# Hydrogen reaction:
# 
# H₂ → 2H⁺ + 2e⁻
# 
# Oxygen reaction:
# 
# ½O₂ + 2H⁺ + 2e⁻ → H₂O

# %%
# ==========================================================
# STOICHIOMETRIC RATIOS
# ==========================================================

S_H2 = 1.15
S_O2 = 2.00

rho_ideal_gas = 0.04462

# ==========================================================
# FARADAY LAW
# ==========================================================

n_dot_H2_a_cons = (
    N_cells * I_FC
) / (2 * F)

n_dot_O2_c_cons = (
    N_cells * I_FC
) / (4 * F)

# ==========================================================
# STANDARD LPM
# ==========================================================

V_H2_a_cons = (
    n_dot_H2_a_cons
    / rho_ideal_gas
    * 60
)

V_O2_c_cons = (
    n_dot_O2_c_cons
    / rho_ideal_gas
    * 60
)

V_H2_a_in = S_H2 * V_H2_a_cons
V_O2_c_in = S_O2 * V_O2_c_cons

V_H2_a_out = V_H2_a_in - V_H2_a_cons
V_O2_c_out = V_O2_c_in - V_O2_c_cons

print("Hydrogen consumption =", round(n_dot_H2_a_cons, 5), "mol/s")
print("Oxygen consumption  =", round(n_dot_O2_c_cons, 5), "mol/s")

# %% [markdown]
# # Model Verification
# 
# The numerical outputs obtained from this notebook reproduce the results reported in the associated peer-reviewed publications.
# 
# The implementation follows the same governing equations, constants, operating assumptions, and parameter values used in the published studies.
# 
# The notebook therefore serves as an open-source reference implementation of the validated PEMFC model.

# %%
# ==========================================================
# REFERENCE PERFORMANCE POINT
# ==========================================================

print("----- REFERENCE OPERATING POINT -----")

print(f"Cell voltage          : {U_cell:.4f} V")
print(f"Stack voltage         : {U_stack:.2f} V")
print(f"Stack power           : {P_stack:.2f} W")
print(f"Electrical efficiency : {ETA_e:.4f}")
print(f"H2 consumption        : {n_dot_H2_a_cons:.5f} mol/s")
print(f"O2 consumption        : {n_dot_O2_c_cons:.5f} mol/s")

# %% [markdown]
# # References
# 
# If this model is used in academic work, please cite:
# 
# Boodaghi, H., et al.
# Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses. Arabian Journal for Science and Engineering, 2023. https://doi.org/10.1007/s13369-023-08410-7
# 
# Boodaghi, H., et al.
# Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV-PEMFC-PEME-ORC integrated framework. Thermal Science and Engineering Progress, 2026. https://doi.org/10.1016/j.tsep.2026.104773


