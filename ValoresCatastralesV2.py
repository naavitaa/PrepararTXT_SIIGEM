# ===============================================================
# SCRIPT QGIS – Generación de valores catastrales GC203T05
# ⚠️ Ejecutar desde la Consola Python de QGIS
# ===============================================================

import os
import math
import pandas as pd

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from qgis.core import QgsVectorLayer

# ───────────────────────────────────────────────────────────────
# FUNCIÓN DE ERROR CONTROLADO
# ───────────────────────────────────────────────────────────────
def error(msg):
    QMessageBox.critical(
        None,
        "Error en la ejecución del script",
        msg
    )
    raise Exception(msg)

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
    error(
        "No se seleccionó ningún archivo DBF.\n\n"
        "El proceso fue cancelado antes de iniciar."
    )

# ───────────────────────────────────────────────────────────────
# 2. Cargar DBF como capa QGIS
# ───────────────────────────────────────────────────────────────
layer = QgsVectorLayer(ruta_dbf, "GC203T05", "ogr")

if not layer.isValid():
    error(
        "No fue posible cargar el archivo DBF.\n\n"
        "Verifique que:\n"
        "• El archivo no esté dañado\n"
        "• Sea un DBF válido\n"
        "• Corresponda al layout GC203T05"
    )

data = [f.attributes() for f in layer.getFeatures()]
columnas = [f.name() for f in layer.fields()]

if not data:
    error(
        "El archivo DBF se cargó correctamente,\n"
        "pero no contiene registros."
    )

df = pd.DataFrame(data, columns=columnas)

# ───────────────────────────────────────────────────────────────
# 3. Validación de columnas
# ───────────────────────────────────────────────────────────────
columnas_requeridas = [
    "MUNICIPIO", "ZONA", "MANZANA", "LOTE", "EDIFICIO", "DEPTO",
    "VTERRPROP", "VTERRCOM", "VCONSPROP", "VCONSCOM"
]

faltantes = [c for c in columnas_requeridas if c not in df.columns]

if faltantes:
    error(
        "El archivo DBF no tiene el formato esperado (GC203T05).\n\n"
        "Faltan las siguientes columnas:\n"
        "• " + "\n• ".join(faltantes)
    )

# ───────────────────────────────────────────────────────────────
# 4. Datos manuales
# ───────────────────────────────────────────────────────────────
EJERCICIO, ok = QInputDialog.getText(None, "Ejercicio", "Ingresa el AÑO:")
if not ok:
    error("Proceso cancelado por el usuario.")

if not EJERCICIO.isdigit() or len(EJERCICIO) != 4:
    error(
        "El EJERCICIO ingresado no es válido.\n\n"
        "Debe ser un año de 4 dígitos.\n"
        "Ejemplo: 2024"
    )

P_INICIO, ok = QInputDialog.getText(None, "Periodo inicio", "Ingresa el PERIODO INICIO:")
if not ok:
    error("Proceso cancelado por el usuario.")

P_FIN, ok = QInputDialog.getText(None, "Periodo fin", "Ingresa el PERIODO FIN:")
if not ok:
    error("Proceso cancelado por el usuario.")

try:
    p_inicio = int(P_INICIO)
    p_fin = int(P_FIN)
except ValueError:
    error("Los periodos deben ser valores numéricos entre 1 y 12.")

if not (1 <= p_inicio <= 12) or not (1 <= p_fin <= 12):
    error(
        "Los periodos deben estar en el rango de 1 a 12.\n"
        "Ejemplo válido: Inicio 1 / Fin 6"
    )

if p_inicio > p_fin:
    error("El PERIODO INICIO no puede ser mayor que el PERIODO FIN.")

ESTATUS, ok = QInputDialog.getText(None, "Estatus", "Ingresa la CLAVE DE ESTATUS:")
if not ok:
    error("Proceso cancelado por el usuario.")

try:
    estatus = int(ESTATUS)
except ValueError:
    error("El ESTATUS debe ser un valor numérico entre 1 y 9.")

if not (1 <= estatus <= 9):
    error("El ESTATUS debe estar en el rango de 1 a 9.")

ESTATUS = str(estatus)

MAX_REG, ok = QInputDialog.getInt(
    None,
    "Registros por TXT",
    "Número máximo de registros por archivo TXT:",
    40000, 1, 1000000
)

if not ok:
    error("Proceso cancelado por el usuario.")

# ───────────────────────────────────────────────────────────────
# 5. Carpeta destino
# ───────────────────────────────────────────────────────────────
destino = QFileDialog.getExistingDirectory(None, "Selecciona carpeta destino")
if not destino:
    error("No se seleccionó carpeta destino.")

# ───────────────────────────────────────────────────────────────
# 6. Procesamiento
# ───────────────────────────────────────────────────────────────
def z(val, n):
    return str(val).split('.')[0].zfill(n)

df["CLAVE_CATASTRAL"] = (
    df["MUNICIPIO"].apply(lambda x: z(x, 3)) +
    df["ZONA"].apply(lambda x: z(x, 2)) +
    df["MANZANA"].apply(lambda x: z(x, 3)) +
    df["LOTE"].apply(lambda x: z(x, 2)) +
    df["EDIFICIO"].apply(lambda x: z(x, 2)) +
    df["DEPTO"].apply(lambda x: z(x, 4))
)

for c in ["VTERRPROP", "VTERRCOM", "VCONSPROP", "VCONSCOM"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df[f"VC{EJERCICIO}"] = (
    df["VTERRPROP"] +
    df["VTERRCOM"] +
    df["VCONSPROP"] +
    df["VCONSCOM"]
).astype(int)

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
# 7. Exportación
# ───────────────────────────────────────────────────────────────
for mun in df_final["MUNICIPIO"].unique():
    df_m = df_final[df_final["MUNICIPIO"] == mun].drop(columns=["MUNICIPIO"])
    if df_m.empty:
        continue

    try:
        nombre = municipios_dic.get(int(mun), "DESCONOCIDO")
    except ValueError:
        nombre = "DESCONOCIDO"

    base = f"{mun}_{nombre}_VALORES_{EJERCICIO}"

    df_m.to_excel(os.path.join(destino, f"{base}.xlsx"), index=False)

    total = len(df_m)
    partes = math.ceil(total / MAX_REG)

    for i in range(partes):
        df_m.iloc[i*MAX_REG:(i+1)*MAX_REG].to_csv(
            os.path.join(destino, f"{base}_PARTE_{i+1}.txt"),
            sep="|",
            index=False,
            header=False,
            lineterminator="\n"
        )

QMessageBox.information(
    None,
    "Proceso finalizado",
    "🎉 El proceso se completó con éxito.\n\n"
    "Los archivos TXT y Excel fueron generados correctamente."
)