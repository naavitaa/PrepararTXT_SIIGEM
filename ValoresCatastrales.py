# ===============================================================
# SCRIPT QGIS – Generación de valores catastrales GC203T05
# ⚠️ Este script debe ejecutarse desde el entorno Python de QGIS
# ===============================================================

import os
import math
import pandas as pd

# ───────────────────────────────────────────────────────────────
# Dependencias QGIS / PyQt
# ───────────────────────────────────────────────────────────────
try:
    from PyQt5.QtWidgets import QFileDialog, QInputDialog
    from qgis.core import QgsVectorLayer
except ImportError:
    raise Exception(
        "Este script debe ejecutarse desde el entorno Python de QGIS."
    )

# ───────────────────────────────────────────────────────────────
# 0. Diccionario de municipios
# ───────────────────────────────────────────────────────────────
municipios_dic = {
    1: "Cuautitlán", 2: "Coyotepec", 3: "Huehuetoca", 4: "Melchor Ocampo",
    5: "Teoloyucán", 6: "Tepotzotlán", 7: "Tultepec", 8: "Tultitlán",
    9: "Chalco", 10: "Amecameca", 11: "Atlautla", 12: "Ayapango",
    13: "Cocotitlán", 14: "Ecatzingo", 15: "Ixtapaluca", 16: "Juchitepec",
    17: "Ozumba", 18: "Temamatla", 19: "Tenango Del Aire", 20: "Tepetlixpa",
    21: "Tlalmanalco", 22: "El Oro", 23: "Acambay", 24: "Atlacomulco",
    25: "Temascalcingo", 26: "Ixtlahuaca", 27: "Jiquipilco", 28: "Jocotitlán",
    29: "Morelos", 30: "San Felipe Del Progreso", 31: "Jilotepec", 32: "Aculco",
    33: "Chapa de Mota", 34: "Polotitlán", 35: "Soyaniquilpan de Juárez",
    36: "Timilpan", 37: "Villa del Carbón", 38: "Lerma", 39: "Ocoyoacac",
    40: "Otzolotepec", 41: "San Mateo Atenco", 42: "Xonacatlán",
    43: "Otumba", 44: "Axapusco", 45: "Nopaltepec",
    46: "San Martín de las Pirámides", 47: "Tecámac", 48: "Temascalapa",
    49: "Sultepec", 50: "Almoloya de Alquisiras", 51: "Amatepec",
    52: "Texcaltitlán", 53: "Tlatlaya", 54: "Zacualpan", 55: "Temascaltepec",
    56: "San Simón de Guerrero", 57: "Tejupilco", 58: "Tenancingo",
    59: "Coatepec Harinas", 60: "Ixtapan de La Sal", 61: "Malinalco",
    62: "Ocuilan", 63: "Tonatico", 64: "Villa Guerrero",
    65: "Zumpahuacán", 66: "Tenango Del Valle", 67: "Almoloya del Río",
    68: "Atizapán", 69: "Calimaya", 70: "Capulhuac", 71: "Chapultepec",
    72: "Xalatlaco", 73: "Joquicingo", 74: "Mexicaltzingo",
    75: "Rayón", 76: "San Antonio La Isla", 77: "Texcalyacac",
    78: "Tianguistenco", 79: "Texcoco", 80: "Acolman", 81: "Atenco",
    82: "Chiautla", 83: "Chicoloapan", 84: "Chiconcuac",
    85: "Chimalhuacán", 86: "La Paz", 87: "Nezahualcóyotl",
    88: "Papalotla", 89: "Teotihuacán", 90: "Tepetlaoxtoc",
    91: "Tezoyuca", 92: "Tlalnepantla de Baz",
    93: "Coacalco de Berriozábal", 94: "Ecatepec de Morelos",
    95: "Huixquilucan", 96: "Isidro Fabela", 97: "Jilotzingo",
    98: "Naucalpan de Juárez", 99: "Nicolás Romero",
    100: "Atizapán de Zaragoza", 101: "Toluca",
    102: "Almoloya de Juárez", 103: "Metepec", 104: "Temoaya",
    105: "Villa Victoria", 106: "Zinacantepec", 107: "Valle de Bravo",
    108: "Amanalco", 109: "Donato Guerra", 110: "Ixtapan Del Oro",
    111: "Otzoloapan", 112: "Santo Tomás", 113: "Villa de Allende",
    114: "Zacazonapan", 115: "Zumpango", 116: "Apaxco",
    117: "Hueypoxtla", 118: "Jaltenco", 119: "Nextlalpan",
    120: "Tequixquiac", 121: "Cuautitlán Izcalli",
    122: "Valle de Chalco Solidaridad", 123: "Luvianos",
    124: "San José del Rincón", 125: "Tonanitla"
}

# ───────────────────────────────────────────────────────────────
# 1. Seleccionar DBF
# ───────────────────────────────────────────────────────────────
ruta_dbf, _ = QFileDialog.getOpenFileName(
    None,
    "Selecciona el DBF GC203T05",
    "",
    "DBF (*.dbf)"
)

