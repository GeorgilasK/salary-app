import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

st.title("📊 Πίνακας Υπολογισμού Αποδοχών")
st.write("Συμπληρώστε τα στοιχεία στη στήλη **'Προς Επεξεργασία (D)'**. Τα υπόλοιπα κελιά είναι κλειδωμένα.")

# 1. Φόρτωση του αρχείου Excel
@st.cache_data
def load_data():
    # Διαβάζουμε το φύλλο Calc, ξεκινώντας από τη γραμμή που αρχίζουν τα δεδομένα
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc")
    return df

df_original = load_data()

# 2. Επιλογή των στηλών B, C, D, E, F, G
# Προσαρμόζουμε το εύρος ανάλογα με το αρχείο σας (π.χ. γραμμές 5 έως 45)
df_display = df_original.iloc[4:44, [1, 2, 3, 4, 5, 6]] 
df_display.columns = ['Περιγραφή', 'Παράμετρος', 'Προς Επεξεργασία (D)', 'Αποτέλεσμα/Τιμή', 'Επεξήγηση 1', 'Επεξήγηση 2']

# 3. Δημιουργία διαδραστικού πίνακα (Data Editor)
edited_df = st.data_editor(
    df_display,
    column_config={
        "Περιγραφή": st.column_config.Column(disabled=True),
        "Παράμετρος": st.column_config.Column(disabled=True),
        "Προς Επεξεργασία (D)": st.column_config.NumberColumn(
            help="Συμπληρώστε την τιμή εδώ",
            format="%.2f",
        ),
        "Αποτέλεσμα/Τιμή": st.column_config.Column(disabled=True),
        "Επεξήγηση 1": st.column_config.Column(disabled=True),
        "Επεξήγηση 2": st.column_config.Column(disabled=True),
    },
    hide_index=True,
    use_container_width=True,
)

# 4. Κουμπί Υπολογισμού
if st.button("🔄 Εκτέλεση Υπολογισμού"):
    st.info("Εδώ η εφαρμογή συνδέει τις νέες τιμές της στήλης D με τις φόρμουλες του Excel...")
    # Εδώ μπαίνει ο κώδικας που στέλνει τα δεδομένα στο Excel (όπως δείξαμε πριν)
    # και επιστρέφει το τελικό αποτέλεσμα από το κελί D43.
    st.success("Το Καθαρό Πληρωτέο εμφανίζεται στο κάτω μέρος του πίνακα ή στο αντίστοιχο κελί.")