import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

additional_gold_recipes = [
    {
        "slug": "ayam-songkem-madura-firhan",
        "title": "Ayam Songkem Madura Pedas Gurih",
        "chef": "@firhanmci6",
        "description": "Resep Ayam Songkem khas Madura ala Chef @firhanmci6: ayam utuh dibalut sambal cabai bawang minyak panas dan dikukus berbungkus daun pisang.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/DQyd_mtiZpz/",
        "servings": "4-5 Porsi",
        "prep_time": "20 menit",
        "cook_time": "50 menit kukus",
        "calories": "Authentic Madura Steamed Chicken",
        "groups": [
            ("Bahan Marinasi Ayam", [
                ("Ayam Pejantan Besar (Belah bekakak)", "1", "ekor", "Cuci bersih & tiriskan"),
                ("Saus Tiram", "2", "sdm", ""),
                ("Minyak Wijen", "2", "sdm", "Pengharum alami"),
                ("Tepung Tapioka", "4", "sdm", "Mengunci kelembapan sari ayam"),
                ("Garam", "1.5", "sdt", ""),
                ("Lada Bubuk", "1", "sdt", "")
            ]),
            ("Bahan Sambal Songkem", [
                ("Cabai Merah Keriting", "35", "buah", "Cincang kasar"),
                ("Cabai Rawit Merah", "15", "buah", "Pedas nampol"),
                ("Bawang Merah", "15", "butir", ""),
                ("Bawang Putih", "10", "butir", ""),
                ("Daun Bawang (Iris)", "2", "batang", ""),
                ("Terasi Bakar", "2", "sdt", "Aroma sedap khas Madura"),
                ("Minyak Panas Mendidih", "80", "ml", "Untuk menyiram bumbu aromatik"),
                ("Kaldu Ayam Bubuk", "2", "sdt", ""),
                ("Gula Pasir", "3", "sdt", ""),
                ("Penyedap Rasa / MSG", "2", "sdt", ""),
                ("Garam", "1", "sdt", "")
            ]),
            ("Bahan Pelengkap Bungkus", [
                ("Daun Pisang Lebar (Layu di atas api)", "secukupnya", "lembar", "Untuk membungkus rapat"),
                ("Batang Sereh (Memarkan)", "2", "batang", ""),
                ("Daun Salam", "6", "lembar", "")
            ])
        ],
        "steps": [
            (1, "Marinasi Ayam Pejantan", "Lumuri 1 ekor ayam pejantan dengan saus tiram, minyak wijen, garam, lada bubuk, dan tepung tapioka. Balurkan merata ke seluruh badan dan rongga ayam, lalu diamkan 15 menit.", 0),
            (2, "Cincang Bumbu Sambal & Siram Minyak Panas", "Cincang kasar bawang merah, bawang putih, cabai merah keriting, cabai rawit, dan daun bawang di chopper. Pindahkan ke mangkuk, bumbui terasi, kaldu ayam bubuk, gula, garam, dan penyedap. Siram dengan 80 ml minyak panas mendidih, lalu aduk rata.", 0),
            (3, "Balur Ayam dengan Sambal Tebal", "Balurkan seluruh racikan sambal ke seluruh permukaan ayam hingga tertutup bumbu tebal dan meresap.", 0),
            (4, "Bungkus Rapat Daun Pisang", "Bentangkan daun pisang lebar. Taruh sereh memar dan daun salam di bagian dasar, letakkan ayam berbumbu di atasnya, lalu bungkus rapat dan semat kedua ujungnya dengan lidi/tusuk gigi.", 0),
            (5, "Kukus hingga Empuk Berkaldu", "Kukus ayam songkem selama 45–60 menit dengan api sedang hingga daging ayam pejantan empuk lembut dan mengeluarkan kaldu aromatik yang sedap.", 3000),
            (6, "Sajikan", "Buka bungkusan daun pisang selagi panas mengepul. Sajikan ayam songkem bersama nasi hangat dan siramkan kuah sambalnya!", 0)
        ]
    },
    {
        "slug": "infused-shrimp-oil-leyosatria",
        "title": "Infused Shrimp Oil (Minyak Kulit & Kepala Udang)",
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
    },
    {
        "slug": "crispy-salt-roasted-chicken-bones",
        "title": "Crispy Salt-Roasted Chicken Bones (Xương Gà Rang Muối)",
        "chef": "Phương Phương (@emmersweet)",
        "description": "Camilan renyah krispi gurih khas Vietnam dari tulang ayam/kerongkong yang dibumbui rempah dan digoreng sangrai garam.",
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
            ("Bahan Pelapis & Bumbu Rang Muối", [
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
    },
    {
        "slug": "tahu-bulat-kopong-tasikmalaya",
        "title": "Tahu Bulat Kopong Gurih Renyah",
        "chef": "@nikadewanti",
        "description": "Resep tahu bulat kopong renyah dan gurih khas tasikmalaya, anti kempis saat digoreng.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/DOsLlG6EqLX/",
        "servings": "20-25 Butir Tahu Bulat",
        "prep_time": "20 menit",
        "cook_time": "15 menit goreng",
        "calories": "Indonesian Streetfood",
        "groups": [
            ("Bahan Tahu Bulat Kopong", [
                ("Tahu Putih Segar (Peras airnya dengan kain)", "10", "buah (±500 gr)", "Wajib diperas sampai benar-benar kering"),
                ("Kuning Telur", "1", "butir", "Pengikat adonan & melembutkan"),
                ("Bawang Putih Bubuk", "1/2", "sdt", ""),
                ("Merica / Lada Bubuk", "1/2", "sdt", ""),
                ("Baking Powder Double Acting", "1/2", "sdt", "Kunci tahu mengembang kopong"),
                ("Garam Dapur", "1/2", "sdt", ""),
                ("Gula Pasir & Kaldu Bubuk", "1/2", "sdm", ""),
                ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
            ])
        ],
        "steps": [
            (1, "Peras Air Tahu hingga Kering", "Hancurkan tahu putih, lalu bungkus dengan kain bersih atau serbet tipis. Peras sekuat tenaga hingga air di dalam tahu keluar maksimal dan ampas tahu benar-benar kering.", 0),
            (2, "Bumbui & Uleni Adonan", "Campurkan ampas tahu kering dengan kuning telur, bawang putih bubuk, merica bubuk, garam, gula pasir, kaldu bubuk, dan baking powder. Aduk dan uleni hingga adonan halus kalis.", 0),
            (3, "Bulatkan Tahu", "Ambil sejumput adonan tahu, bulatkan dengan telapak tangan hingga licin dan mulus tanpa retakan (ukuran sebesar bola pingpong).", 0),
            (4, "Simpan di Kulkas (Chiller)", "Tata bola tahu di wadah tertutup, simpan di kulkas minimal 1-2 jam agar adonan set dan baking powder bereaksi sempurna.", 3600),
            (5, "Goreng dari Minyak Hangat", "Masukkan bola tahu ke dalam wajan berisi minyak yang masih hangat (api kecil). Aduk-aduk terus perlahan. Saat tahu mulai mengembang dan mengapung, besarkan ke api sedang. Goreng sambil terus diaduk bolak-balik selama 10-15 menit hingga kulitnya kering garing kecokelatan. Angkat dan tiriskan!", 600)
        ]
    },
    {
        "slug": "nori-gulung-udang-crispy-snack",
        "title": "Nori Gulung Udang Crispy (Snack Anak & Keluarga)",
        "chef": "@radigafams",
        "description": "Olahan udang cincang gurih berbalut lembaran rumput laut nori renyah, favorit anak-anak dan kaya protein.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/DLmX-4gP-X_/",
        "servings": "3 Porsi Camilan",
        "prep_time": "15 menit",
        "cook_time": "10 menit panggang teflon",
        "calories": "High Protein Kids Snack",
        "groups": [
            ("Bahan Adonan Udang Nori", [
                ("Daging Udang Kupas Segar", "200", "gr", "Cincang halus / chopper"),
                ("Wortel Rebus (Cincang halus)", "2", "sdm", "Nutrisi sayur untuk anak"),
                ("Jagung Manis Rebus (Pipil)", "2", "sdm", "Memberi rasa manis alami"),
                ("Daun Bawang (Iris tipis)", "1", "batang", ""),
                ("Tepung Tapioka / Maizena", "1.5", "sdm", "Pengikat adonan kenyal"),
                ("Kaldu Jamur / Penyedap Rasa", "1/2", "sdt", ""),
                ("Minyak Wijen & Garam", "1/2", "sdt", "Pengharum adonan"),
                ("Lembaran Nori / Rumput Laut Panggang", "secukupnya", "lembar", "Gunting sesuai ukuran"),
                ("Minyak Goreng", "secukupnya", "sdm", "Untuk olesan pan teflon")
            ])
        ],
        "steps": [
            (1, "Haluskan Daging Udang", "Masukkan 200 gr udang kupas ke dalam chopper atau cincang halus dengan pisau hingga bertekstur pasta lengket.", 0),
            (2, "Campur Sayuran & Bumbu", "Campurkan pasta udang dengan wortel cincang, jagung manis pipil, daun bawang, tepung tapioka, kaldu jamur, garam, dan minyak wijen. Aduk rata hingga menjadi adonan kalis.", 0),
            (3, "Bungkus dengan Lembaran Nori", "Ambil selembar nori, ratakan adonan udang di atasnya, lalu gulung atau lipat rapat membentuk persegi panjang/silinder.", 0),
            (4, "Panggang di Pan Teflon", "Panaskan teflon anti-lengket dengan sedikit olesan minyak. Panggang nori udang di atas api kecil-sedang selama 3-4 menit tiap sisi hingga udang matang kemerahan dan nori krispi harum.", 360),
            (5, "Sajikan", "Angkat dan potong-potong sesuai gigitan anak. Sajikan hangat sebagai camilan sehat penambah nafsu makan si kecil!", 0)
        ]
    },
    {
        "slug": "crispy-potato-rings-iramsfoodstory",
        "title": "Crispy Potato Rings (Cincang Kentang Renyah Gurih)",
        "chef": "@iramsfoodstory",
        "description": "Camilan cincin kentang goreng renyah bumbu peterseli lada hitam yang gurih krispi.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/Dbf3m9UTLQi/",
        "servings": "3 Porsi",
        "prep_time": "20 menit",
        "cook_time": "15 menit goreng",
        "calories": "Crispy Potato Snack",
        "groups": [
            ("Bahan Adonan Kentang Ring", [
                ("Kentang Besar (Kupas & Rebus empuk)", "3", "buah (±450 gr)", "Haluskan tanpa gumpalan"),
                ("Tepung Maizena (Cornstarch)", "6-8", "sdm", "Pengikat adonan krispi"),
                ("Tepung Terigu Serbaguna", "2", "sdm", ""),
                ("Susu Cair / Air", "1-2", "sdm", "Gunakan jika adonan terlalu kering"),
                ("Garam Halus", "1/2", "sdt", ""),
                ("Chili Flakes (Cabai bubuk kasar)", "1", "sdt", ""),
                ("Kaldu Ayam Bubuk", "1/2", "sdm", ""),
                ("Bawang Putih Bubuk", "1", "sdm", ""),
                ("Lada Hitam Bubuk", "1/2", "sdt", ""),
                ("Peterseli / Parsley Cincang", "1", "sdm", ""),
                ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
            ])
        ],
        "steps": [
            (1, "Kupas & Rebus Kentang", "Kupas kentang dan potong dadu. Rebus dalam air mendidih bergaram selama 12–15 menit hingga empuk lembut saat ditusuk garpu.", 720),
            (2, "Tiriskan & Haluskan", "Tiriskan kentang hingga uap air menguap kering. Haluskan kentang selagi hangat sampai lembut tanpa gumpalan.", 0),
            (3, "Bumbui & Campur Tepung", "Masukkan garam, kaldu ayam bubuk, chili flakes, bawang putih bubuk, lada hitam, dan peterseli cincang. Tambahkan 2 sdm terigu dan 6-8 sdm maizena (tambahkan 1-2 sdm susu jika terlalu kering). Aduk hingga kalis elastis.", 0),
            (4, "Bentuk Cincin (Ring)", "Ambil sedikit adonan, bulatkan lalu pipihkan tebal. Gunakan spuit/sumpit untuk melubangi bagian tengahnya hingga membentuk cincin rapi.", 0),
            (5, "Dinginkan di Kulkas (30 Menit)", "Tata cincin kentang di atas nampan dan simpan di chiller kulkas selama 30 menit agar kokoh dan tidak hancur saat digoreng.", 1800),
            (6, "Goreng Deep-Fry Crispy", "Panaskan minyak pada suhu 175°C. Goreng cincin kentang secara bertahap selama 3–4 menit hingga kuning keemasan dan super renyah. Tiriskan dan sajikan hangat!", 240)
        ]
    }
]

for r_data in additional_gold_recipes:
    cursor.execute("SELECT id FROM recipes WHERE slug = ?", (r_data['slug'],))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r_data['slug'], r_data['title'], r_data['chef'], r_data['description'],
            r_data['youtube_id'], r_data['media_url'], r_data['servings'],
            r_data['prep_time'], r_data['cook_time'], r_data['calories']
        ))
        r_id = cursor.lastrowid
        for g_idx, (g_name, items) in enumerate(r_data['groups']):
            cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (r_id, g_name, g_idx))
            g_id = cursor.lastrowid
            for i_idx, it in enumerate(items):
                cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))
        for st in r_data['steps']:
            cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (r_id, st[0], st[1], st[2], st[3]))
        print(f"Added Gold-Standard Recipe: {r_data['title']}")

conn.commit()
conn.close()
