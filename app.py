import streamlit as st

st.set_page_config(layout="wide", page_title="Payroll Full Sheet")

# CSS για διακριτικά labels και Borders
st.markdown("""
    <style>
    .stNumberInput label, .stSelectbox label {
        font-size: 0.8rem !important;
        color: #666 !important;
    }
    .element-container { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΕΔΟΜΕΝΑ ---
klimakia_data = {"Α": 2589.31, "Β": 2508.87, "Γ": 2428.41, "Δ": 2364.07, "8": 1570.34} # κλπ

st.title("📊 Αναλυτική Κατάσταση Μισθοδοσίας")
col_widths = [3, 2, 2, 4]

# --- ΓΡΑΜΜΗ 5 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d5_sel = c2.selectbox("D5", list(klimakia_data.keys()))
    e5 = klimakia_data[d5_sel]
    c1.write("b5: ΜΙΣΘΟΛΟΓΙΚΟ ΚΛΙΜΑΚΙΟ")
    c3.write(f"e5: **{e5:,.2f} €**")
    c4.write("f5: επιλογή από πίνακα D254:D280")

# --- ΓΡΑΜΜΗ 6 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d6 = c2.number_input("D6", step=1, value=0)
    e6 = d6 * 0.025 * e5
    c1.write("b6: ΧΡΟΝΟΕΠΙΔΟΜΑ")
    c3.write(f"e6: **{e6:,.2f} €**")
    c4.write("f6: ετη εργασιας , μειον την τριετια 2012-2014")

# --- ΓΡΑΜΜΗ 11 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    e11 = e5 + e6
    c1.markdown("**b11: ΒΑΣΙΚΟΣ ΜΙΣΘΟΣ**")
    c3.markdown(f"**{e11:,.2f} €**")
    c4.write("f11: =SUM(E5:E6)")

# --- ΓΡΑΜΜΗ 7 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d7_choice = c2.selectbox("D7", ["ΟΧΙ", "ΝΑΙ"])
    e7 = (e11 * 0.10) if d7_choice == "ΝΑΙ" else 0.0
    c1.write("b7: ΕΠΙΔΟΜΑ ΓΑΜΟΥ")
    c3.write(f"e7: **{e7:,.2f} €**")
    c4.write('f7: =IF(D7="NAI";E11*10%;0)')

# --- ΓΡΑΜΜΗ 9 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d9 = c2.selectbox("D9", [0, 5, 10, 15, 20, 25, 30])
    e9 = float(d9)
    c1.write("b9: ΠΟΛΥΕΤΙΑ")
    c3.write(f"e9: **{e9:,.2f} €**")
    c4.write("f9: Ποσό πολυετίας")

# --- ΓΡΑΜΜΗ 12 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    e12 = e7 + e9
    c1.markdown("**b12: ΠΡΟΣΑΥΞΗΣΕΙΣ ΜΙΣΘΟΥ**")
    c3.markdown(f"**{e12:,.2f} €**")
    c4.write("f12: =SUM(E7:E10)")

# --- ΓΡΑΜΜΗ 14 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    e14 = e11 + e12
    c1.markdown("### b14: ΚΑΤΑΒΑΛΛΟΜΕΝΕΣ")
    c3.markdown(f"### {e14:,.2f} €")
    c4.write("f14: =E11+E12")

# --- ΓΡΑΜΜΕΣ 17, 18, 19 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d17 = c2.number_input("D17", value=162.50)
    c1.write("b17: ΩΡΕΣ ΚΑΝ. ΑΠΑΣΧΟΛΗΣΗΣ")
    c4.write("f17: Βάση για ωρομίσθιο")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d18 = c2.number_input("D18", value=0.0)
    c1.write("b18: ΩΡΕΣ ΑΔΕΙΑΣ")
    c4.write("f18: Δεδομένα ωραρίου")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d19 = c2.number_input("D19", value=0.0)
    c1.write("b19: ΩΡΕΣ ΑΠΟΥΣΙΑΣ")
    c4.write("f19: Δεδομένα ωραρίου")

# --- ΓΡΑΜΜΗ 21 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    c21 = c2.number_input("C21", value=162.50)
    e21 = 1570.34 * 0.1136
    c1.write("b21: ΕΠΙΔΟΜΑ ΒΑΡΔΙΑΣ (0201)")
    c3.write(f"e21: **{e21:,.2f} €**")
    c4.write("f21: 11,36% επί του 8ου κλιμακίου για βαρδια Πρ-Απογ-Νυχ.")

# --- ΓΡΑΜΜΗ 22 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d22 = c2.selectbox("D22", [0, 1, 2, 3, 4, 5])
    family_map = {0: 0, 1: 29.35, 2: 58.70, 3: 91.09, 4: 155.69, 5: 220.29}
    e22 = family_map[d22]
    c1.write("b22: ΕΠΙΔ.ΟΙΚ.ΒΑΡΩΝ ΑΠΟ ΚΑΝ.ΑΠΑΣΧ.")
    c3.write(f"e22: **{e22:,.2f} €**")
    c4.write("f22: (1-2 παιδιά x 29,35e // 3ο 32,39e // 4+ x 64,6e)")

# ΥΠΟΛΟΓΙΣΜΟΣ D177
d177 = (e14 + e21 + e22) / d17 if d17 > 0 else 0.0

# --- ΓΡΑΜΜΕΣ 29, 30, 31 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d29 = c2.number_input("D29", step=1, value=0)
    e29 = d177 * d29 * 1.20
    c1.write("b29: 41 ΥΠΕΡΕΡΓΑΣΙΑ 20%")
    c3.write(f"e29: **{e29:,.2f} €**")
    c4.write("f29: D177*D29*120%")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d30 = c2.number_input("D30", step=1, value=0)
    e30 = d177 * d30 * 1.40
    c1.write("b30: ΥΠΕΡΩΡΙΑ Μ.Α. 1,4")
    c3.write(f"e30: **{e30:,.2f} €**")
    c4.write("f30: D177*D30*140%")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d31 = c2.number_input("D31", step=1, value=0)
    e31 = d177 * d31 * 1.20
    c1.write("b31: 51 ΥΠΕΡΩΡΙΑ Χ.Α. 120%")
    c3.write(f"e31: **{e31:,.2f} €**")
    c4.write("f31: D177*D31*120%")

# --- ΓΡΑΜΜΕΣ 33, 34, 35, 36 ---
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d33 = c2.number_input("D33", step=1, value=0)
    e33 = d33 * (e14 / 162.50) * 0.25
    c1.write("b33: ΠΡΟΣΑΥΞΗΣΗ ΝΥΧΤΑΣ")
    c3.write(f"e33: **{e33:,.2f} €**")
    c4.write("f33: (E14/162,5)*D33*25%")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d34 = c2.number_input("D34", step=1, value=0)
    e34 = d177 * d34 * 1.20 * 0.25
    c1.write("b34: 43 ΠΡΟΣ.ΥΠΕΡΕΡΓΑΣΙΑΣ ΝΥΚΤΑΣ 20%")
    c3.write(f"e34: **{e34:,.2f} €**")
    c4.write("f34: D177*D34*120%*25%")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d35 = c2.number_input("D35", step=1, value=0)
    e35 = d177 * d35 * 1.40 * 0.25
    c1.write("b35: ΠΡΟΣ.ΥΠΕΡΩΡΙΑΣ ΝΥΧΤΑΣ")
    c3.write(f"e35: **{e35:,.2f} €**")
    c4.write("f35: D177*D35*140%*25%")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(col_widths)
    d36 = c2.number_input("D36", step=1, value=0)
    e36 = d177 * d36 * 1.80 * 0.25
    c1.write("b36: ΠΡΟΣ.ΥΠΕΡΩΡΙΑΣ ΝΥΚΤΑΣ Χ.A. 120%")
    c3.write(f"e36: **{e36:,.2f} €**")
    c4.write("f36: D177*D36*180%*25%")
