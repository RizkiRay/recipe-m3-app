import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "cilok-isi-gajih-jando-bumbu-kacang-amb-sari",
    "title": "Cilok Isi Jando (Lemak Sapi Gurih) & Bumbu Kacang Kental",
    "chef": "Nita Ambarsari (@amb.sari)",
    "description": "Cilok kenyal empuk tidak keras saat dingin dengan isian potongan gajih / jando sapi gurih lumer berkaldu, disiram bumbu saus kacang kental legit gurih pedas khas jualan abang-abang.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DbyJ3tQBhta/",
    "servings": "30-40 Butir (Porsi Rumah Tangga / Jualan Kecil)",
    "prep_time": "30 menit",
    "cook_time": "40 menit",
    "calories": "Gurih Kenyal / Street Food Favorit",
    "groups": [
        ("Bahan Isian Jando Gurih", [
            ("Lemak Sapi / Tetelan Jando", "250", "gr", "Rebus empuk lalu potong dadu kecil"),
            ("Bawang Putih", "4", "siung", "Cincang halus"),
            ("Daun Bawang Segar", "2", "batang", "Iris halus"),
            ("Garam", "1/2", "sdt", "Penyeimbang gurih"),
            ("Kaldu Sapi Bubuk", "1", "sdt", "Penyedap rasa kaldu"),
            ("Merica Bubuk", "1/2", "sdt", "Aroma hangat"),
            ("Minyak Goreng", "2", "sdm", "Untuk menumis bumbu isian")
        ]),
        ("Bahan Adonan Biang & Kulit Cilok", [
            ("Tepung Tapioka / Kanji", "250", "gr", "Kunci tekstur kenyal lentur"),
            ("Tepung Terigu Protein Sedang", "250", "gr", "Pemberi struktur lembut empuk"),
            ("Bawang Putih Halus", "5", "siung", "Giling halus"),
            ("Daun Bawang", "3", "batang", "Iris tipis"),
            ("Garam Dapur", "1.5", "sdt", "Garam beryodium"),
            ("Kaldu Sapi / Ayam Bubuk", "1.5", "sdm", "Rasa gurih umami"),
            ("Merica Bubuk", "1", "sdt", "Aroma sedap"),
            ("Air Bersih", "450", "ml", "Rebus bersama bumbu biang hingga mendidih")
        ]),
        ("Bahan Saus Sambal Kacang Kental", [
            ("Kacang Tanah Goreng", "150", "gr", "Giling / blender halus bersama air"),
            ("Cabai Merah Keriting & Rawit", "10", "buah", "Rebus lalu haluskan"),
            ("Bawang Putih", "3", "siung", "Haluskan"),
            ("Gula Merah / Gula Jawa", "50", "gr", "Sisir halus"),
            ("Air Asam Jawa", "1", "sdm", "Penyegar rasa"),
            ("Garam", "1", "sdt", ""),
            ("Air Bersih", "300", "ml", "Untuk melarutkan kuah kacang"),
            ("Minyak Goreng", "3", "sdm", "Untuk menumis saus kacang")
        ])
    ],
    "steps": [
        (1, "Olah & Tumis Isian Gajih Jando", "Cuci bersih lemak sapi/jando. Rebus dalam air mendidih selama 15 menit hingga empuk dan lemak bening, lalu tiriskan dan potong dadu kecil-kecil. Panaskan 2 sdm minyak di wajan, tumis 4 siung bawang putih cincang hingga harum, masukkan potongan jando, irisan daun bawang, garam, kaldu sapi bubuk, dan merica. Aduk rata selama 3 menit hingga wangi gurih meresap, lalu angkat dan sisihkan.", 180),
        (2, "Rebus Kuah Kaldu Biang Bumbu", "Dalam panci, campurkan 450 ml air, 5 siung bawang putih halus, 1.5 sdt garam, 1.5 sdm kaldu bubuk, dan 1 sdt merica. Aduk rata lalu rebus hingga benar-benar mendidih bergolak.", 300),
        (3, "Buat Adonan Biang Tepung Terigu", "Kecilkan api kompor ke level paling kecil. Masukkan seluruh tepung terigu ke dalam panci air bumbu yang mendidih. Aduk cepat dan kuat menggunakan spatula kayu hingga adonan terigu menggumpal kalis menyatu (adonan biang basah). Matikan api dan biarkan uap panasnya berkurang sekitar 5 menit.", 180),
        (4, "Uleni Adonan Bersama Tepung Tapioka", "Pindahkan adonan biang terigu hangat ke dalam wadah baskom besar. Masukkan irisan daun bawang dan tepung tapioka secara bertahap sambil diuleni perlahan dengan tangan hingga tercampur rata, kalis, elastis, dan mudah dibentuk (jangan diuleni terlalu kuat/lama agar cilok tidak alot).", 240),
        (5, "Bentuk Bulatan & Beri Isian Jando", "Ambil sejumput adonan cilok (sekitar 15-20 gram), pipihkan di telapak tangan, lalu beri 1 sendok teh potongan isian jando gurih di bagian tengah. Rapatkan dan bulatkan adonan hingga permukaannya mulus dan tertutup rapat agar lemak tidak bocor saat direbus.", 0),
        (6, "Rebus Cilok Hingga Mengapung", "Didihkan air yang banyak dalam panci besar dengan tambahan 1 sdm minyak goreng agar cilok tidak saling menempel. Masukkan bulatan cilok satu per satu. Rebus dengan api sedang hingga cilok mengapung ke permukaan air (tanda adonan luar matang), biarkan mengapung selama 5 menit agar bagian dalam matang sempurna, lalu angkat dan tiriskan.", 600),
        (7, "Kukus Cilok di Dandang Agar Awet Lembut", "Pindahkan cilok yang sudah direbus ke dalam dandang/kukusan yang sudah dipanaskan. Kukus cilok dengan api sedang-kecil selama 15-20 menit hingga cilok benar-benar tanak, empuk lembut, dan aroma jando semerbak.", 900),
        (8, "Masak Saus Bumbu Kacang Kental", "Panaskan 3 sdm minyak di wajan. Masukkan bumbu halus (cabai dan bawang putih), tumis hingga harum matang. Masukkan kacang tanah halus, air, gula merah sisir, air asam jawa, dan garam. Aduk terus menggunakan whisk/spatula dengan api kecil hingga saus mengental, meletup-letup, dan mengeluarkan minyak kemerahan yang sedap.", 480),
        (9, "Sajikan Cilok Hangat dengan Bumbu Kacang", "Ambil cilok jando hangat dari kukusan, tata di piring atau mangkuk saji, lalu siram dengan saus bumbu kacang kental melimpah. Tambahkan kecap manis dan saus sambal sesuai selera. Nikmati selagi hangat kenyal gurih lumer!", 0)
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
print("Successfully saved Cilok Jando recipe to SQLite DB!")
