import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "peking-duck-arsyan-dwianto",
    "title": "Peking Duck Rumahan (Bebek Peking Kulit Crispy & Daging Juicy)",
    "chef": "Arsyan Dwianto (@arsyandwianto_)",
    "description": "Bebek Peking otentik ala restoran bintang lima: bumbu rempah aromatik disangrai & dihaluskan untuk marinasi rongga dalam, teknik pemisahan kulit agar tipis renyah, siraman glasir cuka madu, proses dry-aging kulkas 24 jam, dan dipanggang hingga kulit crispy mengilap serta daging tetap lembut juicy.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdbHOjGTgeg/",
    "servings": "4-6 Porsi",
    "prep_time": "30 menit (+ 24 jam dry-aging)",
    "cook_time": "60 menit",
    "calories": "Otentik Chinese Roast Duck",
    "groups": [
        ("Bahan Utama Bebek Utuh", [
            ("Bebek Utuh Segar (Peking Duck)", "1", "ekor (±2 - 2.2 kg)", "Bersihkan rongga dalam & keringkan"),
            ("Tusuk Sate Bambu / Skewer", "2-3", "buah", "Untuk menjahit/mengunci rongga bawah bebek")
        ]),
        ("Bumbu Rempah Sangrai (Spice Mix Rongga Dalam)", [
            ("Bubuk Ngo Hiong (Five Spice Powder)", "1", "sdm", "Aroma rempah khas"),
            ("Bunga Lawang (Star Anise)", "2", "kuntum", "Sangrai wangi & haluskan"),
            ("Kayu Manis", "1", "batang kecil", "Sangrai wangi & haluskan"),
            ("Lada Sichuan / Merica Putih", "1", "sdt", "Sangrai wangi & haluskan"),
            ("Bawang Putih Parut", "4", "siung", ""),
            ("Jahe Parut", "2", "cm", ""),
            ("Saus Hoisin", "2", "sdm", "Base saus gurih manis"),
            ("Kecap Asin / Soy Sauce", "1", "sdm", ""),
            ("Minyak Wijen", "1", "sdm", ""),
            ("Gula Pasir & Garam", "1", "sdt", "")
        ]),
        ("Bahan Siraman Glasir Kulit (Vinegar & Maltose Glaze)", [
            ("Air Mendidih", "500", "ml", "Untuk menyiram kulit pertama kali"),
            ("Cuka Beras Putih (Rice Vinegar)", "3", "sdm", "Kunci kulit kering & renyah"),
            ("Madu Murni / Maltosa", "2", "sdm", "Memberi warna merah karamel mengilap"),
            ("Kecap Asin", "1", "sdm", "")
        ]),
        ("Pelengkap Penyajian", [
            ("Kulit Pancake Peking Duck", "10-15", "lembar", "Kukus hangat"),
            ("Mentimun", "1", "buah", "Iris bentuk korek api"),
            ("Daun Bawang", "2", "batang", "Iris halus memanjang"),
            ("Saus Hoisin / Saus Manis Bebek", "3-4", "sdm", "Sebagai cocolan")
        ])
    ],
    "steps": [
        (1, "Sangrai & Racik Bumbu Rempah Rongga Dalam", "Sangrai bunga lawang, kayu manis, dan lada Sichuan hingga harum semerbak, lalu giling/haluskan. Campurkan bubuk rempah dengan ngo hiong, saus hoisin, kecap asin, minyak wijen, bawang putih parut, jahe, gula, dan garam. Aduk hingga menjadi pasta marinasi.", 0),
        (2, "Marinasi Rongga Dalam & Kunci Bebek", "Balurkan seluruh pasta bumbu rempah ke dalam rongga dalam perut dan tulang-tulang bebek secara merata (jangan terkena kulit luar). Rapatkan dan jahit rongga bawah bebek menggunakan tusuk bambu (skewer) agar bumbu dan uap sari daging terkunci rapat di dalam saat dipanggang.", 0),
        (3, "Pisahkan Kulit & Siram Glasir Cuka Madu", "Gunakan pompa udara/air compressor bersih untuk meniupkan udara di antara lapisan kulit dan daging bebek hingga kulit mengembang dan terpisah (rahasia kulit tipis super renyah). Siram seluruh permukaan kulit bebek dengan air panas mendidih, lalu siram merata dengan campuran cuka beras, madu/maltosa, dan kecap asin.", 0),
        (4, "Proses Keringkan Kulit (Dry-Aging 24 Jam)", "Gantung atau letakkan bebek di atas rak kawat dalam kulkas dalam kondisi terbuka tanpa tutup (uncovered) selama 24 jam hingga kulit bebek benar-benar kering kencang, tipis, dan berwarna merah kecokelatan.", 0),
        (5, "Panggang Hingga Kulit Crispy & Juicy", "Panaskan oven suhu 180°C (mode fan/convection). Panggang bebek selama 50-60 menit sambil diputar posisinya hingga seluruh kulit berwarna cokelat keemasan mengilap (deep golden brown) dan renyah garing. Istirahatkan (resting) 10 menit sebelum diiris.", 3600),
        (6, "Iris Tipis & Sajikan Bersama Pelengkap", "Iris tipis kulit renyah beserta daging bebek yang lembut juicy. Sajikan hangat di atas piring bersama kulit pancake kukus, irisan mentimun, daun bawang, dan cocolan saus hoisin.", 0)
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
        recipe_data['slug'], recipe_data['title'], recipe_data['chef'], recipe_data['description'],
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
print("Done!")
