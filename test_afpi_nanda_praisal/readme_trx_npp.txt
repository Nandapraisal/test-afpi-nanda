# PENJELASAN SCRIPT: Ekstraksi & Penyimpanan Data Excel ke SQLite


==================================================
1. PERSIAPAN: LIBRARY YANG HARUS DIINSTAL, FILE PENDUKUNG
==================================================
Sebelum menjalankan script ini, pastikan Python telah menginstal library berikut:

 Library : pip install pandas openpyxl
 File    : "STATISTIK LPBBTI Desember 2024 (1) _ For Testing .xlsx", test-afpi.db, dashboard.html

Library `sqlite3` dan `math` adalah bawaan Python, jadi tidak perlu instalasi tambahan.



==================================================
2. TOTAL SCRIPT
==================================================
    1. get_data_excel.py : Fungsi utama mengambil data TRX dan NPP ke dalam database test-afpi.db
    2. ticket_size.py    : Fungsi membuat ticket_size ke dalam view "ticket_size"
    3. rules_validasi.py : Menghasilkan nilai validasi di setiap bulan
    4. table_check.py    : Menampilkan DETAIL struktur table/view dari database test-afpi.db
    5. select_data.py    : Menampilkan isi data untuk keperluan cek/validasi
    6. dashboard.html     : Menampilkan data hasil olahan dalam bentuk visual (web dashboard)



==================================================
3. FLOW
==================================================
Script berjalan sesuai urutan berikut:

1. Membaca file Excel mengambil data/valuenya:
   - Sheet '16' → data TRX
   - Sheet '18' → data NPP

2. Membersihkan nilai dan konversi ke integer:
   - Desimal >= 0.5 dibulatkan ke atas (ceil)
   - Desimal < 0.5 dibulatkan ke bawah (floor)

3. Menyimpan data ke SQLite:
   - Database: test-afpi.db
   - Tabel: TRX (id, bulan, trx), NPP (id, bulan, npp), view ticket_size(id, bulan, ticket_size)

3. Dashboard:
   - File `dashboard.html` membaca data dari database data dari database yang diupload sebelum dibuka
   - Menampilkan visualisasi data TRX, NPP, dan ticket_size
   - Dipakai untuk monitoring dan presentasi



==================================================
4. STRUKTUR SCRIPT
==================================================

🔹 get_data_excel.py
- Membaca data Excel sheet 16 dan 18
- Ekstrak nama bulan dan nilai dari baris tertentu
- Bersihkan & ubah format angka → integer
- Simpan ke SQLite dalam tabel TRX dan NPP

🔹 ticket_size.py
- Hitung rasio NPP / TRX
- Simpan dalam view SQLite bernama ticket_size
- Format: id, bulan, ticket_size

🔹 rules_validasi.py
- Hitung nilai validasi dari data TRX dan NPP tiap bulan
- Output untuk kebutuhan validasi / monitoring kualitas data

🔹 table_check.py
- Menampilkan semua tabel dan view
- Info: nama tabel/view, struktur kolom, sumber view

🔹 select_data.py
- Menampilkan isi dari tabel dan view di database
- Dipakai untuk pengecekan data manual

🔹 dashboard.html
- File HTML statis berisi grafik dan tabel
- Menampilkan data dari database via upload database
- Didesain untuk kemudahan monitoring dan visualisasi



==================================================
5. OUTPUT
==================================================

Script akan memberikan hasil berupa:

- Daftar bulan yang diproses
- Nilai TRX & NPP (mentah & bersih)
- Tampilan preview DataFrame
- Konfirmasi penyimpanan ke database
- Tampilan visualisasi dalam dashboard.html (grafik, tabel)



==================================================
6. FILE OUTPUT
==================================================

Database: test-afpi.db

Tabel:
- TRX: id, bulan, trx
- NPP: id, bulan, npp

View:
- ticket_size: id, bulan, ticket_size

Dashboard:
- dashboard.html: berisi tampilan web dari data yang telah diproses



==================================================
✅ Selesai! Data berhasil diproses
==================================================

