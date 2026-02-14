import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
NOMBRE_ARCHIVO = 'data/llegada_autobuses.csv'

df = pd.read_csv(NOMBRE_ARCHIVO)

def cargar_y_limpiar_datos():
    
    if not os.path.exists(NOMBRE_ARCHIVO):
        print(f"\n ERROR CRÍTICO: No se encuentra el archivo '{NOMBRE_ARCHIVO}'.")
        print(f" {os.getcwd()}")
        return None

    try:
        
        try:
            df = pd.read_csv(NOMBRE_ARCHIVO, encoding='utf-8')
        except UnicodeDecodeError:
            print(" Aviso: Codificación UTF-8 falló, intentando con Latin-1...")
            df = pd.read_csv(NOMBRE_ARCHIVO, encoding='latin-1')

        # ESTANDARIZACIÓN DE COLUMNAS
        # Esto elimina espacios en blanco al inicio/final de los nombres de columnas para poder utilizar mejor los datos
        
        df.columns = df.columns.str.strip()
        
        # Opcional: Convertir todo a minúsculas para evitar errores de tipeo

        # Esta columna permite encontrar las principales columnas para poder  realizar los historicos
        columnas_criticas = ['retraso_minutos', 'dia_semana', 'ocupacion_porcentaje']
        for col in columnas_criticas:
            if col not in df.columns:
                print(f" No se encontró la columna '{col}' en el CSV.")
                print(f"   Columnas detectadas: {list(df.columns)}")
                return None
        
        return df

    except Exception as e:
        print(f"\n Ocurrió un error al leer el archivo: {e}")
        return None

def mostrar_promedios_por_dia(df):
    print("\n--- CONSULTA DE PROMEDIOS POR DÍA ---")
    
    # Obtenemos la lista de días únicos presentes en el archivo 
    dias_disponibles = df['dia_semana'].unique()
    print(f"Días encontrados en tu archivo: {', '.join(map(str, dias_disponibles))}")
    
    dia_input = input("Escribe el día que quieres analizar: ").strip()
    
    # Filtro insensible a mayúsculas/minúsculas
    try:
        datos_dia = df[df['dia_semana'].astype(str).str.lower() == dia_input.lower()]
        
        if datos_dia.empty:
            print(f" No hay registros para '{dia_input}'. Revisa si escribiste bien el día.")
        else:
            prom_retraso = datos_dia['retraso_minutos'].mean()
            # Manejo de error si la columna ocupación tiene valores nulos
            prom_ocupacion = datos_dia['ocupacion_porcentaje'].fillna(0).mean() 
            total_viajes = len(datos_dia)

            print(f"\n RESULTADOS PARA: {dia_input.upper()}")
            print("-" * 40)
            print(f"Viajes analizados: {total_viajes}")
            print(f"Promedio de Retraso: {prom_retraso:.2f} min")
            print(f"Promedio de Ocupación: {prom_ocupacion:.2f}%")
            print("-" * 40)
            
    except Exception as e:
        print(f" Error al procesar los datos del día: {e}")

def analizar_retrasos_general(df):
    print("\n---  ANÁLISIS GLOBAL DE TIEMPOS ---")
    
    retraso_total_promedio = df['retraso_minutos'].mean()
    max_retraso = df['retraso_minutos'].max()
    
    # Identificar la ruta con peor desempeño
    if 'ruta' in df.columns:
        peor_ruta = df.groupby('ruta')['retraso_minutos'].mean().idxmax()
        retraso_peor_ruta = df.groupby('ruta')['retraso_minutos'].mean().max()
        info_ruta = f"La ruta más lenta es '{peor_ruta}' con {retraso_peor_ruta:.1f} min de retraso promedio."
    else:
        info_ruta = "(No se encontró columna 'ruta' para análisis detallado)"

    print(f" Retraso promedio de TODA la flota: {retraso_total_promedio:.2f} minutos")
    print(f" El retraso más largo registrado fue de: {max_retraso} minutos")
    print(f" {info_ruta}")

def analizar_congestion(df):
    print("\n---  DÍA DE MAYOR CONGESTIÓN ---")
    
    # Agrupamos por día y calculamos el promedio de retrasos
    # Asumimos que más retraso = más congestión
    ranking = df.groupby('dia_semana')['retraso_minutos'].mean().sort_values(ascending=False)
    
    dia_peor = ranking.index[0]
    valor_peor = ranking.iloc[0]
    
    print(f"El día con mayor congestión (basado en retrasos) es el: **{dia_peor.upper()}**")
    print(f"Con un retraso promedio de {valor_peor:.2f} minutos.")
    
    print("\nRanking completo (de peor a mejor):")
    print(ranking.map('{:.2f} min'.format))

def analizar_impacto_clima(df):
    print("\n---  ANÁLISIS DE IMPACTO DEL CLIMA ---")
    
    # Verificamos que existan las columnas necesarias
    if 'clima' not in df.columns or 'retraso_minutos' not in df.columns:
        print(" Error: Faltan columnas de clima o retraso en el CSV.")
        return

    # Agrupamos por tipo de clima calculando promedios clave
    # Esto le dice al usuario: "Cuando llueve, el bus tarda X minutos másaas
    impacto = df.groupby('clima')[['retraso_minutos', 'velocidad_promedio_kmh', 'nivel_congestion']].agg({
        'retraso_minutos': 'mean',
        'velocidad_promedio_kmh': 'mean',
        'nivel_congestion': lambda x: x.mode()[0] if not x.mode().empty else 'N/A' # Moda para ver congestión más común
    }).sort_values(by='retraso_minutos', ascending=False)
    
    print("Promedios históricos según el clima:")
    print("-" * 60)
    print(f"{'CLIMA':<15} | {'RETRASO PROM.':<15} | {'VELOCIDAD':<10} | {'CONGESTIÓN TÍPICA'}")
    print("-" * 60)
    
    for clima, fila in impacto.iterrows():
        print(f"{clima:<15} | {fila['retraso_minutos']:>6.2f} min      | {fila['velocidad_promedio_kmh']:>5.2f} km/h | {fila['nivel_congestion']}")
    print("-" * 60)

