# Predictor de llegadas de autobuses urbanos con enfoque en datos históricos y ambientales

## Descripción General

Este repositorio contiene el desarrollo del sistema predictivo diseñado para el análisis de tiempos de llegada en el transporte público urbano. El proyecto se enfoca en el procesamiento masivo de datos logísticos utilizando la librería Pandas para realizar limpieza de datos, cálculo de métricas de congestión y evaluación del impacto de variables ambientales en la eficiencia de los traslados. Esto  es una pequeña parte del Trabajo terminal que estoy realizando ya que se usa una pequeña muestra de los datos de llegada de los autobuses.

## Funcionamiento del Sistema

El software opera mediante un flujo de procesamiento de datos estructurado en módulos:

1. **Carga de Datos**: El sistema identifica y valida la presencia de archivos de datos en formato CSV dentro del directorio local del proyecto.
2. **Limpieza y Preprocesamiento**: Se implementan rutinas para normalizar las series de tiempo y manejar valores nulos en los registros de llegada.
3. **Módulo de Análisis Estadístico**: El motor de cálculo agrupa los datos por día de la semana y variables ambientales para determinar promedios de retraso.
4. **Interfaz de Usuario**: Se dispone de un menú interactivo en consola que permite al usuario seleccionar entre diversos tipos de reportes y predicciones.

### Módulos Interactivos

* **Consultar métricas por día**: Desglose de tiempos de llegada específicos.
* **Reporte General de Retrasos**: Análisis global del desempeño del sistema de autobuses.
* **Identificar Día de Mayor Congestión**: Detección automática de picos de ineficiencia.
* **Analizar impacto del Clima**: Evaluación de cómo factores ambientales afectan la puntualidad.
* **Predicción de Llegada Personalizada**: Estimación de tiempos basada en el contexto actual del usuario.

## Tecnologías Utilizadas

El proyecto está desarrollado íntegramente en Python , utilizando las siguientes librerías de soporte:

* **Pandas**: Para la manipulación y análisis de estructuras de datos masivas.
* **OS / Sys**: Para la gestión de rutas de archivos y parámetros del sistema.
* **Datetime / Timedelta**: Para el procesamiento avanzado de marcas temporales y cálculos de intervalos de tiempo.

## Instalación y Ejecución

### Requisitos Previos

Es necesario contar con Python 3.8 o superior y las dependencias listadas en el archivo de requerimientos.



### Ejecución del Código

Para iniciar el sistema interactivo, ejecute el script principal desde la terminal:

```bash
python buses.py

```

*Nota: Asegúrese de que el archivo de datos `llegada_autobuses.csv` se encuentre dentro de la carpeta `data/`  para que no haya tema de que no encuentra los datos*

## EJEMPLO DE RESULTADOS
Calcula medidas de promedio y estandarización de los datos históricos para normalizar los registros de llegada y asegurar la consistencia en el análisis de las variables ambientales. A través de este procesamiento estadístico, el sistema determina el promedio de retrasos por día y evalúa el impacto del clima en la puntualidad del servicio, permitiendo una comparación técnica entre diferentes escenarios operativos.

* **Día de mayor congestión**: Sábado.
* **Retraso promedio máximo**: 13.74 minutos.

### Ranking de retraso por día (de mayor a menor)

1. Sábado: 13.74 min.
2. Domingo: 12.75 min.
3. Jueves: 12.34 min.
4. Miércoles: 11.99 min.
5. Martes: 11.84 min.
6. Viernes: 11.38 min.
7. Lunes: 11.19 min.

## Autor

* **Yahir Ortiz** - Estudiante de Ingeniería en Inteligencia Artificial, ESCOM-IPN.

---
<img width="1394" height="1095" alt="image" src="https://github.com/user-attachments/assets/13589a5e-102c-49de-b6ad-74ae2f0db233" />
<img width="1165" height="656" alt="image" src="https://github.com/user-attachments/assets/eb482be7-d83e-4607-bacb-c070da4979f3" />
<img width="887" height="529" alt="image" src="https://github.com/user-attachments/assets/58848e93-a191-4a0d-aee5-ddffc7b5c4bc" />
<img width="880" height="636" alt="image" src="https://github.com/user-attachments/assets/cfb7ad18-ad5f-4cf2-a138-132c00c6efa6" />
<img width="802" height="636" alt="image" src="https://github.com/user-attachments/assets/81337443-9e2c-4f46-91eb-83f3ca578e25" />



