import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Fix Recipe 339: Pizza Telur & Daging Tanpa Tepung (@triananda.yb)
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 339")
g_339 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_339,))

clean_ings_339 = [
    ("Dada Ayam Giling / Daging Cincang", "250", "gr", "Bahan dasar adonan pizza"),
    ("Telur Ayam", "2", "butir", "Pengikat adonan"),
    ("Tomat Merah Segar (Rebus & kupas kulit)", "3", "buah", "Bahan dasar saus pizza"),
    ("Bawang Putih (Cincang halus)", "2", "siung", "Bumbu saus"),
    ("Keju Mozarella (Parut)", "75", "gr", "Topping lumer"),
    ("Oregano Kering", "1", "sdt", "Aroma khas pizza Italia"),
    ("Chili Flakes (Cabai bubuk kasar)", "1/2", "sdt", ""),
    ("Garam, Lada, Kaldu Sapi Bubuk", "secukupnya", "", "")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_339):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_339, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 339")
clean_steps_339 = [
    (1, "Buat Saus Tomat Segar", "Rebus tomat yang sudah dikerat selama 5 menit, kupas kulitnya, lalu blender bersama bawang putih cincang, oregano, chili flakes, garam, dan kaldu sapi hingga halus kental.", 300),
    (2, "Campur Adonan Dasar Pizza", "Campurkan daging ayam giling dengan telur, garam, lada, dan oregano. Aduk rata hingga membentuk adonan padat kalis.", 0),
    (3, "Panggang Base Pizza", "Ratakan adonan daging di atas pan/loyang yang dilapisi baking paper hingga berbentuk bundar pipih. Panggang dalam oven/airfryer suhu 200°C selama 20 menit hingga matang kokoh.", 1200),
    (4, "Beri Topping & Lelehkan Keju", "Keluarkan base pizza, olesi permukaan atasnya dengan saus tomat segar dan taburi parutan keju mozarella melimpah.", 0),
    (5, "Panggang Ulang & Sajikan", "Panggang kembali selama 5 menit dengan api atas hingga keju mozarella meleleh dan kecokelatan. Potong segitiga dan nikmati selagi hangat!", 300)
]
for st in clean_steps_339:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (339, st[0], st[1], st[2], st[3]))

# 2. Fix Recipe 352: BBQ Fried Chicken Wings (@jonatan.mci13)
cursor.execute("UPDATE recipes SET title = 'BBQ Fried Chicken Wings with Smoked Butter' WHERE id = 352")
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 352")
g_352 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_352,))

clean_ings_352 = [
    ("Sayap Ayam (Potong drumette & wingette)", "10-12", "potong (±500 gr)", "Cuci bersih"),
    ("Susu Cair Segar", "200", "ml", "Bahan buttermilk marinade"),
    ("Jeruk Lemon (Ambil zest kulit & perasan airnya)", "1", "buah", "Campurkan ke susu agar mengental jadi buttermilk"),
    ("Bawang Putih Bubuk & Garam", "1", "sdm", "Bumbu marinasi"),
    ("Tepung Terigu & Tepung Beras", "150", "gr", "Campuran pelapis krispi"),
    ("Mentega (Butter) Berkualitas", "100", "gr", "Untuk smoked butter"),
    ("Saus Barbecue (BBQ Sauce)", "150", "ml", "Glaze saus sayap"),
    ("Minyak Goreng", "secukupnya", "", "Untuk deep-fry")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_352):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_352, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 352")
clean_steps_352 = [
    (1, "Buat Buttermilk Marinade", "Campurkan susu cair dengan perasan lemon, parutan kulit lemon (zest), bawang putih bubuk, dan garam. Aduk dan diamkan 5 menit hingga susu mengental menjadi buttermilk.", 0),
    (2, "Marinasi Sayap Ayam", "Rendam potongan sayap ayam ke dalam larutan buttermilk. Simpan di kulkas minimal 2 jam (atau semalaman) agar daging empuk juicy meresap.", 7200),
    (3, "Balur Tepung & Goreng Krispi", "Gulingkan sayap ayam basah ke campuran tepung kering, remas perlahan agar keriting. Goreng di minyak panas (170°C) selama 10-12 menit hingga matang keemasan dan renyah. Tiriskan.", 660),
    (4, "Buat Smoked Butter & Glaze BBQ", "Lelehkan butter, lalu beri asap arang panas di wadah tertutup selama 5 menit untuk aroma smoky. Campurkan smoked butter dengan saus BBQ.", 300),
    (5, "Tossing & Sajikan", "Masukkan sayap ayam goreng renyah ke mangkuk saus BBQ smoked butter. Aduk rata (toss) hingga seluruh sayap terbalut mengkilap dan sajikan hangat!", 0)
]
for st in clean_steps_352:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (352, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("Recipes 339 and 352 rigorously cleaned and updated!")
