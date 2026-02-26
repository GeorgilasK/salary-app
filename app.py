import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση του Excel και του mapping για το D5
@st.cache_data
def load_all_data():
    df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
    # Mapping από C254:D280
    ref_table = df_raw.iloc[253:280, [2, 3]] 
    ref_table.columns = ['key', 'value']
    mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
    
    # Περιοχή B3:J287 για εμφάνιση
    df_display = df_raw.iloc[2:287, 1:10].copy()
    df_display.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    return df_display, mapping, df_raw

df_display, d5_mapping, full_excel = load_all_data()

st.title("📊 Υπολογιστής Μισθοδοσίας")

# --- ΤΜΗΜΑ ΥΠΟΛΟΓΙΣΜΩΝ (Metrics) ---
st.subheader("🚀 Ζωντανά Αποτελέσματα")
metrics_container = st.container() # Χώρος για τις κάρτες

# 2. Ρύθμιση του Πίνακα AgGrid
gb = GridOptionsBuilder.from_dataframe(df_display)
gb.configure_default_column(editable=False, resizable=True)

# Λίστες για τα Dropdowns
d5_list = list(d5_mapping.keys())
d7_list = ["ΝΑΙ", "ΟΧΙ"]
d22_list = ["0", "1", "2", "3", "4", "5"]

# Ενεργοποίηση επεξεργασίας στη στήλη D με Dropdown
gb.configure_column("D", 
                    editable=True, 
                    cellEditor='agSelectCellEditor', 
                    cellEditorParams={'values': d5_list + d7_list + d22_list},
                    cellStyle={'background-color': '#e1f5fe'})

grid_options = gb.build()

grid_response = AgGrid(
    df_display,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    theme='alpine'
)

# 3. ΕΚΤΕΛΕΣΗ ΛΟΓΙΚΗΣ EXCEL ΣΕ PYTHON
updated_data = grid_response['data']

if updated_data is not None:
    try:
        # Μετατροπή σε DataFrame για ευκολία
        u_df = pd.DataFrame(updated_data)
        
        # Λήψη τιμών από τις σωστές θέσεις (D5=index 2, D7=index 4, D22=index 19, D43=index 40)
        d5_sel = str(u_df.iloc[2, 2])
        d22_sel = int(u_df.iloc[19, 2]) if u_df.iloc[19, 2] != "" else 0
        d4
