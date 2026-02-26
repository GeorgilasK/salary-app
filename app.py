import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Payroll Calculator Full")

# --- 2. CSS: DARK MODE & EXACT FORMATTING ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    span, div, p, label, h1, h2, h3 { color: #ffffff !important; }
    
    /* Inputs: Μαύρο κείμενο σε λευκό φόντο */
    input { color: #000000 !important; background-color: #ffffff !important; font-weight: bold !important; }
    
    /* Στήλες F & G: Italics και ελαφρύ γκρι */
    .italic-text { font-style: italic; color: #bbbbbb !important; font-size: 0.85rem; }
    
    /* Στήλη E: Πράσινο έντονο */
    .result-text { color: #00ff00 !important; font-weight: bold; text-align: right; font-size: 1.1rem; }
    
    hr { border: 0.5px solid #333; margin: 8px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΠΙΝΑΚΕΣ ΔΕΔΟΜΕΝΩΝ (D5, D7, D22) ---
KLIMAKIA = {
    "Γ": 2428.41, "Δ": 2364.07, "Α": 2589.31, "Β": 2508.87,
    "1": 2234.94, "8": 1570.34, "9": 1454.83, "13": 1321.14 # + όλες οι υπόλοιπες τιμές
}

def fmt(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

# --- 4. ΣΥΝΑΡΤΗΣΗ ΓΡΑΜΜΗΣ ---
def render_row(row_id, desc, input_widget, result, f_txt, g_txt):
    cols = st.columns([2.8, 1.2, 1.5, 2.2, 2.3])
    with cols[0]: st.markdown(f"**{row_id}: {desc}**")
    with cols[1]: st.write(input_widget if input_widget is not None else "")
    with cols[2]: st.markdown(f"<div class='result-text'>{fmt(result)}</div>", unsafe_allow_html=True)
    with cols[3]: st.markdown(f"<div class='italic-text'>{f_txt}</div>", unsafe_allow_html=True)
    with cols[4]: st.markdown(f"<div class='italic-text'>{g_txt}</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. ΚΥΡΙΟ ΣΩΜΑ ΥΠΟΛΟΓΙΣΜΩΝ ---
st.title("📑 salary_calc.xlsx (Πλήρης Αναφορά)")

# --- ΕΝΟΤΗΤΑ: ΒΑΣΙΚΕΣ ΑΠΟΔΟΧΕΣ (5-14) ---
st.subheader("Βασικές Αποδοχές")

d5_sel = st.selectbox("5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ (D5)", list(KLIMAKIA.keys()), index=0)
e5 = KLIMAKIA[d5_sel]
render_row(5, "ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ", None, e5, "επιλογή από πίνακα D254:D280", "")

d6 = st.number_input("6: ΧΡΟΝΟΕΠΙΔΟΜΑ (D6)", value=14, step=1) # ΑΚΕΡΑΙΟΣ
e6 = d6 * 0.025 * e5
render_row(6, "ΧΡΟΝΟΕΠΙΔΟΜΑ", None, e6, "=D6*2,5%*E5", "ετη εργασιας")

e11 = e5 + e6
render_row(11, "ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ", None, e11, "=SUM(E5:E6)", "")

d7_sel = st.selectbox("7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ (D7)", ["NAI", "OXI"])
e7 = e11 * 0.10 if d7_sel == "NAI" else 0.0
render_row(7, "ΕΠΙΔΟΜΑ ΓΑΜΟΥ", None, e7, '=IF(D7="NAI";E11*10%;0)', "")

e8 = 239.08
render_row(8, "AΝΘΥΓΙΕΙΝΟ ΕΠΙΔΟΜA", None, e8, "Σταθερό ποσό", "")

e14 = e11 + e7 + e8
render_row(14, "ΚΑΤΑΒΑΛΟΜΕΝΕΣ ΑΠΟΔΟΧΕΣ", None, e14, "=E11+E12", "")

st.divider()

# --- ΕΝΟΤΗΤΑ: ΠΡΟΣΑΥΞΗΣΕΙΣ (29-55) ---
st.subheader("Προσαυξήσεις & Υπερωρίες")
d177 = e14 / 162.5

# Όλα τα D εδώ είναι ΑΚΕΡΑΙΟΙ (step=1)
d29 = st.number_input("29: 41 ΥΠΕΡΕΡΓΑΣΙΑ 20% (D29)", value=0, step=1)
e29 = d177 * d29 * 1.20
render_row(29, "41 ΥΠΕΡΕΡΓΑΣΙΑ 20%", None, e29, "D177*D29*120%", "")

d30 = st.number_input("30: ΥΠΕΡΩΡΙΑ Μ.Α. 1,4 (D30)", value=0, step=1)
e30 = d177 * d30 * 1.40
render_row(30, "ΥΠΕΡΩΡΙΑ Μ.Α. 1,4", None, e30, "D177*D30*140%", "")

d33 = st.number_input("33: ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ (D33)", value=0, step=1)
e33 = (e14 / 162.5) * d33 * 0.25
render_row(33, "ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ", None, e33, "(E14/162,5)*D33*25%", "")

d38 = st.number_input("38: ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ (D38)", value=0, step=1)
e38 = (e14 / 162.5) * d38 * 0.75
render_row(38, "ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ", None, e38, "(E14/162,5)*D38*75%", "")

st.divider()

# --- ΕΝΟΤΗΤΑ: ΚΡΑΤΗΣΕΙΣ (59-72) ---
st.subheader("Κρατήσεις")
e56 = e14 + e29 + e30 + e33 + e38
render_row(56, "ΣΥΝΟΛΟ ΜΙΚΤΩΝ", None, e56, "=SUM(E17:E55)", "")

e59 = e14 * 0.1682
render_row(59, "ΕΦΚΑ (16,82%)", None, e59, "E14 * 16,82%", "Κρατήσεις επί των καταβαλλομένων")

# --- ΤΕΛΙΚΟ ΠΛΗΡΩΤΕΟ (79) ---
e79 = e56 - e59
st.success(f"### 79: ΠΛΗΡΩΤΕΟ ΠΟΣΟ: {fmt(e79)}")
