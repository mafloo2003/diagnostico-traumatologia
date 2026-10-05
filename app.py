import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="SE Traumatología y Reumatología",
    page_icon="🦴",
    layout="centered"
)

st.title("🦴 Sistema Experto: Diagnóstico de Enfermedades Óseas y Articulares")
st.caption("Especialidad: Traumatología / Reumatología")

st.markdown("""
> **Aviso médico:** Este software es un prototipo interactivo con fines educacionales. 
> No sustituye la evaluación clínica presencial, radiografías, ecografías ni análisis de laboratorio (líquido sinovial, reactantes de fase aguda).
""")

st.divider()

# --- FORMULARIO DE RECOLECCIÓN DE DATOS ---
st.subheader("1. Características del Dolor y Articulación Afectada")

patron_articular = st.selectbox(
    "¿Cuántas articulaciones están afectadas principalmente?",
    [
        "Monoarticular (Solo 1 articulación)",
        "Oligoarticular (De 2 a 4 articulaciones)",
        "Poliarticular (5 o más articulaciones)"
    ]
)

articulaciones_especificas = st.multiselect(
    "Seleccione las articulaciones afectadas:",
    ["Dedo gordo del pie (1ª MTP)", "Rodilla", "Cadera", "Muñeca / Manos (Metacarpofalángicas)", "Columna vertebral", "Otras"]
)

ritmo_dolor = st.radio(
    "¿Cómo se comporta el dolor con el movimiento o el reposo?",
    [
        "Inflamatorio: Empeora en reposo o al despertar, mejora con el movimiento (Acompañado de rigidez matutina > 30 min)",
        "Mecánico: Empeora con la carga/movimiento y al final del día, mejora significativamente con el reposo",
        "Atroz y continuo: Dolor severo e insoportable que no cede en ninguna posición"
    ]
)

st.subheader("2. Signos Inflamatorios y Síntomas Sistémicos")
col1, col2 = st.columns(2)
with col1:
    eritema_calor = st.checkbox("Enrojecimiento y calor local intenso")
    hinchazon = st.checkbox("Hinchazón / Derrame articular evidente")
    fiebre = st.checkbox("Fiebre o escalofríos")
with col2:
    imposibilidad_carga = st.checkbox("Incapacidad absoluta para apoyar o mover la articulación")
    deformidad = st.checkbox("Deformidad articular o nódulos visibles")
    fatiga = st.checkbox("Cansancio generalizado o pérdida de peso")

st.subheader("3. Factores de Riesgo y Antecedentes")
col3, col4 = st.columns(2)
with col3:
    edad = st.number_input("Edad del paciente", min_value=1, max_value=120, value=55)
    trauma_reciente = st.checkbox("Golpe o traumatismo reciente en la zona")
    hiperuricemia = st.checkbox("Antecedente de ácido úrico alto (Gota)")
with col4:
    infeccion_reciente = st.checkbox("Infección previa reciente (respiratoria, urinaria o cutánea)")
    cirugia_protesis = st.checkbox("Cirugía previa o presencia de prótesis en la articulación")
    historia_familiar = st.checkbox("Antecedentes familiares de enfermedades autoinmunes")

st.divider()

