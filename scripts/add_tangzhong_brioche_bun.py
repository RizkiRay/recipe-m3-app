import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "tangzhong-brioche-burger-bun-ryannehamdali",
    "title": "Brioche Burger Bun Tangzhong (Roti Burger Super Empuk Fluffy Buttery)",
    "chef": "Anne (@ryannehamdali)",
    "description": "Roti burger brioche homemade super lembut, fluffy, dan wangi mentega tanpa pengawet. Menggunakan metode Tangzhong (water roux) agar tekstur roti tetap empuk moist berhari-hari dan kokoh menahan isian burger daging juicy.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DaHVfkkJMlD/",
    "servings": "6-8 Buah Bun",
    "prep_time": "30 menit (Proofing 1.5 jam)",
    "cook_time": "20 menit",
    "calories": "Fluffy Empuk / Buttery Lembut",
    "groups": [
        ("Bahan Tangzhong (Water Roux)", [
            ("Air Bersih", "100", "ml", "Air suhu ruang"),
            ("Tepung Terigu Protein Tinggi", "20", "gr", "Campur rata sebelum dimasak")
        ]),
        ("Bahan Kering Roti (Dry Dough)", [
            ("Tepung Terigu Protein Tinggi", "300", "gr", "Ayak halus"),
            ("Gula Pasir", "30", "gr", ""),
            ("Ragi Instan (Yeast)", "7", "gr", "Pastikan aktif")
        ]),
        ("Bahan Basah & Lemak (Wet & Fat)", [
            ("Telur Ayam", "1", "butir", "Suhu dingin"),
            ("Kuning Telur", "1", "butir", "Suhu dingin"),
            ("Susu Cair Full Cream Dingin", "40", "ml", "Kocok rata bersama telur"),
            ("Unsalted Butter (Mentega Tawar)", "55", "gr", "Suhu ruang lunak"),
            ("Garam", "8", "gr", "")
        ]),
        ("Bahan Olesan (Egg Wash) & Taburan", [
            ("Kuning Telur", "1", "butir", "Kocok lepas"),
            ("Susu Cair", "1", "sdm", "Campur ke kuning telur"),
            ("Biji Wijen Putih & Hitam (Sesame Seeds)", "1", "sdm", "Taburan atas roti")
        ])
    ],
    "steps": [
        (1, "Masak Pasta Tangzhong", "Campurkan 100 ml air dan 20 gr tepung terigu di panci kecil. Masak di atas api kecil sambil diaduk terus hingga mengental membentuk pasta halus (water roux). Angkat dan dinginkan hingga mencapai suhu ruang.", 180),
        (2, "Mixer Adonan Awal", "Masukkan 300 gr tepung terigu protein tinggi, 30 gr gula pasir, dan 7 gr ragi instan ke mangkuk standing mixer. Tuangkan campuran 1 butir telur utuh, 1 kuning telur, dan 40 ml susu cair dingin. Uleni/mixer dengan kecepatan rendah hingga adonan menggumpal dan setengah kalis.", 300),
        (3, "Tambahkan Tangzhong, Butter & Garam", "Masukkan pasta Tangzhong yang sudah dingin, 55 gr unsalted butter, dan 8 gr garam. Mixer kembali dengan kecepatan sedang selama 10-12 menit hingga adonan kalis elastis sempurna (lulus windowpane test: tidak mudah robek saat direntangkan tipis transparan).", 720),
        (4, "Istirahatkan Adonan (First Proofing)", "Bulatkan adonan menjadi bola halus, tutup wadah dengan kain lembap atau plastic wrap. Istirahatkan selama 30-45 menit hingga volume adonan mengembang 2 kali lipat.", 2400),
        (5, "Kempiskan, Timbang & Rounding Rapi", "Kempiskan adonan untuk membuang gas udara. Bagi dan timbang adonan masing-masing 70 gr (atau 80-100 gr untuk burger ukuran jumbo). Lakukan rounding (memutar dan mengunci adonan di meja kerja) hingga permukaannya mulus licin tanpa kerutan.", 300),
        (6, "Proofing Akhir di Loyang (Second Proofing)", "Tata bulatan adonan di atas loyang yang telah dialasi baking paper dengan memberi jarak. Tutup dan diamkan selama 45-60 menit hingga mengembang ringan, puffy, dan membal saat disentuh perlahan.", 3600),
        (7, "Oles Egg Wash & Panggang Oven 180°C", "Olesi perlahan permukaan bun dengan campuran kuning telur dan susu cair. Taburi biji wijen putih dan hitam. Panggang di oven suhu 180°C selama 18-20 menit hingga permukaan roti berwarna cokelat keemasan (golden brown).", 1200),
        (8, "Panggang Belah Bun untuk Burger", "Keluarkan bun dari oven, olesi sedikit butter selagi panas agar mengilap. Saat akan disajikan untuk burger, belah dua lalu panggang sisi dalam bun di atas wajan dengan sedikit mentega hingga renyah keemasan.", 120)
    ]
}

cursor.execute("SELECT id FROM recipes WHERE slug = ?", (recipe_data['slug'],))
row = cursor.fetchone()
if row:
    recipe_id = row[0]
    cursor.execute("DELETE FROM ingredients WHERE group_id IN (SELECT id FROM ingredient_groups WHERE recipe_id = ?)", (recipe_id,))
    cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("""
    UPDATE recipes SET title = ?, chef = ?, description = ?, youtube_id = ?, media_url = ?, servings = ?, prep_time = ?, cook_time = ?, calories = ?
    WHERE id = ?
    """, (
        recipe_data['title'], recipe_data['chef'], recipe_data['description'],
        recipe_data['youtube_id'], recipe_data['media_url'], recipe_data['servings'],
        recipe_data['prep_time'], recipe_data['cook_time'], recipe_data['calories'], recipe_id
    ))
    r_id = recipe_id
    print(f"Updating existing recipe id: {r_id}")
else:
    cursor.execute("""
    INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recipe_data['slug'], recipe_data['title'], recipe_data['chef'], recipe_data['description'],
        recipe_data['youtube_id'], recipe_data['media_url'], recipe_data['servings'],
        recipe_data['prep_time'], recipe_data['cook_time'], recipe_data['calories']
    ))
    r_id = cursor.lastrowid
    print(f"Inserted new recipe id: {r_id}")

for g_idx, (g_name, items) in enumerate(recipe_data['groups']):
    cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (r_id, g_name, g_idx))
    g_id = cursor.lastrowid
    for i_idx, it in enumerate(items):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))

for st in recipe_data['steps']:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (r_id, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print(f"Successfully saved recipe {recipe_data['slug']} with ID {r_id}!")
