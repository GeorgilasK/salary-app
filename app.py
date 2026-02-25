import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση του Excel για τις περιγραφές και τις τιμές αναφοράς
@st.cache_data
def load_excel_data():
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Πίνακας αντιστοιχίας C254:D280 για το D5
    ref_table = df.iloc[253:280, [2, 3]] 
    ref_table.columns = ['key', 'value']
    mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
    return df, mapping

try:
    data, d5_mapping = load_excel_data()
    st.title("💰 Ολοκληρωμένος Υπολογισμός Μισθού")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Παράμετροι Εισαγωγής")
        
        # D5: Dropdown από C254-280
        d5_label = str(data.iloc[4, 1])
        d5_choice = st.selectbox(d5_label, options=list(d5_mapping.keys()))
        d5_base_value = float(d5_mapping.get(d5_choice, 0))

        # D22: Dropdown για το E22 (0 έως 5)
        d22_label = "Επιλογή Επιπέδου (D22)" # Ή ό,τι γράφει το Β22
        d22_val = st.selectbox(d22_label, options=[0, 1, 2, 3, 4, 5])

        # D7: Dropdown ΝΑΙ/ΟΧΙ
        d7_label = str(data.iloc[6, 1])
        d7_val = st.selectbox(d7_label, options=["ΝΑΙ", "ΟΧΙ"])

        # D43: Τιμή Χρήστη
        d43_label = str(data.iloc[42, 1])
        d43_val = st.number_input(d43_label, value=0.0, format="%.2f")

    # --- ΥΠΟΛΟΓΙΣΜΟΙ ΒΑΣΕΙ ΤΩΝ ΤΥΠΩΝ ΣΟΥ ---

    # 1. Υπολογισμός E22 (IF συνάρτηση)
    if d22_val == 0: e22 = 0.0
    elif d22_val == 1: e22 = 29.35
    elif d22_val == 2: e22 = 29.35 * 2
    elif d22_val == 3: e22 = (29.35 * 2) + 32.39
    elif d22_val == 4: e22 = (29.35 * 2) + 32.39 + 64.6
    elif d22_val == 5: e22 = (29.35 * 2) + 32.39 + 64.6 + 64.6
    else: e22 = 0.0

    # 2. Υπολογισμός E21 (11,36% του D265)
    # Εδώ θεωρούμε ότι το D265 είναι η τιμή που αντιστοιχεί στο D5 από τον πίνακα
    e21 = d5_base_value * 0.1136

    # 3. Υπολογισμός E14 (SUM E11:E12)
    # Παίρνουμε τις τιμές από το Excel για τα E11 και E12
    e11 = float(data.iloc[10, 4]) if not pd.isna(data.iloc[10, 4]) else 0.0
    e12 = float(data.iloc[11, 4]) if not pd.isna(data.iloc[11, 4]) else 0.0
    e14 = e11 + e12

    # 4. Υπολογισμός D177: (E14 + E21 + E22) / D17
    d17 = float(data.iloc[16, 3]) if not pd.isna(data.iloc[16, 3]) else 160.0 # Προεπιλογή 160 αν είναι κενό
    d177_val = (e14 + e21 + e22) / d17

    # 5. Τελικός Υπολογισμός E43: (D177 * D43) * 120% * 175%
    e43_result = (d177_val * d43_val) * 1.20 * 1.75

    # --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
    st.markdown("---")
    with col2:
        st.subheader("Ανάλυση Υπολογισμού")
        st.write(f"**E14 (Σύνολο E11+E12):** {e14:.2f} €")
        st.write(f"**E21 (Κρατήσεις 11,36%):** {e21:.2f} €")
        st.write(f"**E22 (Επίπεδο {d22_val}):** {e22:.2f} €")
        st.write(f"**D177 (Ωρομίσθιο βάσης):** {d177_val:.4f} €")
        
        st.success(f"### 📈 Αποτέλεσμα E43: {e43_result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

except Exception as e:
    st.error(f"Παρουσιάστηκε σφάλμα: {e}")
