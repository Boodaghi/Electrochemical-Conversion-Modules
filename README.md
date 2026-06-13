# Electrochemical Conversion Modules

Welcome to the **Electrochemical-Conversion-Modules** repository. This open-access library features high-fidelity computational models for advanced electrochemical conversion cells, hydrogen conditioning arrays, and complex transient energy storage subsystems. 

By transitioning classic empirical or EES formulations into robust, self-contained Python structures, this suite provides researchers with high-throughput tools to track degradation boundaries, mass transfers, and voltage overpotential dynamics natively.

---

## 📚 Associated Publications

These models form the computational framework for the following peer-reviewed research papers:

1. **H. Boodaghi**, et al. *"Design and Performance Assessment of a Novel Poly-generation System with Stable Production of Electricity, Hydrogen, and Hot Water: Energy and Exergy Analyses."* **Arabian Journal for Science and Engineering** (2023). [DOI: 10.1007/s13369-023-08410-7](https://doi.org/10.1007/s13369-023-08410-7)
2. **H. Boodaghi**, et al. *"Achieving holistic sustainability in solar-hydrogen systems: A 6E-based multi-objective optimization of a PV–PEMFC–PEME–ORC integrated framework."* **Thermal Science and Engineering Progress** (2026). [DOI: 10.1016/j.tsep.2026.104773](https://doi.org/10.1016/j.tsep.2026.104773)

---

## 🔬 Component Frameworks

### 1. PEM Fuel Cell (`PEMFC.ipynb`)
The fuel cell model utilizes a rigorous **Ulleberg-style semi-empirical formulation** rather than generalized textbook parameters. It cleanly handles mass transport and concentration drop-offs by lumping them directly into a current-dependent empirical membrane resistance function using a water-deficiency exponent ($\gamma = 1.2$).

Key mathematical elements implemented:
* **Interfacial Channel Depletion:** Accounts for localized reactant depletion along gas flow channels via exponential decay functions.
* **Activation Overpotential:** Evaluated using pre-fitted numerical kinetic coefficients matched to experimental data.
* **HHV Efficiency Tracking:** Evaluates first-law electrical efficiency directly against the Higher Heating Value (HHV) reference state of hydrogen ($\approx 285.83 \text{ kJ/mol}$).

### 2. PEM Electrolyzer (`PEME.ipynb`)
The inverse electrochemical process maps water splitting kinetics to determine precise voltage inputs, overpotentials, and high-purity hydrogen/oxygen production rates under varying thermal and pressure states.

---

## 📂 Repository Architecture & Submodule Mapping

This workspace is explicitly structured into modular, self-contained subdirectories. Each module includes its own standalone documentation tracker, production scripts, and interactive visual workbooks:

```text
Electrochemical-Conversion-Modules/
├── CITATION.cff           # Global citation registry for academic indexing
├── README.md              # Global electrochemical portfolio front-page documentation
├── requirements.txt       # Unified environment package installation manifest
├── Battery/
│   ├── Battery.ipynb      # Non-linear Saupe-Schöner lead-acid battery voltage model
│   ├── Battery.py         # Production standalone battery bank runtime script
│   └── README.md          # Subfolder tracker mapping overpotential equations & gassing ramps
├── Hydrogen_Storage/
│   ├── Storage.ipynb      # Precision Leachman Fundamental EOS hydrogen tank model
│   ├── Storage.py         # Production standalone compressed gas charging script
│   └── README.md          # Subfolder tracker verifying quantum compressibility deviations
├── Oxygen_Storage/
│   ├── Storage.ipynb      # Precision Stewart-Jacobsen Fundamental EOS tank model
│   ├── Storage.py         # Production standalone compressed gas charging script
│   └── README.md          # Subfolder tracker verifying quantum compressibility deviations
├── PEME/
│   ├── PEME.ipynb         # Proton Exchange Membrane Electrolyzer electrochemical cell stack model
│   ├── PEME.py            # The production-ready standalone Python runtime execution script
│   └── README.md          # Validation tracking descriptor linked to the 2026 TSEP paper
└── PEMFC/
    ├── PEMFC.ipynb        # Proton Exchange Membrane Fuel Cell polarization overpotential model
    ├── PEME.py            # The production-ready standalone Python runtime execution script    
    └── README.md          # Validation tracking descriptor linked to the 2026 TSEP paper

```

## 🛠️ Dependencies & Execution

To run these notebooks locally within your JupyterLab or VS Code environment, ensure you have standard scientific computing libraries installed:

```bash
pip install numpy matplotlib pandas scipy coolprop 
