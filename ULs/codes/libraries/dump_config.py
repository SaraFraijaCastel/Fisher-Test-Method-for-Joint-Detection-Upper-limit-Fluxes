import yaml

# Tus valores
bin_size       = 0.3
spectral_index = 2.07
PATH_BASE      = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/'
GRB_KN_DIR     = PATH_BASE
GITLAB_DIR     = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GitLab_kn_paper/'
name           = '_plus_5/'
label          = '__plus_5'

config = {
    'BASE_DIR': PATH_BASE,
    'GRB_KN_DIR': GRB_KN_DIR,
    'PATH_BASE': PATH_BASE,
    'Delta': -5,
    'GITLAB_DIR': GITLAB_DIR,
    'GRBsINFO': PATH_BASE + 'data/ULs/config/GRB_List.csv',
    'bin_size': bin_size,
    'spectral_index': spectral_index,
    'PATH_GRBs_Healpix': PATH_BASE + f'data/healpix_maps_{spectral_index}_ER/',
    'PATH_GENERAL': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/{name}',
    'energy_ranges': PATH_BASE + f'config/Energy_ranges.csv',
    'GRBINFO_folder': PATH_BASE + 'data/ULs/config/',
    'OUTPUT_folder': PATH_BASE + f'data/ULs/files/PSF_{bin_size}/alfa={spectral_index}/{name}',
    'PATH_SH': PATH_BASE + f'data/ULs/codes/PSF_{bin_size}/alfa={spectral_index}/{name}',
    'RECALCULATED': PATH_BASE + 'data/corrected/',
    'File_1st_transit': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_index}/{name}Coordinates_with_Max_Sig_1_0{bin_size}.csv',
    'File_2nd_transit': PATH_BASE + f'data/ULs/config/Coordinates/PSF_{bin_size}/alfa={spectral_ind ex}/{name}Coordinates_with_Max_Sig_2_0{bin_size}.csv',
    'EBL_list': ['Franceschini08', 'Gilmore12Fiducial'],
    'LABEL_UL_CODE': 'ER',
    'LABELS': [f'1{label}', f'2{label}'],
    'PATH_LATEX': PATH_BASE + f'/data/ULs/Latex/{name}',
    'FORCE_BINSIZE': False
}

with open('config.yml', 'w') as f:
    yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
