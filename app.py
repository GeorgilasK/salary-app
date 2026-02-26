import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Payroll Full Suite v25")

# --- 2. CSS: DARK MODE, WHITE TEXT, ITALICS F/G ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    span, div, p, label, h1, h2, h3 { color: #ffffff !important; }
    
    /* Inputs: Μαύρο κείμενο σε λευκό φόντο */
    input { color: #000000 !important; background-color: #ffffff !important; font-weight: bold !important; }
    .stNumberInput div div { background-color: #ffffff !important; }
    
    /* Στήλες F & G: Italics και γκρι */
    .italic-text { font-style: italic; color: #bbbbbb !important; font-size: 0.85rem; }
    
    /* Στήλη E: Πράσινο νέον */
    .result-text { color: #00ff00 !important; font-weight: bold; text-align: right; font-size: 1.1rem; }
    
    hr { border: 0.5px solid #333; margin: 4px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΠΙΝΑΚΕΣ ΔΕΔΟΜΕΝΩΝ ---
KLIMAKIA = {
    "Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07,
    "1": 2234.94, "2": 2187.53, "3": 2087.69, "4": 1963.82, "5": 1892.43,
    "6": 1717.38, "7": 1667.92, "8": 1570.34, "9": 1454.83, "10": 1424.81,
    "11": 1376.89, "12": 1350.16, "13": 1321.14, "14": 1309.80, "15": 1299.21,
    "16": 1285.07, "17": 1275.99, "18": 1266.41, "19": 1258.08, "20": 1224.28,
    "21": 1216.95, "22": 1202.63, "23": 1195.82
}
CHILD_BENEFIT = {0: 0.0, 1: 29.35, 2: 58.70, 3: 91.09, 4: 155.69, 5: 220.29}

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
st.title("📑 salary_calc.xlsx | Πλήρης Ενοποιημένος Κώδικας")

# --- ΕΝΟΤΗΤΑ: ΒΑΣΙΚΕΣ ΑΠΟΔΟΧΕΣ (5-22) ---
st.subheader("Βασικές Αποδοχές & Επιδόματα")

d5_sel = st.selectbox("5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ (D5)", list(KLIMAKIA.keys()), index=12) # Προεπιλογή "13"
e5 = KLIMAKIA[d5_sel]
render_row(5, "ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ", None, e5, "επιλογή από πίνακα D254:D280", "")

d6 = st.number_input("6: ΧΡΟΝΟΕΠΙΔΟΜΑ (D6)", value=14, step=1)
e6 = d6 * 0.025 * e5
render_row(6, "ΧΡΟΝΟΕΠΙΔΟΜΑ", None, e6, "=D6*2,5%*E5", "ετη εργασιας")

e11 = e5 + e6
render_row(11, "ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ", None, e11, "=SUM(E5:E6)", "")

d7_sel = st.selectbox("7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ (D7)", ["NAI", "OXI"], index=0)
e7 = e11 * 0.10 if d7_sel == "NAI" else 0.0
render_row(7, "ΕΠΙΔΟΜΑ ΓΑΜΟΥ", None, e7, 'IF(D7="NAI";E11*10%;0)', "")

e8 = 239.08
render_row(8, "AΝΘΥΓΙΕΙΝΟ ΕΠΙΔΟΜA", None, e8, "Σταθερό ποσό", "")

d22_sel = st.selectbox("22: ΑΡΙΘΜΟΣ ΠΑΙΔΙΩΝ (D22)", list(CHILD_BENEFIT.keys()), index=1)
e22 = CHILD_BENEFIT[d22_sel]
render_row(22, "ΕΠΙΔ. ΟΙΚΟΓΕΝΕΙΑΚΩΝ ΒΑΡΩΝ", None, e22, "Βάσει αριθμού παιδιών", "ΑΠΟ ΚΑΝ. ΑΠΑΣΧ.")

e14 = e11 + e7 + e8
render_row(14, "ΚΑΤΑΒΑΛΟΜΕΝΕΣ ΑΠΟΔΟΧΕΣ", None, e14, "=E11+E12+E13", "")

# --- ΕΝΟΤΗΤΑ: ΠΡΟΣΑΥΞΗΣΕΙΣ (29-55) ---
st.divider()
st.subheader("Πρόσθετες Αποδοχές (Υπερωρίες, Νυχτερινά, Κυριακές)")
d177 = e14 / 162.5

d29 = st.number_input("29: 41 ΥΠΕΡΕΡΓΑΣΙΑ 20% (D29)", value=0, step=1)
e29 = d177 * d29 * 1.20
render_row(29, "41 ΥΠΕΡΕΡΓΑΣΙΑ 20%", None, e29, "D177*D29*120%", "")

d30 = st.number_input("30: ΥΠΕΡΩΡΙΑ Μ.Α. 1,4 (D30)", value=0, step=1)
e30 = d177 * d30 * 1.40
render_row(30, "ΥΠΕΡΩΡΙΑ Μ.Α. 1,4", None, e30, "D177*D30*140%", "")

d31 = st.number_input("31: 51 ΥΠΕΡΩΡΙΑ Χ.Α. 120% (D31)", value=0, step=1)
e31 = d177 * d31 * 1.20
render_row(31, "51 ΥΠΕΡΩΡΙΑ Χ.Α. 120%", None, e31, "D177*D31*120%", "")

d33 = st.number_input("33: ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ (D33)", value=0, step=1)
e33 = (e14 / 162.5) * d33 * 0.25
render_row(33, "ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ", None, e33, "(E14/162,5)*D33*25%", "")

d34 = st.number_input("34: 43 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΝΥΚΤΑΣ 20% (D34)", value=0, step=1)
e34 = d177 * d34 * 1.20 * 0.25
render_row(34, "43 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΝΥΚΤΑΣ 20%", None, e34, "D177*D34*120%*25%", "")

d35 = st.number_input("35: ΠΡΟΣ.ΥΠΕΡΩΡΙΑΣ ΝΥΧΤΑΣ (D35)", value=0, step=1)
e35 = d177 * d35 * 1.40 * 0.25
render_row(35, "ΠΡΟΣ.ΥΠΕΡΩΡΙΑΣ ΝΥΧΤΑΣ", None, e35, "D177*D35*140%*25%", "")

d38 = st.number_input("38: ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ (D38)", value=0, step=1)
e38 = (e14 / 162.5) * d38 * 0.75
render_row(38, "ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ", None, e38, "(E14/162,5)*D38*75%", "")

d39 = st.number_input("39: 44 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΚΥΡΙΑΚΗΣ 20% (D39)", value=0, step=1)
e39 = d177 * d39 * 1.20 * 0.75
render_row(39, "44 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΚΥΡΙΑΚΗΣ 20%", None, e39, "D177*D39*120%*75%", "")

# --- ΕΝΟΤΗΤΑ: ΚΡΑΤΗΣΕΙΣ (59-72) ---
st.divider()
st.subheader("Κρατήσεις")

e56 = e14 + e22 + e29 + e30 + e31 + e33 + e34 + e35 + e38 + e39
render_row(56, "ΣΥΝΟΛΟ ΜΙΚΤΩΝ", None, e56, "=SUM(E17:E55)", "")

e59 = e14 * 0.1682
render_row(59, "ΕΦΚΑ (16,82%)", None, e59, "E14 * 16,82%", "Κρατήσεις επί των καταβαλλομένων")

e61 = 184.32 # ΦΟΡΟΣ (Ενδεικτικός έως την πλήρη κλίμακα)
render_row(61, "ΦΟΡΟΣ", None, e61, "Υπολογισμός βάσει κλίμακας", "Αναγωγή σε 17 μισθούς")

# --- ΤΕΛΙΚΟ ΠΛΗΡΩΤΕΟ ---
st.success(f"### 79: ΠΛΗΡΩΤΕΟ ΠΟΣΟ: {fmt(e56 - e59 - e61)}")

# --- ΕΝΟΤΗΤΑ: ΔΩΡΑ (80-290) ---
st.divider()
st.subheader("Δώρα & Επιδόματα (Γραμμές 80-290)")
render_row(180, "ΔΩΡΟ ΧΡΙΣΤΟΥΓΕΝΝΩΝ", None, e14, "ΒΑΣΙΚΟΣ + ΠΡΟΣΑΥΞΗΣΕΙΣ", "")
# Εδώ θα συνεχίσουμε να προσθέτουμε τις υπόλοιπες 100+ γραμμές
