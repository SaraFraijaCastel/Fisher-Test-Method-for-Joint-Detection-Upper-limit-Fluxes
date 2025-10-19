This project is the application of Fisher's Statistical Method to calculate joint probability in a sample.
Here the sample consists on Gamma ray Bursts (GRBs) obtained trough the Fermi-Database. Data were cleaned,
those GRBs with redshifts less than 5 and with large uncertainty in position  (less than 1 degree) were ruled out.

Analysis of the Whole GRB distribution was made using Fisher's method supposing a normal distribution.  
The project is made this way:
# ULs — Upper Limits pipeline

This repository contains scripts and utilities to generate and run upper-limit (UL) calculations for GRBs. It includes generators for batch Bash scripts, plotting utilities and configuration loaders.

## Quick overview
- Generate per-GRB Bash jobs to run `zebra-flux-norm-fit` and collect ULs.
  - Generator (parallel per-GRB): [`libraries.ul_script_paral.generate_ul_script`](codes/libraries/ul_script_paral.py) and runner [`libraries.ul_script_paral.run_ul_scripts`](codes/libraries/ul_script_paral.py) — see [codes/libraries/ul_script_paral.py](codes/libraries/ul_script_paral.py).
  - Monolithic generator: [`libraries.ul_script.generate_ul_script`](codes/libraries/ul_script.py) and runner [`libraries.ul_script.run_ul_scripts`](codes/libraries/ul_script.py) — see [codes/libraries/ul_script.py](codes/libraries/ul_script.py).

- Plotting and UL post-processing:
  - Plot generator: [`libraries.ul_plot.generate_upper_limits_plots`](codes/libraries/ul_plot.py) — see [codes/libraries/ul_plot.py](codes/libraries/ul_plot.py).
  - Small utilities used by plotting: [`others.up_plot.get_ul_value`](codes/others/up_plot.py) — see [codes/others/up_plot.py](codes/others/up_plot.py).

- Configuration and entry points:
  - YAML loader: [`libraries.load_config.load_config`](codes/libraries/load_config.py) — see [codes/libraries/load_config.py](codes/libraries/load_config.py).
  - Notebook examples: [codes/main.ipynb](codes/main.ipynb), [codes/libraries/Tets_rapidos/Fisher.ipynb](codes/Tets_rapidos/Fisher.ipynb) (examples in repo).

- Example generated Bash job (one of many): [scripts/PSF/alfa=2.07/pseudo/UL1_Franceschini08_0.3_ER_GRB201214672.sh](scripts/PSF/alfa=2.07/pseudo/UL1_Franceschini08_0.3_ER_GRB201214672.sh)

## Typical workflow

1. Edit configuration (paths, bin_size, EBL list, etc.) in:
   - [config/config.yml](config/config.yml)
   - use the loader: [`libraries.load_config.load_config`](codes/libraries/load_config.py)

2. Generate and submit scripts:
   - From Python (example):
     ```py
     from libraries.load_config import load_config
     from libraries.ul_script_paral import run_ul_scripts
     cfg = load_config('config/config.yml')
     run_ul_scripts(cfg)
     ```
     (See [`libraries.ul_script_paral.run_ul_scripts`](codes/libraries/ul_script_paral.py) for details.)

   - The generators create Bash scripts under the `scripts/` tree (e.g. [scripts/PSF/...](scripts/PSF/)) and write sbatch lines to batch launcher files.

3. Inspect results:
   - Output CSVs are written to the `data/ULs/files/...` locations controlled by config (see `OUTPUT_folder` in [config/config.yml](config/config.yml)).
   - Plot results using [`libraries.ul_plot.generate_upper_limits_plots`](codes/libraries/ul_plot.py) or the notebooks in `codes/`.

## Useful paths
- Script generators and runners:
  - [codes/libraries/ul_script_paral.py](codes/libraries/ul_script_paral.py)
  - [codes/libraries/ul_script.py](codes/libraries/ul_script.py)
- Plotting:
  - [codes/libraries/ul_plot.py](codes/libraries/ul_plot.py)
  - [codes/others/up_plot.py](codes/others/up_plot.py)
- Config:
  - [config/config.yml](config/config.yml)
- Example generated scripts:
  - [scripts/PSF/alfa=2.07/pseudo/UL1_Franceschini08_0.3_ER_GRB201214672.sh](scripts/PSF/alfa=2.07/pseudo/UL1_Franceschini08_0.3_ER_GRB201214672.sh)

## Notes & tips
- The loader [`libraries.load_config.load_config`](codes/libraries/load_config.py) builds derived paths (PATH_GENERAL, GRBsINFO, etc.) from the YAML — prefer using it to avoid path mistakes.
- Generated Bash scripts use `sbatch` headers suitable for your SLURM cluster; inspect logs referenced in the headers for run details.
- If you need per-GRB isolation (one job per GRB) use the parallel generator [`libraries.ul_script_paral.generate_ul_script`](codes/libraries/ul_script_paral.py). For single large job use [`libraries.ul_script.generate_ul_script`](codes/libraries/ul_script.py).
