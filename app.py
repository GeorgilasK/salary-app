import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

st.title("📊 Πίνακας Υπολογισμού Αποδοχών")

# 1. Φόρτωση του αρχείου Excel
@st.cache_data
def load_data():
    # Διαβάζουμε το Excel - σιγουρέψου ότι το όνομα είναι σωστό
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    # Επιλογή στηλών B(1), C(2), D(3), E(4), G(6)
    df_selected = df.iloc[:, [1, 2, 3, 4, 6]].copy()
    
    # Ονομασία στηλών
    df_selected.columns = ['Περιγραφή', 'Παράμετρος', 'Προς Επεξεργασία (D)', 'Αποτέλεσμα (Ε)', 'Επεξήγηση (G)']
    
    # Καθαρισμός None
    df_selected = df_selected.fillna('')
    return df_selected

df_display = load_data()

# 2. Ρύθμιση του Πίνακα
# Εδώ ορίζουμε το Dropdown για τα κελιά που θέλεις (π.χ. ΝΑΙ/ΟΧΙ ή νούμερα)
edited_df = st.data_editor(
    df_display,
    column_config={
        "Περιγραφή": st.column_config.Column(disabled=True),
        "Παράμετρος": st.column_config.Column(disabled=True),
        "Προς Επεξεργασία (D)": st.column_config.SelectboxColumn(
            "Προς Επεξεργασία (D)",
            help="Επιλέξτε τιμή από τη λίστα",
            options=[
                "", "NAI", "OXI", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
            ], # Πρόσθεσε εδώ όλες τις επιλογές που έχει το Dropdown σου στο Excel
            required=False,
        ),
        "Αποτέλεσμα (Ε)": st.column_config.NumberColumn(
            "Αποτέλεσμα (Ε)",
            format="%.2f €", # Εδώ επιβάλλουμε 2 δεκαδικά και το σύμβολο του Ευρώ
            disabled=True
        ),
        "Επεξήγηση (G)": st.column_config.Column(disabled=True),
    },
    hide_index=True,
    use_container_width=True,
)

# 3. Μήνυμα για τον χρήστη
st.info("💡 Για να αλλάξετε τιμή, κάντε κλικ στο κελί της στήλης D και επιλέξτε από τη λίστα.")

if st.button("🔄 Ενημέρωση Υπολογισμών"):
    st.success("Οι τιμές καταχωρήθηκαν προσωρινά στον πίνακα.")
