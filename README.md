# Feat Knowledge Acquisition / Explanation Facility AC

# Knowledge Acquisition 
*adalah fitur untuk menambah, mengedit, atau menghapus aturan (rules) baru melalui antarmuka.*

- Menampilkan semua aturan (rules) yang sudah ada.
- Menambah aturan baru dengan menentukan nama kerusakan, gejala-gejala yang berkaitan, dan solusi.
- Mengedit aturan yang sudah ada jika ada kesalahan atau pembaruan.
- Menghapus aturan yang sudah tidak relevan.
Aturan-aturan yang di edit pada fitur ini akan menjadi pengetahuan dasar sistem pakar untuk mendiagnosis masalah AC.

# Explanation Facility 
*sebagai penampilkan penjelasan mengapa sistem menanyakan gejala tertentu (WHY) dan bagaimana hasil diagnosis diperoleh (HOW).*

WHY – Mengapa gejala ini ditanyakan
Menjelaskan alasan sistem menanyakan gejala tertentu,
Contoh : Gejala 'ac tidak dingin' digunakan untuk mendeteksi kemungkinan 'freon habis atau kompresor rusak'.

HOW – Bagaimana hasil diagnosis diperoleh
Menjelaskan bagaimana sistem sampai pada hasil diagnosis,
Contoh : Diagnosis 'freon habis atau kompresor rusak.' diperoleh karena 'ac tidak dingin' dan Solusi yang disarankan: Periksa freon dan kompresor AC.

# 🔗 Hubungan Kedua Fitur
-> Knowledge Acquisition berfungsi sebagai tempat penyimpanan pengetahuan sekaligus menjadi antarmuka untuk edit knowledge base.Untuk Explanation Facility membaca data dari fitur tersebut untuk memberikan penjelasan( WHY dan HOW ). 

# 🚀 Cara Menjalankan Program
1 – Tanpa Database
- Jalankan knowledge_acquisition.py untuk menambah atau ubah aturan.
- Jalankan explanation_facility.py untuk bertanya “WHY” dan “HOW”.

2 – Dengan menggunakan Database atau file json internal
- Hubungkan koneksi ke dalam kedua file.
- Jalankan kedua modul — data akan otomatis tersimpan dan bisa digunakan secara bersama.

# 📚 Kesimpulan
Sistem pakar diagnosis AC ini terdiri dari dua fitur utama yang saling berkaitan. 
Knowledge Acquisition berfungsi sebagai antarmuka manajemen pengetahuan yang memungkinkan pengguna untuk menambah, mengedit, menampilkan, dan menghapus aturan diagnosis AC, termasuk nama kerusakan, gejala-gejala terkait, dan solusinya. Sementara itu, Explanation Facility berperan sebagai mekanisme transparansi sistem dengan menjelaskan alasan sistem menanyakan gejala tertentu (WHY) dan bagaimana proses diagnosa menghasilkan kesimpulan tertentu (HOW). 
Kedua fitur ini bekerja secara terintegrasi, di mana Knowledge Acquisition menyediakan basis pengetahuan yang kemudian dibaca oleh Explanation Facility untuk memberikan penjelasan kepada pengguna. 
Program dapat dijalankan secara mandiri tanpa database atau terintegrasi dengan database/file JSON untuk penyimpanan data yang persisten dan dapat diakses bersama oleh kedua modul.
