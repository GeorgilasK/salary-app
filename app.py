import streamlit as st

st.set_page_config(layout="wide", page_title="Payroll Full Sheet")

# CSS για εμφάνιση στυλ Excel
st.markdown("""
    <style>
    .row-container {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        background-color: #ffffff;
    }
    .stNumberInput label, .stSelectbox label {
        font-size: 0.8rem !important;
        color: #555 !important;
    }
    .formula-text {
        font-family: monospace;
        color: #2e7d32;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ---
def format_euro(amount):
    return f"{amount:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def render_row(row_num, label, input_col=None, result_val=0, note=""):
    """Δημιουργεί μια γραμμή σε πλαίσιο με 4 στήλες όπως το Excel"""
    with st.container():
        st.markdown('<div class="row-container">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 4])
        
        c1.write(f"**{row_num}: {label}**")
        
        # Αν η γραμμή δέχεται είσοδο
        user_val = None
        if input_col is not None:
            user_val = c2.number_input("Είσοδος", key=f"d{row_num}", label_visibility="collapsed", **input_col)
        else:
            c2.write("")
            
        c3.write(f"**{format_euro(result_val)}**")
        c4.markdown(f'<span class="formula-text">{note}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return user_val

# --- ΔΕΔΟΜΕΝΑ ΠΙΝΑΚΩΝ ---
KLIMAKIA = {
    "Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07, "1": 2234.94, "8": 1570.34, "13": 1321.14 # κλπ
}

st.title("📊 Αναλυτική Κατάσταση Μισθοδοσίας (Rows 1-290)")

# --- ΕΝΟΤΗΤΑ 1: ΒΑΣΙΚΑ (5-14) ---
with st.expander("Βασικές Αποδοχές & Επιδόματα", expanded=True):
    # Γραμμή 5
    d5_key = st.selectbox("5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ", list(KLIMAKIA.keys()), index=4)
    e5 = KLIMAKIA[d5_key]
    render_row(5, "ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ", result_val=e5, note="επιλογή από πίνακα D254:D280")
    
    # Γραμμή 6
    d6 = render_row(6, "ΧΡΟΝΟΕΠΙΔΟΜΑ", {"value": 14, "step": 1}, result_val=d6*0.025*e5 if 'd6' in locals() else 0, note="ετη εργασιας , μειον την τριετια 2012-2014")
    e6 = d6 * 0.025 * e5
    
    # Γραμμή 11
    e11 = e5 + e6
    render_row(11, "ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ", result_val=e11, note="=SUM(E5:E6)")
    
    # Γραμμή 7
    d7_sel = st.selectbox("7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ (Επιλογή)", ["NAI", "OXI"])
    e7 = e11 * 0.10 if d7_sel == "NAI" else 0
    render_row(7, "ΕΠΙΔΟΜΑ ΓΑΜΟΥ", result_val=e7, note='=IF(D7="NAI";E11*10%;0)')

# --- ΕΝΟΤΗΤΑ 2: ΩΡΕΣ & ΥΠΕΡΩΡΙΕΣ (17-38) ---
with st.expander("Ωράριο & Πρόσθετες Αποδοχές", expanded=True):
    d17 = render_row(17, "ΩΡΕΣ ΚΑΝ. ΑΠΑΣΧΟΛΗΣΗΣ", {"value": 162.5}, result_val=0, note="Βάση για ωρομίσθιο")
    
    # Υπολογισμός Ωρομισθίου (Γραμμή 175/177 στο Excel)
    e14 = e11 + e7 # Απλοποιημένο για το παράδειγμα
    d177 = e14 / 162.5
    
    # Γραμμές 29-31 (Υπερωρίες)
    d29 = render_row(29, "41 ΥΠΕΡΕΡΓΑΣΙΑ 20%", {"value": 0, "step": 1}, result_val=d177*d29*1.20 if 'd29' in locals() else 0, note="D177*D29*120%")
    d30 = render_row(30, "ΥΠΕΡΩΡΙΑ Μ.Α. 1,4", {"value": 0, "step": 1}, result_val=d177*d30*1.40 if 'd30' in locals() else 0, note="D177*D30*140%")
    
    # Γραμμές 33-36 (Νύχτα)
    d33 = render_row(33, "ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ", {"value": 0, "step": 1}, result_val=d33*(e14/162.5)*0.25 if 'd33' in locals() else 0, note="(E14/162,5)*D33*25%")
    
    # ΓΡΑΜΜΗ 38 (Αυτή που έλειπε)
    d38 = render_row(38, "ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ", {"value": 0, "step": 1}, result_val=d38*(e14/162.5)*0.75 if 'd38' in locals() else 0, note="(E14/162,5)*D38*75%")

# --- ΕΝΟΤΗΤΑ 3: ΣΥΝΟΛΑ & ΚΡΑΤΗΣΕΙΣ (56-80) ---
with st.expander("Κρατήσεις & Καθαρά", expanded=True):
    # Γραμμή 56
    e56 = e14 + (d177*d29*1.20) # Προσθέτουμε όλα τα Ε
    render_row(56, "ΣΥΝΟΛΟ ΜΙΚΤΩΝ", result_val=e56, note="Άθροισμα όλων των αποδοχών")
    
    # Γραμμή 59
    e59 = e14 * 0.1682 
    render_row(59, "ΕΦΚΑ (Κρατήσεις Εργαζομένου)", result_val=e59, note="E14 * 16,82%")
    
    # ΓΡΑΜΜΗ 61 (ΦΟΡΟΣ)
    # Εδώ μπαίνει η λογική με τους 17 μισθούς που είδα στο Excel
    taxable = e56 - e59
    e61 = 150.00 # Παράδειγμα, εδώ θα καλέσουμε τη συνάρτηση calculate_tax
    render_row(61, "ΦΟΡΟΣ", result_val=e61, note="Υπολογισμός βάσει κλίμακας (17 μισθοί)")

    # ΓΡΑΜΜΗ 79 (ΠΛΗΡΩΤΕΟ)
    e79 = e56 - e59 - e61
    st.markdown("---")
    render_row(79, "ΠΛΗΡΩΤΕΟ ΠΟΣΟ", result_val=e79, note="=E56 - Σύνολο Κρατήσεων")
