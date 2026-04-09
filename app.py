# --- DENTRO DEL BLOQUE DEL RECEPTOR (col2) ---
if st.button("Validar Trayectoria"):
    if 't_gen' in st.session_state:
        # 1. CAPTURA DEL MOMENTUM ACTUAL (Mn)
        t_intento = Decimal(time.time())
        
        # 2. CÁLCULO DEL DIFERENCIAL (Aquí es donde nace 'latencia')
        latencia = t_intento - st.session_state['t_gen']
        
        # 3. EJECUCIÓN DEL TRAYECTOR DEFENSIVO
        # Ahora 'latencia' ya existe y puede ser enviada a la función
        estado, mensaje_salida = auditoria_defensiva(latencia, fase_privada, intento_fase)
        
        # 4. RESULTADO SEGÚN LA RESOLUCIÓN DEL OBSERVADOR
        if estado == "SINCERIDAD":
            st.success(f"✅ IDENTIDAD RECUPERADA: {mensaje_salida}")
            st.balloons()
        elif estado == "ESPEJISMO":
            st.warning("⚠️ DESVIACIÓN DETECTADA: Trayectoria interceptada.")
            st.code(mensaje_salida, language="bash")
            st.info("El interceptor ha sido desviado a coordenadas falsas.")
        else:
            st.error(mensaje_salida)
    else:
        st.error("Error: No hay un pulso generado para validar.")
