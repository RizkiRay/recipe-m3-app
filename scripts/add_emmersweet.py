import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "salt-roasted-crispy-chicken-bones",
    "title": "Crispy Salt-Roasted Chicken Bones (Xương Gà Rang Muối)",
    "chef": "Phương Phương (@emmersweet)",
    "description": "Camilan renyah krispi gurih khas Vietnam dari tulang ayam/kerongkong yang dibumbui rempah dan digoreng sangrai garam (Salt-Roasted Chicken Bones).",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdVxzx_FUEX/",
    "servings": "2-3 Porsi Camilan",
    "prep_time": "15 menit",
    "cook_time": "20 menit goreng & sangrai",
    "calories": "Crunchy Vietnamese Salt-Roasted Snack",
    "groups": [
        ("Bahan Utama Tulang Ayam", [
            ("Kerongkong / Tulang Ayam Segar (Potong kecil)", "500", "gr", "Bersihkan & tiriskan kering"),
            ("Bawang Putih (Cincang halus)", "4", "siung", "Bumbu marinasi"),
            ("Jahe & Serai (Memarkan)", "2", "batang", "Penghilang amis"),
            ("Kecap Asin / Kecap Ikan (Fish Sauce)", "1.5", "sdm", ""),
            ("Lada Bubuk & Kaldu Bubuk", "1/2", "sdt", "")
        ]),
        ("Bahan Pelapis & Bumbu Rang Muối (Garam Sangrai)", [
            ("Tepung Maizena / Tepung Tapioka", "4-5", "sdm", "Pelapis kering agar renyah krispi"),
            ("Garam Laut / Garam Halus", "1", "sdt", "Disangrai dengan bumbu rempah"),
            ("Cabai Rawit / Cabai Kering (Iris)", "3", "buah", ""),
            ("Daun Jeruk Purut (Iris halus)", "4", "lembar", "Aroma wangi segar khas Vietnam"),
            ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
        ])
    ],
    "steps": [
        (1, "Marinasi Tulang Ayam", "Potong kerongkong/tulang ayam menjadi potongan kecil agar renyah merata. Campurkan dengan bawang putih cincang, serai, kecap asin, lada bubuk, dan kaldu. Diamkan 15-20 menit.", 0),
        (2, "Balur Tepung Kering", "Taburkan tepung maizena ke potongan tulang ayam hingga seluruh permukaannya terbalut lapisan tipis kering merata.", 0),
        (3, "Goreng Deep-Fry hingga Renyah Garing", "Panaskan minyak banyak dengan api sedang. Goreng tulang ayam berbalut tepung selama 8-10 menit hingga benar-benar kering, garing, dan berwarna cokelat keemasan. Angkat dan tiriskan minyaknya.", 600),
        (4, "Sangrai Bumbu Rang Muối & Sajikan", "Panaskan wajan kering tanpa minyak di atas api kecil. Masukkan irisan cabai, daun jeruk, dan garam, lalu sangrai sebentar hingga wangi. Masukkan tulang ayam goreng garing, aduk cepat hingga bumbu garam menempel rata. Sajikan selagi panas renyah!", 180)
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
    print(f"Successfully added recipe: {recipe_data['title']}")

conn.commit()
conn.close()
