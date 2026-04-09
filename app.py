import streamlit as st
import random
import pandas as pd
from decimal import Decimal

# --- LÓGICA DE DEFENSA ACTIVA (ESPEJISMO) ---

def generar_ruido_sin_sentido():
    """Genera una cadena caótica para confundir al interceptor."""
    caracteres = "0123456789ABCDEF!@#$%^&*()_+¿?¡"
    return "".join(random.choice(caracteres) for _ in range(20))

def auditoria_de_fase(latencia, fase_correcta, fase_intento):
    # Umbral de Soberanía (3 microsegundos)
    UMBRAL = Decimal('0.000003')
    
    # 1. CASO DE ÉXITO: Sincronía Total
    if latencia <= UMBRAL and fase_intento == fase_correcta:
        return "SINCERIDAD", "DESENCRIPTADO"
    
    # 2. CASO DE INTERCEPCIÓN: Latencia detectada (Envenenamiento)
    elif latencia > UMBRAL:
        # El interceptor ve algo que parece código pero no tiene sentido
        mensaje_falso = f"ERR_{generar_ruido_sin_sentido()}_NULL"
        return "ENVENENAMIENTO", mensaje_falso
    
    # 3. CASO DE ERROR DE FASE: Clave incorrecta
    else:
        return "CAOS", "IDENTIDAD_NO_TRAZADA"

# --- INTEGRACIÓN EN LA INTERFAZ ---
# (Este bloque iría dentro del botón 'Validar Trayectoria')

# ... (código previo de cálculo de latencia)

estado, resultado = auditoria_de_fase(latencia, fase_privada, intento_fase)

if estado == "SINCERIDAD":
    st.success(f"M0 REVELADO: {resultado}")
    st.balloons()
elif estado == "ENVENENAMIENTO":
    st.warning("⚠️ ALERTA DE SEGURIDAD: Trayectoria interceptada o latencia excedida.")
    st.error(f"CONTENIDO PARA EL OBSERVADOR: {resultado}")
    st.info("El sistema ha inyectado desorden para proteger la identidad original.")
