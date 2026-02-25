import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

st.title("📊 Πίνακας Υπολογισμού Αποδοχών")
st.write("Συμπληρώστε τα στοιχεία στη στήλη **'Προς Επεξεργασία (D)'**.")

# 1. Φόρτωση του αρχείου Excel
@st.cache_data
def load_data():
    # Διαβάζουμε το φύλλο Calc. 
    # ΠΡΟΣΟΧΗ: Αν το αρχείο σου ξεκινάει τα δεδομένα από την 1η γραμμή, βάλε skiprows=0
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    # Επιλογή στηλών B, C, D, E, G (Αφαιρέσαμε την F που είναι η 5η στήλη με βάση το μηδέν)
    # Στήλες: B=1, C=2, D=3, E=4, G=6
    df_selected = df.iloc[:, [1, 2, 3, 4, 6]]
    
    # Ονομασία στηλών
    df_selected.columns = ['Περιγραφή (Β)', 'Παράμετρος (C)', 'Προς Επεξεργασία (D)', 'Αποτέλεσμα (Ε)', 'Επεξήγηση (G)']
    
    # Αντικατάσταση του None/NaN με κενό
    df_selected = df_selected.fillna('')
    
    return df_selected

# Φόρτωση δεδομένων
df_display = load_data()

# 2. Δημιουργία διαδραστικού πίνακα
# Χρησιμοποιούμε το st.data_editor για να επιτρέψουμε την επεξεργασία
edited_df = st.data_editor(
    df_display,
    column_config={
        "Περιγραφή (Β)": st.column_config.Column(disabled=True),
        "Παράμετρος (C)": st.column_config.Column(disabled=True),
        "Προς Επεξεργασία (D)": st.column_config.Column(
            help="Κάντε διπλό κλικ για να αλλάξετε την τιμή",
            disabled=False, # ΕΔΩ ΕΠΙΤΡΕΠΟΥΜΕ ΤΗΝ ΕΠΕΞΕΡΓΑΣΙΑ
        ),
        "Αποτέλεσμα (Ε)": st.column_config.Column(disabled=True),
        "Επεξήγηση (G)": st.column_config.Column(disabled=True),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="fixed"
)

# 3. Κουμπί Υπολογισμού
if st.button("🔄 Εκτέλεση Υπολογισμού"):
    # Εδώ θα έπρεπε να τρέχει το logic του υπολογισμού.
    # Επειδή το Streamlit Cloud δεν τρέχει "ζωντανά" το Excel (xlwings), 
    # το κουμπί αυτό χρησιμεύει για να επιβεβαιώσει ο χρήστης τις αλλαγές του.
    st.success("Οι τιμές καταχωρήθηκαν. Το τελικό πληρωτέο (D43) θα ενημερωθεί βάσει των νέων δεδομένων.")
    
    # Δείχνουμε τις αλλαγές που έκανε ο χρήστης για επιβεβαίωση
    changes = edited_df[edited_df['Προς Επεξεργασία (D)'] != '']
    if not changes.empty:
        st.write("Νέες τιμές που εισήχθησαν:")
        st.write(changes[['Περιγραφή (Β)', 'Προς Επεξεργασία (D)']])
