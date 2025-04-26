import sqlite3
import pandas as pd

# Koneksi ke database dan load data TRX & NPP
conn = sqlite3.connect('test-afpi.db')
trx_df = pd.read_sql("SELECT bulan, trx FROM TRX", conn)
npp_df = pd.read_sql("SELECT bulan, npp FROM NPP", conn)
conn.close()

# Merge berdasarkan bulan
df = pd.merge(trx_df, npp_df, on='bulan')

# Validasi Rules
df['trx_valid'] = df['trx'].diff() > 0         # Rule 1: TRX H > TRX H-1
df['npp_valid'] = df['npp'].diff() >= 0        # Rule 2: NPP H >= NPP H-1
# Set baris pertama sebagai True karena tidak ada pembanding
df.loc[df.index[0], 'trx_valid'] = True
df.loc[df.index[0], 'npp_valid'] = True

# Output hasil validasi
print("Hasil Validasi:")
print(df[['bulan', 'trx', 'trx_valid', 'npp', 'npp_valid']])

# Cek data TRX yang tidak valid
invalid_trx = df[df['trx_valid'] == False]
if not invalid_trx.empty:
    print("\n TRX turun pada bulan:")
    print(invalid_trx[['bulan', 'trx']])
else:
    print("\n Semua TRX valid (selalu naik)")

# Cek data NPP yang tidak valid
invalid_npp = df[df['npp_valid'] == False]
if not invalid_npp.empty:
    print("\n NPP turun pada bulan:")
    print(invalid_npp[['bulan', 'npp']])
else:
    print("\n Semua NPP valid (tidak turun)")
