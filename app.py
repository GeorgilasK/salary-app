import streamlit as st

st.set_page_config(page_title="Υπολογιστής Μισθού", layout="centered")

st.title("💰 Υπολογισμός Μισθοδοσίας")

# --- ΣΤΗΛΗ D: ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ---

# D5: Μικτό Dropdown (Γράμματα και Αριθμοί μαζί)
d5_label = "Κατηγορία / Βαθμός (D5)" 
# Φτιάχνουμε τη λίστα: Α, Β, Γ, Δ και μετά 1 έως 23
d5_options = ["Α", "Β", "Γ", "Δ"] + [str(i) for i in range(1, 24)]
d5_val = st.selectbox(d5_label, options=d5_options)

# D6: Προϋπηρεσία (Απλός αριθμός)
d6_val = st.number_input("Έτη Προϋπηρεσίας (D6)", min_value=0, value=0)

# D7: Το άλλο Dropdown (Εδώ βάλε ό,τι επιλογές έχει το δικό σου D7)
# Αν π.χ. το D7 έχει ΝΑΙ/ΟΧΙ, το βάζουμε έτσι:
d7_label = "Άλλη Παράμετρος (D7)"
d7_val = st.selectbox(d7_label, options=["Επιλογή 1", "Επιλογή 2", "Επιλογή 3"])

# D9: Χειροκίνητη εισαγωγή
d9_val = st.number_input("Ειδική Παράμετρος (D9)", min_value=0.0, value=0.0)

# Επιδόματα
d10_val = st.number_input("Επίδομα Θέσης (D10)", min_value=0.0, value=0.0)
d11_val = st.number_input("Ανθυγιεινό (D11)", min_value=0.0, value=0.0)
d12_val = st.number_input("Παραμεθόριος (D12)", min_value=0.0, value=0.0)

st.markdown("---")

# --- ΥΠΟΛΟΓΙΣΜΟΙ (ΠΡΟΣΟΧΗ: Εδώ πρέπει να μπουν οι πράξεις σου) ---

# Παράδειγμα: Αν το D5 είναι "Α", ο βασικός είναι 1200, αν είναι "1" είναι 800 κλπ.
# Αυτό είναι απλώς ένα παράδειγμα για να δεις πώς λειτουργεί:
if d5_val in ["Α", "Β", "Γ", "Δ"]:
    base = 1100
else:
    base = 700 + (int(d5_val) * 10)

final_result = base + d10_val + d11_val + d12_val

# --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΟΣ ---
st.subheader("Αποτέλεσμα (D43)")
st.metric(label="Καθαρό Πληρωτέο", value=f"{final_result:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

st.info("💡 Οι αλλαγές εφαρμόζονται αμέσως μόλις επιλέξετε νέα τιμή.")
