# Electrochemical Conversion Modules

A high-fidelity, open-source Python suite for simulating, validating, and optimizing electrochemical energy conversion components. This repository houses verified, steady-state numerical models for both **Proton Exchange Membrane Electrolyzers (PEME)** and **Proton Exchange Membrane Fuel Cells (PEMFC)**. 

All modules are written in Python (Jupyter Notebooks) and cross-validated directly against Engineering Equation Solver (EES) benchmarks to guarantee thermodynamic and electrochemical precision down to the fourth decimal place.

---

## 📚 Associated Publications

These models form the computational framework for the following peer-reviewed research papers:

1. **H. Boodaghi**, et al. *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering** (2023). [DOI: 10.1007/s13369-023-08410-7](https://doi.org/10.1007/s13369-023-08410-7)
2. **H. Boodaghi**, et al. *"Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework."* **Thermal Science and Engineering Progress** (2026). [DOI: 10.1016/j.tsep.2026.104773](https://doi.org/10.1016/j.tsep.2026.104773)

---

## 🔬 Component Frameworks

### 1. PEM Fuel Cell Module (`PEMFC.ipynb`)
The fuel cell model utilizes a rigorous **Ulleberg-style semi-empirical formulation** rather than generalized textbook parameters. It cleanly handles mass transport and concentration drop-offs by lumping them directly into a current-dependent empirical membrane resistance function using a water-deficiency exponent ($\gamma = 1.2$).

Key mathematical elements implemented:
* **Interfacial Channel Depletion:** Accounts for localized reactant depletion along gas flow channels via exponential decay functions.
* **Activation Overpotential:** Evaluated using pre-fitted numerical kinetic coefficients matched to experimental data.
* **HHV Efficiency Tracking:** Evaluates first-law electrical efficiency directly against the Higher Heating Value (HHV) reference state of hydrogen ($\approx 285.83 \text{ kJ/mol}$).

### 2. PEM Electrolyzer Module (`PEME.ipynb`)
The inverse electrochemical process maps water splitting kinetics to determine precise voltage inputs, overpotentials, and high-purity hydrogen/oxygen production rates under varying thermal and pressure states.

---

## 📊 Validation & Verification Gate

The models are verified at a core reference operating point ($I = 100 \text{ A}$, $T_{\text{stack}} = 333.7 \text{ K}$, $P_{\text{in}} = 3.041 \text{ bar}$):

| Parameter | EES Baseline Target | Python Output | Validation Status |
| :--- | :---: | :---: | :---: |
| **Single Cell Voltage ($V_{\text{cell}}$)** | $0.6722 \text{ V}$ | **$0.6723 \text{ V}$** | **Converged (99.9%)** |
| **Stack Power ($W_{\text{elec}}$)** | $6.722 \text{ kW}$ | **$6.723 \text{ kW}$** | **Converged (99.9%)** |
| **Electrical Efficiency ($\eta_{\text{e}}$)** | $45.56\%$ | **$45.58\%$** | **Converged (99.9%)** |
| **$\text{H}_2$ Consumption/Flow Rate** | $69.69 \text{ SLPM}$ | **$69.69 \text{ SLPM}$** | **Converged (100.0%)** |
| **$\text{O}_2$ Consumption/Flow Rate** | $34.85 \text{ SLPM}$ | **$34.84 \text{ SLPM}$** | **Converged (99.9%)** |

---

## 🛠️ Dependencies & Execution

To run these notebooks locally within your JupyterLab or VS Code environment, ensure you have standard scientific computing libraries installed:

```bash
pip install numpy
