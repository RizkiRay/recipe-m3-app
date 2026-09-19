import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "famichiki-crispy-juicy-japan-chefbintang",
    "title": "Famichiki (Ayam Goreng Crispy Juicy ala FamilyMart Jepang)",
    "chef": "Chef Bintang Bagaskara (@_rasabintang)",
    "description": "Resep autentik Famichiki khas FamilyMart Jepang dengan paha ayam berkulit juicy, baluran potato starch rempah, teknik flash fry 90 detik, dan finishing air fryer 140°C untuk tekstur luar super garing dan daging dalam tetap juicy melimpah.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DWgbLCOkoGC/",
    "servings": "2-3 Porsi (4 Potong)",
    "prep_time": "15 menit (Marinasi 2 jam)",
    "cook_time": "12 menit",
    "calories": "Tinggi Protein / Renyah Gurih Juicy",
    "groups": [
        ("Bahan Utama & Marinasi Basah (Wet Marinade)", [
            ("Paha Ayam Fillet Berkulit", "500", "gr", "Pipihkan melebar dengan rolling pin"),
            ("Bawang Putih", "1", "siung", "Parut halus"),
            ("Garlic Powder (Bawang Putih Bubuk)", "1", "gr", ""),
            ("Garam", "2", "gr", ""),
            ("Gula Pasir", "3", "gr", ""),
            ("MSG / Penyedap Rasa", "1", "gr", ""),
            ("Kecap Asin (Soy Sauce)", "5", "gr", ""),
            ("Cuka Beras (Rice Vinegar)", "1", "gr", ""),
            ("Baking Soda", "1", "gr", ""),
            ("Citric Acid (Asam Sitrat)", "1", "gr", "Opsional penyeimbang rasa"),
            ("Air Bersih", "52", "ml", "Air suhu dingin"),
            ("Potato Starch (Pati Kentang / Maizena)", "20", "gr", "Pengikat kelembapan daging"),
            ("Tepung Terigu Protein Sedang", "15", "gr", "")
        ]),
        ("Bahan Tepung Kering Coating (Crispy Dry Mix)", [
            ("Potato Starch (Pati Kentang / Maizena)", "92", "gr", "Bahan utama renyah remah"),
            ("Tepung Roti (Breadcrumbs)", "2", "gr", "Blender halus bersama tepung"),
            ("Susu Bubuk", "1", "gr", "Aroma gurih creamy"),
            ("Garam", "6", "gr", ""),
            ("Gula Pasir", "2", "gr", ""),
            ("MSG / Penyedap", "3", "gr", ""),
            ("Baking Powder", "2", "gr", ""),
            ("Lada Hitam (Black Pepper)", "1", "gr", "Giling halus"),
            ("Paprika Powder", "1", "gr", ""),
            ("Garlic Powder", "1", "gr", "")
        ]),
        ("Bahan Cairan Pembentuk Tekstur Flake (Flake Liquid)", [
            ("Putih Telur", "8", "gr", "Kocok lepas"),
            ("Minyak Goreng", "1", "gr", ""),
            ("Air Bersih", "9", "ml", "")
        ])
    ],
    "steps": [
        (1, "Pipihkan Daging Paha Ayam", "Letakkan fillet paha ayam berkulit di dalam plastik bening atau di antara baking paper. Pukul-pukul perlahan dengan rolling pin hingga ketebalannya rata dan melebar.", 120),
        (2, "Campur & Marinasi Basah", "Campurkan garam, gula, MSG, garlic powder, parutan bawang putih, kecap asin, cuka beras, baking soda, citric acid, air dingin, potato starch, dan tepung terigu ke dalam wadah. Lumurkan ke potongan ayam hingga merata, lalu simpan di kulkas minimal 2 jam.", 7200),
        (3, "Blender Tepung Coating Kering", "Masukkan potato starch, tepung roti, susu bubuk, garam, gula, MSG, baking powder, lada hitam, paprika powder, dan garlic powder ke dalam blender. Blender hingga seluruh bahan rempah dan tepung roti halus tercampur rata.", 60),
        (4, "Buat Serpihan Gumpalan Flake", "Di mangkuk kecil, kocok putih telur bersama 1 gr minyak dan 9 ml air. Percikkan cairan telur ini sedikit demi sedikit ke mangkuk tepung coating, lalu aduk cepat dengan jari/garpu agar terbentuk gumpalan butiran renyah (flaky crumbs).", 60),
        (5, "Balur Ayam dengan Tepung Coating", "Ambil potongan paha ayam yang telah dimarinasi, balurkan ke dalam campuran tepung coating hingga seluruh permukaan daging dan kulit tertutup rata.", 120),
        (6, "Goreng Cepat (Flash Fry 90 Detik)", "Panaskan minyak goreng yang cukup banyak hingga suhu 175°C. Masukkan ayam dan goreng kilat selama 90 detik hingga kulit tepung set kokoh dan berwarna kuning keemasan. Angkat dan tiriskan.", 90),
        (7, "Panggang Air Fryer (Kunci Kerenyahan & Juicy)", "Tata ayam di dalam keranjang air fryer. Panggang pada suhu 140°C selama 10 menit agar bagian dalam daging matang empuk sempurna dan minyak berlebih keluar sambil mengunci kerenyahan kulit luar.", 600),
        (8, "Sajikan Hangat Famichiki", "Keluarkan Famichiki dari air fryer, diamkan 1 menit agar sari daging terkunci, lalu sajikan hangat selagi renyah garing dan juicy.", 0)
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
