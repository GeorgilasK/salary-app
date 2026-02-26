import streamlit as st

# Ρύθμιση για να πιάνει όλο το πλάτος της οθόνης
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .header-row { background-color: #f0f2f6; font-weight: bold; padding: 10px; border-radius: 5px; }
    .data-row { border-bottom: 1px solid #ddd; padding: 5px 0; }
    .error-msg { color: #FF0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΕΔΟΜΕΝΑ ΚΛΙΜΑΚΙΩΝ ---
klimakia_data = {"Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07, "8": 1570.34} # κλπ

st.title("📊 Payroll Dashboard (Excel Style)")

# Επικεφαλίδες Πίνακα
h1, h2, h3, h4 = st.columns([3, 2, 2, 4])
h1.markdown("<div class='header-row'>Περιγραφή (B)</div>", unsafe_allow_html=True)
h2.markdown("<div class='header-row'>Είσοδος (D)</div>", unsafe_allow_html=True)
h3.markdown("<div class='header-row'>Ποσό (E)</div>", unsafe_allow_html=True)
h4.markdown("<div class='header-row'>Επεξήγηση (F)</div>", unsafe_allow_html=True)

# --- ΓΡΑΜΜΗ 5 ---
r5_1, r5_2, r5_3, r5_4 = st.columns([3, 2, 2, 4])
d5_sel = r5_2.selectbox("Κλιμάκιο", list(klimakia_data.keys()), label_visibility="collapsed")
e5 = klimakia_data.get(d5_sel, 0.0)
r5_1.markdown("b5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ")
r5_3.markdown(f"**{e5:,.2f} €**")
r5_4.text("Επιλογή από πίνακα D254:D280")

# --- ΓΡΑΜΜΗ 6 ---
r6_1, r6_2, r6_3, r6_4 = st.columns([3, 2, 2, 4])
d6 = r6_2.number_input("D6", step=1, value=0, label_visibility="collapsed")
e6 = e5 * (d6 / 100)
r6_1.markdown("b6: ΧΡΟΝΟΕΠΙΔΟΜΑ")
r6_3.markdown(f"**{e6:,.2f} €**")
r6_4.text(f"E5 * {d6}%")

# --- ΓΡΑΜΜΗ 11 ---
r11_1, r11_2, r11_3, r11_4 = st.columns([3, 2, 2, 4])
e11 = e5 + e6
r11_1.markdown("<b>b11: ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ</b>", unsafe_allow_html=True)
r11_3.markdown(f"<b>{e11:,.2f} €</b>", unsafe_allow_html=True)
r11_4.text("SUM(E5:E6)")

# --- ΓΡΑΜΜΗ 17 ---
st.divider()
r17_1, r17_2, r17_3, r17_4 = st.columns([3, 2, 2, 4])
d17 = r17_2.number_input("D17", value=162.50, step=0.50, label_visibility="collapsed")
r17_1.markdown("b17: ΩΡΕΣ ΚΑΝ. ΑΠΑΣΧΟΛΗΣΗΣ")
r17_3.markdown("-")
r17_4.text("Βάση υπολογισμού ωρομισθίου")

# --- ΓΡΑΜΜΗ 21 ---
r21_1, r21_2, r21_3, r21_4 = st.columns([3, 2, 2, 4])
c21 = r21_2.number_input("C21", value=162.5, step=0.5, label_visibility="collapsed")
e21 = 1570.34 * 0.1136 
r21_1.markdown("b21: ΕΠΙΔΟΜΑ ΒΑΡΔΙΑΣ")
r21_3.markdown(f"**{e21:,.2f} €**")
r21_4.text("11,36% επί του 8ου κλιμακίου")

# --- ΓΡΑΜΜΗ 177 ---
st.divider()
d177 = (e11 + e21) / d17 if d17 > 0 else 0.0 # Απλοποιημένο για το παράδειγμα
st.success(f"**Γραμμή 177 - Ωρομίσθιο Υπερωριών (D177): {d177:.2f} €**")

# --- ΓΡΑΜΜΗ 33 (Παράδειγμα Υπερωρίας) ---
r33_1, r33_2, r33_3, r33_4 = st.columns([3, 2, 2, 4])
d33 = r33_2.number_input("D33", step=1, value=0, label_visibility="collapsed")
e33 = d33 * (e11 / 162.50) * 0.25
r33_1.markdown("b33: ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ")
r33_3.markdown(f"**{e33:,.2f} €**")
r33_4.text("Ωρομίσθιο x Ώρες x 25%")
