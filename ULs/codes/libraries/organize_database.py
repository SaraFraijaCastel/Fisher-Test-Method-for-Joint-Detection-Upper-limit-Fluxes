import pandas as pd

PATH_BASE = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/'
GRB_KN_DIR = PATH_BASE
GITLAB_DIR = '/lustre/hawcz01/scratch/userspace/jorgeamontes/GitLab_kn_paper/'

Col1 = ['First Transit Start GPS', 'First Transit Stop GPS', 'error_radius', 'RA', 'DEC']
Col2 = ['Tstart (GPS)', 'Tstop (GPS)', 'Error_Radius', 'Ra', 'Dec']
cols = dict(zip(Col1, Col2))

csv1 = GRB_KN_DIR + '/config/newgrblist.csv'
csv2 = GRB_KN_DIR + 'config/Fermi_catalog_w_redshifts.csv'
csv_merged = 'GRB_List.csv'

def main(csv1, csv2, csv_merged):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    # Renombrar 'name' → 'Name' en ambos
    if 'name' in df1.columns:
        df1 = df1.rename(columns={'name': 'Name'})
    if 'name' in df2.columns:
        df2 = df2.rename(columns={'name': 'Name'})

    # Eliminar columnas conflictivas si están en ambos
    duplicate_cols = ['RA', 'DEC']
    df1 = df1.drop(columns=[col for col in duplicate_cols if col in df1.columns])
    df2 = df2.drop(columns=[col for col in duplicate_cols if col in df2.columns])

    # Hacer merge
    merged = pd.merge(left=df1, right=df2, how='outer', on='Name')

    # Renombrar columnas necesarias
    merged.rename(columns=cols, inplace=True)

    # # Normalizar nombres finales
    if 'ra' in merged.columns:
        merged.rename(columns={'ra': 'Ra'}, inplace=True)
    if 'dec' in merged.columns:
        merged.rename(columns={'dec': 'Dec'}, inplace=True)

    output_path = GRB_KN_DIR + '/data/ULs/config/' + csv_merged
    merged.to_csv(output_path, index=False)
    print(f"[INFO] CSV fusionado generado: {output_path}")

if __name__ == '__main__':
    main(csv1, csv2, csv_merged)
