import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Specifically rewrite and sanitize Recipe 372 (Nori Gulung Udang)
cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = 372")
g_372 = cursor.fetchone()[0]
cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_372,))

clean_ings_372 = [
    ("Daging Udang Kupas Segar", "200", "gr", "Cincang halus / chopper"),
    ("Wortel Rebus (Cincang halus)", "2", "sdm", "Nutrisi sayur untuk anak"),
    ("Jagung Manis Rebus (Pipil)", "2", "sdm", "Memberi rasa manis alami"),
    ("Daun Bawang (Iris tipis)", "1", "batang", ""),
    ("Tepung Tapioka / Maizena", "1.5", "sdm", "Pengikat adonan kenyal"),
    ("Kaldu Jamur / Penyedap Rasa", "1/2", "sdt", ""),
    ("Minyak Wijen & Garam", "1/2", "sdt", "Pengharum adonan"),
    ("Lembaran Nori / Rumput Laut Panggang", "secukupnya", "lembar", "Gunting sesuai ukuran"),
    ("Minyak Goreng", "secukupnya", "sdm", "Untuk olesan pan teflon")
]
for idx, (it, amt, un, nt) in enumerate(clean_ings_372):
    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_372, it, amt, un, nt, idx))

cursor.execute("DELETE FROM instructions WHERE recipe_id = 372")
clean_steps_372 = [
    (1, "Haluskan Daging Udang", "Masukkan 200 gr udang kupas ke dalam chopper atau cincang halus dengan pisau hingga bertekstur pasta lengket.", 0),
    (2, "Campur Sayuran & Bumbu", "Campurkan pasta udang dengan wortel cincang, jagung manis pipil, daun bawang, tepung tapioka, kaldu jamur, garam, dan minyak wijen. Aduk rata hingga menjadi adonan kalis.", 0),
    (3, "Bungkus dengan Lembaran Nori", "Ambil selembar nori, ratakan adonan udang di atasnya, lalu gulung atau lipat rapat membentuk persegi panjang/silinder.", 0),
    (4, "Panggang di Pan Teflon", "Panaskan teflon anti-lengket dengan sedikit olesan minyak. Panggang nori udang di atas api kecil-sedang selama 3-4 menit tiap sisi hingga udang matang kemerahan dan nori krispi harum.", 360),
    (5, "Sajikan", "Angkat dan potong-potong sesuai gigitan anak. Sajikan hangat sebagai camilan sehat penambah nafsu makan si kecil!", 0)
]
for st in clean_steps_372:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (372, st[0], st[1], st[2], st[3]))

# 2. Comprehensive Global Purge across ALL recipes in DB for tools/kitchen equipment & intro fluff:
tools_and_fluff = [
    'Alat', 'alat:', 'Pisau', 'Spatula', 'Teflon', 'Chopper', 'Food processor', 
    'Garpu', 'Sendok', 'Mangkuk', 'Wajan', 'Panci', 'Bahan:', 'Bahan', 'bahan:', 
    'Seasoning', 'seasoning:', 'Bumbu:', 'bumbu:', 'Kalau si kecil', 'Nori udang renyah', 
    'camilan ini', 'bolak-balik', 'Snack Bocil', 'auto nambah'
]

for kw in tools_and_fluff:
    cursor.execute(f"DELETE FROM ingredients WHERE item LIKE '%{kw}%'")

# 3. Clean incomplete units / dangling symbols from items (e.g. "gr udang" -> "Udang kupas")
cursor.execute("SELECT id, item FROM ingredients")
for row in cursor.fetchall():
    i_id, item_text = row
    # Clean leading unit fragments like "gr ", "sdm ", "/2 ", "sdt "
    cleaned_item = re.sub(r'^(?:gr|sdm|sdt|kg|ml|buah|lembar|batang|butir|\/2|\/4|\d+)\s+', '', item_text, flags=re.IGNORECASE)
    cleaned_item = re.sub(r'^[•\-\*\s\(\)\/]+', '', cleaned_item).strip()
    if cleaned_item != item_text:
        cursor.execute("UPDATE ingredients SET item = ? WHERE id = ?", (cleaned_item, i_id))

conn.commit()
conn.close()
print("Purged all tool equipment, intro chatter, and cleaned item prefixes!")
