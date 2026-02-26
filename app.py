import streamlit as st
import pandas as pd
import math

# Ρύθμιση σελίδας
st.set_page_config(page_title="Payroll Calculator - Προσχέδιο", layout="wide")

# --- 1. ΦΟΡΤΩΣΗ ΣΤΑΘΕΡΩΝ ΑΠΟ EXCEL ---
@st.cache_data
def load_data():
    # Εδώ διαβάζουμε τις τιμές που είναι "καρφωτές" στο Excel σου
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    e5_mapping = dict(zip(df.iloc[253:280, 2].astype(str), df.iloc[253:280, 3])) # C254:D280
    e11_base = float(df.iloc[10, 4])   # E11
    d267_val = float(df.iloc[266, 3])  # D267 (Ανθυγιεινό)
    d265_val = float(df.iloc[264, 3])  # D265 (8ο κλιμάκιο για Βάρδια)
    
    return e5_mapping, e11_base, d267_val, d265_val

e5_map, e11_const, d267_const, d265_const = load_data()

st.title("📊 Payroll Calculator (Draft)")
st.info("Το εργαλείο υπολογίζει αυτόματα τις γραμμές 5 έως 177 βάσει των τύπων σου.")

# --- 2. ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ (Inputs) ---
with st.sidebar:
    st.header("⚙️ Παράμετροι Χρήστη")
    d5_choice = st.selectbox("Κλιμάκιο (D5)", options=list(e5_map.keys()))
    g6_years = st.number_input("Συνολικά Έτη Εργασίας (G6)", min_value=0, value=10)
    d7_choice = st.radio("Επίδομα Γάμου (D7)", ["ΝΑΙ", "ΟΧΙ"])
    d9_choice = st.selectbox("Πολυετία (D9)", [0, 5, 10, 15, 20, 25, 30])
    d22_choice = st.selectbox("Οικογενειακά Βάρη (D22)", [0, 1, 2, 3, 4, 5])
    d17_hours = st.number_input("Ώρες Εργασίας Μήνα (D17)", value=162.5)

# --- 3. ΛΟΓΙΚΗ ΥΠΟΛΟΓΙΣΜΩΝ ---

# Γραμμή 5 & 6 (Βασικός & Χρονοεπίδομα)
e5_val = float(e5_map.get(d5_choice, 0))
d6_trieties = math.floor(max(0, g6_years - 3) / 3)
e6_val = d6_trieties * 0.025 * e5_val

# Γραμμή 7 (Γάμου)
e7_val = (e11_const * 0.10) if d7_choice == "ΝΑΙ" else 0.0

# Γραμμή 8 (Ανθυγιεινό)
e8_val = d267_const * 0.1678

# Γραμμή 9 (Πολυετία)
poly_rates = {0:0, 5:0.025, 10:0.05, 15:0.075, 20:0.10, 25:0.125, 30:0.15}
e9_val = e5_val * poly_rates.get(d9_choice, 0)

# Ενδιάμεσα Σύνολα (E11, E12, E14)
e11_val = e5_val + e6_val
e12_val = e7_val + e8_val + e9_val
e14_val = e11_val + e12_val

# Γραμμή 21 & 22 (Βάρδια & Οικ. Βάρη)
e21_val = d265_const * 0.1136
e22_logic = {0:0, 1:29.35, 2:58.7, 3:91.09, 4:155.69, 5:220.29}
e22_val = e22_logic.get(d22_choice, 0)

# Γραμμή 24 (Προσαύξηση Βάρδιας 39,5%)
e24_val = e14_val * 0.395

# Ωρομίσθια (D175, D176, D177)
d175_val = e14_val / 162.5
d176_val = d175_val * 6.5
d177_val = (e14_val + e21_val + e22_val) / d17_hours

# --- 4. ΕΜΦΑΝΙΣΗ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Ανάλυση Αποδοχών")
    st.write(f"**Βασικός (E5):** {e5_val:,.2f} €")
    st.write(f"**Χρονοεπίδομα (E6):** {e6_val:,.2f} €")
    st.write(f"**Επίδ. Γάμου (E7):** {e7_val:,.2f} €")
    st.write(f"**Ανθυγιεινό (E8):** {e8_val:,.2f} €")
    st.write(f"**Πολυετία (E9):** {e9_val:,.2f} €")
    st.divider()
    st.write(f"**ΚΑΤΑΒΑΛΟΜΕΝΕΣ (E14):** {e14_val:,.2f} €")

with col2:
    st.subheader("⚡ Υπολογισμοί Βάσης")
    st.metric("Ωρομίσθιο (D175)", f"{d175_val:,.4f} €")
    st.metric("Ημερομίσθιο (D176)", f"{d176_val:,.2f} €")
    st.metric("Ωρομίσθιο Υπερωρίας (D177)", f"{d177_val:,.4f} €")
    st.warning(f"Προσαύξηση Βάρδιας (E24): {e24_val:,.2f} €")

st.markdown("---")
st.caption("Αναμονή για Γραμμή 43 και Υπερωρίες...")
