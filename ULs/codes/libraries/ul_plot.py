# libraries/ul_plot.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from libraries import dataframe_generator
from scipy.stats import norm
from astropy.io import fits

def non_to_int2(E1, E2, flux, alpha, pivot):
    """Convierte un flujo a un valor integrado según el índice espectral."""
    A = flux / (pivot ** (-alpha))
    if alpha > 2:
        F1 = (E2 ** (2 - alpha)) / (2 - alpha)
        F2 = (E1 ** (2 - alpha)) / (2 - alpha)
        return 1.6 * A * (F1 - F2)
    elif alpha == 2:
        F3 = np.log(E2)
        F4 = np.log(E1)
        return A * (F3 - F4)
    else:
        return None

def expected_value(values, weights):
    """Calcula el valor esperado dada una lista de valores y sus pesos."""
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()

def generate_upper_limits_plots(config):
    """
    Genera DataFrames, procesa los datos y produce gráficos con los límites superiores
    obtenidos por los métodos Franceschini y Gilmore.
    """
    # Usar 'BASE_DIR' si existe, de lo contrario usar 'PATH_BASE'
    BASE_DIR = config.get('BASE_DIR', config.get('PATH_BASE'))
    bin_size = config['bin_size']
    spectral_index = config['spectral_index']
    GRB_KN_DIR = config['GRB_KN_DIR']
    GITLAB_DIR = config['GITLAB_DIR']
    
    # Construir rutas a partir de directorios base
    csvfile = config['GRBsINFO']
    path_zenith = os.path.join(GITLAB_DIR, 'UpperLimits/CSV_FILES_trials/GRB_COORDINATES/zenith.txt')
    upper_limit_dir = os.path.join(GRB_KN_DIR, f'data/ULs/files/PSF_{bin_size}', f'alfa={spectral_index}')
    
    Franceschini_1stT = os.path.join(upper_limit_dir, 'UpperLimit_1_Franceschini08.csv')
    Franceschini_2ndT = os.path.join(upper_limit_dir, 'UpperLimit_2_Franceschini08.csv')
    Gilmore_1stT = os.path.join(upper_limit_dir, 'UpperLimit_1_Gilmore12Fiducial.csv')
    Gilmore_2ndT = os.path.join(upper_limit_dir, 'UpperLimit_2_Gilmore12Fiducial.csv')
    print(Franceschini_1stT, 'eta')
    energy_file = config['energy_ranges']
    
    plots_dir = config.get('plots_dir', '../plots')
    plot_first_path = os.path.join(plots_dir, 'plot_first_transit_hd.png')
    plot_second_path = os.path.join(plots_dir, 'plot_second_transit_hd.png')
    
    # Generar DataFrames usando el módulo dataframe_generator
    df_franceschini = dataframe_generator.DATAFRAME_generator(Franceschini_2ndT, Franceschini_1stT, csvfile, path_zenith)
    df_gilmore = dataframe_generator.DATAFRAME_generator(Gilmore_2ndT, Gilmore_1stT, csvfile, path_zenith)
    df_franceschini.to_csv('data.csv')
    df_gilmore.to_csv('data2.csv')
    # Limpieza de nombres, ordenación y eliminación de duplicados
    df_franceschini['Name'] = df_franceschini["Name"].str.replace(',', '', regex=True)
    df_gilmore['Name'] = df_gilmore["Name"].str.replace(',', '', regex=True)
    df_franceschini=df_franceschini.drop_duplicates()
    df_franceschini.sort_values(by='Name', inplace=True)
    df_gilmore.sort_values(by='Name', inplace=True)
    df_gilmore=df_gilmore.drop_duplicates()
    
    Names = df_franceschini["Name"]
    DEC = df_franceschini['Dec'].copy()
    # if len(DEC) > 13:
    #     DEC.iloc[13] = -23  # Ajuste manual si es necesario
    
    colors = plt.cm.tab20(np.linspace(0, 1, 20))[:14]
    color_hex = [matplotlib.colors.rgb2hex(color) for color in colors]
    
# This section of the code is performing the following tasks:
    # Cargar archivo de energía y convertir a numérico
    Energy = pd.read_csv(energy_file, header=None, names=['Name', 'E1', 'E2'])
    Energy.sort_values(by='Name', inplace=True)
    Energy[['E1', 'E2']] = Energy[['E1', 'E2']].apply(pd.to_numeric, errors='coerce')

    # Asegurar que los límites superiores también son numéricos
    df_franceschini['upperBound'] = pd.to_numeric(df_franceschini['upperBound'], errors='coerce')
    df_franceschini['upperBound_2ndT'] = pd.to_numeric(df_franceschini['upperBound_2ndT'], errors='coerce')
    df_gilmore['upperBound'] = pd.to_numeric(df_gilmore['upperBound'], errors='coerce')
    df_gilmore['upperBound_2ndT'] = pd.to_numeric(df_gilmore['upperBound_2ndT'], errors='coerce')

    # Calcular ULs integradas
    UL_Franceschini_1 = non_to_int2(Energy['E1'], Energy['E2'], df_franceschini['upperBound'], spectral_index, 1)
    UL_Franceschini_2 = non_to_int2(Energy['E1'], Energy['E2'], df_franceschini['upperBound_2ndT'], spectral_index, 1)
    UL_Gilmore_1 = non_to_int2(Energy['E1'], Energy['E2'], df_gilmore['upperBound'], spectral_index, 1)
    UL_Gilmore_2 = non_to_int2(Energy['E1'], Energy['E2'], df_gilmore['upperBound_2ndT'], spectral_index, 1)

    # Guardar por si acaso
    DATA = pd.DataFrame({'F': UL_Franceschini_1, 'G': UL_Gilmore_1})
    DATA.to_csv('UL.csv')

    def plot_ul(names, dec, ul_franceschini, ul_gilmore, color_hex,
                xlabel=r'Declinación [grados]',
                ylabel=r'$\Phi$ [ergs cm$^{-2}$ s$^{-1}$]',
                xlim=(-25, 65), ylim=(1e-13, 1e-8),
                save_path=None):
        fig, ax = plt.subplots()
        for grb, ul_g, d, col in zip(names, ul_gilmore, dec, color_hex):
            ax.errorbar(x=d, y=ul_g, yerr=ul_g / 10, uplims=True, color=col, label=grb)
        ax.set_yscale('log')
        for grb, ul_f, ul_g, d, col in zip(names, ul_franceschini, ul_gilmore, dec, color_hex):
            ax.fill_between([d - 1, d + 1], [ul_f, ul_f], [ul_g, ul_g], color=col, alpha=0.3)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        # ax.legend(bbox_to_anchor=(1.05, 1))
        if save_path is not None:
            plt.savefig(save_path, dpi=600, bbox_inches='tight')
            plt.close(fig)
        else:
            plt.show()
    
    plot_ul(Names, DEC, UL_Franceschini_1, UL_Gilmore_1, color_hex, save_path=plot_first_path)
    plot_ul(Names, DEC, UL_Franceschini_2, UL_Gilmore_2, color_hex, save_path=plot_second_path)
