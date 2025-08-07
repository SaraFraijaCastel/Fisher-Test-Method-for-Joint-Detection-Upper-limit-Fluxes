# libraries/ul_script.py
import os
import pandas as pd
import subprocess

# Constantes para los índices espectrales


def generate_ul_script(GRBINFO, transit, PATH_SH, OUTPUT_folder, RECALCULATED, EBL, PSF, config):
    """
    Genera un script Bash para calcular upper limits para cada GRB.
    
    Parámetros:
      - GRBINFO: Ruta al archivo CSV con información de los GRBs.
      - transit: Número de tránsito (1 o 2).
      - PATH_SH: Ruta donde se almacenan los scripts.
      - OUTPUT_folder: Carpeta de salida para los archivos resultantes.
      - RECALCULATED: Carpeta con archivos recalculados.
      - EBL: Modelo EBL a utilizar.
      - PSF: Valor de PSF (normalmente el bin_size).
      - config: Diccionario de configuración global (contiene PATH_BASE, energy_ranges, LABEL_UL_CODE, etc.).
    """
    PATH_BASE = config['PATH_BASE']
    LABEL_UL_CODE = config['LABEL_UL_CODE']
    os.makedirs(PATH_SH,exist_ok=True)
    # Leer Energy_ranges con nombres de columnas correctos
    energy_ranges_path = config['energy_ranges']
    Energy_ranges = pd.read_csv(energy_ranges_path, names=['Name', 'Emin', 'Emax'])
    Energy_ranges = Energy_ranges.set_index('Name')
    Energy_ranges.sort_values(by='Name', inplace=True)
    spectral_index = config['spectral_index']
    spectral_index_2 = config['spectral_index']
    name_z=config['name_z']
    limit_redshift=float(config['limit_redshift'])
    if name_z=='z':
        sep=''
    elif name_z=='z+pseudo':
        sep='/pseudo/'
    PATH_SH=config['PATH_SH']+sep
    

    # Leer el archivo CSV con información de los GRBs
    Data = pd.read_csv(GRBINFO)
    # Data.sort_values('Name', inplace=True)
    
    
    # Verificar si la columna "Name" existe
    if "Name" not in Data.columns:
        print(f"Error: La columna 'Name' no está en {GRBINFO}. Verifica el formato del archivo.")
        print(f"Columnas disponibles: {Data.columns}")
        return

    # Usar "Name" como índice
    Data = Data.reset_index().drop_duplicates()
    Data = Data.set_index("Name")
    Data[name_z]=Data[name_z].astype(float)
    Data_2 = Data[Data[name_z] < limit_redshift].copy()
    Data_2.reset_index(inplace=True)
    Energy_ranges = Energy_ranges.reset_index()

    # # Debug print to check matching 'Name' values before merge
    print("Valores únicos en 'Name' de Data_2:", Data_2['Name'])
    print("Valores únicos en 'Name' de Energy_ranges:", Energy_ranges['Name'].unique())

    # Hacer merge explícito por nombre de GRB
    Data_2 = pd.merge(Data_2, Energy_ranges, how='left', on='Name')
    # Restaurar índice si lo necesitas
    Data_2 = Data_2.set_index('Name')
    # Eliminar filas que no tengan Emin o Emax definidos
    num_missing = Data_2[['Emin', 'Emax']].isna().any(axis=1).sum()
    if num_missing > 0:
        print(f"Advertencia: {num_missing} GRBs no tienen valores de Emin o Emax y serán omitidos. Verifica {energy_ranges_path}")
        Data_2 = Data_2.dropna(subset=['Emin', 'Emax'])
        Data_2 = Data_2.set_index(Data_2.index.astype(str))  
        Data_2.drop_duplicates(inplace=True)

    for grb in Data_2.index: 
        OUTPUT_FILE = f"{OUTPUT_folder}{sep}UpperLimit_{transit}_{EBL}_{grb}.csv" 
        code =f"""#! /usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o {PATH_SH}/logs/UL{grb}.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH --time=1-24:00:00
#SBATCH -J UL
# Author: Sara Fraija
source /data/disk01/home/smfraijac/.bashrc
hawc_aerie
output_file={OUTPUT_FILE}
DR51={PATH_BASE}/config/pass5.f_DR/zebra-100pct-FHit.root
dir={RECALCULATED}
output_file={OUTPUT_FILE}
rm -f ${{output_file}}\n """
        line = ""
        row = Data_2.loc[grb]
        RA = row['RA']
        print(RA)
        Dec = row['DEC']
        name_z=config['name_z']
        z = row[name_z]
        # Seleccionar el índice espectral según el GRB
        index = spectral_index_2 if grb == 'GRB170817529' else spectral_index
        path_GRB=os.path.join(RECALCULATED,grb,f'transit_{transit}')
        fits_files=[f for f in os.listdir(path_GRB) if f.endswith('.fits.gz')]
        bins=[f.split('_')[-2].replace('bin','') for f in fits_files]
        input_paths=' '.join([f'$dir/{grb}/transit_{transit}/{grb}_corrected_transit_{transit}_bin{b}_N1024.fits.gz' for b in bins])
        bin_tags=' '.join(bins)
        Emin = row['Emin']
        Emax = row['Emax']    
        line += f'PL="PowerLaw,1.0e-10,{index}"\n'
        line += (
            f"ULs=$(zebra-flux-norm-fit -i {input_paths} -b {bin_tags} "
            f"--extrapolate-low-z --dr $DR51 --ra {RA} --dec {Dec} -s $PL "
            f"--ebl {EBL},{z} --pivot 1 --minE {Emin} --maxE {Emax} --fc 2 -V 3)\n"
        )
        line += f'echo -e "{grb} ${{ULs}}" >> $output_file\n'   
        # Guardar el script Bash
        file_path = f"{PATH_SH}UL{transit}_{EBL}_{PSF}_{LABEL_UL_CODE}_{grb}.sh"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as bash_file:
            bash_file.write(code + line)
        with open(f"{PATH_SH}batch_sender.sh", 'a+') as bash_file:
            bash_file.write(f'sbatch {file_path}  \n')
        print(f"Script generado: {file_path}")
