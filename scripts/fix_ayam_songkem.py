import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Properly rewrite Recipe 364: Ayam Songkem Khas Madura by Devy Anastasia
cursor.execute('''
UPDATE recipes 
SET title = 'Ayam Songkem Kukus Khas Madura Pedas Medok',
    description = 'Ayam kukus khas Madura yang dibalut sambal cabai bawang medok dan dibungkus daun pisang harum, sehat tanpa minyak/goreng.'
WHERE id = 364
''')

# Delete old groups and ingredients
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 364")
old_groups = [r[0] for r in cursor.fetchall()]
for gid in old_groups:
    cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (gid,))
cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id = 364")

# Insert 2 clean structured groups: Bahan Ayam & Bahan Sambal Ulek
cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (364, 'Bahan Utama Ayam', 0)")
g_ayam = cursor.lastrowid

ayam_ings = [
    ("Paha Ayam Fillet", "500", "gr", "Potong sesuai selera"),
    ("Saus Tiram", "2", "sdm", "Untuk marinasi ayam"),
    ("Batang Sereh", "1", "batang", "Memarkan"),
    ("Daun Salam", "2", "lembar", ""),
    ("Daun Pisang Segar", "secukupnya", "lembar", "Untuk alas & penutup kukusan")
]
for idx, (it, amt, un, nt) in enumerate(ayam_ings):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_ayam, it, amt, un, nt, idx))

cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (364, 'Bahan Sambal Songkem Medok', 1)")
g_sambal = cursor.lastrowid

sambal_ings = [
    ("Bawang Putih", "8", "siung", ""),
    ("Bawang Merah", "8", "buah", ""),
    ("Cabai Merah Keriting", "7", "buah", ""),
    ("Cabai Merah Besar", "2", "buah", "Memberi warna merah cerah"),
    ("Cabai Rawit Merah", "20", "buah", "Tingkat kepedasan khas Songkem"),
    ("Terasi Bakar / Matang", "1", "buah (±1 sdt)", "Aroma sedap"),
    ("Garam & Penyedap Rasa", "secukupnya", "", "")
]
for idx, (it, amt, un, nt) in enumerate(sambal_ings):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_sambal, it, amt, un, nt, idx))

# Clean instructions
cursor.execute("DELETE FROM instructions WHERE recipe_id = 364")
steps_364 = [
    (1, "Marinasi Ayam", "Potong paha ayam fillet sesuai selera. Campurkan dengan 2 sdm saus tiram, aduk rata dan diamkan selama 10 menit agar meresap.", 0),
    (2, "Haluskan Bumbu Sambal Songkem", "Masukkan bawang putih, bawang merah, cabai merah keriting, cabai merah besar, cabai rawit merah, terasi, garam, dan penyedap ke dalam chopper/blender. Haluskan secara kasar (pulse).", 0),
    (3, "Balur Ayam dengan Sambal", "Campurkan bumbu sambal cincang kasar dengan paha ayam marinasi hingga seluruh permukaan daging ayam terlapisi bumbu tebal.", 0),
    (4, "Bungkus Daun Pisang", "Siapkan wadah/mangkuk tahan panas yang dialasi selembar daun pisang. Masukkan ayam berbumbu, selipkan 1 batang sereh memar dan 2 lembar daun salam di atasnya, lalu tutup rapat kembali dengan daun pisang.", 0),
    (5, "Kukus hingga Matang Empuk", "Panaskan kukusan. Kukus ayam songkem selama 25–30 menit dengan api sedang hingga daging ayam matang empuk, bumbu meresap, dan keluar sari kaldu gurih aromatik.", 1500),
    (6, "Sajikan", "Buka bungkus daun pisang selagi panas. Sajikan ayam songkem bersama nasi hangat atau nasi shirataki dan siramkan kuah sambalnya!", 0)
]
for st in steps_364:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (364, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("Recipe 364 perfectly corrected to Ayam Songkem with exact numbers and clear separated ingredient groups!")