# --- MOTOR DE INFERENCIA ---
def evaluar_caso_trauma():
    # 1. Regla de Urgencia Crítica: Artritis Séptica
    if fiebre and imposibilidad_carga and ("Monoarticular" in patron_articular) and (eritema_calor or trauma_reciente or cirugia_protesis):
        return (
            "ALTA SOSPECHA DE ARTRITIS SÉPTICA (Urgencia Traumatológica)",
            "Infección bacteriana aguda dentro de la articulación. Es una emergencia que puede destruir el cartílago articular en pocas horas.",
            "error",
            [
                "Acudir de inmediato a Urgencias / Traumatología.",
                "Realizar artrocentesis (punción articular) para análisis y cultivo de líquido sinovial antes de iniciar antibióticos.",
                "Solicitar analítica de sangre: Hemograma, VSG y PCR.",
                "Posible indicación de lavado articular quirúrgico y antibioticoterapia intravenosa."
            ]
        )

    # 2. Regla de Crisis Aguda por Microcristales: Gota Aguda
    if ("Dedo gordo del pie (1ª MTP)" in articulaciones_especificas or "Rodilla" in articulaciones_especificas) and ("Monoarticular" in patron_articular) and eritema_calor and hinchazon and (hiperuricemia or "Atroz" in ritmo_dolor):
        return (
            "PROBABLE ARTRITIS GOTOSA AGUDA (Gota)",
            "Inflamación articular aguda por depósito de cristales de urato monosódico.",
            "warning",
            [
                "Consulta con Reumatología o Medicina Interna.",
                "Medición de ácido úrico en sangre (aunque puede estar normal en la crisis aguda).",
                "Tratamiento antiinflamatorio agudo (AINEs, Colchicina o Corticoides según indicación médica).",
                "Evitar aspirina e iniciar dieta baja en purinas (restringir carnes rojas, mariscos y alcohol)."
            ]
        )

    # 3. Regla de Enfermedad Degenerativa: Osteoartritis / Artrosis
    if "Mecánico" in ritmo_dolor and (edad >= 50 or trauma_reciente) and ("Monoarticular" in patron_articular or "Oligoarticular" in patron_articular):
        return (
            "PROBABLE OSTEOARTRITIS / ARTROSIS",
            "Desgaste progresivo del cartílago articular de origen degenerativo o postraumático.",
            "info",
            [
                "Evaluación por Traumatología o Fisiatría.",
                "Solicitar radiografía simple de la articulación afectada en carga (compara espacio articular, osteofitos).",
                "Manejo con fisioterapia, fortalecimiento muscular local y control de peso corporal.",
                "Analgésicos simples o AINEs en fases de exacerbación."
            ]
        )

    # 4. Regla de Enfermedad Inflamatoria Autoinmune: Artritis Reumatoide
    if "Inflamatorio" in ritmo_dolor and "Poliarticular" in patron_articular and ("Muñeca / Manos (Metacarpofalángicas)" in articulaciones_especificas) and (deformidad or fatiga or historia_familiar):
        return (
            "SOSPECHA DE ARTRITIS REUMATOIDE O ARTRITIS INFLAMATORIA",
            "Trastorno autoinmune crónico que afecta principalmente el tejido sinovial de articulaciones pequeñas de forma simétrica.",
            "warning",
            [
                "Evaluación prioritaria por Reumatología.",
                "Solicitar perfil reumático: Factor Reumatoideo (FR), Anticuerpos anti-CCP, VSG y PCR.",
                "Radiografías de manos y pies para valorar erosiones óseas.",
                "Evaluación para inicio oportuno de FÁRME (Fármacos Antirreumáticos Modificadores de la Enfermedad)."
            ]
        )

    # 5. Caso por defecto / Bajo Riesgo o Inespecífico
    return (
        "DOLOR ARTICULAR INESPECÍFICO / TENOPATÍA O LESIÓN LIGAMENTOSA",
        "El cuadro no reúne criterios claros para una patología infecciosa o autoinmune aguda severa en este momento.",
        "success",
        [
            "Guardar reposo relativo de la articulación afectada.",
            "Aplicar frío o calor local según recomendación para control del dolor.",
            "Si la inflamación persiste por más de 7 días o aparece fiebre, consultar al médico general o traumatólogo."
        ]
    )

# --- BOTÓN DE EJECUCIÓN ---
if st.button("Ejecutar Diagnóstico Traumatológico/Reumatológico", type="primary"):
    diagnostico, explicacion, estilo, recomendaciones = evaluar_caso_trauma()

    st.subheader("Resultado del Diagnóstico Experto")
    
    if estilo == "error":
        st.error(f"🚨 **Diagnóstico Principal: {diagnostico}**")
    elif estilo == "warning":
        st.warning(f"⚠️ **Diagnóstico Principal: {diagnostico}**")
    elif estilo == "info":
        st.info(f"ℹ️ **Diagnóstico Principal: {diagnostico}**")
    else:
        st.success(f"✅ **Diagnóstico Principal: {diagnostico}**")

    st.write(f"**Análisis del SE:** {explicacion}")

    st.markdown("**Recomendaciones y Plan Operativo:**")
    for rec in recomendaciones:
        st.markdown(f"- {rec}")
