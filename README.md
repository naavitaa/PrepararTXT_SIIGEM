El código esta diseñado para procesar un archivo DBF, generar claves catastrales, calcular valores y exportar los datos procesados en archivos Excel y TXT segmentados por municipio. A continuación, te proporciono un análisis general del código:

Análisis del Código
  1.- Importación de librerías:
    Se importan librerías como pandas, math, os y módulos de PyQt5 para la interfaz gráfica.
    También se utiliza QgsVectorLayer de qgis.core para cargar el archivo DBF.
  2.- Diccionario de municipios:
    Se define un diccionario municipios_dic que asocia códigos de municipios con sus nombres.
  3.- Selección de archivo DBF:
    Se utiliza QFileDialog para que el usuario seleccione un archivo DBF. Si no se selecciona, se lanza una excepción.
  4.- Entrada de datos manuales:
    Se solicitan datos al usuario mediante cuadros de diálogo (QInputDialog), como el año, periodo de inicio y fin, estatus y el número máximo de registros por archivo TXT.
  5.- Selección de carpeta de destino:
    Se solicita al usuario seleccionar una carpeta de destino para guardar los archivos generados.
  6.- Carga del archivo DBF:
    Se utiliza QgsVectorLayer para cargar el archivo DBF y convertirlo en un DataFrame de pandas.
  7.- Generación de la clave catastral:
    Se crea una nueva columna CLAVE_CATASTRAL combinando valores de varias columnas del DataFrame, rellenando con ceros a la izquierda según sea necesario.
  8.- Cálculo de valores:
    Se suman los valores de las columnas VTERRPROP, VTERRCOM, VCONSPROP y VCONSCOM para generar una nueva columna VC{EJERCICIO}.
  9.- Creación del DataFrame final:
    Se seleccionan y reorganizan las columnas necesarias para el archivo final.
  10.- Procesamiento por municipio:
    Se segmentan los datos por municipio y se generan archivos Excel y TXT para cada municipio.
    Los archivos TXT se dividen en partes si el número de registros supera el límite especificado por el usuario.
  11.- Mensajes de éxito:
    Se imprimen mensajes en la consola para indicar que los archivos TXT se han generado correctamente.

Observaciones
  Validación de datos:
    El código no valida si las columnas necesarias (MUNICIPIO, ZONA, MANZANA, etc.) existen en el archivo DBF antes de procesarlas. Esto podría causar errores si el archivo no tiene el formato esperado.
    Sería útil agregar validaciones adicionales para los datos ingresados por el usuario (por ejemplo, verificar que el año sea un número válido).
  Dependencias:
    El código depende de PyQt5 y qgis.core, por lo que es importante asegurarse de que estas librerías estén instaladas y configuradas correctamente en el entorno.
  Mensajes de error:
    Los mensajes de error son claros, pero podrían ser más descriptivos para ayudar al usuario a entender qué salió mal.
  Optimización:
    El código es funcional, pero podría beneficiarse de algunas optimizaciones, como el uso de funciones para evitar la repetición de código (por ejemplo, para la generación de archivos TXT y Excel).









# README

## Script QGIS – Generación de valores catastrales GC203T05

Este script está diseñado para ejecutarse **exclusivamente desde la Consola Python de QGIS** y tiene como objetivo procesar archivos **DBF GC203T05** para generar:

- Archivos **Excel (.xlsx)** por municipio
- Archivos **TXT delimitados por `|`**, fragmentados por un número máximo de registros

El script implementa validaciones estrictas y manejo controlado de errores para garantizar la calidad de la información generada.

---

## 🧩 Funcionalidad general

A partir de un archivo DBF con estructura GC203T05, el script:

1. Valida que el archivo seleccionado sea correcto y contenga información
2. Solicita al usuario datos administrativos (ejercicio, periodos, estatus)
3. Construye la **clave catastral completa**
4. Calcula el **valor catastral total**
5. Genera salidas por municipio en formatos Excel y TXT

---

## 📂 Insumos requeridos

- Archivo **DBF GC203T05** con las siguientes columnas obligatorias:

```
MUNICIPIO
ZONA
MANZANA
LOTE
EDIFICIO
DEPTO
VTERRPROP
VTERRCOM
VCONSPROP
VCONSCOM
```

---

## 🛡️ Validaciones implementadas

El script cuenta con un esquema robusto de validaciones:

### Archivo DBF
- Verifica que el archivo sea seleccionado
- Comprueba que el DBF sea válido y cargable en QGIS
- Valida que contenga registros
- Confirma que incluya todas las columnas requeridas

### Datos ingresados por el usuario

**Ejercicio**
- Debe ser numérico
- Exactamente 4 dígitos (ej. 2024)

**Periodo inicio / fin**
- Valores numéricos entre 1 y 12
- El periodo inicio no puede ser mayor al periodo fin

**Estatus**
- Valor numérico
- Rango permitido: 1 a 9

**Registros por TXT**
- Valor entero positivo

Ante cualquier inconsistencia, el script muestra un mensaje descriptivo mediante ventanas de QGIS y detiene la ejecución.

---

## 🧮 Procesamiento de la información

### Construcción de la clave catastral

La clave catastral se forma concatenando los siguientes campos, aplicando ceros a la izquierda según corresponda:

| Campo | Longitud |
|-----|---------|
| MUNICIPIO | 3 |
| ZONA | 2 |
| MANZANA | 3 |
| LOTE | 2 |
| EDIFICIO | 2 |
| DEPTO | 4 |


### Cálculo del valor catastral

El valor catastral se obtiene mediante la suma de:

- VTERRPROP
- VTERRCOM
- VCONSPROP
- VCONSCOM

El resultado se guarda en una columna dinámica con el nombre:

```
VC{EJERCICIO}
```

---

## 📤 Salidas generadas

Para cada municipio se generan:

- **Archivo Excel (.xlsx)** con todos los registros del municipio
- **Uno o varios archivos TXT**, según el límite máximo de registros definido

### Formato del TXT

- Delimitador: `|`
- Sin encabezados
- Codificación estándar

---

## 🗺️ Organización de archivos

Los archivos se nombran con la siguiente estructura:

```
<MUNICIPIO>_<NOMBRE_MUNICIPIO>_VALORES_<EJERCICIO>.xlsx
<MUNICIPIO>_<NOMBRE_MUNICIPIO>_VALORES_<EJERCICIO>_PARTE_#.txt
```

---

## ✅ Mensajes al usuario

- Los errores se muestran mediante ventanas emergentes claras y descriptivas
- Al finalizar correctamente, se notifica al usuario que los archivos fueron generados con éxito

---

## 🏁 Consideraciones finales

- El script está pensado para uso **institucional y operativo**
- Evita errores silenciosos y archivos mal formados
- Es adecuado para capacitación, entrega a municipios y procesos productivos

Se recomienda no modificar la estructura sin validar previamente los impactos en los formatos de salida.
