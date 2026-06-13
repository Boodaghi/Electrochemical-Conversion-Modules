# Non-Linear Quasi-Static Lead-Acid Battery Module

This directory houses the electrochemical simulation suite for a multi-cell lead-acid battery bank (Pb-accumulator). The engine tracks voltage dynamics and chemical capacity overvoltage drifts across charging and discharging profiles.

## 📋 Contents
* `Battery.ipynb`: Interactive Jupyter Notebook featuring self-contained Saupe-Schöner math models, multi-stage overpotential scaling, and diurnal performance diagnostics.
* `Battery.py`: Standalone production-ready Python execution script.



## 📊 Core Governing Physics
* **Saupe Polarization Model:** Isolates independent charge/discharge paths for overvoltage calculations ($U_{\text{pol}}$) rather than relying on a fixed internal resistance value.
* **Schöner Gassing Losses:** Maps temperature-dependent parasitic current leaks ($I_{\text{gas}}$) across an exponential Arrhenius-style threshold function. When terminal voltages approach full-charge capacities, excess power shifts dynamically into water electrolysis (gas dissipation).
* **State of Charge (SoC):** Integrates net chemical reaction current ($I_q$) across discrete time intervals ($\Delta t = 0.25\text{ hr}$) to map battery bank storage capacity levels.