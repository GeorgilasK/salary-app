import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

@st.cache_data
def load_data():
    df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Επιλογή B3:J287
    df_subset = df_raw.iloc[2:287, 1:10].copy()
    df_subset.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    df_subset = df_subset.fillna("")
    return df_subset

df = load_data()

# --- JavaScript για Dropdown και Format Ευρώ ---
# Αυτό το κομμάτι επιτρέπει στο AgGrid να δείχνει τη λίστα
cell_editor_js = JsCode("""
function(params) {
    if (params.node.rowIndex === 2) { // Γραμμή 5 (D5)
        return {
            component: 'agRichSelectCellEditor',
            params: { values: ['Α', 'Β', 'Γ', 'Δ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'] }
        };
    }
    if (params.node.rowIndex === 4) { // Γραμμή 7 (D7)
        return {
            component: 'agRichSelectCellEditor',
            params: { values: ['ΝΑΙ', 'ΟΧΙ'] }
        };
    }
    return { component: 'agTextCellEditor' };
}
""")

euro_format_js = JsCode("""
function(params) {
    if (params.value === "" || params.value === null) return "";
    return parseFloat(params.value).toFixed(2) + " €";
}
""")

st.title("📊 Πίνακας Υπολογισμών")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=False, resizable=True)

# Ρύθμιση στήλης D με Dropdown (μέσω JS)
gb.configure_column("D", editable=True, cellEditorSelector=cell_editor_js)

# Ρύθμιση στήλης Ε για 2 δεκαδικά και Ευρώ
gb.configure_column("E", valueFormatter=euro_format_js)

grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    allow_unsafe_jscode=True, # Απαραίτητο για να τρέξει το JavaScript
    theme='alpine',
)

# --- ΕΝΗΜΕΡΩΣΗ ΤΙΜΩΝ ---
updated_df = grid_response['data']

# Εδώ πρέπει να γίνει ο χειροκίνητος υπολογισμός στην Python
# για να δεις την αλλαγή στη στήλη Ε
if grid_response['data'] is not None:
    try:
        # Παράδειγμα: Αν αλλάξει το D43 (Row index 40), υπολόγισε το E43
        d43_val = float(updated_df.iloc[40, 2])
        # Έστω ένας πρόχειρος υπολογισμός για να δεις ότι δουλεύει
        result = d43_val * 1.2 * 1.75 
        
        st.sidebar.metric("Τελικό Αποτέλεσμα (E43)", f"{result:.2f} €")
    except:
        pass

st.info("💡 Κάντε διπλό κλικ στα κελιά της στήλης D για να ανοίξει η λίστα ή να πληκτρολογήσετε.")
