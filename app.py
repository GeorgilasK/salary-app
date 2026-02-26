import streamlit as st

st.set_page_config(layout="wide", page_title="Payroll Calculator - Exact Replica")

# CSS για την οπτική πιστότητα του Excel
st.markdown("""
    <style>
    .excel-row {
        border: 1px solid #e0e0e0;
        padding: 8px;
        margin-bottom: -1px; /* Ενοποίηση πλαισίων όπως στο Excel */
        background-color: white;
        display: flex;
        align-items: center;
    }
    .col-b { width: 25%; font-weight: 500; border-right: 1px solid #f0f0f0; padding-right: 10px; }
    .col-d { width: 15%; border-right: 1px solid #f0f0f0; padding: 0 10px; }
    .col-e { width: 15%; font-weight: bold; color: #1a73e8; border-right: 1px solid #f0f0f0; padding: 0 10px; text-align: right; }
    .col-f { width: 22%; font-size: 0.85rem; color: #666; border-right: 1px solid #f0f0f0; padding: 0 10px; }
    .col-g { width: 23%; font-size: 0.85rem; color: #666; padding-left: 10px; }
    
    /* Διακριτικά Inputs */
    .stNumberInput div div input, .stSelectbox div div div {
        background-color: #fafafa !important;
        border: 1px solid #eee !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΕΔΟΜΕΝΑ ΠΙΝΑΚΩΝ (Από Calc & Temp) ---
KLIMAKIA = {
    "Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07, "1": 2234.94, "2": 2187.53, 
    "3": 2087.69, "4": 1963.82, "5": 1892.43, "6": 1717.38, "7": 1667.92, "8": 1570.34, 
    "9": 1454.83, "10": 1424.81, "11": 1376.89, "12": 1350.16, "13": 1321.14, "14": 1309.80, 
    "15": 1299.21, "16": 1285.07, "17": 1275.99, "18": 1266.41, "19": 1258.08, "20": 1224.28, 
    "21": 1216.95, "22": 1202.63, "23": 1195.82
}

def fmt(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📑 salary_calc.xlsx (Πλήρης Αναπαράσταση)")

# Helper για τη δημιουργία της γραμμής
def draw_excel_row(row_id, desc, input_widget=None, result=0.0, f_text="", g_text=""):
    st.markdown(f"""
    <div class="excel-row">
        <div class="col-b">{row_id}: {desc}</div>
        <div class="col-d" id="input_{row_id}"></div>
        <div class="col-e">{fmt(result)}</div>
        <div class="col-f">{f_text if f_text else ""}</div>
        <div class="col-g">{g_text if g_text else ""}</div>
    </div>
    """, unsafe_allow_html=True)
    # Τοποθέτηση του widget στην κολόνα D μέσω streamlit columns
    # (Επειδή το HTML δεν δέχεται απευθείας widgets, χρησιμοποιούμε columns για το layout)

# --- ΥΠΟΛΟΓΙΣΤΙΚΗ ΜΗΧΑΝΗ (Logic) ---
# Σημείωση: Ορίζουμε τα inputs πρώτα για να έχουμε τις τιμές για τους υπολογισμούς

# --- ΣΕΙΡΑ 5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ**")
with c2: d5 = st.selectbox("D5", options=list(KLIMAKIA.keys()), index=12, label_visibility="collapsed")
e5 = KLIMAKIA[d5]
with c3: st.write(f"**{fmt(e5)}**")
with c4: st.write("επιλογή από πίνακα D254:D280")
with c5: st.write("")

# --- ΣΕΙΡΑ 6: ΧΡΟΝΟΕΠΙΔΟΜΑ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**6: ΧΡΟΝΟΕΠΙΔΟΜΑ**")
with c2: d6 = st.number_input("D6", value=14, step=1, label_visibility="collapsed")
e6 = d6 * 0.025 * e5
with c3: st.write(f"**{fmt(e6)}**")
with c4: st.write("ετη εργασιας , μειον την τριετια 2012-2014")
with c5: st.write("=D6*2,5%*E5")

# --- ΣΕΙΡΑ 11: ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ ---
e11 = e5 + e6
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.markdown("**11: ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ**")
with c2: st.write("")
with c3: st.markdown(f"**{fmt(e11)}**")
with c4: st.write("=SUM(E5:E6)")
with c5: st.write("")

# --- ΣΕΙΡΑ 7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ**")
with c2: d7 = st.selectbox("D7", ["NAI", "OXI"], label_visibility="collapsed")
e7 = e11 * 0.10 if d7 == "NAI" else 0.0
with c3: st.write(f"**{fmt(e7)}**")
with c4: st.write('=IF(D7="NAI";E11*10%;0)')
with c5: st.write("")

# --- ΣΕΙΡΑ 8: ΑΝΘΥΓΙΕΙΝΟ ΕΠΙΔΟΜΑ ---
e8 = 239.08 # Σταθερά από το Calc.csv
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**8: ANΘΥΓΙΕΙΝΟ ΕΠΙΔΟΜA**")
with c2: st.write("")
with c3: st.write(f"**{fmt(e8)}**")
with c4: st.write("Σταθερό ποσό")
with c5: st.write("")

# --- ΣΕΙΡΑ 9: ΠΟΛΥΕΤΙΑ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**9: ΕΠΙΔΟΜΑ ΠΟΛΥΕΤΙΑΣ**")
with c2: d9 = st.selectbox("D9", [0, 5, 10, 15, 20, 25, 30], index=3, label_visibility="collapsed")
poly_map = {0:0, 5:0.025, 10:0.05, 15:0.075, 20:0.1, 25:0.125, 30:0.15}
e9 = e5 * poly_map[d9]
with c3: st.write(f"**{fmt(e9)}**")
with c4: st.write("(ANA 5ETIA, πχ 5-10-15)")
with c5: st.write("")

# --- ΣΕΙΡΑ 12: ΠΡΟΣΑΥΞΗΣΕΙΣ ΜΙΣΘΟΥ ---
e12 = e7 + e8 + e9
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.markdown("**12: ΠΡΟΣΑΥΞΗΣΕΙΣ ΜΙΣΘΟΥ**")
with c2: st.write("")
with c3: st.markdown(f"**{fmt(e12)}**")
with c4: st.write("=SUM(E7:E10)")
with c5: st.write("")

# --- ΣΕΙΡΑ 14: ΚΑΤΑΒΑΛΟΜΕΝΕΣ ΑΠΟΔΟΧΕΣ ---
e14 = e11 + e12
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.markdown("### 14: ΚΑΤΑΒΑΛΟΜΕΝΕΣ ΑΠΟΔΟΧΕΣ")
with c2: st.write("")
with c3: st.markdown(f"### {fmt(e14)}")
with c4: st.write("")
with c5: st.write("")

st.divider()

# --- ΕΝΟΤΗΤΑ ΩΡΩΝ (17-21) ---
# Ωρομίσθιο D175
d175 = e14 / 162.5

c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**17: ΕΡΓΑΣΙΑ ΜΗΝΟΣ**")
with c2: d17 = st.number_input("D17", value=162.5, label_visibility="collapsed")
e17 = d175 * d17
with c3: st.write(f"**{fmt(e17)}**")
with c4: st.write("D175*D17")
with c5: st.write("")

# --- ΣΕΙΡΑ 21: ΕΠΙΔΟΜΑ ΒΑΡΔΙΑΣ ---
e21 = 1570.34 * 0.1136
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**21: ΕΠΙΔΟΜΑ ΒΑΡΔΙΑΣ (0201)**")
with c2: st.write("")
with c3: st.write(f"**{fmt(e21)}**")
with c4: st.write("11,36% επί του 8ου κλιμακίου")
with c5: st.write("για βαρδια Πρ-Απογ-Νυχ.")

# --- ΣΕΙΡΑ 22: ΕΠΙΔΟΜΑ ΟΙΚΟΓΕΝΕΙΑΚΩΝ ΒΑΡΩΝ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**22: ΕΠΙΔ. ΟΙΚΟΓ/ΚΩΝ ΒΑΡΩΝ**")
with c2: d22 = st.selectbox("D22", [0, 1, 2, 3, 4, 5], index=1, label_visibility="collapsed")
child_map = {0:0, 1:29.35, 2:58.70, 3:91.09, 4:155.69, 5:220.29}
e22 = child_map[d22]
with c3: st.write(f"**{fmt(e22)}**")
with c4: st.write("(1-2 παιδιά x 29,35e // 3ο 32,39e // 4+ x 64,6e)")
with c5: st.write("ΑΠΟ ΚΑΝ. ΑΠΑΣΧ.")

# --- ΣΕΙΡΑ 38: ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ ---
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.write("**38: ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ**")
with c2: d38 = st.number_input("D38", value=0.0, label_visibility="collapsed")
e38 = (e14 / 162.5) * d38 * 0.75
with c3: st.write(f"**{fmt(e38)}**")
with c4: st.write("(E14/162,5)*D38*75%")
with c5: st.write("")

# --- ΣΥΝΟΛΑ (56+) ---
st.divider()
e56 = e17 + e21 + e22 + e38 # Και οι υπόλοιπες γραμμές που θα προστεθούν
c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
with c1: st.markdown("### 56: ΣΥΝΟΛΟ ΜΙΚΤΩΝ")
with c3: st.markdown(f"### {fmt(e56)}")
with c4: st.write("=SUM(E17:E55)")
