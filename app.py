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
    # Η σωστή μορφή για το Sidebar input:
d17_val = st.sidebar.number_input("Ώρες Μήνα (D17)", min_value=1.0, value=162.5)
