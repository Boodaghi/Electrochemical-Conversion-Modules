# Proton Exchange Membrane Electrolyzer (PEME) Module

This directory contains the computational framework for simulating a mechanistic Proton Exchange Membrane Electrolyzer (PEME). 

## 📋 Contents
* `PEME.ipynb`: The primary interactive Jupyter Notebook featuring high-fidelity code comments, Markdown descriptions, and step-by-step verification plots.
* `PEME.py`: The production-ready standalone Python runtime execution script.

## 🔬 Mathematical Base
The modeling engine tracks multi-phase water splitting transport kinetics. It implements:
* Butler-Volmer activation dynamics mapped via accurate inverse hyperbolic sine functions.
* Definite numerical integration across the localized membrane thickness to capture the water-content gradient ($\lambda_x$).