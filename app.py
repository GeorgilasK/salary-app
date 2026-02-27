import pandas as pd
import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
import io

def generate_excel(csv_path):
    # Φόρτωση δεδομένων
    df = pd.read_csv(csv_path)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Υπολογισμός Μισθοδοσίας"

    # --- ΟΡΙΣΜΟΣ ΣΤΥΛ ---
    thin_side = Side(border_style="thin", color="000000")
    border_all = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)
    italic_font = Font(italic=True, size=10, color="444444")
    bold_font = Font(bold=True)
    red_font = Font(color="FF0000", bold=True)
    
    # Formats
    currency_format = '#,##0.00€'
    integer_format = '0'

    # Πλάτος στηλών
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 55
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 18
    ws.column_dimensions['E'].width = 35  # Για το warning message
    ws.column_dimensions['F'].width = 45
    ws.column_dimensions['G'].width = 45

    # --- LOOP ΓΙΑ ΤΙΣ 242 ΓΡΑΜΜΕΣ ---
    # Διαβάζουμε το CSV και μεταφέρουμε τα δεδομένα ακριβώς
    for index, row in df.iterrows():
        excel_row = index + 1
        if excel_row > 242:
            break
        
        # Στήλη Β: Περιγραφή
        desc = row.iloc[1] if pd.notnull(row.iloc[1]) else ""
        ws.cell(row=excel_row, column=2).value = desc
        
        # Στήλη D: Τιμές
        val_d = row.iloc[3]
        if pd.notnull(val_d):
            ws.cell(row=excel_row, column=4).value = val_d
            # Μορφοποίηση: Αν είναι μεγάλος αριθμός (>200) ή έχει δεκαδικά, θεώρησέ το Ευρώ
            if isinstance(val_d, (int, float)) and val_d > 0:
                if val_d > 163 or not float(val_d).is_integer():
                    ws.cell(row=excel_row, column=4).number_format = currency_format
                else:
                    ws.cell(row=excel_row, column=4).number_format = integer_format

        # Στήλες F & G: Σημειώσεις (Italics)
        for col_idx, col_val in zip([6, 7], [row.iloc[5], row.iloc[6]]):
            if pd.notnull(col_val):
                cell = ws.cell(row=excel_row, column=col_idx)
                cell.value = str(col_val)
                cell.font = italic_font
                cell.alignment = Alignment(wrap_text=True)

        # Εφαρμογή πλαισίου σε όλη τη γραμμή (A-G)
        for col in range(1, 8):
            ws.cell(row=excel_row, column=col).border = border_all

    # --- ΕΙΔΙΚΑ DROPDOWNS ---
    # D3: Μισθολογικό Κλιμάκιο (1-15)
    dv_d3 = DataValidation(type="list", formula1='"1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"', allow_blank=True)
    ws.add_data_validation(dv_d3)
    dv_d3.add(ws['D3'])

    # D5: Επίδομα Γάμου (ΝΑΙ/ΟΧΙ)
    dv_d5 = DataValidation(type="list", formula1='"ΝΑΙ,ΟΧΙ"', allow_blank=True)
    ws.add_data_validation(dv_d5)
    dv_d5.add(ws['D5'])

    # D7: Πολυετία (5, 10, 15, 20, 25, 30)
    dv_d7 = DataValidation(type="list", formula1='"0,5,10,15,20,25,30"', allow_blank=True)
    ws.add_data_validation(dv_d7)
    dv_d7.add(ws['D7'])

    # D20: Επιλογή Τύπου Εργασίας (Ενδεικτικά values από το excel σου)
    dv_d20 = DataValidation(type="list", formula1='"ΠΛΗΡΕΣ,ΜΕΙΩΜΕΝΟ,ΕΚΤΑΚΤΟ"', allow_blank=True)
    ws.add_data_validation(dv_d20)
    dv_d20.add(ws['D20'])

    # --- ΕΛΕΓΧΟΣ ΩΡΩΝ (D15+D16+D17 = 162.50) ---
    ws['E17'].formula = '=IF(SUM(D15:D17)<>162.5, "⚠ ΑΘΡΟΙΣΜΑ ΩΡΩΝ ≠ 162.50", "")'
    ws['E17'].font = red_font
    ws['E17'].alignment = Alignment(horizontal='left')

    # Επιστροφή του αρχείου ως Stream
    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()

# --- STREAMLIT UI ---
st.title("Salary Calculator Excel Generator")
st.write("Πατήστε το κουμπί για να δημιουργήσετε το Excel με τις 242 γραμμές.")

# Το CSV πρέπει να βρίσκεται στον ίδιο φάκελο στο GitHub
csv_file = 'Georgilas Salary Calc.xlsx - Calc.csv'

if st.button('Δημιουργία Αρχείου Excel'):
    try:
        excel_data = generate_excel(csv_file)
        st.download_button(
            label="Download Excel File",
            data=excel_data,
            file_name="Georgilas_Salary_Calc_Final.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("Το αρχείο δημιουργήθηκε με επιτυχία!")
    except Exception as e:
        st.error(f"Σφάλμα: {e}")
