import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθού", layout="centered")

# 1. Συνάρτηση για να διαβάζουμε τις περιγραφές από το Excel (Στήλη Β)
@st.cache_data
def get_labels():
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Παίρνουμε το κείμενο από τη στήλη Β (index 1) για τις συγκεκριμένες γραμμές
    # Προσοχή: Το index στην Python ξεκινά από το 0, οπότε η γραμμή 5 είναι index 4
    labels = {
        "d5": str(df.iloc[4, 1]),
        "d6": str(df.iloc[5, 1]),
        "d7": str(df.iloc[6, 1]),
        "d9": str(df.iloc[8, 1]),
        "d10": str(df.iloc[9, 1]),
        "d11": str(df.iloc[10, 1]),
        "d12": str(df.iloc[11, 1]),
        "d43": str(df.iloc[42, 1])
    }
    return labels

try:
    labels = get_labels()
except:
    # Αν αποτύχει το διάβασμα, βάλε προσωρινά labels για να μην κρασάρει
    labels = {k: k.upper() for k in ["d5", "d6", "d7", "d9", "d10", "d11", "d12", "d43"]}

st.title("💰 Υπολογισμός Μισθοδοσίας")

# --- ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ΜΕ ΤΑ ΣΩΣΤΑ ΟΝΟΜΑΤΑ ---

# D5: Μικτό Dropdown
d5_options = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
d5_val = st.selectbox(labels["d5"], options=d5_options)

# D6
d6_val = st.number_input(labels["d6"], min_value=0, value=0)

# D7
d7_options = ["Επιλογή 1", "Επιλογή 2"] # Άλλαξε αυτές τις επιλογές αν χρειάζεται
d7_val = st.selectbox(labels["d7"], options=d7_options)

# D9, D10, D11, D12
d9_val = st.number_input(labels["d9"], min_value=0.0, value=0.0)
d10_val = st.number_input(labels["d10"], min_value=0.0, value=0.0)
d11_val = st.number_input(labels["d11"], min_value=0.0, value=0.0)
d12_val = st.number_input(labels["d12"], min_value=0.0, value=0.0)

st.markdown("---")

# --- ΥΠΟΛΟΓΙΣΜΟΣ (Εδώ βάλε τις πράξεις σου) ---
# Παράδειγμα:
result = d10_val + d11_val + d12_val 

# --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΟΣ ---
st.subheader(labels["d43"])
st.metric(label="Σύνολο", value=f"{result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
