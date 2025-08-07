import os
import pandas as pd
import numpy as np

def process_coordinates(config):
    """
    Procesa los archivos de texto con datos de Significance y genera archivos CSV
    combinando la información de coordenadas de los GRBs.

    Se asume que:
      - config['GRBsINFO'] contiene la ruta al CSV con la lista de GRBs.
      - config['PATH_GENERAL'] contiene la ruta donde se encuentran los archivos de texto.
      - config['bin_size'] contiene el valor de bin_size usado en el procesamiento.
    """
    GRBsINFO = config['GRBsINFO']
    coordi = pd.read_csv(GRBsINFO)
    A = coordi['Error_Radius'].drop_duplicates()

    bin_size = config['bin_size']
    List = A[A > bin_size].to_list() + [bin_size]
    PATH_GENERAL = config['PATH_GENERAL']

    for transit in [1, 2]:
        dfs = []    
        for psf in List:
            try:
                file_path = os.path.join(PATH_GENERAL, f'MaxSigHist_{psf}_{transit}.txt')

                if not os.path.exists(file_path):
                    print(f"[AVISO] No se encontró el archivo: {file_path}")
                    continue

                with open(file_path, 'r') as file:
                    lines = file.readlines()

                columns = ['Name', 'transit', 'Significance', 'RA', 'DEC']
                data = []
                for line in lines:
                    line = ' '.join(line.split())
                    line = line.replace('Max:', '').replace(')', '').replace('(', '')
                    line = line.replace(' ', ',').replace(',,', ',')
                    parts = line.split(',')
                    if len(parts) == len(columns):
                        data.append(parts)

                if not data:
                    print(f"[AVISO] El archivo está vacío o mal formateado: {file_path}")
                    continue

                data = np.array(data)
                df = pd.DataFrame(data, columns=columns)
                df['PSF'] = psf
                df.drop_duplicates(inplace=True)
                dfs.append(df)

                if transit == 2:
                    print(data, 'HERE', len(data[0]))
                    print(file_path)

            except Exception as e: 
                print(f"Error processing {file_path}: {e}")
                continue

        if not dfs:
            print(f"[ERROR] No se pudo cargar ningún archivo para el tránsito {transit}. ¿Faltan archivos o están vacíos?")
            continue

        combined_df = pd.concat(dfs, ignore_index=True).drop_duplicates()
        C = combined_df.join(coordi.set_index('Name'), on='Name')
        out_file = os.path.join(os.path.dirname(PATH_GENERAL), f'Coordinates_with_Max_Sig_{transit}_0{bin_size}.csv')
        C.to_csv(out_file, index=False)
        print(f"Archivo generado: {out_file}")
        print(combined_df)
