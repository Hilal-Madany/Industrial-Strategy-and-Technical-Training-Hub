import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
import datetime

# --- CONFIGURATION & PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

st.set_page_config(page_title="Vendor Assessment Pro V2", layout="wide")

# --- SESSION INITIALIZATION ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

# --- SIDEBAR STATUS ---
with st.sidebar:
    st.header("📊 Progress")
    steps = ["Identity", "Legal", "Infrastructure", "Technical", "Performance", "Financial", "Declaration", "Final Report"]
    for i, s in enumerate(steps):
        color = "✅" if st.session_state.step > i+1 else ("🔵" if st.session_state.step == i+1 else "⚪")
        st.write(f"{color} {s}")

st.title("🏛️ Vendor Assessment & Registration Portal")
st.divider()

# --- FORM LOGIC ---
if st.session_state.step == 1:
    st.header("1. Company Basic Profile")
    st.session_state.data['name'] = st.text_input("Full Company Name", st.session_state.data.get('name', "Accumen Techno Marketing Solution"))
    st.session_state.data['reg_office'] = st.text_area("Registered Office Address", st.session_state.data.get('reg_office', "Fatehpur"))
    st.session_state.data['works_addr'] = st.text_area("Works/Factory Address", st.session_state.data.get('works_addr', "Haswa"))
    st.button("Save & Continue ➡️", on_click=next_step)

elif st.session_state.step == 2:
    st.header("2. Statutory & Contact Details")
    c1, c2 = st.columns(2)
    st.session_state.data['pan'] = c1.text_input("PAN No.", st.session_state.data.get('pan', "BVGPM3310K"))
    st.session_state.data['gst'] = c2.text_input("GST No.", st.session_state.data.get('gst', "212601"))
    st.session_state.data['msme_no'] = st.text_input("MSME/Udyam No.", st.session_state.data.get('msme_no', "8408"))
    st.session_state.data['email'] = st.text_input("Official Email", st.session_state.data.get('email', "info.accumentechno@gmail.com"))
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Next Step ➡️", on_click=next_step)

elif st.session_state.step == 3:
    st.header("3. Infrastructure & Setup")
    st.session_state.data['area'] = st.number_input("Total Area (Sq. m.)", value=250)
    st.session_state.data['power'] = st.text_input("Power Connection (kVA)", "2")
    st.session_state.data['commence_year'] = st.text_input("Years of Experience", "4")
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Next Step ➡️", on_click=next_step)

elif st.session_state.step == 4:
    st.header("4. Technical Capacity")
    st.session_state.data['machinery'] = st.text_area("List of Machinery/Tools", st.session_state.data.get('machinery', "LATHE, MILLING"))
    st.session_state.data['grad_staff'] = st.number_input("Graduate Engineers", value=1)
    st.session_state.data['skilled_workers'] = st.number_input("Skilled Staff", value=5)
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Next Step ➡️", on_click=next_step)

elif st.session_state.step == 5:
    st.header("5. Product & Performance")
    st.session_state.data['prod_category'] = st.multiselect("Service Category", ["Marketing", "IT", "Electrical", "Mechanical"], default=["Marketing"])
    st.session_state.data['ref_1'] = st.text_area("Major Reference 1", st.session_state.data.get('ref_1', "SJVN Project Reference"))
    st.session_state.data['govt_exp'] = st.radio("Previous Govt/PSU Experience?", ["Yes", "No"])
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Next Step ➡️", on_click=next_step)

elif st.session_state.step == 6:
    st.header("6. Financial Status")
    st.session_state.data['turnover_3'] = st.number_input("Latest Turnover (Cr)", value=2.5)
    st.session_state.data['networth'] = st.number_input("Current Net Worth (Cr)", value=1.0)
    st.session_state.data['iso9001'] = st.selectbox("ISO 9001 Certification?", ["Yes", "No"])
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    coln.button("Next Step ➡️", on_click=next_step)

elif st.session_state.step == 7:
    st.header("7. Statutory Declaration")
    st.warning("Please confirm that all information provided is true to the best of your knowledge.")
    st.session_state.data['declaration'] = st.checkbox("I hereby declare that the details furnished above are true and correct.")
    
    colb, coln = st.columns(2)
    colb.button("⬅️ Back", on_click=prev_step)
    if st.session_state.data.get('declaration'):
        coln.button("Finalize Report 📜", on_click=next_step)

elif st.session_state.step == 8:
    st.header("8. Generated Assessment Report")
    
    # Logic: Scoring System
    score = 0
    if st.session_state.data.get('iso9001') == "Yes": score += 25
    if st.session_state.data.get('govt_exp') == "Yes": score += 25
    if st.session_state.data.get('turnover_3', 0) > 1: score += 25
    if st.session_state.data.get('grad_staff', 0) >= 1: score += 25
    st.session_state.data['score'] = score

    try:
        template = env.get_template('full_report.html')
        report_html = template.render(d=st.session_state.data, date=datetime.date.today().strftime("%d-%m-%Y"))
        
        # Displaying the Multi-page Report Preview
        st.components.v1.html(report_html, height=1800, scrolling=True)
        
        st.success("Report Generated Successfully! Use 'Print' button inside the report for PDF.")
    except Exception as e:
        st.error(f"Error Loading Template: {e}")
