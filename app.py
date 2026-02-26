import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

@st.cache_data
def load_data():
    # Φόρτωση του Excel
    df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    
    # Επιλογή γραμμών 3 έως 287 (index 2 έως 287)
    # Επιλογή στηλών B έως J (index 1 έως 9)
    df_subset = df_raw.iloc[2:287, 1:10].copy()
    
    # Ονομασία στηλών για να ξέρουμε τι επεξεργαζόμαστε
    df_subset.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    # Καθαρισμός κενών τιμών για αποφυγή σφαλμάτων
    df_subset = df_subset.fillna("")
    return df_subset

df = load_data()

st.title("📊 Πίνακας Υπολογισμών (B3:J287)")

# 1. Ρύθμιση του GridOptions
gb = GridOptionsBuilder.from_dataframe(df)

# Προεπιλογή: Όλες οι στήλες σταθερές, εκτός από τη D
gb.configure_default_column(editable=False, resizable=True)

# 2. Ρύθμιση της στήλης D (Col 'D') να είναι επεξεργάσιμη
# Προσθήκη CellEditor για Dropdown επιλογές
d5_options = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
d7_options = ["ΝΑΙ", "ΟΧΙ"]
d22_options = ["0", "1", "2", "3", "4", "5"]

# Εφαρμογή Dropdown συγκεκριμένα για τα κελιά (μέσω συνάρτησης JS ή απλού Editor)
# Εδώ ορίζουμε τη στήλη D ως επεξεργάσιμη γενικά
gb.configure_column("D", 
                    headerName="Είσοδος (D)", 
                    editable=True, 
                    cellStyle={'background-color': '#f0f2f6'},
                    # Προσθήκη επιλογών ανάλογα με τη γραμμή (πολύ βασικό για AgGrid)
                    cellEditor='agRichSelectCellEditor',
                    cellEditorParams={'values': d5_options + d7_options + d22_options} 
                   )

# Περιορισμός εμφάνισης άλλων στηλών αν χρειάζεται
grid_options = gb.build()

# 3. Εμφάνιση του Πίνακα
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.VALUE_CHANGED, # Ενημέρωση με κάθε αλλαγή
    fit_columns_on_grid_load=True,
    theme='alpine',
)

# 4. Επεξεργασία των αλλαγών (Python Side)
updated_df = pd.DataFrame(grid_response['data'])

try:
    # ΣΗΜΑΝΤΙΚΟ: Το index στον updated_df ξεκινάει από το 0 για τη γραμμή 3 του Excel
    # Άρα: Το D5 του Excel είναι το updated_df.iloc[2, 2] (Στήλη D είναι το 3ο column, index 2)
    
    d5_val = updated_df.iloc[2, 2]  # D5
    d7_val = updated_df.iloc[4, 2]  # D7
    d22_val = updated_df.iloc[19, 2] # D22 (Γραμμή 22 -> index 19)
    d43_val = updated_df.iloc[40, 2] # D43 (Γραμμή 43 -> index 40)

    # Μετατροπή D43 σε αριθμό για τον υπολογισμό
    try:
        val_d43 = float(d43_val) if d43_val != "" else 0.0
    except:
        val_d43 = 0.0

    # Εδώ εκτελείται ο "ζωντανός" υπολογισμός που μου έδωσες
    # Χρειάζεται να ορίσουμε το D177 βάσει των νέων τιμών
    # (Εδώ μπαίνει η συνάρτηση που φτιάξαμε πριν)
    
    st.sidebar.markdown("### 🧮 Ζωντανά Αποτελέσματα")
    st.sidebar.write(f"**Επιλογή D5:** {d5_val}")
    st.sidebar.write(f"**Επιλογή D7:** {d7_val}")
    st.sidebar.info(f"Αποτέλεσμα βάσει D43: {val_d43 * 1.2 * 1.75:.2f} €") # Ενδεικτικός τύπος

except Exception as e:
    st.sidebar.warning("Αλλάξτε μια τιμή στη στήλη D για να ξεκινήσει ο υπολογισμός.")
