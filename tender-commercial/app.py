import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- DIRECTORY SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Comprehensive Vendor Assessment", layout="wide")

# Initialize Session State
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

st.title("🏛️ DETAILED VENDOR ASSESSMENT PORTAL")
st.write(f"**Section {st.session_state.step} of 8**")
st.progress(st.session_state.step / 8)

# --- STEP 1: IDENTITY ---
if st.session_state.step == 1:
    st.header("1. General Identification")
    st.session_state.data['name'] = st.text_input("Name of Supplier / Sub-Vendor", st.session_state.data.get('name', "Accumen Techno Marketing Solution"))
    st.session_state.data['reg_office'] = st.text_area("Registered Office Address", st.session_state.data.get('reg_office', "Fatehpur"))
    st.session_state.data['works_addr'] = st.text_area("Factory Address", st.session_state.data.get('works_addr', "Haswa"))
    c1, c2 = st.columns(2)
    st.session_state.data['tel'] = c1.text_input("Telephone / Mobile", st.session_state.data.get('tel', "9650329719"))
    st.session_state.data['email'] = c2.text_input("Email ID", st.session_state.data.get('email', "info.accumentechno@gmail.com"))
    st.button("Save & Next ➡️", on_click=next_step)

# --- STEP 2: PRODUCTS & SERVICES ---
elif st.session_state.step == 2:
    st.header("2. Products & Services Profile")
    st.session_state.data['prod_category'] = st.multiselect("Select Categories", ["Electrical Items", "Mechanical Spares", "Instrumentation", "Civil Works", "IT Services", "Marketing & Branding"], default=["Marketing & Branding"])
    st.session_state.data['main_products'] = st.text_area("Description of Main Products/Services for which registration is sought", st.session_state.data.get('main_products', ""))
    st.session_state.data['is_dealer'] = st.radio("Are you a Manufacturer or Authorized Dealer?", ["Manufacturer", "Authorized Dealer", "EPC Contractor"])
    st.button("Save & Next ➡️", on_click=next_step)

# --- STEP 3: STATUTORY ---
elif st.session_state.step == 3:
    st.header("3. Statutory Details")
    c1, c2 = st.columns(2)
    st.session_state.data['pan'] = c1.text_input("PAN NO.", st.session_state.data.get('pan', "BVGPM3310K"))
    st.session_state.data['gst'] = c2.text_input("GST NO.", st.session_state.data.get('gst', "212601"))
    st.session_state.data['msme_no'] = st.text_input("MSME/Udyam Reg. No.", st.session_state.data.get('msme_no', "8408"))
    st.button("Save & Next ➡️", on_click=next_step)

# --- STEP 4: PERFORMANCE & REFERENCES ---
elif st.session_state.step == 4:
    st.header("4. Experience & Past Performance")
    st.info("List major orders executed in the last 3 years (Reference for Tender Requirement)")
    st.session_state.data['ref_1'] = st.text_input("Client 1 (Name, Order Value, Year)", st.session_state.data.get('ref_1', ""))
    st.session_state.data['ref_2'] = st.text_input("Client 2 (Name, Order Value, Year)", st.session_state.data.get('ref_2', ""))
    st.session_state.data['govt_exp'] = st.radio("Have you worked with any PSU/Railway before?", ["Yes", "No"])
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 5: TECHNICAL CAPABILITY ---
elif st.session_state.step == 5:
    st.header("5. Technical & Machinery")
    st.session_state.data['machinery'] = st.text_area("List of Machinery & Software Tools", st.session_state.data.get('machinery', "LATHE, MILLING"))
    st.session_state.data['inhouse_test'] = st.radio("In-house Testing/Quality Control available?", ["Yes", "No"], index=0)
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 6: QUALITY COMPLIANCE ---
elif st.session_state.step == 6:
    st.header("6. Quality Systems")
    st.session_state.data['iso9001'] = st.selectbox("ISO 9001:2015 Certified?", ["Yes", "No"], index=0)
    st.session_state.data['iso14001'] = st.selectbox("ISO 14001/45001 Certified?", ["Yes", "No"], index=0)
    st.session_state.data['q_manual'] = st.radio("Do you have a written Quality Manual?", ["Yes", "No"], index=0)
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 7: FINANCIALS ---
elif st.session_state.step == 7:
    st.header("7. Financial Soundness")
    f1, f2, f3 = st.columns(3)
    st.session_state.data['turnover_1'] = f1.number_input("FY 2022-23 (Cr)", value=0.75)
    st.session_state.data['turnover_2'] = f2.number_input("FY 2023-24 (Cr)", value=1.85)
    st.session_state.data['turnover_3'] = f3.number_input("FY 2024-25 (Cr)", value=2.50)
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Save & Next ➡️", on_click=next_step)

# --- STEP 8: FINAL PREVIEW ---
elif st.session_state.step == 8:
    st.header("8. Final Review & One-Page Print")
    
    # Calculate Score
    score = 0
    if st.session_state.data.get('iso9001') == "Yes": score += 25
    if st.session_state.data.get('inhouse_test') == "Yes": score += 25
    if st.session_state.data.get('q_manual') == "Yes": score += 25
    if st.session_state.data.get('turnover_3', 0) > 1.5: score += 25
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(
            d=st.session_state.data, 
            date=datetime.date.today().strftime("%d/%m/%Y")
        )
        
        # We use a large height (1500) so the user can see the whole form
        st.components.v1.html(report_html, height=1200, scrolling=True)
        
        st.warning("⚠️ **Note:** When the print window opens, set **'Layout' to 'Portrait'** and **'Margins' to 'Minimum'** to ensure it fits on one page.")
        
        if st.button("⬅️ Back to Edit"): st.session_state.step = 1

    except Exception as e:
        st.error(f"Template Error: {e}")
