import streamlit as st
import time
import hashlib
import random
from decimal import Decimal, getcontext

# --- CONFIGURACIÓN DE PRECISIÓN (LEY DE CONSERVACIÓN) ---
getcontext().prec = 50 
st.set_page_config(page_title="Validador de Tinta Seca - M0", layout="centered")

def generar_coordenadas_falsas():
    # Coordenadas que parecen reales (Zona metropolitana de Guadalajara)
    lat = random.uniform(20.6500, 20.7000)
    lon = random.uniform(-103.4000, -103.3000)
    return f"SENSITIVE_LOC_DETECTED: {lat:.6f}, {lon:.6f} | PROTOCOL: MI_TEMA_SECRET"

def auditoria_defensiva(latencia, fase_correcta, fase_intento):
    UMBRAL = Decimal('0.000003') # 3 microsegundos de soberanía
    
    # 1. ÉXITO: Sincronía pura (M0)
    if latencia <= UMBRAL and fase_intento == fase_correcta:
        return "SINCERIDAD", "DESENCRIPTADO"
    
    # 2. DEFENSA: Latencia detectada (El interceptor se desvía por nanosegundos)
    elif latencia > UMBRAL:
        return "ESPEJISMO", generar_coordenadas_falsas()
    
    # 3. BLOQUEO: Error de fase (Clave incorrecta)
    else:
        return "BLOQUEO", "ERROR_DE_FASE: IDENTIDAD NO LOCALIZABLE"

# --- INTERFAZ ---
st.title("🔐 Validador de Identidad Temporal")
st.markdown("### Protocolo de Desentropía Operativa")
st.write("Si el observador carece de resolución temporal, la identidad se transmuta en un espejismo.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Emisor (M0)")
    semilla = st.text_input("Frase Semilla", value="DESENCRIPTADO")
    fase_privada = st.text_input("Diferencial de Fase (ΔΦ)", value="1.618033988749895", type="password")
    
    if st.button("Generar Pulso de Identidad"):
        # Guardamos el momento exacto del nacimiento del pulso
        st.session_state['t_gen'] = Decimal(time.time())
        st.session_state['fase_master'] = fase_privada
        st.success("Pulso de Identidad emitido al horizonte.")

with col2:
    st.subheader("Receptor (Auditoría)")
    intento_fase = st.text_input("Validar Fase para acceso", type="password")
    
    if st.button("Validar Trayectoria"):
        if 't_gen' in st.session_state:
            # Calculamos la latencia del trayecto
            t_actual = Decimal(time.time())
            latencia = t_actual - st.session_state['t_gen']
            
            # Ejecutamos el filtro de Torres
            estado, mensaje_salida = auditoria_defensiva(latencia, st.session_state['fase_master'], intento_fase)
            
            if estado == "SINCERIDAD":
                st.success(f"✅ IDENTIDAD CONSERVADA: {mensaje_salida}")
                st.balloons()
            elif estado == "ESPEJISMO":
                st.warning("⚠️ DESVIACIÓN DETECTADA: Latencia fuera de rango.")
                st.code(mensaje_salida, language="bash")
                st.info("El interceptor está siguiendo coordenadas falsas.")
            else:
                st.error(mensaje_salida)
        else:
            st.error("No se ha generado ningún pulso previo.")

st.divider()
st.caption("Basado en el Teorema de Torres: La incertidumbre es una deficiencia del observador.")
