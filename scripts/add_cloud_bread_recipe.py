import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "cloud-bread-fluffy-ais-kitchen",
    "title": "Cloud Bread (Roti Awan Pastel Fluffy Tanpa Terigu)",
    "chef": "Ais's Kitchen (@choco.latteeee____)",
    "description": "Roti awan super lembut dan mengembang fluffy dengan warna pastel cantik, dibuat hanya dengan 3 bahan utama (putih telur, gula pasir, dan maizena) tanpa tepung terigu. Tekstur luar kering keemasan tipis dengan serat dalam seringan kapas.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdiaYEixdDH/",
    "servings": "1 Buah Ukuran Besar (2-3 Porsi)",
    "prep_time": "10 menit",
    "cook_time": "25-30 menit",
    "calories": "Gluten-Free / Rendah Kalori",
    "groups": [
        ("Bahan Utama Cloud Bread", [
            ("Putih Telur", "3", "butir", "Suhu ruang, wadah bersih bebas minyak atau air"),
            ("Gula Pasir", "2", "sdm", "Butiran halus, masukkan bertahap saat dimixer"),
            ("Tepung Maizena", "2", "sdm", "Ayak halus untuk menstabilkan struktur meringue"),
            ("Ekstrak Vanila", "1/2", "sdt", "Perisa penghilang aroma amis telur"),
            ("Pewarna Makanan Pink", "1-2", "tetes", "Opsional untuk sentuhan warna pastel awan")
        ])
    ],
    "steps": [
        (1, "Kocok Putih Telur Hingga Berbusa", "Siapkan mangkuk kaca atau stainless steel yang benar-benar bersih dan kering bebas minyak atau air. Masukkan 3 butir putih telur suhu ruang, lalu kocok menggunakan mikser dengan kecepatan rendah hingga mulai berbusa halus.", 60),
        (2, "Masukkan Gula Pasir Bertahap", "Naikkan kecepatan mikser ke sedang. Masukkan 2 sdm gula pasir secara bertahap (bagi dalam 2-3 tahap) sambil terus dikocok hingga gula larut sempurna dan adonan putih telur mulai mengembang tebal serta mengilap.", 120),
        (3, "Tambahkan Maizena & Ekstrak Vanila", "Masukkan 1/2 sdt ekstrak vanila dan ayak 2 sdm tepung maizena ke dalam mangkuk adonan. Kocok kembali dengan kecepatan tinggi hingga adonan mencapai tahap kaku (stiff peak) di mana adonan tegak dan tidak tumpah saat mangkuk dibalik.", 120),
        (4, "Beri Pewarna Pink & Bentuk Kubah Awan", "Tambahkan 1-2 tetes pewarna makanan pink, lalu mikser sebentar dengan kecepatan rendah atau aduk lipat perlahan menggunakan spatula hingga warna pastel merata. Tuang seluruh adonan ke atas loyang yang telah dialasi baking paper, lalu rapikan membentuk kubah awan yang membulat tinggi.", 60),
        (5, "Panggang Hingga Mengembang Lembut", "Panaskan oven pada suhu 150°C. Masukkan loyang dan panggang selama 25 hingga 30 menit hingga permukaan luar berwarna keemasan tipis dan kering saat disentuh lembut. Matikan oven, keluarkan roti awan, dan sajikan selagi hangat saat teksturnya paling empuk dan mengembang.", 1650)
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
print(f"Successfully processed! Recipe ID: {r_id}, Slug: {recipe_data['slug']}")
