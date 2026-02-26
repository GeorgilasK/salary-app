import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(page_title="Υπολογιστής Μισθοδοσίας", layout="wide")

# 1. Φόρτωση δεδομένων
@st.cache_data
def load_all_data():
    try:
        # Φόρτωση του Excel
        df_raw = pd.read_excel("salary_calc.xlsx", sheet_name="Calc", header=None)
        
        # Mapping για το D5 από C254:D280 (index 253:280)
        ref_table = df_raw.iloc[253:280, [2, 3]] 
        ref_table.columns = ['key', 'value']
        mapping = dict(zip(ref_table['key'].astype(str), ref_table['value']))
        
        # Περιοχή B3:J287 για εμφάνιση (index 2:287, cols 1:10)
        df_display = df_raw.iloc[2:287, 1:10].copy()
        df_display.columns = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        return df_display, mapping, df_raw
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης αρχείου: {e}")
        return None, None, None

df_display, d5_mapping, full_excel = load_all_data()

if df_display is not None:
    st.title("📊 Υπολογιστής Μισθοδοσίας")

    # --- ΤΜΗΜΑ ΥΠΟΛΟΓΙΣΜΩΝ (Metrics) ---
    st.subheader("🚀 Ζωντανά Αποτελέσματα")
    metrics_placeholder = st.empty() # Χώρος που θα ανανεώνεται

    # 2. Ρύθμιση AgGrid
    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_default_column(editable=False, resizable=True)

    # Επιλογές Dropdown
    d5_list = list(d5_mapping.keys())
    d7_list = ["ΝΑΙ", "ΟΧΙ"]
    d22_list = ["0", "1", "2", "3", "4", "5"]

    # Ρύθμιση στήλης D
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

    # 3. Επεξεργασία δεδομένων
    updated_data = grid_response['data']

    if updated_data is not None:
        try:
            # Μετατροπή σε DataFrame για ασφάλεια
            u_df = pd.DataFrame(updated_data)
            
            # Λήψη τιμών (Προσοχή στα indexes μετά το slice B3:J287)
            # D5  -> Row index 2 (Γραμμή 5 του Excel)
            # D7  -> Row index 4 (Γραμμή 7 του Excel)
            # D22 -> Row index 19 (Γραμμή 22 του Excel)
            # D43 -> Row index 40 (Γραμμή 43 του Excel)
            
            d5_sel = str(u_df.iloc[2, 2])
            d22_sel = int(u_df.iloc[19, 2]) if str(u_df.iloc[19, 2]).strip() != "" else 0
            
            try:
                d43_val = str(u_df.iloc[40, 2]).replace(',', '.')
                d43_sel = float(d43_val) if d43_val.strip() != "" else 0.0
            except:
                d43_sel = 0.0

            # --- Υπολογισμοί Python ---
            e11 = float(full_excel.iloc[10, 4]) if not pd.isna(full_excel.iloc[10, 4]) else 0.0
            e12 = float(full_excel.iloc[11, 4]) if not pd.isna(full_excel.iloc[11, 4]) else 0.0
            e14 = e11 + e12

            d5_base_val = float(d5_mapping.get(d5_sel, 0))
            e21 = d5_base_val * 0.1136

            # Λογική E22
            if d22_sel == 0: e22 = 0.0
            elif d22_sel == 1: e22 = 29.35
            elif d22_sel == 2: e22 = 29.35 * 2
            elif d22_sel == 3: e22 = (29.35 * 2) + 32.39
            elif d22_sel == 4: e22 = (29.35 * 2) + 32.39 + 64.6
            elif d22_sel == 5: e22 = (29.35 * 2) + 32.39 + 64.6 + 64.6
            else: e22 = 0.0

            d17 = float(full_excel.iloc[16, 3]) if not pd.isna(full_excel.iloc[16, 3]) else 160.0
            d177_val = (e14 + e21 + e22) / d17
            e43_val = (d177_val * d43_sel) * 1.20 * 1.75

            # Εμφάνιση των Metrics
            with metrics_placeholder.container():
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Ωρομίσθιο (D177)", f"{d177_val:.4f} €")
                m2.metric("Επίδομα (E22)", f"{e22:.2f} €")
                m3.metric("Κρατήσεις (E21)", f"{e21:.2f} €")
                m4.metric("ΤΕΛΙΚΟ Ε43", f"{e43_val:.2f} €")
                st.markdown("---")

        except Exception as ex:
            st.warning(f"Συμπληρώστε τις τιμές στη στήλη D για υπολογισμό.")

st.info("💡 **Διπλό κλικ** στο κελί της στήλης D για επιλογή. Πατήστε **Enter** για επιβεβαίωση.")