if not ruta_dbf:
    raise Exception("No se seleccionó el archivo DBF.")

# ───────────────────────────────────────────────────────────────
# 2. Datos manuales
# ───────────────────────────────────────────────────────────────
EJERCICIO, ok = QInputDialog.getText(None, "Ejercicio", "Ingresa el AÑO:")
if not ok:
    raise Exception("Proceso cancelado")

P_INICIO, ok = QInputDialog.getText(None, "Periodo inicio", "Ingresa el PERIODO INICIO:")
if not ok:
    raise Exception("Proceso cancelado")

P_FIN, ok = QInputDialog.getText(None, "Periodo fin", "Ingresa el PERIODO FIN:")
if not ok:
    raise Exception("Proceso cancelado")

ESTATUS, ok = QInputDialog.getText(None, "Estatus", "Ingresa la CLAVE DE ESTATUS:")
if not ok:
    raise Exception("Proceso cancelado")

MAX_REG, ok = QInputDialog.getInt(
    None,
    "Registros por TXT",
    "Número máximo de registros por archivo TXT:",
    40000, 1, 1000000
)
if not ok:
    raise Exception("Proceso cancelado")

# ───────────────────────────────────────────────────────────────
# 3. Carpeta destino
# ───────────────────────────────────────────────────────────────
destino = QFileDialog.getExistingDirectory(None, "Selecciona carpeta destino")
if not destino:
    raise Exception("No se seleccionó carpeta destino.")

# ───────────────────────────────────────────────────────────────
# 4. Cargar DBF como capa QGIS
# ───────────────────────────────────────────────────────────────
layer = QgsVectorLayer(ruta_dbf, "GC203T05", "ogr")
if not layer.isValid():
    raise Exception("No se pudo cargar el DBF.")

data = [f.attributes() for f in layer.getFeatures()]
columnas = [f.name() for f in layer.fields()]
df = pd.DataFrame(data, columns=columnas)

# ───────────────────────────────────────────────────────────────
# 5. Función ceros a la izquierda
# ───────────────────────────────────────────────────────────────
def z(val, n):
    return str(val).split('.')[0].zfill(n)

# ───────────────────────────────────────────────────────────────
# 6. Clave catastral
# ───────────────────────────────────────────────────────────────
df["CLAVE_CATASTRAL"] = (
    df["MUNICIPIO"].apply(lambda x: z(x, 3)) +
    df["ZONA"].apply(lambda x: z(x, 2)) +
    df["MANZANA"].apply(lambda x: z(x, 3)) +
    df["LOTE"].apply(lambda x: z(x, 2)) +
    df["EDIFICIO"].apply(lambda x: z(x, 2)) +
    df["DEPTO"].apply(lambda x: z(x, 4))
)

# ───────────────────────────────────────────────────────────────
# 7. Calcular valor catastral
# ───────────────────────────────────────────────────────────────
for c in ["VTERRPROP", "VTERRCOM", "VCONSPROP", "VCONSCOM"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df[f"VC{EJERCICIO}"] = (
    df["VTERRPROP"] +
    df["VTERRCOM"] +
    df["VCONSPROP"] +
    df["VCONSCOM"]
).astype(int)

# ───────────────────────────────────────────────────────────────
# 8. Campos finales
# ───────────────────────────────────────────────────────────────
df_final = df[["CLAVE_CATASTRAL", f"VC{EJERCICIO}"]].copy()
df_final["EJERCICIO"] = EJERCICIO
df_final["P_INICIO"] = P_INICIO
df_final["P_FIN"] = P_FIN
df_final["ESTATUS"] = ESTATUS
df_final["MUNICIPIO"] = df["MUNICIPIO"].apply(lambda x: z(x, 3))

df_final = df_final[
    ["CLAVE_CATASTRAL", "EJERCICIO", "P_INICIO", "P_FIN", f"VC{EJERCICIO}", "ESTATUS", "MUNICIPIO"]
]

# ───────────────────────────────────────────────────────────────
# 9. Exportación por municipio
# ───────────────────────────────────────────────────────────────
for mun in df_final["MUNICIPIO"].unique():
    df_m = df_final[df_final["MUNICIPIO"] == mun].drop(columns=["MUNICIPIO"])
    nombre = municipios_dic.get(int(mun), "DESCONOCIDO")
    base = f"{mun}_{nombre}_VALORES_{EJERCICIO}"

    df_m.to_excel(os.path.join(destino, f"{base}.xlsx"), index=False)

    total = len(df_m)
    partes = math.ceil(total / MAX_REG)

    for i in range(partes):
        df_m.iloc[i*MAX_REG:(i+1)*MAX_REG].to_csv(
            os.path.join(destino, f"{base}_PARTE_{i+1}.txt"),
            sep="|", index=False, header=False, lineterminator="\n"
        )

print("\n🎉 PROCESO COMPLETADO CON ÉXITO")
