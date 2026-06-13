# Proton Exchange Membrane Fuel Cell (PEMFC) Module

This directory contains the computational framework for simulating a semi-empirical Proton Exchange Membrane Fuel Cell (PEMFC) stack.

## 📋 Contents
* `PEMFC.ipynb`: The interactive Jupyter Notebook featuring academic documentation, parameter breakdowns, and verification printouts.
* `PEMFC.py`: The optimized standalone Python script for modular system integration.

## 🔬 Mathematical Base
The model bypasses simplified textbook assumptions in favor of a specialized **Ulleberg-style steady-state electrochemical formulation**:
* **Interfacial Pressure Decay:** Evaluates localized reactant depletion along the gas channels via exponential decay functions.
* **Lumped Losses:** Integrates mass transport and concentration drop-offs directly into a current-dependent empirical membrane resistance function using a water-deficiency exponent ($\gamma = 1.2$).