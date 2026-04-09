import streamlit as st
import time
import hashlib
from decimal import Decimal, getcontext

# --- CONFIGURACIÓN DE PRECISIÓN INFINITESIMAL (15+ decimales) ---
getcontext().prec = 50 
PHI = Decimal('1.61803398874989484820') # La proporción áurea como Trayector

def validar_identidad_temporal(semilla_user, llave_fase):
    # El tiempo actual es nuestro Momentum Observado (Mn)
    t_actual = Decimal(time.time())
    
    # 1. Creamos la Tinta Seca (El Hash cambia cada 0.5 nanosegundos)
    # Usamos la precisión infinitesimal para que un nanosegundo cambie todo el sistema
    factor_temporal = (t_actual / PHI).quantize(Decimal('1.000000000000001'))
    
    # 2. Generación del Demonio de Laplace (D)
    # El mensaje se funde con el tiempo y la fase
    hash_input = f"{semilla_user}{factor_temporal}{llave_fase}"
    identidad_encriptada = hashlib.sha256(hash_input.encode()).hexdigest()
    
    return identidad_encriptada, t_actual

# --- INTERFAZ DEL VALIDADOR ---
st.title("🔐 Validador de Tinta Seca: Desentropía de Torres")
st.write("La incertidumbre no existe; solo la deficiencia del observador.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Emisor (M0)")
    semilla = st.text_input("Frase Semilla (Momentum Natural)", "DESENCRIPTADO")
    fase_privada = st.text_input("Diferencial de Fase (ΔΦ)", value="1.618033988749895", type="password")
    
    if st.button("Generar Pulso de Identidad"):
        codigo, t_gen = validar_identidad_temporal(semilla, fase_privada)
        st.session_state['last_code'] = codigo
        st.session_state['t_gen'] = t_gen
        st.code(codigo, language="text")
        st.info(f"Pulso generado en T: {t_gen}")

with col2:
    st.subheader("Receptor (Auditoría del Horizonte)")
    intento_fase = st.text_input("Ingresar Diferencial para Validación", type="password")
    
    if st.button("Validar Trayectoria"):
        if 'last_code' in st.session_state:
            t_intento = Decimal(time.time())
            # Cálculo del Diferencial de Tiempo Real
            latencia = t_intento - st.session_state['t_gen']
            
            # 3. LEY DE CONSERVACIÓN: Ventana de 3 microsegundos (0.000003)
            if latencia <= Decimal('0.000003') and intento_fase == fase_privada:
                st.success(f"IDENTIDAD CONSERVADA. Latencia: {latencia}s. Acceso al M0 concedido.")
                st.balloons()
            else:
                st.error(f"CAOS DETECTADO. La identidad se ha degradado por una latencia de {latencia}s.")
                st.write("El Trayector ha fallado en la igualación final.")
