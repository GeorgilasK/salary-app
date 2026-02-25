import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση του Excel και των τιμών αναφοράς
@st.cache_data
def load_excel_data():
    # Διαβάζουμε όλο το φύλλο Calc
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    # Δημιουργία Λεξικού από τα κελιά C254:D280 (index 253 έως 279)
    # Στήλη C είναι index 2, Στήλη D είναι index 3
    ref_table = df.iloc[253:280, [2, 3]] 
    ref_table.columns = ['key', 'value']
    # Μετατροπή σε λεξικό { 'Α': τιμή, '1': τιμή, ... }
    mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
    
    return df, mapping

try:
    data, d5_mapping = load_excel_data()
    
    st.title("💰 Ολοκληρωμένος Υπολογισμός")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Παράμετροι")
        
        # D5 Dropdown (Παίρνει αυτόματα τις τιμές από τη στήλη C254-280)
        d5_label = str(data.iloc[4, 1])
        d5_options = list(d5_mapping.keys())
        d5_choice = st.selectbox(d5_label, options=d5_options)
        
        # Η τιμή που αντιστοιχεί στην επιλογή (αυτό που θα χρησιμοποιηθεί στον τύπο)
        d5_value_from_table = d5_mapping.get(d5_choice, 0)

        # D7 Dropdown
        d7_label = str(data.iloc[6, 1])
        d7_val = st.selectbox(d7_label, options=["ΝΑΙ", "ΟΧΙ"])

        # D43 Χειροκίνητη Τιμή
        d43_label = str(data.iloc[42, 1])
        d43_val = st.number_input(d43_label, value=0.0, format="%.2f")

    # --- ΥΠΟΛΟΓΙΣΜΟΣ D177 ---
    # Εδώ χρησιμοποιούμε τη φόρμουλα που μου έδωσες: (E14 + E21 + E22) / D17
    # Αν τα E14, E21 κλπ εξαρτώνται από το D5, 
    # τότε το 'd5_value_from_table' είναι αυτό που χρειαζόμαστε.
    
    # ΠΑΡΑΔΕΙΓΜΑ: Αν το D177 στο Excel σου ισούται με την τιμή του πίνακα / D17
    # (Προσάρμοσε τις παρακάτω τιμές αν τα E14, E21 είναι σταθερά ή αν περιλαμβάνονται στο d5_value_from_table)
    e14 = float(data.iloc[13, 4]) # Κελί E14
    e21 = float(data.iloc[20, 4]) # Κελί E21
    e22 = float(data.iloc[21, 4]) # Κελί E22
    d17 = float(data.iloc[16, 3]) # Κελί D17
    
    # Αν το D5 επηρεάζει άμεσα το D177, ο τύπος γίνεται:
    d177_val = (e14 + e21 + e22) / d17 if d17 != 0 else 0

    # --- ΥΠΟΛΟΓΙΣΜΟΣ E43 ---
    # Τύπος: (D177 * D43) * 120% * 175%
    e43_result = (d177_val * d43_val) * 1.20 * 1.75

    st.markdown("---")
    
    with col2:
        st.subheader("Σύνοψη")
        st.write(f"**Επιλογή D5:** {d5_choice} (Τιμή πίνακα: {d5_value_from_table})")
        st.write(f"**Υπολογισμένο D177:** {d177_val:.4f}")
        
        st.success(f"### 📈 Αποτέλεσμα E43: {e43_result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

except Exception as e:
    st.error(f"Σφάλμα: {e}. Βεβαιωθείτε ότι το αρχείο Excel έχει δεδομένα στα κελιά C254-D280.")
