import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "sutbul-korean-marinated-bbq-sauce",
    "title": "Saus Marinasi BBQ Daging ala Sutbul (Korean Sweet & Savory Marinade Sauce)",
    "chef": "Sutbul Modern Korean Dining (@sutbul.jkt)",
    "description": "Rahasia saus marinasi daging dan iga panggang BBQ ala resto Sutbul PIK. Perpaduan gurih manis sari buah apel, pir Korea, mirin, kecap asin, dan aromatik bawang yang direbus 40 menit lalu dikentalkan maizena.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DZ62y3lxNdo/",
    "servings": "4-6 Porsi Marinasi (1-2 kg Daging)",
    "prep_time": "15 menit",
    "cook_time": "40 menit",
    "calories": "Saus Marinasi Gurih Manis Alami",
    "groups": [
        ("Bahan Rebusan Kaldu Aromatik", [
            ("Air Bersih", "1.5", "liter", ""),
            ("Kecap Asin Korea / Soy Sauce (Ganjang)", "250", "ml", ""),
            ("Gula Pasir", "200", "gr", ""),
            ("Korean Mirin", "100", "ml", ""),
            ("Bawang Putih", "10", "siung", "Kupas bersih"),
            ("Apel Merah", "1", "buah", "Iris tebal memanjang"),
            ("Daun Bawang", "2", "batang", "Potong kasar")
        ]),
        ("Bahan Bumbu Puree Halus (Blender)", [
            ("Buah Pir Korea (Korean Pear)", "1", "buah", "Kupas bersih dan potong dadu"),
            ("Bawang Putih", "8", "siung", "Kupas bersih"),
            ("Bawang Bombay", "1", "buah", "Kupas dan potong kasar"),
            ("Daun Bawang", "2", "batang", "Iris kasar"),
            ("Lada Putih Bubuk", "1", "sdt", "")
        ]),
        ("Bahan Pengental & Daging Panggang", [
            ("Tepung Maizena", "2", "sdm", "Larutkan dalam 3 sdm air"),
            ("Daging Iga Sapi / Babi (Ribs / Sliced Meat)", "1", "kg", "Potong siap marinasi")
        ])
    ],
    "steps": [
        (1, "Didihkan Dasar Kuah Marinasi", "Tuang air bersih ke dalam panci besar di atas api sedang. Masukkan kecap asin (soy sauce) dan gula pasir, lalu aduk hingga gula larut sempurna dan air mulai mendidih.", 180),
        (2, "Masukkan Aromatik Rebusan", "Tambahkan Korean mirin, bawang putih utuh yang telah dikupas, irisan apel merah, dan potongan daun bawang ke dalam panci rebusan yang sedang mendidih.", 120),
        (3, "Haluskan Bumbu Buah & Aromatik", "Masukkan potongan buah pir Korea, bawang putih, bawang bombay, irisan daun bawang, dan lada putih ke dalam blender. Proses hingga halus merata membentuk tekstur puree.", 60),
        (4, "Campur Bumbu Halus ke Rebusan", "Tuangkan puree bumbu halus dari blender ke dalam panci rebusan berisi apel dan daun bawang, lalu aduk hingga tercampur rata.", 60),
        (5, "Rebus Perlahan (Simmer) 40 Menit", "Kecilkan api kompor dan rebus saus secara perlahan (simmer) selama 40 menit agar sari manis buah apel dan pir serta aroma rempah terekstraksi maksimal ke dalam kuah kaldu.", 2400),
        (6, "Saring Ampas Saus Marinasi", "Angkat panci lalu tuangkan seluruh kuah melalui saringan kawat halus (mesh strainer) ke dalam wadah bersih. Buang ampas buah dan sayuran rebusan agar hasil saus mulus jernih.", 120),
        (7, "Kentalkan Saus dengan Maizena", "Tuangkan kembali kuah saus yang telah disaring ke panci. Nyalakan api kecil, lalu masukkan larutan tepung maizena sambil diaduk cepat hingga saus mengental, mengilap (glossy), dan meletup-letup.", 180),
        (8, "Marinasi & Panggang Daging BBQ", "Lumuri potongan daging iga (ribs) atau irisan daging dengan saus marinasi Sutbul hingga merata. Diamkan di kulkas minimal 1-2 jam, lalu panggang di atas arang panas sambil diolesi sisa saus hingga harum dan terkaramelisasi.", 0)
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
