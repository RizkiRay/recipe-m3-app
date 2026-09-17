import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Update Recipe 542: Ayam Songkem Madura by Firhan MCI6
cursor.execute('''
UPDATE recipes 
SET title = 'Ayam Songkem Madura Pedas Gurih',
    description = 'Resep Ayam Songkem khas Madura ala Chef @firhanmci6: ayam utuh dibalut sambal cabai bawang minyak panas dan dikukus berbungkus daun pisang.'
WHERE id = 542
''')

# Delete old groups & ingredients
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 542")
g_ids = [r[0] for r in cursor.fetchall()]
for gid in g_ids:
    cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (gid,))
cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id = 542")

# Group 1: Bahan Marinasi Ayam
cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (542, 'Bahan Marinasi Ayam', 0)")
g1 = cursor.lastrowid
g1_items = [
    ("Ayam Pejantan Besar (Belah bekakak)", "1", "ekor", "Cuci bersih & tiriskan"),
    ("Saus Tiram", "2", "sdm", ""),
    ("Minyak Wijen", "2", "sdm", "Pengharum alami"),
    ("Tepung Tapioka", "4", "sdm", "Mengunci kelembapan sari ayam"),
    ("Garam", "1.5", "sdt", ""),
    ("Lada Bubuk", "1", "sdt", "")
]
for idx, (it, amt, un, nt) in enumerate(g1_items):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g1, it, amt, un, nt, idx))

# Group 2: Bahan Sambal Songkem
cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (542, 'Bahan Sambal Songkem', 1)")
g2 = cursor.lastrowid
g2_items = [
    ("Cabai Merah Keriting", "35", "buah", "Cincang kasar"),
    ("Cabai Rawit Merah", "15", "buah", "Pedas nampol"),
    ("Bawang Merah", "15", "butir", ""),
    ("Bawang Putih", "10", "butir", ""),
    ("Daun Bawang (Iris)", "2", "batang", ""),
    ("Terasi Bakar", "2", "sdt", "Aroma sedap khas Madura"),
    ("Minyak Panas Mendidih", "80", "ml", "Untuk menyiram bumbu aromatik"),
    ("Kaldu Ayam Bubuk", "2", "sdt", ""),
    ("Gula Pasir", "3", "sdt", ""),
    ("Penyedap Rasa / MSG", "2", "sdt", ""),
    ("Garam", "1", "sdt", "")
]
for idx, (it, amt, un, nt) in enumerate(g2_items):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g2, it, amt, un, nt, idx))

# Group 3: Bahan Pelengkap Bungkus
cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (542, 'Bahan Pelengkap Bungkus', 2)")
g3 = cursor.lastrowid
g3_items = [
    ("Daun Pisang Lebar (Layu di atas api)", "secukupnya", "lembar", "Untuk membungkus rapat"),
    ("Batang Sereh (Memarkan)", "2", "batang", ""),
    ("Daun Salam", "6", "lembar", "")
]
for idx, (it, amt, un, nt) in enumerate(g3_items):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g3, it, amt, un, nt, idx))

# Steps for Firhan's recipe
cursor.execute("DELETE FROM instructions WHERE recipe_id = 542")
steps_542 = [
    (1, "Marinasi Ayam Pejantan", "Lumuri 1 ekor ayam pejantan dengan saus tiram, minyak wijen, garam, lada bubuk, dan tepung tapioka. Balurkan merata ke seluruh badan dan rongga ayam, lalu diamkan 15 menit.", 0),
    (2, "Cincang Bumbu Sambal & Siram Minyak Panas", "Cincang kasar bawang merah, bawang putih, cabai merah keriting, cabai rawit, dan daun bawang di chopper. Pindahkan ke mangkuk, bumbui terasi, kaldu ayam bubuk, gula, garam, dan penyedap. Siram dengan 80 ml minyak panas mendidih, lalu aduk rata.", 0),
    (3, "Balur Ayam dengan Sambal Tebal", "Balurkan seluruh racikan sambal ke seluruh permukaan ayam hingga tertutup bumbu tebal dan meresap.", 0),
    (4, "Bungkus Rapat Daun Pisang", "Bentangkan daun pisang lebar. Taruh sereh memar dan daun salam di bagian dasar, letakkan ayam berbumbu di atasnya, lalu bungkus rapat dan semat kedua ujungnya dengan lidi/tusuk gigi.", 0),
    (5, "Kukus hingga Empuk Berkaldu", "Kukus ayam songkem selama 45–60 menit dengan api sedang hingga daging ayam pejantan empuk lembut dan mengeluarkan kaldu aromatik yang sedap.", 3000),
    (6, "Sajikan", "Buka bungkusan daun pisang selagi panas mengepul. Sajikan ayam songkem bersama nasi hangat dan siramkan kuah sambalnya!", 0)
]
for st in steps_542:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (542, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("Recipe 542 (Firhan MCI6 Ayam Songkem) perfectly structured and updated!")
