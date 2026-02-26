import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

@st.cache_data
def load_all_data():
    try:
        df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
        ref_table = df_raw.iloc[253:280, [2, 3]] 
        ref_table.columns = ['key', 'value']
        mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
        
        df_display = df_raw.iloc[2:287, 1:10].copy()
        df_display.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        return df_display, mapping, df_raw
    except Exception as e:
        st.error(f"Σφάλμα: {e}")
        return None, None, None

df_display, d5_mapping, full_excel = load_all_data()

# --- JavaScript Logic για ξεχωριστά Dropdowns ανά γραμμή ---
# Row 0 στον πίνακα αντιστοιχεί στη γραμμή 3 του Excel
# Row 2 -> D5, Row 4 -> D7, Row 19 -> D22
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

if df_display is not None:
    st.title("📊 Υπολογιστής Μισθοδοσίας")
    metrics_placeholder = st.empty()

    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_default_column(editable=False, resizable=True)

    # Εφαρμογή του Selector στη στήλη D
    gb.configure_column("D", 
                        editable=True, 
                        cellEditorSelector=cell_editor_selector,
                        cellStyle={'background-color': '#e3f2fd', 'border': '1px solid #bbdefb'})

    grid_options = gb.build()

    grid_response = AgGrid(
        df_display,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True, # Απαραίτητο για το JsCode
        fit_columns_on_grid_load=True,
        theme='alpine'
    )

    # --- ΥΠΟΛΟΓΙΣΜΟΙ ---
    u_df = pd.DataFrame(grid_response['data'])
    if not u_df.empty:
        try:
            d5_sel = str(u_df.iloc[2, 2])
            d22_sel = int(u_df.iloc[19, 2]) if str(u_df.iloc[19, 2]).strip() != "" else 0
            
            d43_raw = str(u_df.iloc[40, 2]).replace(',', '.')
            d43_sel = float(d43_raw) if d43_raw.strip() != "" else 0.0

            # Μαθηματικά (όπως τα ορίσαμε)
            e11 = float(full_excel.iloc[10, 4]) if not pd.isna(full_excel.iloc[10, 4]) else 0.0
            e12 = float(full_excel.iloc[11, 4]) if not pd.isna(full_excel.iloc[11, 4]) else 0.0
            e14 = e11 + e12
            e21 = float(d5_mapping.get(d5_sel, 0)) * 0.1136

            levels = {0:0.0, 1:29.35, 2:58.7, 3:91.09, 4:155.69, 5:220.29}
            e22 = levels.get(d22_sel, 0.0)

            d17 = float(full_excel.iloc[16, 3]) if not pd.isna(full_excel.iloc[16, 3]) else 160.0
            d177 = (e14 + e21 + e22) / d17
            e43 = (d177 * d43_sel) * 1.2 * 1.75

            with metrics_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Ωρομίσθιο (D177)", f"{d177:.4f} €")
                m2.metric("Επίδομα (E22)", f"{e22:.2f} €")
                m3.metric("Κρατήσεις (E21)", f"{e21:.2f} €")
                m4.metric("ΣΥΝΟΛΟ Ε43", f"{e43:.2f} €")
                st.markdown("---")
        except:
            st.sidebar.info("Εκκρεμεί συμπλήρωση τιμών")

st.info("💡 **Οδηγία:** Διπλό κλικ στο κελί της στήλης D. Το μενού προσαρμόζεται αυτόματα στη γραμμή που βρίσκεστε.")
