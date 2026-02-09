# Análisis de Tiempo de Ejecución - prob_cond_bin

Este documento describe cómo usar el módulo de análisis de tiempo para estudiar el comportamiento de la función `prob_cond_bin`.

## Descripción

El análisis de tiempo mide cómo varía el tiempo de ejecución de la función `prob_cond_bin` en función de:
1. **Número de variables de interés**: Variables cuya distribución condicional se calcula
2. **Número de variables condicionadas**: Variables sobre las que se condiciona

## Uso

### Opción 1: Análisis Automático (Recomendado)

Ejecuta directamente el módulo `timing_analyzer.py`:

```bash
python3 timing_analyzer.py
```

El script te pedirá:
- **Número de variables**: El número total de variables (recomendado 8-15 para un análisis rápido)

El análisis ejecutará múltiples configuraciones automáticamente y generará:
- **Tabla con resultados**: Mostrada en la consola
- **Archivo CSV**: `timing_results.csv` con todos los datos tabulares
- **Gráficos** (si matplotlib está disponible): `timing_results.png` con visualizaciones

### Opción 2: Desde el menú principal

Ejecuta `main.py` y selecciona la opción 2:

```bash
python3 main.py
```

Luego selecciona:
```
1. Calcular probabilidades condicionales
2. Análisis de tiempo de ejecución (prob_cond_bin)
```

Elige la opción 2.

## Resultados

### Tabla de Resultados

La salida mostrará una tabla con el siguiente formato:

```
======================================================================================================
ANÁLISIS DE TIEMPO DE EJECUCIÓN - prob_cond_bin
======================================================================================================
Config          Variables                      Tiempo Promedio      Rango       
                I / C / Otros                  (ms)                 (ms)        
------------------------------------------------------------------------------------------------------
I=0,C=0,O=8     0 / 0 / 8                           0.154705      0.1393 - 0.1682
I=0,C=1,O=7     0 / 1 / 7                           0.075208      0.0745 - 0.0759
...
```

Donde:
- **Config**: Configuración (I=variables interés, C=variables condicionadas, O=variables otras)
- **I / C / Otros**: Desglose de variables
- **Tiempo Promedio**: Tiempo medio de ejecución en milisegundos
- **Rango**: Mínimo y máximo entre repeticiones

### Archivo CSV

El archivo `timing_results.csv` contiene los datos tabulares con las siguientes columnas:

```
Config,Variables_Interes,Variables_Condicionadas,Variables_Otras,Tiempo_Promedio_ms,Tiempo_Min_ms,Tiempo_Max_ms
```

Puedes abrir este archivo en Excel, Google Sheets o cualquier herramienta de análisis de datos.

### Gráficos

Si matplotlib está instalado, se generará un archivo `timing_results.png` con 4 gráficos:

1. **Gráfico 1**: Tiempo vs Número de Variables de Interés
   - Muestra cómo aumenta el tiempo según crece el número de variables de interés

2. **Gráfico 2**: Tiempo vs Número de Variables Condicionadas  
   - Muestra cómo varía el tiempo con el número de variables condicionadas

3. **Gráfico 3**: Heatmap de Tiempo de Ejecución
   - Mapa de calor bidimensional mostrando el tiempo para cada combinación
   - Eje X: Variables Condicionadas
   - Eje Y: Variables de Interés
   - Color más oscuro = tiempo más largo

4. **Gráfico 4**: Distribución de Tiempos
   - Box plot mostrando la variação de tiempos para diferentes configuraciones

## Instalación de Dependencias (Opcional)

### Para gráficos

Si deseas generar los gráficos PNG, instala matplotlib y numpy:

```bash
pip3 install matplotlib numpy
```

O en sistemas con restricciones:

```bash
apt-get install python3-matplotlib python3-numpy
```

### Sin gráficos

El análisis funciona perfectamente sin matplotlib. Generará:
- Tabla de resultados en la consola
- Archivo CSV con todos los datos

## Interpretación de Resultados

### Observaciones Típicas

1. **Crecimiento Exponencial**: El tiempo generalmente crece exponencialmente con el número de variables de interés (ya que la salida es $2^n$)

2. **Impacto de Variables Condicionadas**: Más variables condicionadas generalmente reducen el tiempo (menos estados a calcular)

3. **Variabilidad**: Puede haber variación entre ejecuciones debido a carga del sistema

## Ejemplos

### Análisis con 10 variables

```bash
echo "10" | python3 timing_analyzer.py
```

Esto generará resultados para todas las combinaciones posibles de:
- Variables de interés: 0 a 10
- Variables condicionadas: 0 a (10 - variables_interés)

### Análisis con 12 variables

```bash
echo "12" | python3 timing_analyzer.py
```

Para un análisis más completo (puede tomar más tiempo).

## Archivos Generados

- `timing_results.csv` - Datos tabulares en formato CSV
- `timing_results.png` - Gráficos PNG (si matplotlib está disponible)

## Notas

- Cada medición se repite 3 veces y se calcula el promedio
- Se generan varias configuraciones para cada par (variables_interés, variables_condicionadas)
- El tiempo se mide en milisegundos (ms)
- Los resultados pueden variar ligeramente según la carga del sistema
