import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from libraries import dataframe_generator

bin_size = 0.3
spectral_index = 2.07
PATH_BASE = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/'
GRB_KN_DIR = PATH_BASE
GITLAB_DIR = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GitLab_kn_paper/'
TABLE1_PATH = PATH_BASE + 'data/ULs/Latex/Tables_NT/Table_1.txt'

config = {
    'BASE_DIR': PATH_BASE,
    'GRB_KN_DIR': GRB_KN_DIR,
    'PATH_BASE': PATH_BASE,
    'GITLAB_DIR': GITLAB_DIR,
    'GRBsINFO': PATH_BASE + 'data/ULs/config/GRB_List.csv',
    'bin_size': bin_size,
    'spectral_index': spectral_index,
    'PATH_GRBs_Healpix': PATH_BASE + f'data/healpix_maps_{spectral_index}_ER/',
    'PATH_GENERAL': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/',
    'energy_ranges': PATH_BASE + f'config/Energy_ranges.csv',
    'GRBINFO_folder': PATH_BASE + 'data/ULs/config/',
    'OUTPUT_folder': PATH_BASE + f'data/ULs/files/PSF_{bin_size}/alfa={spectral_index}/',
    'PATH_SH': PATH_BASE + f'data/ULs/codes/PSF_{bin_size}/alfa={spectral_index}/',
    'RECALCULATED': PATH_BASE + 'data/corrected/',
    'File_1st_transit': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/Coordinates_with_Max_Sig_1_0{bin_size}.csv',
    'File_2nd_transit': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/Coordinates_with_Max_Sig_2_0{bin_size}.csv',
    'EBL_list': ['Franceschini08', 'Gilmore12Fiducial'],
    'LABEL_UL_CODE': 'ER',
    'LABELS': ['1', '2'],
    'PATH_LATEX': PATH_BASE + f'/data/ULs/Latex/',
    'TABLE1_PATH': TABLE1_PATH
}

# Leer GRBs desde el archivo oficial Table_1.txt
with open(TABLE1_PATH, 'r') as f:
    lines = f.readlines()

all_grb_names = [line.split('&')[0].strip() for line in lines if line.strip().startswith('GRB')]
all_grb_names = pd.Series(all_grb_names).str.replace(',', '', regex=True).unique()

# Cargar los archivos de upper limits
upper_limit_dir = os.path.join(config['GRB_KN_DIR'], f"data/ULs/files/PSF_{bin_size}/alfa={spectral_index}")
Franceschini_1stT = os.path.join(upper_limit_dir, 'UpperLimit_1_Franceschini08.csv')
Franceschini_2ndT = os.path.join(upper_limit_dir, 'UpperLimit_2_Franceschini08.csv')

try:
    df_1st = pd.read_csv(Franceschini_1stT, delim_whitespace=True, header=None)
    df_1st.columns = ['Name', 'Model', 'Norm', 'Index', 'TS', 'Dec', 'RA', 'UL', 'UL_minus']
except Exception as e:
    print("Error leyendo el archivo de primer tránsito:", e)
    df_1st = pd.DataFrame()

try:
    df_2nd = pd.read_csv(Franceschini_2ndT, delim_whitespace=True, header=None)
    df_2nd.columns = ['Name', 'Model', 'Norm', 'Index', 'TS', 'Dec', 'RA', 'UL', 'UL_minus']
except Exception as e:
    print("Error leyendo el archivo de segundo tránsito:", e)
    df_2nd = pd.DataFrame()

if 'Name' in df_1st.columns:
    df_1st['Name'] = df_1st['Name'].astype(str).str.replace(',', '', regex=True)
if 'Name' in df_2nd.columns:
    df_2nd['Name'] = df_2nd['Name'].astype(str).str.replace(',', '', regex=True)

df_1st_valid = df_1st[pd.to_numeric(df_1st['UL'], errors='coerce').notna()]
df_2nd_valid = df_2nd[pd.to_numeric(df_2nd['UL'], errors='coerce').notna()]

plotted_1st = set(df_1st_valid['Name'].unique()) if not df_1st_valid.empty else set()
plotted_2nd = set(df_2nd_valid['Name'].unique()) if not df_2nd_valid.empty else set()

not_plotted_1st = sorted(set(all_grb_names) - plotted_1st)
not_plotted_2nd = sorted(set(all_grb_names) - plotted_2nd)

# Mostrar GRBs no ploteados con razón
print("\nGRBs que no se plotearon del primer tránsito (tabla 1):")
for grb in not_plotted_1st:
    print(f"- {grb}: No en archivo de upper limits del primer tránsito o UL inválido")

print("\nGRBs que no se plotearon del segundo tránsito (tabla 1):")
for grb in not_plotted_2nd:
    print(f"- {grb}: No en archivo de upper limits del segundo tránsito o UL inválido")

# Crear base de datos con upper limits
def get_ul_value(grb, df):
    if grb in df['Name'].values:
        val = df[df['Name'] == grb]['UL'].values[0]
        return val if pd.notna(val) else '-'
    return '-'

df_combined_ul = pd.DataFrame({
    'GRB': all_grb_names,
    'UL_1st_transit': [get_ul_value(grb, df_1st_valid) for grb in all_grb_names],
    'UL_2nd_transit': [get_ul_value(grb, df_2nd_valid) for grb in all_grb_names]
})

df_combined_ul.to_csv("combined_upper_limits_table.csv", index=False)
print("\nArchivo generado: combined_upper_limits_table.csv")
