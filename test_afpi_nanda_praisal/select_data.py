import sqlite3
import pandas as pd

# Koneksi ke database
conn = sqlite3.connect('test-afpi.db')

# mendapatkan Nilai TRX
df = pd.read_sql("""
    SELECT 
        t.bulan,
        trx,
        npp,
        ticket_size
    FROM TRX t
    JOIN NPP n on n.bulan = t.bulan
    JOIN ticket_size ts on n.bulan = ts.bulan
    """, conn)
print(df)

conn.close() #close connection