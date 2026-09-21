import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "fung-khiuk-thong-kuah-angkak-tannatalia",
    "title": "Fung Khiuk Thong (Sup Ayam Kampung Kuah Angkak & Kembang Tahu)",
    "chef": "Natalia Tan / Maetan (@tannatalia)",
    "description": "Sup herbal tradisional khas Hakka/Tionghoa berkuah merah alami dari seduhan angkak, jahe wangi, ayam kampung gurih empuk, dan kembang tahu (fucuk) lembut. Menu comfort food legendaris berkhasiat menghangatkan tubuh dan memulihkan stamina saat kurang enak badan atau masa pemulihan.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/Ddaa4nuPZMr/",
    "servings": "4-5 Porsi",
    "prep_time": "15 menit",
    "cook_time": "45 menit",
    "calories": "Tinggi Nutrisi / Hangat Herbal Alami",
    "groups": [
        ("Bahan Utama Sup & Herbal", [
            ("Ayam Kampung", "1", "ekor", "Potong 8-12 bagian dan cuci bersih"),
            ("Beras Angkak Merah", "1.5", "sdm", "Ulek atau giling hingga halus"),
            ("Jahe Segar", "50", "gr", "Kupas dan iris tipis memanjang"),
            ("Kembang Tahu (Fucuk)", "50", "gr", "Rendam air hangat hingga lembut lalu tiriskan"),
            ("Minyak Wijen / Minyak Goreng", "2", "sdm", "Untuk menumis jahe"),
            ("Air Bersih", "1.5", "liter", "Untuk kuah kaldu")
        ]),
        ("Bumbu Perasa & Aromatik", [
            ("Garam", "1", "sdt", "Penyeimbang rasa gurih"),
            ("Kaldu Jamur", "1", "sdt", "Penyedap rasa alami"),
            ("Arak Masak (Shao Hsing Wine / Arak Putih)", "2", "sdm", "Aroma wangi khas oriental (opsional)")
        ])
    ],
    "steps": [
        (1, "Persiapan Bahan & Ulek Angkak", "Cuci bersih potongan ayam kampung dan tiriskan. Ulek 1.5 sdm beras angkak hingga menjadi bubuk halus di dalam cobek/lesung. Rendam kembang tahu (fucuk) dalam air hangat sampai lentur lembut, lalu potong-potong sesuai selera. Kupas jahe dan iris tipis bentuk korek api.", 0),
        (2, "Tumis Jahe Hingga Harum", "Panaskan 2 sdm minyak di wajan atau panci sup dengan api sedang. Masukkan irisan jahe segar, lalu tumis hingga layu, wangi semerbak, dan sedikit kecokelatan untuk mengeluarkan aroma hangat alaminya.", 120),
        (3, "Masukkan Ayam Kampung & Balur Angkak", "Masukkan potongan ayam kampung ke dalam tumisan jahe. Aduk dan tumis cepat hingga permukaan daging ayam berubah warna mengunci sari kaldunya. Taburkan bubuk angkak halus, lalu aduk merata sampai seluruh daging ayam terbalur warna merah merona alami.", 180),
        (4, "Rebus Kuah Kaldu Hingga Mendidih", "Tuang 1.5 liter air bersih ke dalam panci hingga ayam terendam sempurna. Besarkan api hingga kuah mendidih, lalu kecilkan api ke level sedang-kecil. Tutup panci dan biarkan kaldu ayam matang perlahan selama 25-30 menit agar sari kaldu ayam kampung keluar maksimal dan daging mulai empuk.", 1500),
        (5, "Tambahkan Kembang Tahu & Bumbu Perasa", "Buka tutup panci, masukkan kembang tahu (fucuk) yang telah lembut. Bumbui dengan 1 sdt garam, 1 sdt kaldu jamur, dan 2 sdm arak masak (Shao Hsing wine / arak putih). Aduk perlahan dan masak kembali selama 10-15 menit hingga kuah kaldu merah meresap pekat ke dalam kembang tahu.", 600),
        (6, "Cek Rasa & Sajikan Hangat", "Koreksi rasa kuah kaldu (harus gurih asin pas berpadu aroma hangat jahe dan khas angkak). Matikan api, tuang sup ayam angkak beserta kuah merah melimpah ke dalam mangkuk saji. Nikmati selagi hangat mengepul bersama nasi putih!", 0)
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
    print(f"Updated recipe id: {r_id}")
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
    print(f"Inserted recipe id: {r_id}")

for g_idx, (g_name, items) in enumerate(recipe_data['groups']):
    cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (r_id, g_name, g_idx))
    g_id = cursor.lastrowid
    for i_idx, it in enumerate(items):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))

for st in recipe_data['steps']:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (r_id, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print("Successfully synced recipe to SQLite DB!")
