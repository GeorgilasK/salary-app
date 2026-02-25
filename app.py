import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Πίνακας Τιμών (Εδώ πρέπει να συμπληρώσεις τα ποσά από το Excel σου)
# Αντιστοιχία D5 -> E14, E21, E22, D17
data_map = {
    "Α": {"E14": 1200.0, "E21": 100.0, "E22": 50.0, "D17": 160.0},
    "Β": {"E14": 1100.0, "E21": 90.0, "E22": 45.0, "D17": 160.0},
    "Γ": {"E14": 1000.0, "E21": 80.0, "E22": 40.0, "D17": 160.0},
    "Δ": {"E14": 900.0, "E21": 70.0, "E22": 35.0, "D17": 160.0},
    # Πρόσθεσε εδώ τις τιμές για τα νούμερα 1 έως 23
    "1": {"E14": 800.0, "E21": 50.0, "E22": 20.0, "D17": 160.0},
}

# Συνάρτηση για να παίρνουμε τις περιγραφές (Στήλη Β)
@st.cache_data
def load_labels():
    try:
        df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
        return df
    except:
        return None

df_labels = load_labels()

st.title("💰 Ολοκληρωμένος Υπολογισμός Μισθού")

# --- ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Παράμετροι")
    
    # D5 Dropdown
    d5_label = df_labels.iloc[4, 1] if df_labels is not None else "Κατηγορία (D5)"
    d5_options = list(data_map.keys()) # Παίρνει αυτόματα ό,τι έχεις στο data_map
    d5_val = st.selectbox(d5_label, options=d5_options)

    # D7 Dropdown
    d7_label = df_labels.iloc[6, 1] if df_labels is not None else "Επιλογή (D7)"
    d7_val = st.selectbox(d7_label, options=["ΝΑΙ", "ΟΧΙ"])

    # D43 Χειροκίνητη Τιμή
    d43_label = df_labels.iloc[42, 1] if df_labels is not None else "Τιμή Χρήστη (D43)"
    d43_val = st.number_input(d43_label, value=0.0, format="%.2f")

# --- ΥΠΟΛΟΓΙΣΜΟΣ D177 ---
# Παίρνουμε τις τιμές που αντιστοιχούν στο D5 που επέλεξε ο χρήστης
vals = data_map.get(d5_val, {"E14": 0, "E21": 0, "E22": 0, "D17": 1})

e14 = vals["E14"]
e21 = vals["E21"]
e22 = vals["E22"]
d17 = vals["D17"]

# Φόρμουλα D177: (E14 + E21 + E22) / D17
d177_val = (e14 + e21 + e22) / d17

# --- ΥΠΟΛΟΓΙΣΜΟΣ E43 ---
# Φόρμουλα: (D177 * D43) * 120% * 175%
e43_result = (d177_val * d43_val) * 1.20 * 1.75

# --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
st.markdown("---")
with col2:
    st.subheader("Ανάλυση Ενδιάμεσων Τιμών")
    st.write(f"**Τιμή D177:** {d177_val:.4f}")
    st.write(f"(Βασίζεται στα: E14={e14}, E21={e21}, E22={e22}, D17={d17})")

st.success(f"### 📈 Αποτέλεσμα E43: {e43_result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

st.info(f"Τύπος υπολογισμού: ({d177_val:.4f} * {d43_val}) * 1,20 * 1,75")
