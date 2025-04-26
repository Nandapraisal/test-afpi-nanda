import pandas as pd
from datetime import datetime
import sqlite3
import math

# Load data
excel_file = 'STATISTIK LPBBTI Desember 2024 (1) _ For Testing .xlsx'
trx_df = pd.read_excel(excel_file, sheet_name='16', header=None)
npp_df = pd.read_excel(excel_file, sheet_name='18', header=None)
bulan_row_trx = trx_df.iloc[1, 2:]  # Baris kedua, kolom ke-3 dan seterusnya
bulan_row_npp = npp_df.iloc[1, 2:]

def process_month_series(series):
    month_cols = []
    for val in series:
        if isinstance(val, datetime):
            month_cols.append(val.strftime('%b-%y'))
        elif isinstance(val, str):
            try:
                dt = datetime.strptime(val.strip(), '%b-%y')
                month_cols.append(dt.strftime('%b-%y'))
            except ValueError:
                try:
                    dt = datetime.strptime(val.strip(), '%b %y')
                    month_cols.append(dt.strftime('%b-%y'))
                except ValueError:
                    month_cols.append(val.strip())  # biarin string-nya aja
        else:
            month_cols.append(str(val))  # misal angka atau NaN
    return month_cols

# Process columns for both sheets
bulan_cols_trx = process_month_series(bulan_row_trx)
bulan_cols_npp = process_month_series(bulan_row_npp)

print("TRX Months:", bulan_cols_trx)
print("NPP Months:", bulan_cols_npp)

# Ambil sebanyak jumlah bulan yang berhasil dideteksi
trx_values = trx_df.iloc[43, 2:2+len(bulan_cols_trx)].tolist()
npp_values = npp_df.iloc[43, 2:2+len(bulan_cols_npp)].tolist()


print("TRX Amount:", trx_values)
print("NPP Amount:", npp_values)

# === STEP 3: CLEAN AND CONVERT DATA ===
def clean_number(value):
    """Convert value to integer dengan aturan pembulatan custom"""
    try:
        if isinstance(value, str):
            cleaned = value.replace('.', '').replace(',', '.').replace('–', '').replace('-', '').strip()
            num = float(cleaned)
        else:
            num = float(value)

        desimal = num - int(num)
        if desimal >= 0.5:
            return math.ceil(num)
        else:
            return math.floor(num)
    except:
        return 0

# Bersihkan data TRX dan NPP
trx_cleaned = [clean_number(val) for val in trx_values]
npp_cleaned = [clean_number(val) for val in npp_values]

# === STEP 4: CREATE DATAFRAMES ===
trx_df = pd.DataFrame({
    'id': range(1, len(bulan_cols_trx) + 1),
    'bulan': bulan_cols_trx,
    'trx': trx_cleaned
})

npp_df = pd.DataFrame({
    'id': range(1, len(bulan_cols_npp) + 1),
    'bulan': bulan_cols_npp,
    'npp': npp_cleaned
})

# === STEP 5: SAVE TO SQLITE ===
db_file = 'test-afpi.db'
conn = sqlite3.connect(db_file)

# Buat tabel TRX
conn.execute("""
CREATE TABLE IF NOT EXISTS TRX (
    id INTEGER PRIMARY KEY,
    bulan TEXT NOT NULL,
    trx INTEGER NOT NULL
)
""")

# Buat tabel NPP
conn.execute("""
CREATE TABLE IF NOT EXISTS NPP (
    id INTEGER PRIMARY KEY,
    bulan TEXT NOT NULL,
    npp INTEGER NOT NULL
)
""")

# Simpan data
trx_df.to_sql('TRX', conn, if_exists='replace', index=False)
npp_df.to_sql('NPP', conn, if_exists='replace', index=False)

conn.close()

print(f"✅ Data berhasil disimpan:")
print(f"- Database SQLite: {db_file} (tabel TRX)")
print(f"- Database SQLite: {db_file} (tabel NPP)")
print("\nPreview Data TRX:")
print(trx_df.to_string(index=False))
print("\nPreview Data NPP:")
print(npp_df.to_string(index=False))