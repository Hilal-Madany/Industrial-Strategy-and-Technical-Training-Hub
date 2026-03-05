import streamlit as st
import pdfkit
from jinja2 import Environment, FileSystemLoader
import base64

# Page Config
st.set_page_config(page_title="PSU Vendor Assessment Portal", layout="wide")

st.title("🏛️ Vendor Assessment & Registration Portal")
st.subheader("Standardized Format for Indian PSUs & Railways")

# Form Sections
with st.form("vendor_form"):
    st.markdown("### A. General & Statutory Information")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name (Full)")
        pan = st.text_input("PAN No.")
    with col2:
        address = st.text_area("Registered Office Address", height=68)
        gst = st.text_input("GST No.")

    st.markdown("### B. Technical & Quality Evaluation")
    c1, c2, c3 = st.columns(3)
    iso = c1.selectbox("ISO 9001 Certified?", ["Yes", "No"])
    testing = c2.selectbox("In-house Testing Facilities?", ["Yes", "No"])
    exp = c3.selectbox("Prior PSU/Railway Experience?", ["Yes", "No"])

    submit = st.form_submit_button("Generate Official Report")

if submit:
    # Logic: Scoring based on PSU requirements
    score = 0
    if iso == "Yes": score += 30
    if testing == "Yes": score += 40
    if exp == "Yes": score += 30
    
    status = "QUALIFIED" if score >= 70 else "UNDER REVIEW"

    # Prepare Data for PDF
    data = {
        "company_name": company_name,
        "address": address,
        "gst": gst,
        "pan": pan,
        "iso": iso,
        "testing": testing,
        "exp": exp,
        "score": score,
        "status": status
    }

    # Generate HTML from Template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')
    html_out = template.render(d=data)

    # Convert to PDF
    # Note: On Streamlit Cloud, you may need to point to the local binary or use a specific buildpack
    pdf = pdfkit.from_string(html_out, False)
    
    st.success(f"Report Generated! Final Score: {score}/100")
    
    # Download Button
    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name=f"Assessment_{company_name}.pdf",
        mime="application/pdf"
    )
