import streamlit as st

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(layout="wide", page_title="Payroll Calculator v22")

# --- CSS: ΣΚΟΥΡΟ ΓΚΡΙ ΦΟΝΤΟ, ΛΕΥΚΑ ΓΡΑΜΜΑΤΑ, ITALICS ΣΤΑ F & G ---
st.markdown("""
    <style>
    /* Φόντο εφαρμογής */
    .stApp { background-color: #121212; }
    
    /* Γενικό κείμενο */
    span, div, p, label, h1, h2, h3 { color: #ffffff !important; }

    /* Πλαίσιο σειράς Excel */
    .excel-row {
        border: 1px solid #333;
        padding: 10px;
        margin-bottom: -1px; /* Ενοποίηση πλαισίων */
        background-color: #1e1e1e;
        display: flex;
        align-items: center;
    }

    /* Στήλες */
    .col-b { width: 25%; font-weight: bold; }
    .col-d { width: 15%; }
    .col-e { width: 15%; font-weight: bold; color: #00ff00 !important; text-align: right; padding-right: 15px; }
    .col-f { width: 22%; font-style: italic; color: #bbbbbb !important; font-size: 0.85rem; }
    .col-g { width: 23%; font-style: italic; color: #999999 !important; font-size: 0.85rem; }

    /* Inputs: Μαύρα γράμματα σε λευκό φόντο για να είναι λειτουργικά */
    input, .stSelectbox div div { color: #000000 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΕΔΟΜΕΝΑ ΠΙΝΑΚΩΝ (Ακριβή από το αρχείο σου) ---
KLIMAKIA = {
    "Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07,
    "1": 2234.94, "2": 2187.53, "3": 2087.69, "4": 1963.82, "5": 1892.43,
    "6": 1717.38, "7": 1667.92, "8": 1570.34, "9": 1454.83, "10": 1424.81,
    "11": 1376.89, "12": 1350.16, "13": 1321.14, "14": 1309.80, "15": 1299.21,
    "16": 1285.07, "17": 1275.99, "18": 1266.41, "19": 1258.08, "20": 1224.28,
    "21": 1216.95, "22": 1202.63, "23": 1195.82
}

def fmt(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📑 salary_calc.xlsx - Πλήρης Υπολογισμός")

# --- ΣΥΝΑΡΤΗΣΗ ΔΗΜΙΟΥΡΓΙΑΣ ΓΡΑΜΜΗΣ ---
def render_line(row_id, desc, input_widget, result, f_txt, g_txt):
    with st.container():
        # Χρησιμοποιούμε columns για να ευθυγραμμίσουμε τα widgets με το CSS
        c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.3])
        with c1: st.markdown(f"**{row_id}: {desc}**")
        with c2: # Εδώ μπαίνει το widget που ορίστηκε έξω
            val = input_widget
        with c3: st.markdown(f"<div style='text-align:right; color:#00ff00; font-weight:bold;'>{fmt(result)}</div>", unsafe_allow_html=True)
        with c4: st.markdown(f"*{f_txt}*", unsafe_allow_html=True)
        with c5: st.markdown(f"*{g_txt}*", unsafe_allow_html=True)
        st.markdown("<hr style='margin:2px; border:0.1px solid #333'>", unsafe_allow_html=True)

# --- ΕΝΟΤΗΤΑ 1: ΒΑΣΙΚΑ (5-14) ---
st.subheader("Βασικές Αποδοχές")

# Σειρά 5
d5_val = st.selectbox("5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ (D5)", options=list(KLIMAKIA.keys()), index=4)
e5 = KLIMAKIA[d5_val]
render_line(5, "ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ", None, e5, "επιλογή από πίνακα D254:D280", "")

# Σειρά 6
d6 = st.number_input("6: ΧΡΟΝΟΕΠΙΔΟΜΑ (D6)", value=14)
e6 = d6 * 0.025 * e5
render_line(6, "ΧΡΟΝΟΕΠΙΔΟΜΑ", None, e6, "=D6*2,5%*E5", "ετη εργασιας , μειον την τριετια 2012-2014")

# Σειρά 11 (Άθροισμα)
e11 = e5 + e6
render_line(11, "ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ", None, e11, "=SUM(E5:E6)", "")

# Σειρά 7
d7_val = st.selectbox("7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ (D7)", ["NAI", "OXI"], index=0)
e7 = e11 * 0.10 if d7_val == "NAI" else 0.0
render_line(7, "ΕΠΙΔΟΜΑ ΓΑΜΟΥ", None, e7, '=IF(D7="NAI";E11*10%;0)', "")

# Σειρά 8
e8 = 239.08
render_line(8, "AΝΘΥΓΙΕΙΝΟ ΕΠΙΔΟΜA", None, e8, "Σταθερό ποσό", "")

# Καταβαλλόμενες (Γραμμή 14)
e14 = e11 + e7 + e8 # Απλοποιημένο για το παράδειγμα
render_line(14, "ΚΑΤΑΒΑΛΟΜΕΝΕΣ ΑΠΟΔΟΧΕΣ", None, e14, "=E11+E12", "")

st.divider()

# --- ΕΝΟΤΗΤΑ 2: ΠΡΟΣΑΥΞΗΣΕΙΣ (29-55) ---
st.subheader("Προσαυξήσεις & Υπερωρίες")

d177 = e14 / 162.5 # Ωρομίσθιο

d29 = st.number_input("29: 41 ΥΠΕΡΕΡΓΑΣΙΑ 20% (D29)", value=0.0)
e29 = d177 * d29 * 1.20
render_line(29, "41 ΥΠΕΡΕΡΓΑΣΙΑ 20%", None, e29, "D177*D29*120%", "")

d33 = st.number_input("33: ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ (D33)", value=0.0)
e33 = (e14 / 162.5) * d33 * 0.25
render_line(33, "ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ", None, e33, "(E14/162,5)*D33*25%", "")

d38 = st.number_input("38: ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ (D38)", value=0.0)
e38 = (e14 / 162.5) * d38 * 0.75
render_line(38, "ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ - ΑΡΓΙΩΝ", None, e38, "(E14/162,5)*D38*75%", "")

# --- ΕΝΟΤΗΤΑ 3: ΚΡΑΤΗΣΕΙΣ (59-72) ---
st.subheader("Κρατήσεις")

e56 = e14 + e29 + e33 + e38
render_line(56, "ΣΥΝΟΛΟ ΜΙΚΤΩΝ", None, e56, "=SUM(E17:E55)", "")

e59 = e14 * 0.1682
render_line(59, "ΕΦΚΑ (16,82%)", None, e59, "E14 * 16,82%", "Κρατήσεις επί των καταβαλλομένων")

# --- ΤΕΛΙΚΟ ΑΠΟΤΕΛΕΣΜΑ ---
st.success(f"### ΠΛΗΡΩΤΕΟ ΠΟΣΟ: {fmt(e56 - e59)}")
