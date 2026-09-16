import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Update Recipe 144: Sambal Ijo Padang
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 144")
g_144 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_144,))
clean_ings_144 = [
    ("Cabai Hijau Besar & Keriting", "250", "gr", "Rebus sebentar dengan sedikit garam"),
    ("Cabai Rawit Hijau", "50", "gr", "Untuk rasa pedas mantap"),
    ("Bawang Merah", "8-10", "siung", "Goreng/kukus bersama cabai"),
    ("Tomat Hijau", "3", "buah", "Memberi rasa asam segar"),
    ("Daun Jeruk Purut", "4", "lembar", "Sobek-sobek untuk aroma harum"),
    ("Minyak Kelapa / Minyak Goreng Panas", "4-5", "sdm", "Kunci sambal ijo berkilau dan tidak hitam"),
    ("Garam, Gula, Kaldu Jamur", "secukupnya", "", "")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_144):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_144, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 144")
clean_steps_144 = [
    (1, "Rebus Singkat Cabai & Bawang", "Didihkan air dengan sedikit garam (garam membantu menjaga warna hijau segar). Masukkan cabai hijau, cabai rawit, tomat hijau, dan bawang merah. Rebus sebentar selama 3-5 menit saja, angkat dan tiriskan segera.", 240),
    (2, "Ulek Kasar", "Ulek kasar cabai, tomat, dan bawang merah yang sudah direbus (jangan terlalu halus/blender halus agar tekstur sambal ijo autentik Padang tetap terasa).", 0),
    (3, "Tumis Bumbu & Daun Jeruk", "Panaskan 4-5 sdm minyak goreng. Tumis sambal ijo ulek bersama sobekan daun jeruk di atas api kecil-sedang. Bumbui garam, gula, dan kaldu jamur secukupnya.", 180),
    (4, "Masak hingga Tanak", "Masak hingga minyak keluar dan sambal matang tanak (tidak bau langu). Angkat dan sajikan bersama ayam/bebek goreng atau rendang!", 0)
]
for st in clean_steps_144:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (144, st[0], st[1], st[2], st[3]))

# 2. Update Recipe 120: Daging Sapi Berselimut
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 120")
g_120 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_120,))
clean_ings_120 = [
    ("Daging Sapi (Has Dalam / Sukiyaki Cut)", "300", "gr", "Iris tipis melebar"),
    ("Bawang Putih (Cincang halus)", "3", "siung", "Bumbu marinasi"),
    ("Kecap Asin & Minyak Wijen", "1", "sdm", ""),
    ("Lada Bubuk & Kaldu Bubuk", "1/2", "sdt", ""),
    ("Telur Ayam", "2", "butir", "Kocok lepas untuk lapisan"),
    ("Tepung Terigu & Maizena", "5", "sdm", "Campuran pelapis krispi"),
    ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_120):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_120, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 120")
clean_steps_120 = [
    (1, "Marinasi Irisan Daging", "Campurkan irisan tipis daging sapi dengan bawang putih cincang, kecap asin, minyak wijen, lada bubuk, dan kaldu. Diamkan 15 menit agar bumbu meresap.", 0),
    (2, "Balur Tepung & Telur", "Gulingkan irisan daging ke dalam tepung terigu-maizena kering, lalu celupkan ke kocokan telur hingga terbungkus rata.", 0),
    (3, "Goreng Renyah", "Goreng dalam minyak panas sedang selama 3-4 menit hingga lapisan telur dan tepung mengembang renyah keemasan dan daging matang empuk.", 240),
    (4, "Sajikan", "Angkat dan tiriskan di atas cooling rack. Nikmati selagi panas dengan cocolan saus sambal atau saus mayones!", 0)
]
for st in clean_steps_120:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (120, st[0], st[1], st[2], st[3]))

# 3. Update Recipe 46: Bakso Sapi Low Carb
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 46")
g_46 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_46,))
clean_ings_46 = [
    ("Daging Sapi Giling Segar (Dingin)", "500", "gr", "Pilih yang minim lemak"),
    ("Putih Telur", "2", "butir", "Pengganti tepung untuk mengikat adonan"),
    ("Batu Es Serut", "100", "gr", "Menjaga suhu adonan tetap dingin"),
    ("Bawang Putih Goreng", "2", "sdm", ""),
    ("Bawang Merah Goreng", "2", "sdm", ""),
    ("Baking Powder", "1/2", "sdt", "Membuat tekstur bakso mekar kenyal"),
    ("Garam Kasar / Garam Dapur", "1.5", "sdm", "Penting untuk ekstraksi protein"),
    ("Lada Bubuk & Kaldu Jamur", "1", "sdt", "")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_46):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_46, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 46")
clean_steps_46 = [
    (1, "Giling Daging & Garam", "Masukkan daging sapi dingin ke food processor bersama garam. Giling selama 2-3 menit hingga serat protein pecah dan adonan lengket elastis.", 180),
    (2, "Emulsikan dengan Putih Telur & Es", "Tambahkan es serut, putih telur, bawang putih goreng, bawang merah goreng, lada, kaldu jamur, dan baking powder. Giling hingga menjadi pasta adonan bakso yang halus dan mengkilap.", 120),
    (3, "Bentuk Bola Bakso", "Rebus air dalam panci hingga panas (jangan mendidih bergolak, suhu ±80°C). Matikan api kompor sementara. Bentuk bola bakso dengan genggaman tangan dan sendok, cemplungkan ke dalam air panas hingga mengapung.", 0),
    (4, "Rebus Matang & Tiriskan", "Nyalakan kembali api kecil kompor, masak bakso selama 10-15 menit hingga matang sempurna sampai ke bagian dalam. Angkat dan celupkan ke air es agar tekstur bakso semakin kenyal membal!", 600)
]
for st in clean_steps_46:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (46, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("All recipes rigorously sanitized with clean, pure culinary data!")
