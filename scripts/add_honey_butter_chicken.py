import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "honey-butter-chicken-breast-teikuu",
    "title": "Honey Butter Chicken Breast (Ayam Dada Saus Madu Mentega)",
    "chef": "Teikuu Hikou Kitchen (@teikuuhikou_kitchen)",
    "description": "Potongan stik dada ayam lembut juicy berbalut tepung maizena/katakuriko, dipanggang wajan lalu diglasir saus honey butter khas Jepang (mentega gurih, madu murni, kecap asin shoyu, dan bawang putih harum).",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DbsuZssh4Qp/",
    "servings": "2 Porsi",
    "prep_time": "10 menit",
    "cook_time": "8 menit",
    "calories": "Tinggi Protein / Gurih Manis",
    "groups": [
        ("Bahan Utama Ayam & Baluran", [
            ("Dada Ayam Fillet", "350", "gr", "Potong bentuk stik tebal 1.5 cm"),
            ("Tepung Maizena / Tapioka / Katakuriko", "2", "sdm", "Baluran renyah juicy"),
            ("Garam", "1/4", "sdt", "Marinasi dasar"),
            ("Lada Hitam / Merica Bubuk", "1/4", "sdt", ""),
            ("Minyak Goreng", "2", "sdm", "Untuk memanggang di teflon")
        ]),
        ("Bahan Saus Honey Butter Glasir", [
            ("Salted Butter (Mentega Asin)", "20", "gr", "Kunci aroma gurih creamy"),
            ("Madu Murni", "2", "sdm", "Rasa manis karamel alami"),
            ("Kecap Asin Jepang (Shoyu) / Soy Sauce", "1", "sdm", "Rasa umami gurih"),
            ("Bawang Putih Parut / Garlic Paste", "1", "sdt", "Aroma harum sedap"),
            ("Daun Peterseli (Parsley) Segar", "1", "sdm", "Cincang halus untuk taburan")
        ])
    ],
    "steps": [
        (1, "Potong & Marinasi Dada Ayam", "Potong fillet dada ayam menjadi bentuk stik memanjang dengan ketebalan sekitar 1.5 cm. Lumuri dan remas perlahan dengan garam dan merica bubuk hingga merata.", 0),
        (2, "Balur Lapisan Maizena", "Taburkan 2 sdm tepung maizena (katakuriko) ke potongan ayam. Balur secara merata ke seluruh permukaan stik ayam untuk mengunci kelembapan (juiciness) daging saat dipanggang.", 0),
        (3, "Panggang Ayam di Teflon", "Panaskan 2 sdm minyak di wajan teflon dengan api sedang. Panggang stik ayam bolak-balik hingga matang dan kedua sisi berwarna cokelat keemasan. Jangan overcooked agar daging tidak kering/seret.", 240),
        (4, "Keringkan Minyak & Masak Saus Honey Butter", "Gunakan tisu dapur untuk menyerap sisa minyak berlebih di wajan. Masukkan 20 gr salted butter, 2 sdm madu, 1 sdm kecap asin shoyu, dan 1 sdt bawang putih parut. Aduk dan tumis cepat selama 1 menit hingga saus berbusa mengilap (glaze) dan membalut seluruh potongan ayam.", 60),
        (5, "Taburi Parsley & Sajikan", "Pindahkan ayam honey butter ke piring saji, taburi dengan cincangan daun peterseli segar. Nikmati hangat bersama nasi putih atau sebagai camilan lauk!", 0)
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
