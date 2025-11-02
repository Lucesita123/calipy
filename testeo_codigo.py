# Importamos Streamlit y librerías necesarias
import streamlit as st
import os 
import re 

# -----------------------------------------------------------
# FUNCIONES DE PERSISTENCIA Y ANÁLISIS (SEMANA 4 & 5)
# -----------------------------------------------------------

# Lee el historial y lo convierte en una Lista de Diccionarios.
def leer_historial():
    archivo_nombre = "registro_calorias.txt"
    registros = [] 
    
    # Comprueba si el archivo existe antes de intentar leer
    if not os.path.exists(archivo_nombre):
        st.sidebar.info("HISTORIAL: No se ha encontrado un registro anterior.")
        return registros 

    try:
        with open(archivo_nombre, 'r') as archivo:
            # Iteramos sobre cada línea del archivo
            for linea in archivo:
                # Usa Expresiones Regulares para encontrar los dos números flotantes
                # Esto asume que el formato de guardado es "limite:X kcal, Consumo:Y kcal\n"
                numeros_str = re.findall(r'(\d+\.?\d*)', linea)
                
                if len(numeros_str) == 2:
                    # Crea un diccionario con los datos del día
                    registro = {
                        'limite': float(numeros_str[0]),
                        'consumo': float(numeros_str[1])
                    }
                    registros.append(registro)
                    
            return registros
            
    except Exception as e:
        st.error(f"ERROR al leer el historial: {e}")
        return registros 


# Función de Persistencia: Guarda el diagnóstico final en un archivo (modo 'a' para añadir).
def guardar_registro(limite, calorias):
    with open ("registro_calorias.txt", 'a') as archivo: 
        diagnostico_final = f"limite:{limite}kcal, Consumo:{calorias} kcal\n"
        archivo.write(diagnostico_final)
        # Usamos st.success para notificar al usuario en la web
        st.success("✅ ¡Registro de calorías guardado en 'registro_calorias.txt'!")
        # Recarga la app para que el historial se actualice inmediatamente
        st.rerun()


# -----------------------------------------------------------
# FUNCIONES DE ENTRADA CON STREAMLIT (WIDGETS)
# -----------------------------------------------------------

# Función para obtener el límite calórico del usuario (usa st.number_input).
def obtener_limite():
    # st.number_input crea un campo numérico interactivo en la web
    limite_calorias = st.number_input(
        "Por favor, ingrese su límite de calorías diario (kcal):", 
        min_value=500.0, 
        max_value=10000.0, 
        value=2000.0, 
        step=50.0,
        key='limite_input'
    )
    # Solo devolvemos el valor. La lógica de advertencia se maneja en ejecutar_app()
    return limite_calorias


# Función para sumar las calorías consumidas en 5 comidas (usa st.number_input).
def sumar_calorias():
    st.subheader("Ingreso de Consumo Diario")
    
    # Creamos 5 widgets de Streamlit en lugar de usar un bucle con input()
    comidas = [
        st.number_input("Calorías Consumidas (Comida 1):", min_value=0.0, value=0.0, step=10.0, key='c1'),
        st.number_input("Calorías Consumidas (Comida 2):", min_value=0.0, value=0.0, step=10.0, key='c2'),
        st.number_input("Calorías Consumidas (Comida 3):", min_value=0.0, value=0.0, step=10.0, key='c3'),
        st.number_input("Calorías Consumidas (Comida 4):", min_value=0.0, value=0.0, step=10.0, key='c4'),
        st.number_input("Calorías Consumidas (Comida 5):", min_value=0.0, value=0.0, step=10.0, key='c5'),
    ]

    # Sumamos las entradas automáticamente
    cals_total = sum(comidas)
    
    # Mostramos la suma total en tiempo real
    st.info(f"Total Consumido Acumulado: **{cals_total:.1f} kcal**")
    
    return cals_total


# -----------------------------------------------------------
# FUNCIÓN DE ANÁLISIS (COMPLETADA PARA SEMANA 5)
# -----------------------------------------------------------

def mostrar_resumen(historial):
    total_registros = len(historial)
    suma_consumo = 0.0
    suma_limite = 0.0
    
    st.sidebar.subheader("📊 Análisis Histórico")
    
    if total_registros == 0:
        st.sidebar.warning("No hay suficientes datos para un análisis.")
        return

    # BLOQUE 1: ACUMULACIÓN (Lógica de suma corregida y completada)
    for registro in historial:
        # 1. Suma el consumo de este día a suma_consumo
        suma_consumo += registro['consumo'] 
        # 2. Suma el límite de este día a suma_limite
        suma_limite += registro['limite']  
    
    # BLOQUE 2: CÁLCULO Y DISPLAY (Lógica de promedio corregida y completada)
    # 3. Calcula el promedio del consumo total (Protegido de división por cero)
    promedio_consumo = suma_consumo / total_registros if total_registros > 0 else 0.0
    # 4. Calcula el promedio del límite total (Protegido de división por cero)
    promedio_limite = suma_limite / total_registros if total_registros > 0 else 0.0
    
    # Muestra los resultados usando los widgets de métricas de Streamlit
    st.sidebar.metric(label="Días Registrados", value=total_registros)
    st.sidebar.metric(label="Consumo Promedio Histórico", value=f"{promedio_consumo:.2f} kcal")
    st.sidebar.metric(label="Límite Promedio Histórico", value=f"{promedio_limite:.2f} kcal")


# -----------------------------------------------------------
# LA FUNCIÓN PRINCIPAL DE STREAMLIT
# -----------------------------------------------------------

def ejecutar_app():
    # Configuración de la página
    st.set_page_config(page_title="App de Calorías", layout="centered")
    st.title("🏃‍♂️ Control de Calorías Diario")
    st.markdown("Una aplicación para monitorear tu historial de límites y consumos calóricos.")

    # 1. Carga el historial (Semana 4)
    historial_de_datos = leer_historial()
    
    # 2. Muestra el resumen (Semana 5)
    mostrar_resumen(historial_de_datos)
    
    # 3. Obtener y calcular datos nuevos
    col1, col2 = st.columns(2)
    
    with col1:
        limite = obtener_limite()
        
        # ✅ Lógica de advertencia de rango bajo CORREGIDA: 
        # Esta es la manera correcta de mostrar el aviso en Streamlit.
        if limite < 1200:
            st.warning("⚠️ ¡Atención! El límite calórico ingresado es muy bajo. Consulta a un profesional de la salud antes de iniciar una dieta tan restrictiva.")
            
    with col2:
        # El consumo se calcula en tiempo real con los widgets
        calorias = sumar_calorias()


    st.markdown("---")
    st.header("Resultado del Día")
    
    # 4. Mostrar diagnóstico (Semana 3)
    st.markdown(f"**Límite diario:** {limite:.1f} kcal")
    st.markdown(f"**Total consumido:** {calorias:.1f} kcal")
    
    diferencia = limite - calorias
    
    if st.button("Analizar y Guardar Registro"):
        if diferencia >= 0:
            st.success(f"🥳 ¡Felicidades! Estás **{diferencia:.1f} kcal** por debajo de tu límite.")
            st.balloons()
        else:
            st.error(f"⚠️ ¡Atención! Has sobrepasado tu límite por **{-diferencia:.1f} kcal**.")

        # 5. Guarda el nuevo registro (Semana 4)
        guardar_registro(limite, calorias)


# Llamada principal que inicia la aplicación
if __name__ == "__main__":
    ejecutar_app()
