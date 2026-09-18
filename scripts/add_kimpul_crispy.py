import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "ayam-kimpul-crispy-dapurmamazela",
    "title": "Kimpul Crispy Gurih Renyah (Olahan Umbi Kimpul Pengganti Ayam)",
    "chef": "Dapur Mamazela (@dapurmamazela)",
    "description": "Camilan renyah & gurih dari umbi talas kimpul yang dipotong menyerupai daging ayam fillet, dimarinasi bumbu gurih meresap, lalu dibalut adonan tepung basah & kering dan digoreng crispy keemasan (golden brown). Renyah di luar, lembut empuk di dalam.",
    "youtube_id": "",
    "media_url": "https://vt.tiktok.com/ZSqtvFQtR/",
    "servings": "3-4 Porsi",
    "prep_time": "15 menit",
    "cook_time": "15 menit",
    "calories": "Camilan / Lauk Nabati Renyah",
    "groups": [
        ("Bahan Utama Umbi Kimpul", [
            ("Umbi Talas Kimpul Segar", "500", "gr", "Kupas bersih & potong memanjang/potong dadu sedang"),
            ("Air Garam", "500", "ml", "Untuk merendam & menghilangkan getah umbi"),
            ("Minyak Goreng", "500", "ml", "Untuk menggoreng deep fry")
        ]),
        ("Bumbu Marinasi Kimpul", [
            ("Bawang Putih Bubuk", "1", "sdt", "Aroma gurih sedap"),
            ("Ketumbar Bubuk", "1/2", "sdt", ""),
            ("Kaldu Bubuk", "1", "sdt", ""),
            ("Garam", "1/2", "sdt", ""),
            ("Merica Bubuk", "1/4", "sdt", "")
        ]),
        ("Bahan Adonan Tepung Crispy", [
            ("Tepung Bumbu Serbaguna / Terigu", "150", "gr", "Bagi adonan basah & kering"),
            ("Tepung Maizena / Tapioka", "2", "sdm", "Memberikan tekstur ekstra renyah"),
            ("Air Es / Dingin", "100", "ml", "Untuk melarutkan adonan tepung basah")
        ])
    ],
    "steps": [
        (1, "Kupas & Rendam Kimpul", "Kupas bersih kulit umbi talas kimpul, potong memanjang menyerupai irisan daging ayam fillet atau stik. Rendam dalam air garam selama 10 menit untuk membersihkan getah, lalu bilas air mengalir hingga bersih dan tiriskan.", 0),
        (2, "Marinasi Kimpul", "Taburkan bawang putih bubuk, ketumbar bubuk, kaldu bubuk, garam, dan merica ke potongan kimpul. Aduk rata dan remas perlahan agar bumbu meresap ke dalam pori-pori umbi selama 10-15 menit.", 0),
        (3, "Siapkan Adonan Tepung Basah & Kering", "Bagi tepung menjadi dua wadah. Wadah 1: larutkan sebagian tepung bumbu dan maizena dengan air es hingga kental sedang (adonan basah). Wadah 2: sisa tepung bumbu kering dan maizena (adonan kering).", 0),
        (4, "Balut Tepung Berlapis", "Ambil potongan kimpul yang sudah dimarinasi, celupkan ke dalam mangkuk adonan tepung basah hingga rata, lalu gulingkan dan remas perlahan di atas mangkuk adonan tepung kering sampai terbentuk lapisan keriting renyah.", 0),
        (5, "Goreng Deep Fry Golden Brown", "Panaskan minyak goreng yang cukup banyak dengan api sedang. Masukkan kimpul bertepung, goreng hingga matang mengapung dan permukaannya renyah berwarna kuning keemasan (golden brown). Angkat, tiriskan, dan sajikan selagi panas!", 480)
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
