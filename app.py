import streamlit as st

st.set_page_config(page_title="Υπολογιστής Μισθού", layout="centered")

st.title("💰 Υπολογισμός Μισθοδοσίας")
st.info("Συμπληρώστε τα στοιχεία στη στήλη D")

# --- ΔΗΜΙΟΥΡΓΙΑ ΤΩΝ ΠΕΔΙΩΝ ΟΠΩΣ ΣΤΟ EXCEL ---

# D5: Κατηγορία (Dropdown)
st.subheader("Στοιχεία Κατάταξης")
d5_label = "Βαθμός/Κατηγορία (D5)" # Εδώ γράψε την περιγραφή της στήλης Β
d5_val = st.selectbox(d5_label, options=["Α", "Β", "Γ", "Δ"])

# D6: Προϋπηρεσία
d6_label = "Έτη Προϋπηρεσίας (D6)"
d6_val = st.number_input(d6_label, min_value=0, value=0)

# D7: Κλιμάκιο (Dropdown 1-23)
d7_label = "Μισθολογικό Κλιμάκιο (D7)"
d7_options = list(range(1, 24))
d7_val = st.selectbox(d7_label, options=d7_options)

st.markdown("---")
st.subheader("Επιδόματα & Λοιπά")

# D10: Επίδομα Θέσης
d10_label = "Επίδομα Θέσης (D10)"
d10_val = st.number_input(d10_label, min_value=0.0, value=0.0, format="%.2f")

# D11: Ανθυγιεινό
d11_label = "Ανθυγιεινό Επίδομα (D11)"
d11_val = st.number_input(d11_label, min_value=0.0, value=0.0, format="%.2f")

# D12: Παραμεθόριος
d12_label = "Επίδομα Απομακρυσμένων (D12)"
d12_val = st.number_input(d12_label, min_value=0.0, value=0.0, format="%.2f")

# --- ΕΔΩ ΜΠΑΙΝΟΥΝ ΟΙ ΜΑΘΗΜΑΤΙΚΕΣ ΦΟΡΜΟΥΛΕΣ ΣΟΥ ---
# Παράδειγμα υπολογισμού (Αντικατάστησε με τις δικές σου πράξεις)
# Έστω: Βασικός = 1000 + (Κλιμάκιο * 30)
basic_salary = 1000 + (d7_val * 30)
total_gross = basic_salary + d10_val + d11_val + d12_val
net_salary = total_gross * 0.75 # Παράδειγμα 25% κρατήσεις

# --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
st.markdown("---")
st.success(f"### 💶 Καθαρό Πληρωτέο (D43): {net_salary:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

# Αν θέλεις να φαίνονται και οι ενδιάμεσοι υπολογισμοί (Στήλη Ε)
with st.expander("Δείτε την ανάλυση των υπολογισμών"):
    st.write(f"Βασικός Μισθός: {basic_salary:.2f} €")
    st.write(f"Σύνολο Κρατήσεων: {total_gross - net_salary:.2f} €")
