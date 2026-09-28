import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "chinese-velvet-chicken-breasts-beena",
    "title": "Chinese Velvet Chicken Breasts (Ayam Velvet Lembut Saus Pedas Gurih)",
    "chef": "Khana Pakana with BEENA (@khanapakanawithbeena)",
    "description": "Dada ayam super empuk dan silky juicy menggunakan teknik Chinese velveting (dibalur maizena dan baking soda), dipoach cepat dalam air mendidih beraroma jahe, lalu disiram saus aromatik paprika, bawang putih, biji wijen, chili flakes, dan perpaduan saus oriental manis gurih pedas.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdtcxsnsHSF/",
    "servings": "2-3 Porsi",
    "prep_time": "15 menit",
    "cook_time": "5 menit",
    "calories": "Tinggi Protein / Rendah Lemak",
    "groups": [
        ("Bahan Utama Dada Ayam & Velveting", [
            ("Daging Dada Ayam Fillet", "350", "gr", "Iris tipis memanjang"),
            ("Tepung Maizena", "2", "sdm", "Lapisan velveting lembut"),
            ("Baking Soda", "1/2", "sdt", "Pengempuk serat daging alami")
        ]),
        ("Bahan Air Rebusan (Poaching Aromatics)", [
            ("Air Bersih", "1.5", "liter", "Untuk merebus ayam"),
            ("Jahe Segar", "3", "iris", "Iris tipis geprek"),
            ("Garam Laut (Sea Salt)", "1/2", "sdt", "Perasa air rebusan")
        ]),
        ("Bahan Saus Aromatik Manis Pedas Gurih", [
            ("Paprika Hijau", "1/2", "buah", "Cincang halus"),
            ("Paprika Merah", "1/2", "buah", "Cincang halus"),
            ("Bawang Putih", "4-5", "siung", "Cincang halus"),
            ("Daun Bawang", "2", "batang", "Iris halus"),
            ("Cabai Bubuk (Chili Flakes)", "1", "sdm", "Tingkat pedas sesuai selera"),
            ("Biji Wijen Sangrai", "1", "sdm", "Penambah aroma gurih"),
            ("Minyak Goreng Panas", "4", "sdm", "Siram ke bumbu aromatik"),
            ("Kecap Asin (Soy Sauce)", "2", "sdm", "Perasa gurih umami"),
            ("Saus Tiram (Oyster Sauce)", "1", "sdm", "Mama Sita's / saus tiram oriental"),
            ("Sweet Chili Sauce", "1.5", "sdm", "Sensasi manis pedas segar"),
            ("Gula Pasir", "1/2", "sdt", "Penyeimbang rasa"),
            ("Garam Laut (Sea Salt)", "1/4", "sdt", "Penyeimbang rasa"),
            ("Minyak Cabai (Chilli Oil)", "1", "sdm", "Opsional untuk aroma dan warna merah")
        ])
    ],
    "steps": [
        (1, "Iris & Marinasi Velveting Dada Ayam", "Iris tipis dada ayam fillet melintang serat agar empuk maksimal. Masukkan irisan ayam ke dalam mangkuk, tambahkan 2 sdm tepung maizena dan 1/2 sdt baking soda. Aduk dan remas lembut hingga seluruh potongan ayam terlapisi merata dan permukaannya licin lembut.", 0),
        (2, "Siapkan Wadah Bumbu & Siram Minyak Panas", "Dalam mangkuk tahan panas, masukkan paprika hijau cincang, paprika merah cincang, bawang putih cincang, daun bawang iris, chili flakes, dan biji wijen sangrai. Panaskan 4 sdm minyak goreng hingga benar-benar mendidih berasap, lalu siramkan langsung ke atas mangkuk bumbu aromatik agar aromanya meledak wangi.", 60),
        (3, "Tambahkan Saus & Aduk Rata", "Ke dalam mangkuk bumbu aromatik yang sudah disiram minyak panas, masukkan kecap asin, saus tiram, sweet chili sauce, gula pasir, garam laut, dan chili oil (opsional). Aduk rata menggunakan sendok hingga saus menyatu sempurna dan mengilap.", 0),
        (4, "Rebus Cepat Ayam Velvet (Quick Poaching)", "Didihkan 1.5 liter air dalam wok atau panci bersama irisan jahe dan sedikit garam laut. Masukkan irisan ayam berbalur maizena secara bertahap ke dalam air mendidih. Rebus cepat selama 45 detik hingga 1 menit saja sampai daging ayam berubah warna putih matang merata dan sangat lembut (jangan overcooked agar tidak keras).", 60),
        (5, "Tiriskan, Campur Saus & Sajikan", "Angkat segera ayam rebus menggunakan saringan dan tiriskan sisa airnya. Masukkan ayam hangat langsung ke dalam mangkuk saus aromatik manis pedas. Aduk rata hingga seluruh permukaan ayam terbalut saus gurih mengilap. Sajikan hangat bersama nasi putih hangat!", 0)
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

for g_idx, (g_name, items) in enumerate(recipe_data['groups']):
    cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (r_id, g_name, g_idx))
    g_id = cursor.lastrowid
    for i_idx, it in enumerate(items):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))

for st in recipe_data['steps']:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (r_id, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
print(f"Done! Recipe ID: {r_id}, Slug: {recipe_data['slug']}")
