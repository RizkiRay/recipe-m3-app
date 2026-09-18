import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "telur-oseng-terasi-cabe-bawang",
    "title": "Telur Oseng Terasi Cabe Bawang",
    "chef": "@kupicookie",
    "description": "Olahan telur orak-arik berkulit gurih dipadukan tumisan terasi bakar harum, irisan bawang merah melimpah, cabai hijau/merah/rawit, daun jeruk segar, dan daun bawang.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DcVe9HiB5hA/",
    "servings": "2-3 Porsi",
    "prep_time": "10 menit",
    "cook_time": "10 menit",
    "calories": "Lauk Rumahan Cepat Saji",
    "groups": [
        ("Bahan Utama Telur", [
            ("Telur Ayam Segar", "3", "butir", "Kocok lepas"),
            ("Minyak Goreng", "2-3", "sdm", "Untuk menumis & orak-arik")
        ]),
        ("Bumbu Iris & Aromatik Segar", [
            ("Bawang Merah", "10", "siung", "Iris sedang"),
            ("Bawang Putih", "3", "siung", "Cincang halus"),
            ("Cabai Hijau Besar", "2", "buah", "Iris serong"),
            ("Cabai Merah Besar", "1", "buah", "Iris serong"),
            ("Cabai Rawit Merah", "5-10", "buah", "Iris bulat"),
            ("Daun Jeruk Purut", "3-4", "lembar", "Buang tulang daun, iris tipis"),
            ("Daun Bawang", "2", "batang", "Iris sedang")
        ]),
        ("Seasoning & Penyedap", [
            ("Terasi Bakar / Matang", "1", "sdt", "Haluskan"),
            ("Garam", "1/2", "sdt", ""),
            ("Lada Bubuk", "1/4", "sdt", ""),
            ("Kaldu Jamur", "1/2", "sdt", ""),
            ("Bawang Goreng", "1", "sdm", "Taburan opsional")
        ])
    ],
    "steps": [
        (1, "Orak-Arik Telur Berkulit", "Panaskan wajan dengan sedikit minyak hingga benar-benar panas. Tuang telur, orak-arik kasar, lalu diamkan sejenak hingga bagian dasar agak berkulit kecokelatan gurih. Angkat dan sisihkan.", 120),
        (2, "Tumis Bumbu Iris & Daun Jeruk", "Panaskan minyak sisa di wajan yang sama. Tumis bawang putih cincang, irisan bawang merah, cabai hijau, cabai merah, cabai rawit, dan irisan daun jeruk hingga layu dan beraroma harum semerbak.", 120),
        (3, "Masukkan Terasi & Bumbu Penyedap", "Tambahkan terasi halus, garam, lada bubuk, dan kaldu jamur. Aduk cepat hingga terasi larut dan tercampur rata bersama tumisan cabai bawang.", 60),
        (4, "Campur Telur & Daun Bawang", "Masukkan kembali telur orak-arik dan irisan daun bawang ke dalam wajan. Aduk cepat dengan api sedang-besar hingga seluruh bumbu meresap rata ke serat telur.", 60),
        (5, "Sajikan Hangat", "Angkat dan sajikan di atas piring bersama taburan bawang goreng jika suka. Nikmati bersama nasi putih panas!", 0)
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
