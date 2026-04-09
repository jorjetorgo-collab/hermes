import streamlit as st
import pandas as pd
import numpy as np
import time
import hashlib
import random
from decimal import Decimal, getcontext

# --- CONFIGURACIÓN DE SOBERANÍA ---
getcontext().prec = 50 
st.set_page_config(page_title="Teorema de Torres - Hub", layout="wide")

# --- FUNCIONES DEL TRAYECTOR ---

def generar_coordenadas_falsas():
    # Desvío táctico para el interceptor
    lat = random.uniform(20.6, 20.7) # Cerca de Guadalajara para despistar
    lon = random.uniform(-103.4, -103.3)
    return f"SENSITIVE_DATA_LOC: {lat:.6f}, {lon:.6f} | STATUS: ENCRYPTED"

def auditoria_defensiva(latencia, fase_correcta, fase_intento):
    UMBRAL = Decimal('0.000003') # 3 microsegundos
    if latencia <= UMBRAL and fase_intento == fase_correcta:
        return "SINCERIDAD", "DESENCRIPTADO"
    elif latencia > UMBRAL:
        return "ESPEJISMO", generar_coordenadas_falsas()
    else:
        return "BLOQUEO", "ERROR_DE_FASE: IDENTIDAD NO LOCALIZABLE"

# --- INTERFAZ DE USUARIO ---
st.sidebar.title("🛡️ Ley de Conservación de Identidad")
app_mode = st.sidebar.selectbox("Selecciona el Experimento", 
                                ["1. Enjambre de Drones (M0)", "2. Criptografía de Tinta Seca"])

if app_mode == "1. Enjambre de Drones (M0)":
    st.header("🛸 Simulación de Enjambre (Trayector N)")
    v_kmh = st.sidebar.slider("Velocidad (km/h)", 10, 150, 60)
    radio_elipse = st.sidebar.slider("Radio de Órbita (m)", 1, 20, 8)
    
    if st.button("Lanzar Trayector"):
        n_drones = 52
        v_ms = v_kmh / 3.6
        placeholder = st.empty()
        
        for t in np.arange(0, 40, 0.4):
            puntos = []
            for i in range(n_drones):
                # Cruce sigmoidal para evitar el avance "errático"
                factor_cruce = 1 / (1 + np.exp(-0.2 * (t - 20)))
                x_inicio = (i / 51) * 2000 - 1000
                x_actual = x_inicio + (-x_inicio - x_inicio) * factor_cruce
                
                y_base = v_ms * t - (abs(i - 25.5) * 15)
                dx = np.cos(2 * np.pi * 0.3 * t) * radio_elipse
                dy = np.sin(2 * np.pi * 0.3 * t) * (radio_elipse * 0.5)
                
                puntos.append({'X': x_actual + dx, 'Y': y_base + dy, 'Unidad': i})
            
            df = pd.DataFrame(puntos)
            with placeholder.container():
                st.scatter_chart(df, x='X', y='Y', size=40)
            time.sleep(0.01)

elif app_mode == "2. Criptografía de Tinta Seca":
    st.header("🔐 Validador de Identidad Temporal")
    st.write("El interceptor será desviado por su propia latencia estructural.")
    
    col1, col2 = st.columns(2)
    with col1:
        semilla = st.text_input("M0 (Semilla)", value="DESENCRIPTADO")
        fase_privada = st.text_input("Fase Eli (ΔΦ)", value="1.618033988749895", type="password")
        if st.button("Generar Pulso"):
            t_gen = Decimal(time.time())
            st.session_state['t_gen'] = t_gen
            st.session_state['fase'] = fase_privada
            st.success(f"Pulso generado a las {t_gen}")
            
    with col2:
        intento_fase = st.text_input("Validar con Fase", type="password")
        if st.button("Validar Trayectoria"):
            if 't_gen' in st.session_state:
                latencia = Decimal(time.time()) - st.session_state['t_gen']
                estado, resultado = auditoria_defensiva(latencia, st.session_state['fase'], intento_fase)
                
                if estado == "SINCERIDAD":
                    st.success(f"IDENTIDAD CONSERVADA: {resultado}")
                elif estado == "ESPEJISMO":
                    st.warning("⚠️ DESVIACIÓN TÁCTICA ACTIVADA")
                    st.code(resultado)
                else:
                    st.error(resultado)
