import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

st.title("📊 Πίνακας Υπολογισμού Αποδοχών")

# 1. Φόρτωση του αρχείου Excel
@st.cache_data
def load_data():
    # Διαβάζουμε το Excel
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    # Επιλογή στηλών B(1), C(2), D(3), E(4), G(6)
    df_selected = df.iloc[:, [1, 2, 3, 4, 6]].copy()
    
    # Ονομασία στηλών
    df_selected.columns = ['Περιγραφή', 'Παράμετρος', 'Προς Επεξεργασία (D)', 'Αποτέλεσμα (Ε)', 'Επεξήγηση (G)']
    
    # Μετατροπή της στήλης Ε σε αριθμητική για να δουλέψει το format του ευρώ
    df_selected['Αποτέλεσμα (Ε)'] = pd.to_numeric(df_selected['Αποτέλεσμα (Ε)'], errors='coerce')
    
    # Καθαρισμός None/NaN
    df_selected = df_selected.fillna('')
    return df_selected

df_display = load_data()

# 2. Δημιουργία της λίστας επιλογών για το Dropdown (Α, Β, Γ, Δ και 1 έως 23)
dropdown_options = ["", "Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]

# 3. Ρύθμιση του Πίνακα
edited_df = st.data_editor(
    df_display,
    column_config={
        "Περιγραφή": st.column_config.Column(disabled=True),
        "Παράμετρος": st.column_config.Column(disabled=True),
        "Προς Επεξεργασία (D)": st.column_config.SelectboxColumn(
            "Προς Επεξεργασία (D)",
            help="Επιλέξτε τιμή (Α-Δ ή 1-23)",
            options=dropdown_options,
            required=False,
        ),
        "Αποτέλεσμα (Ε)": st.column_config.NumberColumn(
            "Αποτέλεσμα (Ε)",
            format="%.2f €", 
            disabled=True
        ),
        "Επεξήγηση (G)": st.column_config.Column(disabled=True),
    },
    hide_index=True,
    use_container_width=True,
)

st.info("💡 Κάντε κλικ στα κελιά της στήλης D για να επιλέξετε τιμή. Οι στήλες περιγραφής και αποτελεσμάτων είναι κλειδωμένες.")

if st.button("🔄 Επιβεβαίωση Τιμών"):
    st.success("Οι τιμές ενημερώθηκαν στον πίνακα.")