def estimar_llegada_personalizada(df):
    print("\n--- PREDICCIÓN DE LLEGADA  ---")
    
    # 1. Obtener datos del usuario
    ruta_input = input("¿Qué ruta vas a tomar? (Ej. Ruta Principal): ").strip()
    dia_input = input("¿Qué día de la semana es? (Ej. Lunes,martes ): ").strip()
    hora_input = input("¿A qué hora está PROGRAMADO tu autobús? ( ej. 08:30): ").strip()

    try:
        # Convertimos la hora del usuario a objeto datetime para poder sumar o restar ya depende del usuario
        hora_usuario = datetime.strptime(hora_input, "%H:%M")
        
        # Filtramos el DatcxaFrame por Ruta y Día
        filtro = (df['ruta'].str.lower() == ruta_input.lower()) & \
                 (df['dia_semana'].str.lower() == dia_input.lower())
        
        datos_historicos = df[filtro].copy()

        if datos_historicos.empty:
            print(f"No tengo datos históricos para la {ruta_input} los días {dia_input}.")
            return

  
        
        # Convertimos la columna 'hora_programada' a 
        datos_historicos['hora_dt'] = pd.to_datetime(datos_historicos['hora_programada'], format='%H:%M', errors='coerce')
        
        # Como to_datetime agrega fecha actual, solo nos importan las horas. 
        # Truco: Usamos .dt.hour para filtrar
        hora_buscada = hora_usuario.hour
        
        # Filtramos buses que pasaron 1 hora antes o 1 después de la hora deseada que ingresa el usuario
        datos_cercanos = datos_historicos[
            (datos_historicos['hora_dt'].dt.hour >= hora_buscada - 1) & 
            (datos_historicos['hora_dt'].dt.hour <= hora_buscada + 1)
        ]

        if datos_cercanos.empty:
            print(f"Tengo datos del día, pero no en horarios cercanos a las {hora_input}.")
            # Fallback: Usamos el promedio general del día si no hay horas cercanas
            retraso_estimado = datos_historicos['retraso_minutos'].mean()
            aviso = "(Promedio general del día, no por hora específica)"
        else:
            retraso_estimado = datos_cercanos['retraso_minutos'].mean()
            aviso = "(Basado en horarios similares)"

        # CÁLCULO FINAL 
        # Hora Estimada = Hora Programada + Retraso Promedio Histórico
        hora_real_estimada = hora_usuario + timedelta(minutes=retraso_estimado)
        
        print(f"\nREPORTE DE PREDICCIÓN PARA {ruta_input.upper()}")
        print(f"Día: {dia_input} |  Hora Base: {hora_input}")
        print("." * 50)
        print(f"Basado en {len(datos_cercanos)} registros históricos {aviso}...")
        print(f"El retraso promedio suele ser de: {retraso_estimado:.0f} minutos.")
        print(f"HORA ESTIMADA DE LLEGADA REAL: {hora_real_estimada.strftime('%H:%M')}")
        print("." * 50)

    except ValueError:
        print(" Error: Asegúrate de escribir la hora en formato HH:MM (ejemplo: 14:30).")
    except Exception as e:
        print(f" Ocurrió un error en el cálculo: {e}")

def menu():
    print("🔄 Cargando base de datos...")
    df = cargar_y_limpiar_datos()
    
    if df is None:
        return # Detener si falló la carga
#Este es el menu simple para decirle al usario que es lo que quiere hacer
    while True:
        # --- MOSTRAR MENÚ ---
        print("\n" + "▒"*50)
        print("     SISTEMA DE GESTIÓN DE AUTOBUSES")
        print("▒"*50)
        print("1.  Consultar métricas por Día")
        print("2.   Reporte General de Retrasos")
        print("3.  Identificar Día de Mayor Congestión")
        print("4.   Analizar impacto del Clima")      # Nueva función
        print("5.  Predicción de Llegada (Personalizada)") # Nueva función
        print("6.  Salir")
        print("▒"*50)
        
        opcion = input(" Seleccione una opción: ")

        # --- LÓGICA DE OPCIONES ---
        if opcion == '1':
            mostrar_promedios_por_dia(df)
            input("\n[Enter] para continuar...")
            
        elif opcion == '2':
            analizar_retrasos_general(df)
            input("\n[Enter] para continuar...")
            
        elif opcion == '3':
            analizar_congestion(df)
            input("\n[Enter] para continuar...")
            
        elif opcion == '4':
            analizar_impacto_clima(df)
            input("\n[Enter] para continuar...")
            
        elif opcion == '5':
            estimar_llegada_personalizada(df)
            input("\n[Enter] para continuar...")
            
        elif opcion == '6':
            print("Cerrando sistema... ¡Hasta luego!")
            break
            
        else:
            print("\n Opción inválida. Por favor seleccione entre 1 y 6.")

if __name__ == "__main__":
    menu()