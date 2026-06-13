# High-Fidelity High-Pressure Real-Gas Hydrogen Storage Module

This directory contains the computational simulation framework for a compressed hydrogen gas storage vessel. The engine uses a fundamental explicit Helmholtz energy equation of state to track real-gas density deviations under continuous charging profiles.

## 📋 Contents
* `Storage.ipynb`: Interactive Jupyter Notebook featuring the Leachman Fundamental EOS framework, compressibility tracking loops, and diurnal pressure accumulation charts.
* `Storage.py`: Standalone production-ready Python execution script for system integrations.

## 🔬 Scholarly Reference & Validation Source
The baseline system volume scales, initial cushion pressure limits, and multi-physics coupling parameters align with the high-pressure gas storage circuit evaluated in:

> **Boodaghi, H.**, et al. (2023). *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering**, 48. [DOI: 10.1007/s13369-023-08410-7](https://doi.org/10.1007/s13369-023-08410-7)

> **H. Boodaghi**, et al. *"Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework."* **Thermal Science and Engineering Progress** (2026). [DOI: 10.1016/j.tsep.2026.104773](https://doi.org/10.1016/j.tsep.2026.104773)

## 📊 Core Governing Physics
* **Leachman Fundamental EOS Benchmark:** Replaces typical cubic equations of state (which miscalculate hydrogen's quantum deviations near room temperature) with the benchmark Helmholtz formulation implemented across NIST REFPROP and CoolProp databases. Density uncertainty remains below 0.04% over the engineering range.
* **Real-Gas Compressibility Mapping:** Captures the dynamic shift of the compressibility factor ($Z > 1.0$) caused by molecular repulsion under high pressures.
* **Mass Conservation Law:** Integrates hourly electrolyzer hydrogen mass yields directly to track transient density accumulations ($\rho = m/V$) inside a rigid $2.5\text{ m}^3$ cylinder shell.