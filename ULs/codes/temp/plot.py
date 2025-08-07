import csv
ruta_archivo='/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/files/UpperLimit_1_Francesschini.csv'
def leer_columnas_seleccionadas(ruta_archivo):
    columnas_seleccionadas = []
    with open(ruta_archivo, mode='r') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            columnas_seleccionadas.append([fila[0], fila[5], fila[6]])
    return columnas_seleccionadas

ruta_archivo = "datos.csv"
columnas = leer_columnas_seleccionadas(ruta_archivo)

for fila in columnas:
    print(fila)
