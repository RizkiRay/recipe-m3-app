import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "infused-shrimp-oil-minyak-kulit-udang",
    "title": "Infused Shrimp Oil (Minyak Kulit & Kepala Udang Kaya Umami)",
    "chef": "@leyosatria_",
    "description": "Cara membuat minyak aroma udang (infused shrimp oil) dari sisa kepala dan cangkang udang dengan rasio 1:1 untuk penguat rasa umami masakan.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdTfMgqvyd8/",
    "servings": "1 Botol Minyak Aromatik (Stok Dapur)",
    "prep_time": "5 menit",
    "cook_time": "15 menit",
    "calories": "Aromatic Umami Oil",
    "groups": [
        ("Bahan Utama", [
            ("Kulit & Kepala Udang Segar", "1", "bagian (misal 200 gr)", "Cuci bersih & tiriskan hingga kering"),
            ("Minyak Goreng Dingin", "1", "bagian (rasio 1:1)", "Gunakan minyak sayur netral")
        ]),
        ("Bahan Tambahan (Opsional)", [
            ("Tomato Paste / Pasta Tomat", "1", "sdm", "Memberi warna merah pekat & aroma segar penyeimbang")
        ])
    ],
    "steps": [
        (1, "Campur Kepala Udang & Minyak Dingin", "Campurkan cangkang dan kepala udang bersama minyak goreng dingin di dalam wajan dengan perbandingan rasio 1:1 (jangan masukkan ke minyak yang sudah panas agar aroma terekstrak perlahan).", 0),
        (2, "Masak dengan Api Sedang", "Nyalakan kompor dengan api sedang. Masak sambil sesekali diaduk hingga cangkang dan kepala udang terlihat kering garing dan warna minyak berubah menjadi cokelat kemerahan.", 720),
        (3, "Tambahkan Tomato Paste (Opsional)", "Matikan api kompor. Selagi minyak masih panas, tambahkan 1 sdm tomato paste untuk membuat warna minyak merah pekat alami dan memberi rasa segar penyeimbang aroma udang.", 0),
        (4, "Saring & Simpan", "Saring minyak dari ampas kepala udang ke dalam botol kaca bersih. Minyak udang siap digunakan kapan saja untuk menaikkan rasa umami nasi goreng, mie, tumisan, atau sup!", 0)
    ]
}

cursor.execute("SELECT id FROM recipes WHERE slug = ?", (recipe_data['slug'],))
if not cursor.fetchone():
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
    print(f"Successfully added transcribed recipe: {recipe_data['title']}")

conn.commit()
conn.close()
