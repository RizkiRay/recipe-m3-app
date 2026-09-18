import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "chinese-velvet-chicken-breast",
    "title": "Chinese Velvet Chicken Breast (Ayam Velvet Lembut Saus Pedas Gurih)",
    "chef": "Victor Wokmanyama (@victorwokmanyama)",
    "description": "Dada ayam super empuk & juicy menggunakan teknik Chinese velveting (dibalur maizena & baking soda, ditipiskan hingga translucent), direbus cepat (poached 1 menit), lalu disiram saus aromatik capsicum, bawang putih, wijen, dan chili oil gurih pedas.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/Dc5mvCTyMlO/",
    "servings": "2-3 Porsi",
    "prep_time": "15 menit",
    "cook_time": "5 menit",
    "calories": "Tinggi Protein / Rendah Lemak",
    "groups": [
        ("Bahan Utama Ayam & Velveting", [
            ("Dada Ayam Fillet", "300-400", "gr", "Iris tipis"),
            ("Tepung Maizena", "1/2", "cup", "Lapisan velveting"),
            ("Baking Soda", "1/2", "sdt", "Pengempuk serat daging alami")
        ]),
        ("Bahan Air Rebusan (Poaching Aromatics)", [
            ("Air Bersih", "1.5", "liter", "Untuk merebus"),
            ("Lada Sichuan (Sichuan Peppercorns)", "1", "sdt", "Aroma khas oriental"),
            ("Daun Bawang", "2", "batang", "Potong sedang"),
            ("Jahe Segar", "3", "iris", "Iris tipis"),
            ("Cooking Wine / Shaoxing Wine", "1-2", "sdm", "Penghilang amis (opsional)")
        ]),
        ("Bahan Saus Aromatik Gurih Pedas", [
            ("Paprika Hijau", "1/2", "buah", "Cincang halus"),
            ("Paprika Merah", "1/2", "buah", "Cincang halus"),
            ("Bawang Putih", "4-5", "siung", "Cincang halus"),
            ("Daun Bawang", "2", "batang", "Cincang halus"),
            ("Minyak Goreng Panas", "3-4", "sdm", "Siram ke bumbu aromatik"),
            ("Kecap Asin (Soy Sauce)", "2", "sdm", ""),
            ("Saus Tiram (Oyster Sauce)", "1", "sdm", ""),
            ("Gula Pasir", "1", "sdt", "Penyeimbang rasa"),
            ("Garam Laut (Sea Salt)", "1/2", "sdt", ""),
            ("Biji Wijen Sangrai", "1", "sdt", ""),
            ("Minyak Cabai (Chilli Oil)", "1-2", "sdm", "Sesuai selera pedas")
        ])
    ],
    "steps": [
        (1, "Iris & Balur Campuran Maizena", "Iris tipis dada ayam. Dalam mangkuk, campurkan 1/2 cup tepung maizena dan 1/2 sdt baking soda. Masukkan irisan ayam dan aduk rata hingga setiap potongan ayam terbalut lapisan tepung secara merata.", 0),
        (2, "Pipihkan Ayam (Pounding Thin)", "Letakkan irisan ayam di atas talenan, tutup dengan plastik wrap. Pukul perlahan menggunakan rolling pin hingga sangat tipis dan agak tembus pandang (translucent). Sisihkan ayam yang sudah dipipihkan.", 0),
        (3, "Racik Saus Aromatik Bawang & Cabai", "Dalam mangkuk tahan panas, masukkan paprika hijau cincang, paprika merah cincang, bawang putih cincang, dan daun bawang cincang. Siram dengan minyak goreng panas mendidih agar aroma harum keluar. Tambahkan kecap asin, saus tiram, gula pasir, garam laut, biji wijen, dan chili oil. Aduk hingga rata.", 0),
        (4, "Rebus Cepat Bertahap (Batch Poaching)", "Didihkan air dalam panci besar bersama lada Sichuan, daun bawang, jahe, dan cooking wine. Masukkan irisan ayam secara bertahap dalam porsi kecil (small batches) agar air tetap mendidih stabil. Masak cepat sekitar 1 menit hingga daging ayam berubah putih matang sempurna tanpa sisa warna merah muda.", 60),
        (5, "Aduk Bersama Saus & Sajikan", "Angkat dan tiriskan ayam rebus, langsung masukkan ke dalam mangkuk saus aromatik. Aduk rata hingga seluruh permukaan ayam terlapisi saus gurih pedas. Sajikan hangat bersama nasi putih pulen!", 0)
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
