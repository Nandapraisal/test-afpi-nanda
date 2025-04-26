import sqlite3
import pandas as pd

# Koneksi ke database
conn = sqlite3.connect('test-afpi.db')
cursor = conn.cursor()

# Buat view ticket_size
cursor.execute("DROP VIEW IF EXISTS ticket_size")
cursor.execute("""
CREATE VIEW IF NOT EXISTS ticket_size AS
    SELECT 
        t.id, 
        t.bulan, 
        CAST(n.npp AS FLOAT) / NULLIF(CAST(t.trx AS FLOAT), 0) AS ticket_size
    FROM TRX t 
    JOIN NPP n ON t.bulan = n.bulan;    
""")
conn.commit()

# Ambil data dari view ticket_size
df_ticket = pd.read_sql("""SELECT 
        t.id, 
        t.bulan, 
        ROUND(CAST(n.npp AS FLOAT) / CAST(t.trx AS FLOAT), 6) AS ticket_size 
    FROM TRX t 
    JOIN NPP n ON t.bulan = n.bulan   """, conn)

df_ticket_dari_view = pd.read_sql("""SELECT 
      *
    FROM ticket_size 
     """, conn)
conn.close()

# Tampilkan hasil
print("View: ticket_size")
print(df_ticket)
print(df_ticket_dari_view)

