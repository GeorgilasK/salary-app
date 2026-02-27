import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

# Φόρτωση των δεδομένων από το CSV που ανέβηκε
df = pd.read_csv('Georgilas Salary Calc.xlsx - Calc.csv')

wb = Workbook()
ws = wb.active
ws.title = "Υπολογισμός Μισθοδοσίας"

# Ορισμός στυλ
thin_side = Side(border_style="thin", color="000000")
border_all = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)
italic_font = Font(italic=True, size=10)
bold_font = Font(bold=True)
red_font = Font(color="FF0000", bold=True)
currency_format = '#,##0.00€'
integer_format = '0'

# Ρύθμιση πλατών στηλών για αναγνωσιμότητα
ws.column_dimensions['B'].width = 50
ws.column_dimensions['D'].width = 15
ws.column_dimensions['F'].width = 40
ws.column_dimensions['G'].width = 40

# --- ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΕΦΑΡΜΟΓΗ ΠΛΑΙΣΙΟΥ ΣΕ ΚΑΘΕ ΓΡΑΜΜΗ ---
def apply_row_border(row_idx, max_col=7):
    for col_idx in range(1, max_col + 1):
        ws.cell(row=row_idx, column=col_idx).border = border_all

# --- ΕΠΕΞΕΡΓΑΣΙΑ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΤΟ CSV ---
for index, row in df.iterrows():
    excel_row = index + 1
    if excel_row > 242: break # Περιορισμός στο όριο που έθεσες
    
    # Στήλη Β: Περιγραφή
    ws.cell(row=excel_row, column=2).value = row.iloc[1] if pd.notnull(row.iloc[1]) else ""
    
    # Στήλη D: Τιμές / Inputs (Θα μορφοποιηθούν παρακάτω)
    val_d = row.iloc[3]
    if pd.notnull(val_d):
        ws.cell(row=excel_row, column=4).value = val_d
    
    # Στήλη F & G: Σημειώσεις (Italics)
    for col_idx, col_val in zip([6, 7], [row.iloc[5], row.iloc[6]]):
        if pd.notnull(col_val):
            cell = ws.cell(row=excel_row, column=col_idx)
            cell.value = col_val
            cell.font = italic_font
    
    # Εφαρμογή πλαισίου σε όλη τη γραμμή (Α-G)
    apply_row_border(excel_row)

# --- ΕΙΔΙΚΕΣ ΜΟΡΦΟΠΟΙΗΣΕΙΣ & ΛΟΓΙΚΗ ---

# 1. Έλεγχος ωρών D15, D16, D17 (Πρέπει να είναι 162.50)
# Χρήση Conditional Formatting ή Formula Note στο κελί E17
warning_formula = '=IF(SUM(D15:D17)<>162.5, "ΠΡΟΣΟΧΗ: Άθροισμα ωρών ≠ 162.50", "")'
ws['E17'].formula = warning_formula
ws['E17'].font = red_font

# 2. Μορφοποίηση αριθμών
# Έστω ότι οι καταβαλλόμενες αποδοχές και τα σύνολα είναι σε συγκεκριμένες γραμμές βάσει του αρχείου σου
for r in range(1, 243):
    cell_d = ws.cell(row=r, column=4)
    # Αν το κελί έχει τιμή και δεν είναι dropdown (manual entry logic)
    if isinstance(cell_d.value, (int, float)):
        # Τα ευρώ με 2 δεκαδικά, οι ώρες/ποσότητες ακεραίους (εκτός αν είναι το 162.5)
        if r in [9, 10, 11, 21, 25, 242]: # Παραδείγματα γραμμών με ευρώ (θα προσαρμοστούν)
            cell_d.number_format = currency_format
        else:
            cell_d.number_format = integer_format

# 3. Dropdown Menus (Παράδειγμα για το κελί D4 - Έγγαμος)
dv = DataValidation(type="list", formula1='"NAI,OXI"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(ws['D4'])

# Αποθήκευση (Προσωρινή - Θα συνεχίσουμε στο επόμενο μέρος αν χρειαστεί)
wb.save("Georgilas_Salary_Calc_Fixed.xlsx")
