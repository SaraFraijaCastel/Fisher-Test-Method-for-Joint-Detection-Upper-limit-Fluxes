import os
import pandas as pd
import numpy as np
import shutil

def generate_bash_script(grb, ra, dec1, bin_size, path, config):
    GRBs = pd.read_csv(config['GRBsINFO'])
    PATH_GENERAL = config['PATH_GENERAL']
    OUTPUT_folder = config['OUTPUT_folder']
    LABELS = config['LABELS']
    Delta=config['Delta']
    dec=dec1+Delta
    PATH_CODES = os.path.join(PATH_GENERAL, 'scripts')
    os.makedirs(OUTPUT_folder, exist_ok=True)
    os.makedirs(PATH_GENERAL, exist_ok=True)

    window_size = bin_size * 2
    PATH_GRBs = os.path.join(path, grb)
    hist_path = os.path.join(PATH_GENERAL, 'SIG_ALL_GRBs')
    BINSIZE_FORCE=config['FORCE_BINSIZE']
    os.makedirs(hist_path, exist_ok=True)
    if BINSIZE_FORCE==True:
        bin_size=bin_size
    else:    
        bin_size = max(bin_size, GRBs.loc[GRBs['Name'] == grb, 'Error_Radius'].values[0])

    script = f"""#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o {PATH_GRBs}/{grb}/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J UL{grb}
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || {{ echo >&2 "plotMercator.py no encontrado"; exit 1; }}

RA={ra}
DEC={dec}
Bin_size={bin_size}
Hist_path={hist_path}
Window_size={window_size}
for Label in {LABELS[0]} {LABELS[1]}; do
    GRB={grb}_$Label
    label2=${{Label%%_*}}
    output_file={hist_path}/{grb}_PSF_{bin_size}_Hist$Label.txt
    max_output_file={PATH_GENERAL}/MaxSigHist_{bin_size}_${{label2}}.txt
    rm -f "$output_file"

    transit_file={PATH_GRBs}/transit_${{label2}}/{grb}_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "{hist_path}/{grb}.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "{grb},$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for {grb} label $Label. Possible file corruption." >&2
    else
        echo -e "{grb},$Label,$Maxi" >> "$max_output_file"
    fi

done
"""
    return script

def create_script_file(content, grb, bin_size, config):
    PATH_GENERAL = config['PATH_GENERAL']
    PATH_CODES = os.path.join(PATH_GENERAL, 'scripts')
    file_path = os.path.join(PATH_CODES, f'MaxSig{grb}_{bin_size}.sh')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as file:
        file.write(content)

def generate_scripts_for_all_grbs(bin_size, path, config):
    GRBs = pd.read_csv(config['GRBsINFO'])

    if 'RA' not in GRBs.columns:
        if 'Ra' in GRBs.columns:
            GRBs['RA'] = GRBs['Ra']
        else:
            raise KeyError("No se encontró la columna RA ni Ra en el archivo GRB_List.csv")
    if 'DEC' not in GRBs.columns:
        if 'Dec' in GRBs.columns:
            GRBs['DEC'] = GRBs['Dec']
        else:
            raise KeyError("No se encontró la columna DEC ni Dec en el archivo GRB_List.csv")

    for _, row in GRBs.iterrows():
        grb, ra, dec = row['Name'], row['RA'], row['DEC']
        
        # ⚠️ Verifica si existe al menos un archivo .fits.gz
        exists_any = False
        for label in config['LABELS']:
            fits_path = os.path.join(path, grb, f'transit_{label[0]}', f'{grb}_transit_{label}.fits.gz')
            if os.path.exists(fits_path):
                exists_any = True
                break

        if not exists_any:
            print(f"[SKIP] No existen archivos .fits.gz para {fits_path}, se omite generación de script.")
            continue

        script_content = generate_bash_script(grb, ra, dec, bin_size, path, config)
        create_script_file(script_content, grb, bin_size, config)

    GRBs = pd.read_csv(config['GRBsINFO'])

    # Asegura que RA y DEC estén disponibles
    if 'RA' not in GRBs.columns:
        if 'Ra' in GRBs.columns:
            GRBs['RA'] = GRBs['Ra']
        else:
            raise KeyError("No se encontró la columna RA ni Ra en el archivo GRB_List.csv")
    if 'DEC' not in GRBs.columns:
        if 'Dec' in GRBs.columns:
            GRBs['DEC'] = GRBs['Dec']
        else:
            raise KeyError("No se encontró la columna DEC ni Dec en el archivo GRB_List.csv")

    for _, row in GRBs.iterrows():
        grb, ra, dec = row['Name'], row['RA'], row['DEC']
        script_content = generate_bash_script(grb, ra, dec, bin_size, path, config)
        create_script_file(script_content, grb, bin_size, config)

def generate_batch_sender(bin_size, config):
    GRBs = pd.read_csv(config['GRBsINFO'])
    PATH_GENERAL = config['PATH_GENERAL']
    PATH_CODES = os.path.join(PATH_GENERAL, 'scripts')
    batch_file_path = os.path.join(PATH_CODES, f'BatchSenderMax_{bin_size}.sh')
    os.makedirs(os.path.dirname(batch_file_path), exist_ok=True)
    if os.path.exists(batch_file_path):
        os.remove(batch_file_path)
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write(f'rm -f {PATH_GENERAL}/MaxSig_{bin_size}_*.txt\n')
        for grb in GRBs['Name']:
            script_path = os.path.join(PATH_CODES, f'MaxSig{grb}_{bin_size}.sh')
            batch_file.write(f'bash {script_path}\n')