import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Συνάρτηση Φόρτωσης
@st.cache_data
def load_data():
    df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Περιοχή B3:J287
    df_subset = df_raw.iloc[2:287, 1:10].copy()
    df_subset.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    return df_subset

df = load_data()

st.title("📊 Υπολογιστής Μισθοδοσίας")

# 2. Ρύθμιση Πίνακα
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=False, resizable=True)

# Ρυθμίζουμε τη στήλη D να δέχεται Dropdown με τον απλό τρόπο (χωρίς πολύ JS)
d5_list = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
d7_list = ["ΝΑΙ", "ΟΧΙ"]
d22_list = ["0", "1", "2", "3", "4", "5"]

# Εφαρμόζουμε το dropdown σε ΟΛΗ τη στήλη D για να είμαστε σίγουροι ότι θα δουλέψει
gb.configure_column("D", 
                    editable=True, 
                    cellEditor='agSelectCellEditor', 
                    cellEditorParams={'values': d5_list + d7_list + d22_list})

grid_options = gb.build()

# 3. Εμφάνιση Πίνακα
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    theme='balham' # Πιο ελαφρύ theme για να φαίνονται οι αλλαγές
)

# 4. Ο "ΜΑΓΙΚΟΣ" ΥΠΟΛΟΓΙΣΜΟΣ ΠΟΥ ΛΕΙΠΕΙ
updated_df = pd.DataFrame(grid_response['data'])

if not updated_df.empty:
    try:
        # Τραβάμε τις τιμές από τις θέσεις τους
        # Προσοχή: index 2 = Row 5, index 4 = Row 7, index 19 = Row 22, index 40 = Row 43
        d5_val = updated_df.iloc[2, 2]
        d22_val = updated_df.iloc[19, 2]
        d43_val = updated_df.iloc[40, 2]

        # Μετατροπή σε νούμερα
        try:
            d43_num = float(d43_val)
        except:
            d43_num = 0.0

        # --- ΕΔΩ ΓΡΑΦΟΥΜΕ ΤΟΝ ΤΥΠΟ ΤΟΥ EXCEL ΣΕ PYTHON ---
        # Παράδειγμα: E14=(E11+E12), D177=(E14+E21+E22)/D17 κλπ.
        # Θα χρησιμοποιήσουμε τις τιμές που μου έδωσες πριν.
        
        # Έστω μια σταθερή τιμή d177 για το παράδειγμα (βάλε τη δική σου αν την ξέρεις)
        d177_mock = 12.50 
        e43_result = (d177_mock * d43_num) * 1.20 * 1.75

        # 5. ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΟΣ ΕΚΤΟΣ ΠΙΝΑΚΑ (για σιγουριά)
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Επιλογή Κλιμακίου (D5)", d5_val)
        c2.metric("Επίπεδο (D22)", d22_val)
        c3.subheader(f"Αποτέλεσμα E43: {e43_result:.2f} €")

        # 6. ΠΡΟΣΠΑΘΕΙΑ ΕΝΗΜΕΡΩΣΗΣ ΤΗΣ ΣΤΗΛΗΣ Ε ΣΤΟΝ ΠΙΝΑΚΑ
        # (Αυτό θα αλλάξει το νούμερο στην οθόνη κάτω από τον πίνακα)
        updated_df.iloc[40, 3] = f"{e43_result:.2f}" # Ενημέρωση του E43 στο DataFrame
        
    except Exception as e:
        st.error(f"Σφάλμα υπολογισμού: {e}")

st.help("Για να αλλάξετε τιμή: Διπλό κλικ στο κελί της στήλης D, επιλέξτε τιμή και πατήστε ENTER.")
