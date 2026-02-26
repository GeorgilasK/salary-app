import streamlit as st

st.set_page_config(layout="wide", page_title="Payroll Professional v21")

# --- CSS: ΣΚΟΥΡΟ ΓΚΡΙ ΦΟΝΤΟ & ΛΕΥΚΑ ΓΡΑΜΜΑΤΑ ---
st.markdown("""
    <style>
    .stApp { background-color: #1e1e1e; }
    .excel-row {
        border: 1px solid #444;
        padding: 10px;
        margin-bottom: 5px;
        background-color: #2d2d2d;
        border-radius: 5px;
        display: flex;
        align-items: center;
    }
    /* Λευκά γράμματα παντού */
    span, div, p, label, h1, h2, h3 { color: #ffffff !important; }
    
    .col-b { width: 25%; font-weight: bold; }
    .col-d { width: 15%; }
    .col-e { width: 15%; font-weight: bold; color: #4ade80 !important; text-align: right; }
    .col-f { width: 20%; font-size: 0.85rem; color: #cccccc !important; }
    .col-g { width: 25%; font-size: 0.85rem; color: #aaaaaa !important; }

    /* Inputs: Μαύρο κείμενο μέσα σε λευκό/γκρι πεδίο για να φαίνεται τι γράφεις */
    input, .stSelectbox div div { color: #000000 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΕΔΟΜΕΝΑ ΠΙΝΑΚΩΝ (Ακριβή από Excel) ---
KLIMAKIA = {
    "1": 2234.94, "2": 2187.53, "3": 2087.69, "4": 1963.82, "5": 1892.43, "6": 1717.38, 
    "7": 1667.92, "8": 1570.34, "9": 1454.83, "10": 1424.81, "11": 1376.89, "12": 1350.16, 
    "13": 1321.14, "14": 1309.80, "15": 1299.21, "16": 1285.07, "17": 1275.99, "18": 1266.41, 
    "19": 1258.08, "20": 1224.28, "21": 1216.95, "22": 1202.63, "23": 11
