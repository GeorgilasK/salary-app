import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

@st.cache_data
def load_all_data():
    try:
        df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
        # Mapping για D5
        ref_table = df_raw.iloc[253:280, [2, 3]] 
        ref_table.columns = ['key', 'value']
        mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
        
        # Περιοχή B3:J287
        df_display = df_raw.iloc[2:287, 1:10].copy()
        df_display.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        # Μετατροπή της στήλης Ε σε αριθμητική για να δέχεται τα δεκαδικά
        df_display['E'] = pd.to_numeric(df_display['E'], errors='coerce').fillna(0.0)
        
        return df_display, mapping, df_raw
    except Exception as e:
        st.error(f"Σφάλμα: {e}")
        return None, None, None

df_display, d5_mapping, full_excel = load_all_data()

# JS για ξεχωριστά Dropdowns
cell_editor_selector = JsCode("""
function(params) {
    if (params.node.rowIndex === 2) {
        return {
            component: 'agSelectCellEditor',
            params: { values: ['Α', 'Β', 'Γ', 'Δ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'] },
            popup: true
        };
    }
    if (params.node.rowIndex === 4) {
        return {
            component: 'agSelectCellEditor',
            params: { values: ['ΝΑΙ', 'ΟΧΙ'] },
            popup: true
        };
    }
    if (params.node.rowIndex === 19) {
        return {
            component: 'agSelectCellEditor',
            params: { values: ['0', '1', '2', '3', '4', '5'] },
            popup: true
        };
    }
    return null;
}
""")

# JS για μορφοποίηση 2 δεκαδικών στη στήλη Ε
euro_format = JsCode("""
function(params) {
    if (params.value === undefined || params.value === null || params.value === "") return "";
    return parseFloat(params.value).toLocaleString('el-GR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' €';
}
""")

if df_display is not None:
    st.title("📊 Υπολογιστής Μισθοδοσίας")
    
    # Χώρος για τα Metrics στην κορυφή
    metrics_placeholder = st.empty()

    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_default_column(editable=False, resizable=True)

    # Ρύθμιση στήλης D (Dropdowns)
    gb.configure_column("D", editable=True, cellEditorSelector=cell_editor_selector)

    # Ρύθμιση στήλης Ε (2 δεκαδικά)
    gb.configure_column("E", valueFormatter=euro_format, type=["numericColumn"])

    grid_options = gb.build()

    # Εμφάνιση πίνακα
    grid_response = AgGrid(
        df_display,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        theme='alpine'
    )

    # --- Επεξεργασία και "Ζωντανή" Ενημέρωση ---
    u_df = pd.DataFrame(grid_response['data'])
    
    if not u_df.empty:
        try:
            # Λήψη τιμών εισόδου
            d5_sel = str(u_df.iloc[2, 2])
            d22_sel = int(u_df.iloc[19, 2]) if str(u_df.iloc[19, 2]).strip() != "" else 0
            d43_raw = str(u_df.iloc[40, 2]).replace(',', '.')
            d43_sel = float(d43_raw) if d43_raw.strip() != "" else 0.0

            # Υπολογισμοί (ίδιοι με πριν)
            e11 = float(full_excel.iloc[10, 4]) if not pd.isna(full_excel.iloc[10, 4]) else 0.0
            e12 = float(full_excel.iloc[11, 4]) if not pd.isna(full_excel.iloc[11, 4]) else 0.0
            e14 = e11 + e12
            e21 = float(d5_mapping.get(d5_sel, 0)) * 0.1136
            
            levels = {0:0.0, 1:29.35, 2:58.7, 3:91.09, 4:155.69, 5:220.29}
            e22 = levels.get(d22_sel, 0.0)
            
            d17 = float(full_excel.iloc[16, 3]) if not pd.isna(full_excel.iloc[16, 3]) else 160.0
            d177 = (e14 + e21 + e22) / d17
            e43_final = (d177 * d43_sel) * 1.2 * 1.75

            # Εμφάνιση Metrics
            with metrics_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Ωρομίσθιο (D177)", f"{d177:.4f} €")
                m2.metric("Επίδομα (E22)", f"{e22:.2f} €")
                m3.metric("Κρατήσεις (E21)", f"{e21:.2f} €")
                m4.metric("ΣΥΝΟΛΟ Ε43", f"{e43_final:.2f} €")
                st.markdown("---")
            
            # Αν θες να ενημερώνεται η στήλη Ε "οπτικά" στον πίνακα, 
            # αυτή η έκδοση του AgGrid απαιτεί rerender. 
            # Προς το παρόν τα metrics είναι η πιο αξιόπιστη λύση.
            
        except Exception as e:
            st.sidebar.error("Συμπληρώστε τα πεδία")

st.info("💡 **Tip:** Αφού επιλέξετε τιμή στο D, πατήστε **Enter**. Το αποτέλεσμα θα εμφανιστεί αμέσως στις κάρτες στην κορυφή.")
