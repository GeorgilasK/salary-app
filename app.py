import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

@st.cache_data
def load_all_data():
    try:
        df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
        # Mapping για D5 (Κλιμάκια)
        ref_table = df_raw.iloc[253:280, [2, 3]] 
        ref_table.columns = ['key', 'value']
        mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
        
        # Περιοχή B3:J287
        df_display = df_raw.iloc[2:287, 1:10].copy()
        df_display.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        return df_display, mapping, df_raw
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης: {e}")
        return None, None, None

df_display, d5_mapping, full_excel = load_all_data()

# JavaScript για τα dropdowns (D5, D7, D22)
cell_editor_selector = JsCode("""
function(params) {
    if (params.node.rowIndex === 2) { // D5
        return { component: 'agSelectCellEditor', params: { values: ['Α', 'Β', 'Γ', 'Δ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'] }, popup: true };
    }
    if (params.node.rowIndex === 4) { // D7
        return { component: 'agSelectCellEditor', params: { values: ['ΝΑΙ', 'ΟΧΙ'] }, popup: true };
    }
    if (params.node.rowIndex === 19) { // D22
        return { component: 'agSelectCellEditor', params: { values: ['0', '1', '2', '3', '4', '5'] }, popup: true };
    }
    return null;
}
""")

if df_display is not None:
    st.title("📊 Υπολογιστής Μισθοδοσίας")
    metrics_placeholder = st.empty()

    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_default_column(editable=False, resizable=True)
    gb.configure_column("D", editable=True, cellEditorSelector=cell_editor_selector)
    grid_options = gb.build()

    grid_response = AgGrid(
        df_display,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        theme='alpine'
    )

    u_df = pd.DataFrame(grid_response['data'])
    
    if not u_df.empty:
        try:
            # 1. Λήψη τιμών εισόδου από τη στήλη D
            d5_sel = str(u_df.iloc[2, 2])
            d7_sel = str(u_df.iloc[4, 2]) # "ΝΑΙ" ή "ΟΧΙ"
            d22_sel = int(u_df.iloc[19, 2]) if str(u_df.iloc[19, 2]).strip() != "" else 0
            d43_raw = str(u_df.iloc[40, 2]).replace(',', '.')
            d43_sel = float(d43_raw) if d43_raw.strip() != "" else 0.0

            # 2. Σταθερές από το Excel (E11, E12, D17)
            e11 = float(full_excel.iloc[10, 4]) if not pd.isna(full_excel.iloc[10, 4]) else 0.0
            e12 = float(full_excel.iloc[11, 4]) if not pd.isna(full_excel.iloc[11, 4]) else 0.0
            d17 = float(full_excel.iloc[16, 3]) if not pd.isna(full_excel.iloc[16, 3]) else 160.0

            # --- Η ΛΟΓΙΚΗ ΤΩΝ ΣΥΝΑΡΤΗΣΕΩΝ ΣΟΥ ---

            # E14 = E11 + E12
            e14 = e11 + e12

            # Υπολογισμός Ε7 (αυτό που ζήτησες: IF(D7="ΝΑΙ";E11*10%;0))
            e7 = (e11 * 0.10) if d7_sel == "ΝΑΙ" else 0.0

            # E21 = D265 * 11,36% (Το D265 αντιστοιχεί στην επιλογή του D5)
            d5_base_val = float(d5_mapping.get(d5_sel, 0))
            e21 = d5_base_val * 0.1136

            # E22 (IF συνάρτηση για D22)
            levels = {0:0.0, 1:29.35, 2:58.7, 3:91.09, 4:155.69, 5:220.29}
            e22 = levels.get(d22_sel, 0.0)

            # Τελικό Ωρομίσθιο (D177)
            # Εδώ πρόσθεσα και το e7 στον υπολογισμό αν συμμετέχει στο άθροισμα
            d177_val = (e14 + e21 + e22 + e7) / d17
            
            # Τελικό Ποσό (Ε43)
            e43_val = (d177_val * d43_sel) * 1.20 * 1.75

            # 3. Ενημέρωση των Metrics
            with metrics_placeholder.container():
                st.markdown(f"### 📋 Ανάλυση για: Κλιμάκιο {d5_sel} | Παιδιά: {d7_sel}")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Επίδομα Παιδιών (E7)", f"{e7:.2f} €")
                m2.metric("Επίδομα Θέσης (E22)", f"{e22:.2f} €")
                m3.metric("Ωρομίσθιο (D177)", f"{d177_val:.4f} €")
                m4.metric("ΤΕΛΙΚΟ Ε43", f"{e43_val:.2f} €")
                st.markdown("---")
            
        except Exception as e:
            st.warning("Παρακαλώ συμπληρώστε τις τιμές στη στήλη D.")

st.info("💡 Κάντε διπλό κλικ στη στήλη D για αλλαγή. Μόλις αλλάξετε το 'ΝΑΙ/ΟΧΙ', το Ε7 θα υπολογιστεί αμέσως.")
