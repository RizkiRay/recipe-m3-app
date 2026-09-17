import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Update recipe 356 with complete Sambal Petis Madura ingredients & steps
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 356")
g_356 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_356,))

clean_ings_356 = [
    ("Petis Ikan / Petis Kupang Madura Asli", "3", "sdm", "Aroma gurih khas Madura"),
    ("Cabai Rawit Merah & Hijau", "15-20", "buah", "Sesuaikan tingkat kepedasan"),
    ("Bawang Putih", "4", "siung", "Goreng setengah matang"),
    ("Gula Pasir", "1", "sdt", "Penyeimbang rasa gurih petis"),
    ("Garam & Penyedap Rasa", "1/2", "sdt", ""),
    ("Air Hangat", "3-4", "sdm", "Untuk melarutkan petis"),
    ("Minyak Goreng Panas", "2", "sdm", "Disiramkan ke ulekan cabai")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_356):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_356, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 356")
clean_steps_356 = [
    (1, "Ulek Bawang & Cabai Rawit", "Ulek cabai rawit merah, cabai rawit hijau, dan bawang putih goreng bersama garam dan gula di cobek hingga setengah halus.", 0),
    (2, "Siram Minyak Panas", "Siram ulekan cabai bawang dengan 2 sdm minyak goreng panas mendidih agar aroma bawang dan pedas cabai keluar semerbak.", 0),
    (3, "Campurkan Petis Madura", "Tambahkan 3 sdm petis ikan Madura dan sedikit air hangat. Aduk dan ulek rata bersama sambal cabai hingga kekentalan sambal pas dan pekat mengkilap.", 120),
    (4, "Sajikan", "Sambal petis Madura siap disajikan sebagai cocolan tahu goreng panas, tempe, kerupuk, atau ceker!", 0)
]
for st in clean_steps_356:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (356, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("Recipe 356 updated with 100% complete culinary ingredients and steps!")