def run_ul_scripts(config):
    """
    Ejecuta la generación y el lanzamiento de los scripts de upper limits para cada modelo EBL.
    """
    PATH_BASE = config['PATH_BASE']
    bin_size = config['bin_size']
    name_z=config['name_z']
    if name_z=='z':
        sep=''
    elif name_z=='z+pseudo':    
        sep='/pseudo/'
    PATH_SH = config['PATH_SH']+sep
    os.makedirs(PATH_SH+sep,exist_ok=True)
    OUTPUT_folder = config['OUTPUT_folder']
    RECALCULATED = config['RECALCULATED']
    EBL_list = config['EBL_list']
    PATH_GENERAL=config['PATH_GENERAL']
    os.makedirs(PATH_SH,exist_ok=True)
    # Construir rutas a los archivos con las coordenadas procesadas
    File_1st_transit = os.path.join(os.path.dirname(PATH_GENERAL), f'Coordinates_with_Max_Sig_1_0{bin_size}.csv')
    File_2nd_transit = os.path.join(os.path.dirname(PATH_GENERAL), f'Coordinates_with_Max_Sig_2_0{bin_size}.csv')    
    for EBL in EBL_list:
        generate_ul_script(File_1st_transit, transit=1, PATH_SH=PATH_SH,OUTPUT_folder=OUTPUT_folder, RECALCULATED=RECALCULATED,EBL=EBL, PSF=bin_size, config=config)
        generate_ul_script(File_2nd_transit, transit=2, PATH_SH=PATH_SH,OUTPUT_folder=OUTPUT_folder, RECALCULATED=RECALCULATED,EBL=EBL, PSF=bin_size, config=config)
        # Ejecutar los scripts generados
        script1 = f"{PATH_SH}UL1_{EBL}_{bin_size}_{config['LABEL_UL_CODE']}.sh"
        script2 = f"{PATH_SH}UL2_{EBL}_{bin_size}_{config['LABEL_UL_CODE']}.sh"
        # subprocess.Popen(['bash', script1])
        # subprocess.Popen(['bash', script2])
