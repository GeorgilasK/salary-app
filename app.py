import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση του Excel για τις περιγραφές
@st.cache_data
def load_labels():
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    return df

try:
    data = load_labels()
    
    st.title("💰 Υπολογιστής Μισθοδοσίας")
    st.info("Συμπληρώστε τα στοιχεία για τον υπολογισμό του E43")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Παράμετροι Εισαγωγής")
        
        # D5: Μικτό Dropdown
        d5_label = data.iloc[4, 1] if not pd.isna(data.iloc[4, 1]) else "Κατηγορία (D5)"
        d5_options = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
        d5_val = st.selectbox(d5_label, options=d5_options)

        # D7: ΝΑΙ / ΟΧΙ
        d7_label = data.iloc[6, 1] if not pd.isna(data.iloc[6, 1]) else "Επιλογή (D7)"
        d7_val = st.selectbox(d7_label, options=["ΝΑΙ", "ΟΧΙ"])

        # D43: Τιμή Χρήστη
        d43_label = data.iloc[42, 1] if not pd.isna(data.iloc[42, 1]) else "Τιμή Χρήστη (D43)"
        d43_val = st.number_input(d43_label, value=0.0, format="%.2f")

    with col2:
        st.subheader("Επιπλέον Στοιχεία")
        # Εδώ μπορείς να προσθέσεις τα D9, D10 κλπ αν επηρεάζουν το D177
        d9_val = st.number_input(f"{data.iloc[8, 1]} (D9)", value=0.0)
        
        # ΠΡΟΣΟΧΗ: Επειδή η φόρμουλα ζητάει το D177, πρέπει να ξέρουμε πώς προκύπτει.
        # Αν το D177 είναι σταθερό (π.χ. 10.50), το βάζουμε εδώ. 
        # Αν αλλάζει, θα πρέπει να μου πεις τη φόρμουλα του D177.
        d177_val = 10.50 # ΠΡΟΣΩΡΙΝΗ ΤΙΜΗ - Άλλαξέ την με την πραγματική τιμή του D177

    # --- ΥΠΟΛΟΓΙΣΜΟΣ E43 ---
    # Τύπος: (D177 * D43) * 120% * 175%
    # Στα μαθηματικά: (d177 * d43) * 1.20 * 1.75
    e43_result = (d177_val * d43_val) * 1.20 * 1.75

    st.markdown("---")
    
    # Εμφάνιση Αποτελέσματος E43
    e43_label = "Αποτέλεσμα Υπολογισμού (E43)"
    st.metric(label=e43_label, value=f"{e43_result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.write(f"**Ανάλυση:** ({d177_val} * {d43_val}) * 1,20 * 1,75 = {e43_result:,.2f} €")

except Exception as e:
    st.error(f"Παρουσιάστηκε πρόβλημα: {e}")
