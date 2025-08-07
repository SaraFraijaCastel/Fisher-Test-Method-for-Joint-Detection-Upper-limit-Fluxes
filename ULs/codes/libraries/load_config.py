import yaml
import os

def load_config(yaml_path="config.yml"):
    with open(yaml_path, "r") as f:
        cfg = yaml.safe_load(f)

    # Parámetros base
    name = cfg["name"]
    label = cfg["label"]
    Delta = cfg["Delta"]
    bin_size = cfg["bin_size"]
    spectral_index = cfg["spectral_index"]
    PATH_BASE = cfg["PATH_BASE"]
    healpix_folder = cfg["healpix_folder"]
    GRB_CSV = cfg["GRB_CSV"]
    # Generar rutas derivadas
    cfg.update({
        'GRB_KN_DIR': PATH_BASE,
        'GRBsINFO': os.path.join(PATH_BASE, f'data/ULs/config/Data/{GRB_CSV}'),
        'PATH_GRBs_Healpix': os.path.join(PATH_BASE, f'data/{healpix_folder}/'),
        'PATH_GENERAL': os.path.join(PATH_BASE, f'data/ULs/config/Coordinates/PSF/PSF_{bin_size}/alfa={spectral_index}/{name}'),
        'energy_ranges': os.path.join(PATH_BASE, 'config/{ENERGY_CSV_FILE}'),
        'GRBINFO_folder': os.path.join(PATH_BASE, 'data/ULs/config/'),
        'OUTPUT_folder': os.path.join(PATH_BASE, f'data/ULs/files/PSF_{bin_size}/alfa={spectral_index}/{name}'),
        'PATH_SH': os.path.join(PATH_BASE, f'data/ULs/scripts/PSF/PSF_{bin_size}/alfa={spectral_index}/{name}'),
        'RECALCULATED': os.path.join(PATH_BASE, 'data/corrected/'),
        'File_1st_transit_coord': os.path.join(PATH_BASE, f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/{name}/Coordinates_with_Max_Sig_1_0{bin_size}.csv'),
        'File_2nd_transit_coord': os.path.join(PATH_BASE, f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/{name}/Coordinates_with_Max_Sig_2_0{bin_size}.csv'),
        'File_1st_transit': os.path.join(PATH_BASE, f'data/ULs/files/PSF_{bin_size}/alfa={spectral_index}/{name}/UpperLimit_1_Gilmore12Fiducial.csv'),
        'File_2nd_transit': os.path.join(PATH_BASE, f'data/ULs/files/PSF_{bin_size}/alfa={spectral_index}/{name}/UpperLimit_2_Gilmore12Fiducial.csv'),
        'LABELS': [f'1{label}', f'2{label}'],
        'PATH_LATEX': os.path.join(PATH_BASE, f'data/ULs/Latex/{name}')
    })

    return cfg