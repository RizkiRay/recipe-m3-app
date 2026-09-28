import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "nasi-hainam-rice-cooker-firhan",
    "title": "Nasi Hainam Rice Cooker Praktis & Gurih Wangi",
    "chef": "Chef Firhan Ashari (@firhan_ashari)",
    "description": "Nasi Hainam praktis anti-ribet masak langsung di dalam rice cooker dengan paha ayam juicy beraroma jahe dan minyak wijen, disajikan lengkap dengan sambal hainam segar asam pedas gurih.",
    "youtube_id": "",
    "media_url": "https://vt.tiktok.com/ZSbrHgyvA/",
    "servings": "3-4 Porsi",
    "prep_time": "15 menit",
    "cook_time": "30 menit",
    "calories": "± 480 kkal / porsi",
    "groups": [
        ("Bahan Marinasi Ayam", [
            ("Paha Ayam", "4", "potong", "Paha utuh / paha atas bawah"),
            ("Jeruk Nipis", "1", "buah", "Peras airnya"),
            ("Saus Tiram", "1", "sdm", "Lumuri ke seluruh permukaan ayam")
        ]),
        ("Bahan Nasi Hainam (Rice Cooker)", [
            ("Beras", "400", "gr", "Cuci bersih dan tiriskan"),
            ("Bawang Putih", "8", "siung", "Cincang halus"),
            ("Bawang Bombay", "1/2", "buah", "Cincang halus"),
            ("Jahe Segar", "1", "jempol", "Kupas lalu cincang halus"),
            ("Kecap Asin", "2", "sdm", "Kecap asin gurih"),
            ("Saus Tiram", "1", "sdm", "Penambah rasa umami"),
            ("Kecap Ikan", "1", "sdm", "Aroma khas oriental"),
            ("Kaldu Ayam Bubuk", "1", "sdt", "Penyedap rasa ayam"),
            ("Lada Putih Bubuk", "1/2", "sdt", "Perasa pedas hangat"),
            ("Penyedap Rasa", "1", "sdt", "Penyedap rasa / micin"),
            ("Daun Bawang", "2", "batang", "Potong panjang atau simpulkan"),
            ("Air Bersih", "700", "ml", "Takaran cairan masak nasi"),
            ("Minyak Wijen", "2", "sdm", "Tuang terakhir setelah nasi matang")
        ]),
        ("Bahan Sambal Hainam Segar", [
            ("Cabai Rawit Merah", "4", "buah", "Pedas segar"),
            ("Cabai Merah Keriting", "3", "buah", "Warna merah cerah"),
            ("Jahe Segar", "1/2", "ruas jari", "Kupas bersih"),
            ("Air Matang", "5", "sdm", "Cairan blender"),
            ("Saus Tomat", "5", "sdm", "Rasa asam manis segar"),
            ("Saus Sambal", "1", "sdm", "Sentuhan pedas manis"),
            ("Kaldu Bubuk", "1", "sdt", "Penyedap rasa"),
            ("Kecap Ikan", "1", "sdm", "Gurih umami khas sambal hainam")
        ])
    ],
    "steps": [
        (1, "Marinasi Potongan Paha Ayam", "Cuci bersih 4 potong paha ayam. Masukkan ke dalam wadah, lalu lumuri dengan perasan air 1 buah jeruk nipis dan 1 sdm saus tiram. Remas-remas lembut hingga merata, lalu diamkan (marinasi) selama 10–15 menit agar bumbu meresap dan bau amis hilang.", 600),
        (2, "Tumis Bumbu Aromatik", "Panaskan sedikit minyak di wajan. Tumis 8 siung bawang putih cincang, 1/2 buah bawang bombay cincang, dan 1 jempol jahe cincang hingga matang, harum wangi, dan berwarna sedikit kecokelatan. Angkat.", 180),
        (3, "Racik Nasi di Rice Cooker", "Masukkan 400 gr beras yang sudah dicuci bersih ke dalam wadah rice cooker (inner pot). Masukkan bumbu tumisan bawang dan jahe, 2 sdm kecap asin, 1 sdm saus tiram, 1 sdm kecap ikan, 1 sdt kaldu ayam bubuk, 1/2 sdt lada putih bubuk, 1 sdt penyedap rasa, 2 batang daun bawang, dan tuangkan 700 ml air. Aduk rata agar semua bumbu tercampur sempurna.", 0),
        (4, "Susun Ayam & Masak Hingga Matang", "Tata potongan paha ayam yang sudah dimarinasi tepat di atas permukaan beras dan bumbu. Tutup rice cooker, lalu tekan tombol Cook (masak nasi seperti biasa) hingga berpindah ke mode Warm dan nasi matang tanak.", 1800),
        (5, "Beri Minyak Wijen & Aduk Nasi", "Setelah matang, buka rice cooker. Angkat paha ayam dan daun bawang, sisihkan. Tuangkan 2 sdm minyak wijen ke atas nasi hainam hangat, lalu aduk nasi secara merata hingga pulen, beraroma harum, dan butiran nasi mengilap.", 0),
        (6, "Blender Sambal Hainam", "Masukkan 4 buah cabai rawit merah, 3 buah cabai merah keriting, 1/2 ruas jari jahe, 5 sdm air, 5 sdm saus tomat, 1 sdm saus sambal, 1 sdt kaldu bubuk, dan 1 sdm kecap ikan ke dalam blender atau food processor. Haluskan hingga tekstur saus tercampur rata dan halus.", 60),
        (7, "Potong Ayam & Sajikan", "Potong-potong paha ayam hainam sesuai selera. Sajikan nasi hainam hangat di piring bersama potongan ayam juicy, siraman sambal hainam segar, serta pelengkap irisan timun segar.", 0)
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
