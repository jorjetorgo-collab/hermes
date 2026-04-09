import streamlit as st
import random
from decimal import Decimal

# --- GENERADOR DE COORDENADAS FANTASMA ---
def generar_coordenadas_falsas():
    # Genera una ubicación plausible pero aleatoria (ej. en medio del Océano o el Desierto)
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return f"COORD_SENSITIVE: {lat:.6f}, {lon:.6f} | STATUS: ENCRYPTED_STREAM"

def auditoria_defensiva(latencia, fase_correcta, fase_intento):
    UMBRAL = Decimal('0.000003') # 3 microsegundos de soberanía
    
    # 1. ÉXITO: Sincronía pura (M0)
    if latencia <= UMBRAL and fase_intento == fase_correcta:
        return "SINCERIDAD", "DESENCRIPTADO"
    
    # 2. DEFENSA: Latencia detectada (Hackers / Interceptores)
    elif latencia > UMBRAL:
        # El interceptor recibe datos que parecen valiosos pero son señuelos
        return "ESPEJISMO", generar_coordenadas_falsas()
    
    # 3. BLOQUEO: Error de fase
    else:
        return "BLOQUEO", "ERROR_DE_FASE: IDENTIDAD NO LOCALIZABLE"

# --- INTERFAZ DE AUDITORÍA ---
# (Dentro del flujo de validación de tu app)

# ... [código previo de cálculo de latencia] ...

estado, mensaje_salida = auditoria_defensiva(latencia, fase_privada, intento_fase)

if estado == "SINCERIDAD":
    st.success(f"✅ IDENTIDAD RECUPERADA: {mensaje_salida}")
    st.balloons()
elif estado == "ESPEJISMO":
    st.warning("⚠️ DESVIACIÓN DETECTADA: Activando contramedidas de fase.")
    st.code(mensaje_salida, language="bash")
    st.info("El interceptor está siguiendo una trayectoria señuelo.")
