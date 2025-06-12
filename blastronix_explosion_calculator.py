
import streamlit as st
from fpdf import FPDF
import base64
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Blastronix – Calculadora de Energía Explosiva", layout="centered")

# --- CABECERA ---
st.image("https://i.imgur.com/gub9jFO.png", width=250)  # Logo Blastronix en línea
st.title("Calculadora de Energía Explosiva")
st.markdown("**Versión inicial – Blastronix Technical Solutions**")

st.markdown("---")

# --- PARÁMETROS DE ENTRADA ---
st.header("🔧 Parámetros de entrada")

col1, col2 = st.columns(2)

with col1:
    length = st.number_input("Longitud del explosivo (m)", min_value=0.1, value=3.0, step=0.1)
    diameter = st.number_input("Diámetro del explosivo (mm)", min_value=10, value=32, step=1)
    energy_MJ_kg = st.number_input("Energía específica del explosivo (MJ/kg)", min_value=0.1, value=4.2, step=0.1)

with col2:
    density = st.number_input("Densidad del explosivo (g/cm³)", min_value=0.1, value=1.2, step=0.1)
    hole_diameter = st.number_input("Diámetro del taladro (mm)", min_value=10, value=38, step=1)

# --- CÁLCULOS ---
volume_explosive_m3 = (3.1416 / 4) * (diameter / 1000) ** 2 * length
mass_kg = volume_explosive_m3 * (density * 1000)
explosion_energy_MJ = mass_kg * energy_MJ_kg

explosive_area = (3.1416 / 4) * (diameter ** 2)
hole_area = (3.1416 / 4) * (hole_diameter ** 2)
coupling = (explosive_area / hole_area) * 100

# --- RESULTADOS ---
st.markdown("---")
st.header("📈 Resultados calculados")

col1, col2 = st.columns(2)
col1.metric("💣 Energía total de explosión (MJ)", f"{explosion_energy_MJ:.2f}")
col1.metric("🧨 Carga explosiva por taladro (kg)", f"{mass_kg:.2f}")
col2.metric("⚡ Energía disponible por taladro (MJ)", f"{explosion_energy_MJ:.2f}")
col2.metric("🌀 Acoplamiento del explosivo (%)", f"{coupling:.1f}")

# --- EXPORTACIÓN A PDF ---
st.markdown("---")
st.subheader("📤 Exportar a PDF")

def generar_pdf(energia, masa, acoplamiento):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Cálculo de Energía Explosiva - Blastronix", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Energía total de explosión: {energia:.2f} MJ", ln=True)
    pdf.cell(0, 10, f"Carga explosiva por taladro: {masa:.2f} kg", ln=True)
    pdf.cell(0, 10, f"Acoplamiento del explosivo: {acoplamiento:.1f} %", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="Blastronix_Explosion_Report.pdf">📄 Descargar PDF</a>'

st.markdown(generar_pdf(explosion_energy_MJ, mass_kg, coupling), unsafe_allow_html=True)
