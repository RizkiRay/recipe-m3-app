import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "pangsit-kuah-ayam-gurih-janelleandmom",
    "title": "Pangsit Kuah Ayam Gurih & Kaldu Ceker Medok",
    "chef": "Janelle & Mom (@janelleandmom)",
    "description": "Pangsit rebus lembut gurih dengan isian paha ayam cincang juicy bertekstur, dibumbui minyak wijen dan perasan jahe, disajikan bersama kuah kaldu ceker dan bawang putih gurih harum mirip kuah mie ayam legendaris.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/Dd2yJmPT-sm/",
    "servings": "4-5 Porsi (25-30 Butir Pangsit)",
    "prep_time": "25 menit",
    "cook_time": "45 menit",
    "calories": "Gurih Segar / Comfort Food Hangat",
    "groups": [
        ("Bahan Isian Pangsit Ayam (Juicy)", [
            ("Daging Paha Ayam Fillet", "500", "gr", "Potong dadu kecil siap giling"),
            ("Bawang Putih", "3", "siung", "Kupas bersih"),
            ("Daun Bawang", "2", "batang", "Iris halus"),
            ("Kecap Asin", "1.5", "sdm", "Pemberi rasa gurih asin"),
            ("Minyak Wijen", "1", "sdm", "Aroma sedap wangi"),
            ("Gula Pasir", "1", "sdt", "Penyeimbang rasa"),
            ("Garam", "3/4", "sdt", "Garam beryodium"),
            ("Lada Putih Bubuk", "1/2", "sdt", "Aroma hangat"),
            ("Jahe Segar", "5", "gr", "Parut halus lalu peras ambil airnya saja"),
            ("Tepung Maizena", "1", "sdm", "Pengikat tekstur agar adonan tetap lembut juicy"),
            ("Air Dingin / Es", "2", "sdm", "Menjaga kelembapan adonan daging"),
            ("Kulit Pangsit Rebus", "30", "lembar", "Kulit pangsit khusus rebus yang lentur tipis")
        ]),
        ("Bahan Kuah Kaldu Ceker Gurih", [
            ("Air Bersih", "1.2", "liter", "Untuk merebus sari kaldu"),
            ("Ceker Ayam", "5", "buah", "Cuci bersih dan potong kuku ceker"),
            ("Bawang Putih", "4", "siung", "Memarkan / geprek"),
            ("Kecap Asin", "1.5", "sdm", "Warna dan rasa kaldu gurih"),
            ("Lada Putih Bubuk", "1/2", "sdt", "Penghangat kuah kaldu"),
            ("Garam", "1", "sdt", "Sesuaikan tingkat asin"),
            ("Kaldu Jamur / Micin", "1/2", "sdt", "Penguat rasa umami gurih")
        ]),
        ("Bahan Pelengkap & Penyajian", [
            ("Minyak Bawang Putih", "2", "sdm", "Aroma gurih khas ala mie ayam"),
            ("Bawang Putih Goreng", "2", "sdm", "Taburan renyah wangi"),
            ("Daun Bawang Iris", "1", "batang", "Taburan segar")
        ])
    ],
    "steps": [
        (1, "Haluskan Daging Paha Ayam & Bumbu Awal", "Masukkan 500 gr potongan paha ayam, 3 siung bawang putih, 2 batang irisan daun bawang, 1.5 sdm kecap asin, 1 sdm minyak wijen, 1 sdt gula pasir, 3/4 sdt garam, 1/2 sdt lada putih bubuk, air perasan jahe parut, dan 2 sdm air dingin ke dalam chopper atau food processor. Giling adonan secara bertahap hingga agak tercampur rata namun jangan terlalu lumat agar serat daging tetap bertekstur juicy.", 180),
        (2, "Campur Tepung Maizena ke Adonan", "Buka chopper, masukkan 1 sdm tepung maizena ke dalam adonan daging ayam. Nyalakan chopper kembali sebentar saja hingga tepung maizena menyatu rata dengan adonan. Jangan menggiling terlalu lama agar adonan tidak padat dan hasil rebusan pangsit tetap lembut dan juicy.", 60),
        (3, "Bungkus & Lipat Pangsit Bentuk Ingot", "Siapkan selembar kulit pangsit tipis. Letakkan 1 sendok teh adonan ayam di bagian tengah kulit. Olesi air tipis-tipis di sekeliling pinggir kulit sebagai perekat. Lipat kulit menjadi bentuk persegi panjang, rekatkan tepinya agar tidak ada udara terjebak, lalu pertemukan dan rekatkan kedua sudut bawahnya ke belakang (bentuk ingot perahu tradisional) agar mampu menampung isian daging melimpah. Ulangi sampai seluruh adonan habis.", 600),
        (4, "Rebus Kuah Kaldu Ceker & Bawang Geprek", "Siapkan panci kuah, masukkan 1.2 liter air bersih, 5 buah ceker ayam bersih, dan 4 siung bawang putih geprek. Rebus dengan api sedang hingga air mendidih dan buih kotoran muncul di permukaan, lalu bersihkan buihnya. Kecilkan api dan masak perlahan hingga sari kaldu ceker keluar gurih meresap (30-60 menit atau hingga 2 jam untuk kaldu super medok).", 1800),
        (5, "Bumbui Kuah Kaldu Hingga Pas", "Tambahkan 1.5 sdm kecap asin, 1/2 sdt lada putih bubuk, serta garam dan kaldu jamur/micin secukupnya ke dalam kuah kaldu ceker. Aduk rata dan koreksi rasa kuah hingga gurih segar beraroma bawang putih khas kuah mie ayam. Angkat ceker ayam atau biarkan di dalam kuah sesuai selera.", 180),
        (6, "Rebus Pangsit di Panci Terpisah", "Didihkan air yang cukup banyak di panci terpisah (jangan merebus langsung di kuah kaldu agar kuah tetap bening dan tidak keruh oleh tepung kulit pangsit). Masukkan pangsit mentah secukupnya ke air mendidih. Rebus selama 3-4 menit hingga kulit pangsit berubah licin transparan dan pangsit mengapung matang sempurna ke permukaan, lalu angkat dan tiriskan.", 240),
        (7, "Racik Pangsit & Siram Kuah Panas", "Tata pangsit rebus hangat di dalam mangkuk saji. Beri 1 sendok teh minyak bawang putih di atas pangsit, lalu siram dengan kuah kaldu ceker panas mendidih. Taburi atasnya dengan bawang putih goreng renyah dan irisan daun bawang segar. Nikmati selagi hangat gurih mantap!", 0)
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
    print(f"Updated recipe id: {r_id}")
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
    print(f"Inserted recipe id: {r_id}")

for g_idx, (g_name, items) in enumerate(recipe_data['groups']):
    cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (r_id, g_name, g_idx))
    g_id = cursor.lastrowid
    for i_idx, it in enumerate(items):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))

for st in recipe_data['steps']:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (r_id, st[0], st[1], st[2], st[3]))

conn.commit()
conn.close()
