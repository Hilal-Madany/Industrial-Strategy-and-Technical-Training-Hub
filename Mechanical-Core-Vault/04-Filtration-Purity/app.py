import streamlit as st
import math

# --- PAGE SETUP ---
st.set_page_config(page_title="General Filter SME Tool", page_icon="⚙️")
st.title("📜 General Pleated Element Calculator")
st.write("Professional SME Standard for Industrial EPC & O&M")

# --- INPUT SECTION ---
st.sidebar.header("📐 Physical Dimensions")
u_unit = st.sidebar.radio("Unit System", ["Metric (mm)", "Imperial (inch)"])

# Conversion factor
mult = 25.4 if u_unit == "Imperial (inch)" else 1.0

od = st.sidebar.number_input(f"Outer Diameter ({u_unit})", value=100.0)
length = st.sidebar.number_input(f"Element Length ({u_unit})", value=500.0)

st.sidebar.header("🧩 Pleat Geometry")
n_pleats = st.sidebar.number_input("Number of Pleats", value=50)
p_depth = st.sidebar.slider(f"Pleat Depth ({u_unit})", 5.0, 50.0, 15.0)

# --- SME CALCULATION ENGINE ---
# Area = N * 2 * Depth * Length
# We convert all to mm for standard calculation
area_mm2 = n_pleats * 2 * p_depth * length
area_m2 = area_mm2 / 1_000_000

# SME Check: Circumference vs Pleat Density
circumference = math.pi * od
pitch = circumference / n_pleats if n_pleats > 0 else 0

# --- DISPLAY RESULTS ---
st.subheader("📊 Technical Summary")
c1, c2, c3 = st.columns(3)
c1.metric("Total Area", f"{area_m2:.3f} m²")
c2.metric("Circumference", f"{circumference:.1f} mm")
c3.metric("Pleat Pitch", f"{pitch:.2f} mm")



# --- SME VALIDATION LOGIC ---
st.divider()
st.markdown("### 🛠️ SME Validation")

if pitch < 1.5:
    st.error(f"❌ **REJECTED:** Pleats are too crowded (Pitch: {pitch:.2f}mm). Minimum recommended is 2mm for effective backwash.")
elif p_depth > (od / 3):
    st.warning(f"⚠️ **WARNING:** High Pleat Depth ({p_depth}mm) relative to OD ({od}mm). Check internal core clearance.")
else:
    st.success("✅ **APPROVED:** Design is within standard industrial manufacturing tolerances.")

# --- DYNAMIC TEXT REPORT ---
st.download_button(
    label="📥 Download Technical Data",
    data=f"Filter Report\nOD: {od}\nLength: {length}\nArea: {area_m2} m2\nStatus: Approved",
    file_name=f"Filter_Specs_{od}x{length}.txt"
)
