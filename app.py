import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση του Excel
@st.cache_data
def load_full_excel():
    # Διαβάζουμε όλο το φύλλο Calc
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    return df

try:
    data = load_full_excel()
    
    st.title("💰 " + str(data.iloc[0, 1] if not pd.isna(data.iloc[0, 1]) else "Υπολογιστής Μισθού"))

    # --- ΔΗΜΙΟΥΡΓΙΑ ΠΕΔΙΩΝ ---
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Βασικά Στοιχεία")
        
        # D5 (Dropdown με Α-Δ και 1-23)
        d5_label = data.iloc[4, 1] # Παίρνει την περιγραφή από το Β5
        d5_options = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
        d5_val = st.selectbox(f"{d5_label} (D5)", options=d5_options)

        # D6
        d6_label = data.iloc[5, 1]
        d6_val = st.number_input(f"{d6_label} (D6)", value=0)

        # D7 (Dropdown - Εδώ βάλε τις ΔΙΚΕΣ ΣΟΥ επιλογές)
        d7_label = data.iloc[6, 1]
        # ΑΝΤΙΚΑΤΑΣΤΗΣΕ ΤΙΣ ΠΑΡΑΚΑΤΩ ΕΠΙΛΟΓΕΣ ΜΕ ΤΙΣ ΠΡΑΓΜΑΤΙΚΕΣ ΣΟΥ
        d7_options = ["Επιλογή Α", "Επιλογή Β", "Επιλογή Γ"] 
        d7_val = st.selectbox(f"{d7_label} (D7)", options=d7_options)

    with col2:
        st.subheader("Επιδόματα & Κρατήσεις")
        
        # D9 έως D12
        d9_val = st.number_input(f"{data.iloc[8, 1]} (D9)", value=0.0)
        d10_val = st.number_input(f"{data.iloc[9, 1]} (D10)", value=0.0)
        d11_val = st.number_input(f"{data.iloc[10, 1]} (D11)", value=0.0)
        d12_val = st.number_input(f"{data.iloc[11, 1]} (D12)", value=0.0)

    # --- ΓΡΑΜΜΗ 21 ΚΑΙ ΚΑΤΩ ---
    st.markdown("---")
    st.subheader("Πρόσθετα Στοιχεία (Γραμμή 21+)")
    
    # Παράδειγμα για τη γραμμή 21 (Κελί D21)
    d21_label = data.iloc[20, 1] # Στήλη Β, Γραμμή 21
    d21_val = st.number_input(f"{d21_label} (D21)", value=0.0)

    # --- ΥΠΟΛΟΓΙΣΜΟΣ ΑΠΟΤΕΛΕΣΜΑΤΟΣ ---
    # Εδώ είναι το "κλειδί". Πρέπει να γράψουμε τη φόρμουλα του D43.
    # ΠΡΕΠΕΙ ΝΑ ΜΟΥ ΠΕΙΣ ΤΗ ΦΟΡΜΟΥΛΑ! 
    # Π.χ. result = d5_val + d6_val + d21_val...
    
    st.markdown("---")
    final_label = data.iloc[42, 1] # Περιγραφή από το Β43
    
    # ΠΡΟΣΩΡΙΝΟ ΑΠΟΤΕΛΕΣΜΑ (Μέχρι να μου δώσεις τη φόρμουλα)
    result = d10_val + d11_val + d12_val + d21_val
    
    st.metric(label=str(final_label), value=f"{result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

except Exception as e:
    st.error(f"Σφάλμα κατά την ανάγνωση του Excel: {e}")
