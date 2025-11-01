import pandas as pd
import os
import re

# Archivos generados por tu script bash
archivos = [
    "needle_timesV0.doc",
    "needle_timesV1.doc",
    "needle_timesV2.doc",
    "dboard_timesV0.doc",
    "dboard_timesV1.doc",
    "dboard_timesV2.doc"
]

# Valores de K usados en el script bash
valores_k = [1, 2, 4, 6, 8]

with pd.ExcelWriter("resultados_experimentos.xlsx", engine="openpyxl") as writer:
    for archivo in archivos:
        if not os.path.exists(archivo):
            print(f"⚠️ Archivo no encontrado: {archivo}")
            continue

        # Leer todas las líneas con datos
        with open(archivo, "r") as f:
            lineas = [l.strip() for l in f if l.strip()]

        # Detectar tipo de archivo (V0 = sin K, V1/V2 = con K)
        version = re.search(r"V(\d+)", archivo).group(1)
        version = int(version)

        if version == 0:
            # V0: solo una serie de tiempos
            df = pd.DataFrame({"Tiempo (s)": lineas})
        else:
            # V1 o V2: 10 repeticiones por cada valor de K
            n_por_k = len(lineas) // len(valores_k)
            data = {}
            start = 0
            for k in valores_k:
                end = start + n_por_k
                data[f"K={k}"] = lineas[start:end]
                start = end
            df = pd.DataFrame(data)

        # Guardar en una hoja con el nombre del archivo
        hoja = os.path.splitext(archivo)[0]
        df.to_excel(writer, sheet_name=hoja, index=False)

print("✅ Archivo Excel 'resultados_experimentos.xlsx' generado correctamente.")
