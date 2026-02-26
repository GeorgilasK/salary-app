import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# Φόρτωση δεδομένων από το Excel
@st.cache_data
def load_data():
    # Αντικατάστησε το όνομα με το δικό σου αρχείο
    df = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Ονομάζουμε τις στήλες για ευκολία (A, B, C, D, E...)
    df.columns = [f"Col_{i}" for i in range(len(df.columns))]
    return df

df = load_data()

st.title("📊 Πλήρης Πίνακας Υπολογισμών (AgGrid)")

# Ρύθμιση του AgGrid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True, resizable=True)

# Ρύθμιση Dropdown για το D5 (Col_3, Row 4) και D7 (Col_3, Row 6)
# Σημείωση: Στο AgGrid η ρύθμιση ανά κελί είναι δύσκολη, οπότε επιτρέπουμε 
# την επεξεργασία σε όλη τη στήλη D (Col_3)
gb.configure_column("Col_3", headerName="Προς Επεξεργασία (D)", editable=True)

grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    fit_columns_on_grid_load=True,
    theme='streamlit', # Διαθέσιμα: 'streamlit', 'alpine', 'balham', 'material'
)

# Παίρνουμε τα ενημερωμένα δεδομένα
updated_df = grid_response['data']

# --- ΛΟΓΙΚΗ ΥΠΟΛΟΓΙΣΜΟΥ (Python Side) ---
try:
    # Εδώ τραβάμε τις τιμές από τα συγκεκριμένα κελιά του πίνακα
    # index = Row - 1 (π.χ. Row 5 είναι index 4)
    d5_val = updated_df.iloc[4, 3]  # D5
    d22_val = updated_df.iloc[21, 3] # D22
    d43_val = updated_df.iloc[42, 3] # D43
    
    # Μετατροπή σε αριθμούς (αν είναι δυνατόν)
    try:
        d43_float = float(d43_val)
    except:
        d43_float = 0.0

    # Εδώ βάζεις τους τύπους που είπαμε (παράδειγμα)
    # E14 = E11 + E12
    e11 = float(updated_df.iloc[10, 4])
    e12 = float(updated_df.iloc[11, 4])
    e14 = e11 + e12
    
    # D17
    d17 = float(updated_df.iloc[16, 3])
    
    # D177 και E43 (όπως τα συζητήσαμε)
    # d177 = (e14 + e21 + e22) / d17 ...
    
    st.sidebar.success(f"Τελευταίος Υπολογισμός E43: {d43_float * 1.2 * 1.75:.2f} €") # Ενδεικτικά

except Exception as e:
    st.sidebar.error(f"Αναμονή για έγκυρα δεδομένα...")

st.info("💡 Μπορείτε να επεξεργαστείτε οποιοδήποτε κελί απευθείας στον πίνακα.")
