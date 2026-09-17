import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

recipe_data = {
    "slug": "ikan-bakar-teflon-sambel-terasi-alangtyaz",
    "title": "Ikan Bakar Teflon Bumbu Oles Sambal Terasi",
    "chef": "@alang_tyaz",
    "description": "Ikan bakar teflon beralas daun pisang dengan bumbu oles manis gurih meresap (kecap manis, saus tomat, bawang putih bubuk, merica) dan cocolan sambal terasi segar.",
    "youtube_id": "",
    "media_url": "https://www.instagram.com/reel/DdYieOPMrVf/",
    "servings": "2-3 Porsi",
    "prep_time": "15 menit",
    "cook_time": "20 menit panggang",
    "calories": "Ikan Bakar Teflon Rumahan",
    "groups": [
        ("Bahan Utama Ikan", [
            ("Ikan Segar (Ikan Mas / Nila / Gurame / Mujaer)", "2-3", "ekor (±600 gr)", "Bersihkan & belah punggung/kupu-kupu"),
            ("Air Jeruk Nipis & Garam", "1", "buah", "Untuk melumuri ikan sebelum dipanggang"),
            ("Daun Pisang Segar", "2", "lembar", "Untuk alas wajan teflon agar aroma wangi & tidak gosong")
        ]),
        ("Bumbu Oles Manis Gurih (Hasil Transkrip Voiceover)", [
            ("Minyak Goreng", "2-3", "sdm", "Base bumbu oles"),
            ("Kecap Manis", "3-4", "sdm", "Memberi warna karamel manis"),
            ("Saus Tomat", "2", "sdm", "Memberi rasa asam segar seimbang"),
            ("Bawang Putih Bubuk (Desaku)", "1", "sachet", "Aroma gurih bawang"),
            ("Bumbu Marinasi Ikan", "1/2", "sachet", ""),
            ("Merica / Lada Bubuk (Ladaku)", "1/2", "sdt", ""),
            ("Gula Pasir & Garam", "1/2", "sdt", "")
        ]),
        ("Bahan Cocolan Sambal Terasi", [
            ("Cabai Rawit Merah & Hijau", "15", "buah", ""),
            ("Bawang Merah & Bawang Putih", "4", "siung", "Goreng layu"),
            ("Terasi Bakar", "1", "sdt", "Aroma sedap"),
            ("Tomat Merah Segar", "1", "buah", ""),
            ("Garam & Gula Merah", "secukupnya", "", "")
        ])
    ],
    "steps": [
        (1, "Bersihkan & Belah Ikan", "Bersihkan sisik dan isi perut ikan, cuci hingga bersih. Belah ikan dari punggung (bentuk bekakak/kupu-kupu) agar matang merata saat dipanggang. Lumuri dengan perasan jeruk nipis dan sedikit garam.", 0),
        (2, "Racik Bumbu Olesan", "Dalam mangkuk, campurkan minyak goreng, kecap manis, saus tomat, 1 sachet bawang putih bubuk, 1/2 sachet bumbu marinasi, 1/2 sdt merica bubuk, gula pasir, dan garam. Aduk rata (diudak-udak) hingga tercampur sempurna.", 0),
        (3, "Balur Bumbu ke Seluruh Ikan", "Oleskan dan balurkan bumbu racikan secara tebal dan merata ke seluruh permukaan daging dan kulit ikan. Diamkan 10 menit agar bumbu meresap ke serat daging.", 0),
        (4, "Panggang di Atas Daun Pisang", "Panaskan wajan teflon, beri alas 1-2 lembar daun pisang. Letakkan ikan berbumbu di atas daun pisang. Panggang dengan api kecil-sedang sambil terus diolesi sisa bumbu bolak-balik selama 15–20 menit hingga matang empuk, juicy, dan beraroma wangi daun terbakar.", 900),
        (5, "Racik Sambal Terasi & Sajikan", "Ulek cabai, bawang goreng, tomat, terasi bakar, garam, dan gula merah hingga menjadi sambal terasi yang mantap. Sajikan ikan bakar teflon panas bersama nasi hangat dan cocolan sambal terasi!", 0)
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
    print(f"Added transcribed recipe: {recipe_data['title']}")

conn.commit()
conn.close()
