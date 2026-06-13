# High-Fidelity Compressed Oxygen Storage Module

This directory houses the transient real-gas simulation suite for a compressed oxygen ($O_2$) gas cylinder network. The engine tracks molecular accumulation dynamics, compressibility variations, and volumetric storage safety margins.

## 📋 Contents
* `Storage.ipynb`: Interactive Jupyter Notebook featuring the Stewart-Jacobsen Fundamental EOS framework, real-gas attraction mapping loops, and diurnal pressure accumulation charts.
* `Storage.py`: Standalone production-ready Python execution script for macro-system coupling.

## 🔬 Scholarly Reference & Validation Source
The baseline volume scales, inlet mass ratios, and multi-physics coupling parameters match the engineering design criteria for byproduct gas capture in:

> **Boodaghi, H.**, et al. (2023). *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering**, 48. [DOI: 10.1007/s13369-023-08410-7](https://doi.org/10.1007/s13369-023-08410-7)

## 📊 Core Governing Physics & Safety
* **Stewart-Jacobsen Fundamental EOS:** Replaces typical cubic equations of state (which struggle to accurately resolve real-gas density gradients near critical points) with the benchmark Helmholtz formulation implemented across NIST REFPROP and CoolProp databases.
* **Non-Linear Compressibility Dips:** Natively captures the real-gas attraction phase. At room temperature ($25^\circ C$) and moderate pressures ($10\text{--}120\text{ bar}$), oxygen's intermolecular attractive forces dominate, causing the compressibility factor to dip below ideal limits ($Z < 1.0$) so it compresses more easily.
* **Regulated Safety Ceiling:** Modeled with an absolute operational ceiling of **150 bar** to strictly mirror industrial pure-oxygen handling safety protocols, mitigating spontaneous compression-ignition risks.