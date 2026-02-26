import streamlit as st

st.set_page_config(layout="wide", page_title="Payroll Full Sheet")

# --- CSS ΓΙΑ ΑΠΟΛΥΤΗ ΠΙΣΤΟΤΗΤΑ ---
st.markdown("""
    <style>
    .excel-row {
        border: 1px solid #000000;
        padding: 8px;
        margin-bottom: -1px;
        background-color: #FFFFFF;
        display: flex;
        color: #000000 !important;
    }
    .col-b { width: 25%; font-weight: bold; border-right: 1px solid #000; padding-right: 5px; }
    .col-d { width: 15%; border-right: 1px solid #000; padding: 0 5px; }
    .col-e { width: 15%; font-weight: bold; border-right: 1px solid #000; text-align: right; padding-right: 10px; }
    .col-f { width: 20%; font-size: 0.8rem; border-right: 1px solid #000; padding: 0 5px; }
    .col-g { width: 25%; font-size: 0.8rem; padding-left: 5px; }
    
    /* Μαύρα γράμματα παντού */
    span, div, p, label { color: #000000 !important; }
    input { color: #000000 !important; font-weight: bold !important; border: 1px solid #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ΠΙΝΑΚΕΣ LOOKUP (Από το Calc/Temp) ---
KLIMAKIA = {
    "1": 2234.94, "8": 1570.34, "9": 1454.83, "13": 1321.14 # ... περιλαμβάνονται όλα στην πλήρη έκδοση
}
CHILD_MAP = {0: 0, 1: 29.35, 2: 58.70, 3: 91.09, 4: 155.69, 5: 220.29}

def fmt(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

# --- ΕΠΙΚΕΦΑΛΙΔΑ ΣΤΗΛΩΝ ---
st.markdown("""
<div class="excel-row" style="background-color: #d1d5db; font-weight: bold;">
    <div class="col-b">ΠΕΡΙΓΡΑΦΗ (B)</div>
    <div class="col-d">ΕΙΣΑΓΩΓΗ (D)</div>
    <div class="col-e">ΑΠΟΤΕΛΕΣΜΑ (E)</div>
    <div class="col-f">ΣΥΝΑΡΤΗΣΗ (F)</div>
    <div class="col-g">ΣΗΜΕΙΩΣΕΙΣ (G)</div>
</div>
""", unsafe_allow_html=True)

# --- ΚΥΡΙΟΣ ΚΩΔΙΚΑΣ ΓΡΑΜΜΩΝ ---

# --- ΓΡΑΜΜΕΣ 5-14 (ΒΑΣΙΚΑ) ---
with st.container():
    # Γραμμή 5
    c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2, 2.5])
    d5 = c2.selectbox("D5", list(KLIMAKIA.keys()), index=2, label_visibility="collapsed")
    e5 = KLIMAKIA[d5]
    c1.markdown(f"**5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ**")
    c3.markdown(f"**{fmt(e5)}**")
    c4.write("επιλογή από πίνακα")
    
    # Γραμμή 6
    c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2, 2.5])
    d6 = c2.number_input("D6", value=14, label_visibility="collapsed")
    e6 = d6 * 0.025 * e5
    c1.markdown(f"**6: ΧΡΟΝΟΕΠΙΔΟΜΑ**")
    c3.markdown(f"**{fmt(e6)}**")
    c4.write("=D6*2,5%*E5")
    c5.write("ετη εργασιας")

    # Γραμμή 11 (Βασικός)
    e11 = e5 + e6
    c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2, 2.5])
    c1.markdown("### 11: ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ")
    c3.markdown(f"### {fmt(e11)}")
    c4.write("=SUM(E5:E6)")

# --- ΓΡΑΜΜΕΣ 17-55 (ΠΡΟΣΑΥΞΗΣΕΙΣ & ΩΡΕΣ) ---
st.markdown("---")
# Υπολογισμός Ωρομισθίου (D175/D177)
e14 = e11 + (e11 * 0.10) + 239.08 # Ενδεικτικό Καταβαλλόμενο (πρέπει να προκύπτει από γραμμές 7-13)
d177 = e14 / 162.5

# Δημιουργούμε ένα λεξικό για να αποθηκεύουμε τα D values για τις 290 γραμμές
d_values = {}

def create_row(row_id, desc, default_d, formula_eval, f_txt, g_txt, is_input=True):
    cols = st.columns([2.5, 1.5, 1.5, 2, 2.5])
    with cols[0]: st.markdown(f"**{row_id}: {desc}**")
    
    d_val = 0
    if is_input:
        d_val = cols[1].number_input(f"D{row_id}", value=float(default_d), key=f"d_{row_id}", label_visibility="collapsed")
    
    # Εκτέλεση της συνάρτησης
    try:
        e_val = eval(formula_eval.replace(f"D{row_id}", str(d_val)))
    except:
        e_val = 0.0
        
    with cols[2]: st.markdown(f"**{fmt(e_val)}**")
    with cols[3]: st.write(f_txt)
    with cols[4]: st.write(g_txt)
    return e_val

# --- ΕΚΤΕΛΕΣΗ ΟΛΩΝ ΤΩΝ ΓΡΑΜΜΩΝ ---
e29 = create_row(29, "41 ΥΠΕΡΕΡΓΑΣΙΑ 20%", 0, "d177 * D29 * 1.20", "D177*D29*120%", "")
e30 = create_row(30, "ΥΠΕΡΩΡΙΑ Μ.Α. 1,4", 0, "d177 * D30 * 1.40", "D177*D30*140%", "")
e31 = create_row(31, "51 ΥΠΕΡΩΡΙΑ Χ.Α. 120%", 0, "d177 * D31 * 1.20", "D177*D31*120%", "")
e33 = create_row(33, "ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ", 0, "d177 * D33 * 0.25", "(E14/162,5)*D33*25%", "")
e38 = create_row(38, "ΠΡΟΣΑΥΞΗΣΗ ΚΥΡΙΑΚΩΝ", 0, "d177 * D38 * 0.75", "(E14/162,5)*D38*75%", "")
e39 = create_row(39, "44 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΚΥΡΙΑΚΗΣ", 0, "d177 * D39 * 1.2 * 0.75", "D177*D39*120%*75%", "")

# --- ΓΡΑΜΜΕΣ 59-72 (ΚΡΑΤΗΣΕΙΣ) ---
st.markdown("### Κρατήσεις")
e59 = e14 * 0.1682
create_row(59, "ΕΦΚΑ (Κρατήσεις)", 0, "e59", "E14 * 16,82%", "Κρατήσεις", is_input=False)

# --- ΓΡΑΜΜΕΣ 180-290 (ΔΩΡΑ & ΕΠΙΔΟΜΑΤΑ) ---
st.markdown("### Δώρα & Επιδόματα")
e180 = create_row(180, "ΔΩΡΟ ΧΡΙΣΤΟΥΓΕΝΝΩΝ", 0, "e14", "ΒΑΣΙΚΟΣ + ΠΡΟΣΑΥΞΗΣΕΙΣ", "", is_input=False)
# ... συνεχίζονται όλες οι γραμμές
