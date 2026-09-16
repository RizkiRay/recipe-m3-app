import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "recipes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        chef TEXT,
        description TEXT,
        youtube_id TEXT,
        media_url TEXT,
        servings TEXT,
        prep_time TEXT,
        cook_time TEXT,
        calories TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredient_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        amount TEXT,
        unit TEXT,
        notes TEXT,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (group_id) REFERENCES ingredient_groups(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        step_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        detail TEXT NOT NULL,
        timer_seconds INTEGER DEFAULT 0,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)

    recipes_seed = [
        {
            "slug": "egg-chicken-roll-hokben",
            "title": "Egg Chicken Roll ala HokBen",
            "chef": "Chef Devina Hermawan",
            "description": "Juicy, gurih, kulit empuk berserat lembut, cocok untuk stok lauk beku (frozen food) keluarga.",
            "youtube_id": "ShLeN8usfg8",
            "media_url": "https://youtu.be/ShLeN8usfg8",
            "servings": "4-5 Gulung (±25-30 potong)",
            "prep_time": "25 menit",
            "cook_time": "20 menit kukus + 5 menit goreng",
            "calories": "Cocok untuk stok lauk",
            "groups": [
                ("Bahan Kulit", [
                    ("Telur (atau 1 utuh + 2 kuning)", "2", "butir", "Gunakan 2 putih telur untuk isian daging"),
                    ("Tepung Terigu", "80", "gr", "Protein sedang"),
                    ("Tepung Maizena", "40", "gr", ""),
                    ("Air", "250-280", "ml", "Sesuaikan kekentalan adonan"),
                    ("Minyak Goreng", "2", "sdm", "Campur ke adonan agar tidak lengket"),
                    ("Garam", "1/2", "sdt", ""),
                    ("Kaldu Bubuk", "1/2", "sdt", ""),
                    ("Pewarna Kuning Makanan", "secukupnya", "", "Opsional agar warna cantik")
                ]),
                ("Bahan Isian Daging", [
                    ("Paha Ayam Fillet", "600", "gr", "Keringkan dengan tisu dapur sebelum digiling"),
                    ("Putih Telur", "2", "butir", "Bikin tekstur kenyal dan juicy"),
                    ("Bawang Putih", "5-6", "siung", "Cincang halus"),
                    ("Bawang Goreng", "2", "sdm", "Opsional untuk aroma"),
                    ("Minyak Wijen", "1", "sdm", "Aroma khas HokBen"),
                    ("Bubuk Pala / Ngohiong", "1/2", "sdt", "Opsional"),
                    ("Garam", "1-2", "sdt", "Giling di awal bersama daging"),
                    ("Gula Pasir", "1", "sdm", ""),
                    ("Kaldu Bubuk / MSG", "1", "sdt", ""),
                    ("Lada Putih Bubuk", "1/2", "sdt", ""),
                    ("Es Batu / Air Es", "50-70", "gr", "Menjaga adonan tetap dingin saat digiling"),
                    ("Tepung Maizena", "2-3", "sdm", ""),
                    ("Roti Tawar + Air/Susu 50ml", "2", "lembar", "Opsional: melembutkan tekstur daging")
                ]),
                ("Perekat & Pelengkap", [
                    ("Campuran Terigu + Air", "secukupnya", "", "Lem ujung kulit"),
                    ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
                ])
            ],
            "steps": [
                (1, "Buat Adonan Kulit", "Campur terigu, maizena, telur, air, minyak, garam, kaldu bubuk, dan pewarna kuning. Aduk rata menggunakan whisk hingga licin tanpa gumpalan, lalu saring.", 0),
                (2, "Dadar Kulit Dadar", "Panaskan wajan teflon anti-lengket (api kecil-sedang). Tuang 1 centong adonan, putar wajan hingga rata. Masak sampai pinggir kulit terkelupas sendiri. Angkat dan dinginkan. Ulangi sampai adonan habis.", 0),
                (3, "Giling Daging Pertama", "Keringkan paha ayam fillet. Masukkan ayam, garam, gula, dan kaldu bubuk ke dalam food processor. Giling 2-3 menit sampai serat protein pecah dan tekstur lengket/bouncy.", 180),
                (4, "Bumbui Isian", "Masukkan bawang putih cincang, bawang goreng, lada, bubuk pala, minyak wijen, putih telur, maizena, dan es batu. Giling rata kembali.", 0),
                (5, "Tambahkan Roti Lembut (Opsional)", "Rendam 2 lembar roti tawar dengan 50 ml air/susu. Masukkan ke adonan daging dan giling sebentar sampai menyatu lembut.", 0),
                (6, "Gulung Daging & Kulit", "Ambil selembar kulit dadar (diameter ±26-28cm). Ratakan adonan ayam memanjang di bagian bawah. Gulung 1 putaran, lipat sisi kiri dan kanan ke dalam, gulung rapat. Oleskan larutan terigu sebagai lem di ujungnya.", 0),
                (7, "Kukus Roll", "Siapkan kukusan yang dialasi baking paper/dioles minyak. Kukus Egg Chicken Roll selama 15-20 menit hingga matang. Angkat dan biarkan dingin sempurna agar set & mudah dipotong.", 1200),
                (8, "Potong & Goreng", "Potong serong roll yang sudah dingin. Goreng dalam minyak panas dengan api sedang hingga kuning keemasan dan renyah di luar. Sajikan hangat dengan salad dan saus!", 300)
            ]
        },
        {
            "slug": "ayam-rebus-jahe-bawang-putih",
            "title": "Ayam Rebus Jahe Bawang Putih",
            "chef": "@hendrywijayaa",
            "description": "Dada ayam rebus super empuk, lembut, juicy berkat teknik maizena & baking soda, disiram saus jahe bawang putih pedas gurih.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/DdGXJI4Bb4n/",
            "servings": "1 Porsi (High Protein)",
            "prep_time": "10 menit",
            "cook_time": "5 menit rebus",
            "calories": "675 kcal (+175g nasi) | Protein 51g",
            "groups": [
                ("Bahan Utama & Marinasi Ayam", [
                    ("Dada Ayam Fillet (Iris tipis melebar)", "200", "gr", "Potong berlawanan serat"),
                    ("Tepung Maizena", "25", "gr", "Kunci tekstur daging lembut velvety saat direbus"),
                    ("Baking Soda", "secukupnya", "sejumput", "Melembutkan serat protein daging ayam")
                ]),
                ("Bahan Racikan Saus Jahe Bawang Putih", [
                    ("Bawang Putih (Cincang halus)", "5", "gr", "±2 siung"),
                    ("Jahe (Cincang halus/parut)", "5", "gr", "Aroma segar khas oriental"),
                    ("Daun Bawang (Iris halus)", "10", "gr", ""),
                    ("Cabe Rawit (Iris halus)", "5", "gr", "Sesuaikan level pedas"),
                    ("Chili Flakes / Bubuk Cabe Kasar", "2", "gr", ""),
                    ("Chili Powder", "secukupnya", "", "Opsional untuk warna merah menggoda"),
                    ("Saus Tiram", "10", "gr", "±1 sdm"),
                    ("Minyak Wijen", "3", "gr", "±1 sdt"),
                    ("Gula Pasir", "3", "gr", ""),
                    ("Garam", "3", "gr", ""),
                    ("MSG / Kaldu Jamur", "3", "gr", ""),
                    ("Minyak Panas", "5", "gr", "Untuk menyiram bumbu aromatik agar wangi keluar")
                ])
            ],
            "steps": [
                (1, "Iris & Marinasi Dada Ayam", "Iris tipis melebar 200 gr dada ayam fillet. Taburi 25 gr tepung maizena dan sejumput baking soda. Balurkan rata hingga seluruh permukaan ayam terlapisi tipis.", 0),
                (2, "Racik Bumbu Aromatik", "Dalam mangkuk tahan panas, campurkan bawang putih cincang, jahe cincang, irisan daun bawang, cabe, chili flakes, chili powder, gula, garam, MSG, dan saus tiram.", 0),
                (3, "Siram Minyak Panas & Minyak Wijen", "Panaskan 5-10 ml minyak goreng hingga berasap tipis. Siramkan minyak panas ke atas mangkuk bumbu aromatik agar aroma jahe dan bawang keluar semerbak. Tambahkan minyak wijen, lalu aduk rata.", 0),
                (4, "Rebus Dada Ayam", "Didihkan air secukupnya dalam panci. Masukkan irisan dada ayam yang sudah dimarinasi maizena satu per satu. Rebus dengan api sedang selama 3-5 menit hingga ayam matang dan putih empuk.", 240),
                (5, "Tiriskan & Tuang Saus", "Angkat dan tiriskan dada ayam rebus ke dalam piring saji. Tuangkan racikan saus jahe bawang putih di atasnya. Sajikan selagi hangat bersama 175 gr nasi putih hangat!", 0)
            ]
        },
        {
            "slug": "gil-gamja-kentang-panjang",
            "title": "Gil Gamja (Korean Long Potato Stick)",
            "chef": "@michelealex",
            "description": "Camilan kentang panjang khas Korea yang renyah di luar, kenyal lembut di dalam. Sangat murah meriah, satset, dan cocok untuk ide jualan keluarga.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/p/DbQIRBfP6Qd/",
            "servings": "10 Porsi",
            "prep_time": "15 menit",
            "cook_time": "10 menit goreng",
            "calories": "Crispy & Chewy Korean Snack",
            "groups": [
                ("Bahan Adonan Kentang", [
                    ("Kentang (Kupas & Potong)", "500", "gr", "Pilih kentang pulen"),
                    ("Air", "162", "gr", "Untuk memblender kentang"),
                    ("Tepung Tapioka", "125", "gr", "Kunci tekstur kenyal elastis"),
                    ("Garam", "2/3", "sdt", ""),
                    ("Kaldu Bubuk", "1/2", "sdt", "")
                ]),
                ("Bahan Saus Mayo Pedas", [
                    ("Mayones", "6", "sdm", ""),
                    ("Saus Sambal", "6", "sdm", ""),
                    ("Kental Manis", "1-2", "sdm", "Memberi rasa creamy manis gurih"),
                    ("Perasan Jeruk Nipis", "1", "sdt", "Menyeimbangkan rasa agar segar")
                ])
            ],
            "steps": [
                (1, "Haluskan Kentang", "Masukkan 500 gr kentang yang sudah dikupas dan dipotong bersama 162 gr air ke dalam blender. Blender hingga halus dan cair merata.", 0),
                (2, "Masak Bubur Kentang", "Tuangkan jus kentang ke dalam pan anti-lengket. Masak di atas api kecil-sedang sambil terus diaduk hingga mengental, kenyal, dan berwarna transparan.", 300),
                (3, "Campur Tapioka & Bumbu", "Matikan api. Masukkan 125 gr tepung tapioka, 2/3 sdt garam, dan 1/2 sdt kaldu bubuk. Aduk cepat hingga adonan kalis dan menyatu sempurna.", 0),
                (4, "Bentuk & Goreng Panjang", "Masukkan adonan kentang hangat ke dalam piping bag / plastik segitiga. Panaskan minyak goreng. Gunting ujung piping bag, lalu tekan adonan langsung memanjang ke dalam minyak panas sambil digunting. Goreng di api sedang hingga garing keemasan.", 420),
                (5, "Racik Saus Mayo & Sajikan", "Campurkan mayones, saus sambal, kental manis, dan perasan jeruk nipis hingga rata. Sajikan Gil Gamja panas renyah dengan cocolan saus mayo pedas!", 0)
            ]
        },
        {
            "slug": "sosis-jumbo-homemade",
            "title": "Sosis Jumbo Ayam Homemade (Membal & Kenyal)",
            "chef": "@icenguik",
            "description": "Resep sosis ayam jumbo rumahan dengan formula membal kenyal tanpa rongga udara, cocok untuk stok sarapan atau frozen food sehat.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/DYi0LHDu-8-/",
            "servings": "2 Lonjor Jumbo (50cm, casing 92mm)",
            "prep_time": "30 menit",
            "cook_time": "45 menit kukus/slow boil",
            "calories": "High Protein Homemade Sausage",
            "groups": [
                ("Bahan Daging & Emulsi", [
                    ("Dada Ayam Fillet", "500", "gr", "Giling halus"),
                    ("Paha Ayam Fillet", "150", "gr", "Memberi kelembapan & lemak alami"),
                    ("Lemak Ayam / Sapi / Lard", "50", "gr", "Opsional (versi lean bisa di-skip)"),
                    ("Putih Telur", "50", "gr", "Pengikat protein"),
                    ("Air Es / Es Serut", "190", "gr", "Menjaga suhu adonan tetap dingin saat emulsi")
                ]),
                ("Bumbu & Pelengkap Casing", [
                    ("Garam", "1.5", "sdm", "Penting untuk ekstraksi aktomiosin protein"),
                    ("Gula Pasir", "1", "sdm", ""),
                    ("Bawang Putih Bubuk", "1", "sdm", ""),
                    ("Lada Putih Bubuk", "1", "sdt", ""),
                    ("Pala Bubuk / Ketumbar Bubuk", "1/2", "sdt", ""),
                    ("Tepung Tapioka / Maizena", "50", "gr", ""),
                    ("Casing Sosis Kolagen/Selulosa 92mm", "1", "meter", "Potong @50cm")
                ])
            ],
            "steps": [
                (1, "Giling & Ekstraksi Protein Daging", "Masukkan dada dan paha ayam ke food processor bersama garam. Giling 2-3 menit hingga daging lengket, padat, dan elastis (protein aktomiosin terekstrak).", 180),
                (2, "Emulsikan dengan Es Batu & Bumbu", "Masukkan es batu serut, putih telur, lemak ayam, bawang putih bubuk, lada, pala, dan gula. Proses hingga menjadi pasta emulsi halus mengkilap.", 120),
                (3, "Campurkan Tepung Pengikat", "Tambahkan tepung tapioka/maizena, blender sebentar hingga adonan tercampur rata tanpa gelembung udara besar.", 60),
                (4, "Stuffing ke Dalam Casing", "Masukkan adonan ke dalam piping bag atau alat stuffer. Masukkan ke dalam casing sosis jumbo 92mm. Padatkan rapat dan ikat ujung-ujungnya dengan tali benang dapur.", 0),
                (5, "Pemanasan Lambat (Slow Poaching)", "Kukus atau rebus sosis dalam air bersuhu 75°-80°C (jangan sampai mendidih bergolak) selama 40-45 menit hingga bagian dalam mencapai kematangan sempurna. Angkat dan rendam di air es agar casing kencang.", 2400),
                (6, "Penyajian / Simpan", "Sosis jumbo siap dipotong-potong dan dipanggang di teflon dengan mentega, atau disimpan di freezer untuk stok lauk.", 300)
            ]
        },
        {
            "slug": "takoyaki-ala-gindaco",
            "title": "Takoyaki Crispy Gurih ala Gindaco",
            "chef": "@hildansl",
            "description": "Takoyaki premium dengan adonan gurih dashi, renyah di luar, lumer lembut di dalam, lengkap dengan racikan saus takoyaki spesial.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/DWqNXm1jhnb/",
            "servings": "20-25 Butir Takoyaki",
            "prep_time": "15 menit",
            "cook_time": "15 menit memanggang",
            "calories": "Streetfood Favorit",
            "groups": [
                ("Bahan Adonan Takoyaki", [
                    ("Tepung Terigu", "200", "gr", "Protein sedang"),
                    ("Tepung Maizena", "20", "gr", "Bikin luar tetap crispy"),
                    ("Telur Ayam", "2", "butir", ""),
                    ("Dashi Powder", "2", "sdm", "Kaldu ikan cakalang Jepang"),
                    ("Kecap Asin / Shoyu", "1", "sdm", ""),
                    ("Kaldu Jamur", "1/2", "sdt", ""),
                    ("Baking Powder", "1/2", "sdt", ""),
                    ("Air Bersih", "600", "ml", "Adonan cair encer khas takoyaki")
                ]),
                ("Bahan Isian & Topping", [
                    ("Gurita / Sosis / Keju (Potong dadu)", "150", "gr", "Isian utama"),
                    ("Daun Bawang (Iris halus)", "3", "batang", ""),
                    ("Katsuobushi (Serutan cakalang)", "secukupnya", "", "Topping menari di atas takoyaki"),
                    ("Mayones Pedas/Original", "secukupnya", "", ""),
                    ("Aonori / Bubuk Rumput Laut", "secukupnya", "", "")
                ]),
                ("Racikan Saus Takoyaki", [
                    ("Kecap Inggris (Worcestershire)", "100", "ml", ""),
                    ("Saus Tiram", "50", "ml", ""),
                    ("Saus Tomat / Gula", "2", "sdm", "")
                ])
            ],
            "steps": [
                (1, "Campur Adonan Cair", "Campurkan tepung terigu, maizena, dashi powder, kecap asin, kaldu jamur, baking powder, telur, dan air. Aduk rata menggunakan whisk hingga benar-benar encer dan tidak bergerindil, lalu saring.", 0),
                (2, "Panaskan Cetakan Takoyaki", "Panaskan cetakan takoyaki, olesi minyak cukup banyak ke seluruh lubang agar hasil luar takoyaki renyah keemasan.", 0),
                (3, "Tuang Adonan & Masukkan Isian", "Tuangkan adonan hingga lubang terisi penuh. Masukkan potongan gurita/sosis/keju dan taburi daun bawang cincang melimpah.", 0),
                (4, "Putar & Bulatkan Takoyaki", "Saat bagian bawah mulai berkulit, gunakan tusuk sate untuk memutar takoyaki 90 derajat. Masukkan sisa adonan di pinggiran ke dalam bola, putar perlahan hingga membentuk bola bulat sempurna.", 480),
                (5, "Panggang hingga Crispy", "Tambahkan sedikit minyak di pinggiran cetakan, putar-putar terus hingga seluruh permukaan takoyaki berwarna cokelat keemasan dan renyah.", 300),
                (6, "Beri Saus & Topping", "Angkat ke piring saji. Olesi dengan saus takoyaki, semprot mayones, taburi bubuk aonori, dan beri katsuobushi melimpah di atasnya!", 0)
            ]
        },
        {
            "slug": "ikan-bakar-bima-ntb",
            "title": "Ikan Bakar Khas Bima NTB",
            "chef": "@nenglisaindo",
            "description": "Ikan kakap bakar khas Bima dengan bumbu rempah bakar asam manis pedas gurih yang meresap sempurna sampai ke dalam daging ikan.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/Dcdgpspy1Zk/",
            "servings": "3-4 Porsi",
            "prep_time": "20 menit",
            "cook_time": "15 menit bakar",
            "calories": "Traditional Indonesian Grilled Fish",
            "groups": [
                ("Bahan Utama", [
                    ("Ikan Kakap Merah (Red Snapper)", "700", "gr", "Bersihkan, kerat-kerat badannya"),
                    ("Air Jeruk Nipis & Garam", "1", "buah", "Untuk melumuri ikan sebelum dibakar")
                ]),
                ("Bumbu Halus Khas Bima", [
                    ("Bawang Merah", "80", "gr", "±10-12 siung"),
                    ("Cabe Merah Keriting & Rawit", "40", "gr", "Sesuaikan level pedas"),
                    ("Batang Serai (Ambil putihnya)", "1", "batang", ""),
                    ("Tomat Merah Sedang", "1", "buah", "Memberi keasaman segar"),
                    ("Ketumbar Bubuk", "1", "sdt", ""),
                    ("Garam", "3/4", "sdm", ""),
                    ("Kaldu Jamur", "1", "sdt", ""),
                    ("Gula Pasir", "2", "sdm", "Menyeimbangkan rasa karamel bakar"),
                    ("Minyak Kelapa / Minyak Goreng", "3", "sdm", "Untuk menumis bumbu")
                ])
            ],
            "steps": [
                (1, "Marinasi Ikan Kakap", "Lumuri ikan kakap merah yang sudah dikerat dengan air perasan jeruk nipis dan sedikit garam. Diamkan 10-15 menit untuk menghilangkan bau amis.", 0),
                (2, "Ulek / Haluskan Bumbu Bima", "Haluskan bawang merah, cabe merah, serai, tomat, ketumbar bubuk, garam, kaldu jamur, dan gula pasir hingga tekstur sambal agak kasar berminyak.", 0),
                (3, "Tumis Bumbu Oles", "Tumis bumbu halus dengan sedikit minyak hingga matang harum dan kadar air tomat menyusut. Angkat dan sisihkan sebagian untuk cocolan.", 300),
                (4, "Bakar Ikan Tahap Pertama", "Bakar ikan di atas panggangan arang atau pan grill pemanggang hingga setengah matang di kedua sisinya.", 360),
                (5, "Oles Bumbu Melimpah & Bakar Matang", "Oleskan bumbu tumis tebal-tebal ke seluruh badan dan rongga ikan. Bakar kembali sambil terus dioles bolak-balik hingga bumbu terkaramelisasi harum dan daging ikan matang lembut.", 480),
                (6, "Sajikan", "Sajikan ikan bakar Bima panas dengan nasi hangat, lalapan timun kemangi, dan sisa sambal bumbu bakaran!", 0)
            ]
        },
        {
            "slug": "nugget-hati-ayam-mpasi",
            "title": "Nugget Hati & Paha Ayam Rumahan",
            "chef": "@waqiatussholiha",
            "description": "Nugget ayam sehat bergizi tinggi (kaya zat besi dari hati ayam) yang gurih lembut disukai anak-anak dan keluarga.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/Dcf4e0CTRHQ/",
            "servings": "25-30 Potong Nugget",
            "prep_time": "20 menit",
            "cook_time": "20 menit kukus + 5 menit goreng",
            "calories": "High Iron Nutrient Rich",
            "groups": [
                ("Bahan Adonan Nugget", [
                    ("Daging Paha Ayam Fillet", "500", "gr", "Giling bersama hati"),
                    ("Hati Ayam (Cuci bersih & rebus sebentar)", "100", "gr", "Sumber zat besi tinggi"),
                    ("Roti Tawar", "4", "lembar", "Rendam sedikit air/susu agar adonan empuk"),
                    ("Telur Ayam", "1", "butir", ""),
                    ("Bawang Putih Bubuk", "1", "sdm", ""),
                    ("Lada Bubuk", "1/2", "sdt", ""),
                    ("Garam", "1", "sdt", ""),
                    ("Penyedap Rasa / Kaldu Jamur", "1", "sdt", "")
                ]),
                ("Bahan Pelapis Nugget", [
                    ("Tepung Terigu + Air (Kekentalan sedang)", "secukupnya", "", "Pencelup basah"),
                    ("Tepung Roti / Panko Halus", "150", "gr", "Pelapis luar crispy")
                ])
            ],
            "steps": [
                (1, "Haluskan Daging & Bumbu", "Masukkan paha ayam, hati ayam, roti tawar basah, telur, bawang putih bubuk, lada, garam, dan penyedap ke dalam chopper. Giling hingga halus dan tercampur kalis.", 180),
                (2, "Kukus Adonan Nugget", "Tuangkan adonan ke dalam loyang yang diolesi minyak tipis. Ratakan permukaannya. Kukus selama 20-25 menit hingga matang dan padat.", 1200),
                (3, "Dinginkan & Potong", "Keluarkan dari kukusan, biarkan dingin sempurna. Potong-potong nugget sesuai bentuk selera (kotak atau stik jari).", 0),
                (4, "Balurkan Pelapis Tepung Roti", "Celupkan potongan nugget ke dalam adonan larutan terigu basah, lalu balurkan ke tepung roti panko hingga seluruh permukaan tertutup rapat.", 0),
                (5, "Goreng atau Simpan Freezer", "Goreng di minyak panas dengan api sedang hingga kuning keemasan renyah. Sisa nugget bisa disimpan di kotak kedap udara di freezer hingga 1 bulan!", 300)
            ]
        },
        {
            "slug": "carrot-button-noodles-chili-oil",
            "title": "Carrot Button Noodles with Garlic Chili Oil (2 Ingredients)",
            "chef": "@dandumbrell",
            "description": "Mie kancing kenyal gluten-free hanya dari 2 bahan (wortel & tepung ketan), disiram saus garlic chili oil hitam yang pedas asam gurih.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/Dbpk6T_soKF/",
            "servings": "2 Porsi",
            "prep_time": "20 menit",
            "cook_time": "10 menit",
            "calories": "Gluten-Free Chewy Noodles",
            "groups": [
                ("Bahan Mie Kancing Wortel (2 Bahan)", [
                    ("Wortel (Kupas & Potong bulat)", "400", "gr", "Kukus/rebus hingga empuk"),
                    ("Tepung Beras Ketan (Glutinous Rice Flour)", "200-250", "gr", "Campur saat wortel masih panas")
                ]),
                ("Bahan Saus Garlic Chili Oil", [
                    ("Bawang Putih (Cincang halus)", "2", "siung", ""),
                    ("Daun Bawang (Iris tipis)", "2", "batang", ""),
                    ("Chili Flakes (Cabai bubuk kasar)", "1", "sdt", ""),
                    ("Minyak Goreng Panas", "2", "sdm", "Disiramkan ke bumbu aromatik"),
                    ("Kecap Asin (Soy Sauce)", "1", "sdm", ""),
                    ("Cuka Hitam / Black Vinegar (atau Rice Vinegar)", "1", "sdm", "Aroma asam fermentasi khas oriental")
                ])
            ],
            "steps": [
                (1, "Kukus & Haluskan Wortel", "Kukus 400 gr wortel hingga empuk lembut. Haluskan wortel dengan garpu atau masher selagi panas.", 600),
                (2, "Uleni Adonan Mie Kancing", "Masukkan tepung beras ketan ke dalam tumbukan wortel yang masih hangat bertahap. Uleni hingga menjadi adonan kalis yang mudah dibentuk dan tidak lengket di tangan.", 0),
                (3, "Bentuk Kancing (Button)", "Ambil sejumput adonan, bulatkan seukuran kelereng, lalu tekan tengahnya perlahan dengan jari atau tutup botol hingga berbentuk kancing cekung.", 0),
                (4, "Rebus Mie Kancing", "Didihkan air dalam panci. Masukkan mie kancing wortel. Masak hingga mie mengapung ke permukaan (+ 2 menit), angkat dan tiriskan.", 300),
                (5, "Racik Saus & Siram Minyak Panas", "Dalam mangkuk saji, taruh bawang putih cincang, daun bawang, dan chili flakes. Siram dengan 2 sdm minyak goreng panas mendidih. Tambahkan kecap asin dan cuka hitam, aduk rata.", 0),
                (6, "Aduk & Sajikan", "Masukkan mie kancing wortel rebus yang masih hangat ke dalam mangkuk saus chili oil. Aduk rata hingga terbalut sempurna dan nikmati sensasi kenyal gurihnya!", 0)
            ]
        },
        {
            "slug": "sambal-pecel-lele-berkah-jaya",
            "title": "Sambal Pecel Lele Lamongan Gurih Pedas Nagih",
            "chef": "@yusufasr1927",
            "description": "Rahasia resep takaran sambal pecel lele kaki lima khas Lamongan yang pedas, gurih, manis, dan wangi terasi sedap.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/DdDkVTXP08Z/",
            "servings": "Porsi Banyak (Stok Warung/Keluarga)",
            "prep_time": "15 menit",
            "cook_time": "20 menit goreng & ulek",
            "calories": "Sambal Nusantara Legendaris",
            "groups": [
                ("Bahan Utama Sambal Pecel Lele", [
                    ("Tomat Merah Segar", "2", "kg", "Potong-potong"),
                    ("Cabai Rawit Merah & Hijau", "350", "gr", "Pedes nampol"),
                    ("Bawang Merah", "300", "gr", "Kupas bersih"),
                    ("Gula Merah / Gula Jawa", "250", "gr", "Sisir halus"),
                    ("Terasi Matang / Bakar", "3", "sdt", "Aroma sedap"),
                    ("Garam", "2.5", "sdt", ""),
                    ("Micin / MSG", "3", "sdt", "Kunci gurih khas pecel lele"),
                    ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng bahan")
                ])
            ],
            "steps": [
                (1, "Goreng Bawang & Cabai", "Panaskan minyak cukup banyak. Masukkan bawang merah dan cabai rawit. Goreng dengan api sedang hingga layu matang dan harum, angkat dan tiriskan ke cobek.", 300),
                (2, "Goreng Tomat", "Masukkan potongan tomat ke dalam minyak panas yang sama. Masak dan goreng tomat hingga benar-benar empuk, matang, dan mengeluarkan sari manisnya.", 480),
                (3, "Ulek Bumbu Kasar", "Ulek cabai, bawang, dan terasi di cobek bersama garam dan micin hingga tingkat kehalusan yang diinginkan.", 0),
                (4, "Masukkan Tomat & Gula Merah", "Tambahkan tomat goreng dan sisiran gula merah. Ulek dan ratakan semua bahan sambal hingga menyatu sempurna.", 0),
                (5, "Goreng/Tumis Kembali Sambal", "Tuang sambal ulek ke wajan dengan sedikit minyak, masak kembali sebentar dengan api kecil hingga tanak, berminyak, dan tahan disimpan berhari-hari. Sajikan dengan lele atau ayam goreng!", 300)
            ]
        },
        {
            "slug": "shoyu-ramen-tare-flavor-foundation",
            "title": "Ramen Flavor Foundation 101: Shoyu Tare & Ajitama",
            "chef": "@dhifa.mci11",
            "description": "Fondasi rasa ramen autentik: resep Shoyu Tare kaya umami dan telur ramen marinasi Ajitama lembut lumer.",
            "youtube_id": "",
            "media_url": "https://www.instagram.com/reel/DWGdKP2iU20/",
            "servings": "4-6 Porsi Ramen Bowl",
            "prep_time": "20 menit",
            "cook_time": "15 menit + marinasi semalam",
            "calories": "Authentic Japanese Ramen Base",
            "groups": [
                ("Bahan Shoyu Tare (Kecap Dasar Ramen)", [
                    ("Light Soy Sauce (Kecap Asin Jepang)", "200", "ml", ""),
                    ("Dark Soy Sauce", "100", "ml", "Warna pekat & aroma kedelai kuat"),
                    ("Dashi Powder", "1", "bungkus", "Kaldu ekstrak cakalang/rumput laut"),
                    ("Bawang Bombay (Potong kasar)", "1/2", "buah", ""),
                    ("Jahe Segar (Memarkan)", "2", "cm", ""),
                    ("Daun Bawang", "2", "batang", ""),
                    ("Gula Pasir", "2", "sdm", ""),
                    ("Garam", "1", "sdt", "")
                ]),
                ("Bahan Telur Ramen Ajitama", [
                    ("Telur Ayam Suhu Ruang", "4-6", "butir", ""),
                    ("Cairan Shoyu Tare Dingin", "150", "ml", "Untuk rendaman marinasi"),
                    ("Air Es", "1", "mangkuk", "Untuk menghentikan pematangan telur")
                ])
            ],
            "steps": [
                (1, "Masak Shoyu Tare", "Campurkan light soy sauce, dark soy sauce, dashi powder, bawang bombay, jahe, daun bawang, gula, dan garam ke dalam panci kecil.", 0),
                (2, "Didihkan & Kembangkan Rasa", "Masak bumbu tare di atas api kecil-sedang hingga mendidih dan aroma bumbu aromatik terekstrak sempurna (+ 10-15 menit). Matikan api, saring ampasnya, dan biarkan dingin semalaman agar rasa umami matang.", 600),
                (3, "Rebus Telur Setengah Matang (Ajitama)", "Didihkan air di panci terpisah. Masukkan telur perlahan, rebus tepat 6 menit untuk kuning telur lumer sempurna (jammy yolk).", 360),
                (4, "Rendam Air Es & Kupas", "Segera angkat telur dan rendam dalam mangkuk air es selama 5 menit. Kupas kulit telur perlahan di dalam air agar mulus.", 300),
                (5, "Marinasi Telur", "Rendam telur kupas dalam larutan tare shoyu dingin di wadah tertutup. Simpan di kulkas minimal 4 jam (ideal semalaman) hingga bumbu meresap kecokelatan.", 0),
                (6, "Racik Kuah Ramen", "Untuk menyajikan semangkuk ramen: tuang 2-3 sdm Shoyu Tare ke dasar mangkuk, siram dengan 300 ml kaldu ayam/sapi panas, masukkan mie ramen, dan belah telur Ajitama di atasnya!", 0)
            ]
        }
    ]

    for r_data in recipes_seed:
        cursor.execute("SELECT id FROM recipes WHERE slug = ?", (r_data['slug'],))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute("""
            INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r_data['slug'], r_data['title'], r_data['chef'], r_data['description'],
                r_data['youtube_id'], r_data['media_url'], r_data['servings'],
                r_data['prep_time'], r_data['cook_time'], r_data['calories']
            ))
            rec_id = cursor.lastrowid
            
            for g_idx, (g_name, items) in enumerate(r_data['groups']):
                cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (rec_id, g_name, g_idx))
                g_id = cursor.lastrowid
                for i_idx, it in enumerate(items):
                    cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it[0], it[1], it[2], it[3], i_idx))
            
            for st in r_data['steps']:
                cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (rec_id, st[0], st[1], st[2], st[3]))
            print(f"Added recipe: {r_data['title']}")

    conn.commit()
    conn.close()

def get_recipe_by_slug(slug='ayam-rebus-jahe-bawang-putih'):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM recipes WHERE slug = ?", (slug,))
    recipe = cursor.fetchone()
    if not recipe:
        conn.close()
        return None
    
    recipe_dict = dict(recipe)
    
    cursor.execute("SELECT * FROM ingredient_groups WHERE recipe_id = ? ORDER BY sort_order", (recipe['id'],))
    groups = cursor.fetchall()
    recipe_dict['ingredient_groups'] = []
    for g in groups:
        g_dict = dict(g)
        cursor.execute("SELECT * FROM ingredients WHERE group_id = ? ORDER BY sort_order", (g['id'],))
        g_dict['ingredients_list'] = [dict(i) for i in cursor.fetchall()]
        recipe_dict['ingredient_groups'].append(g_dict)
        
    cursor.execute("SELECT * FROM instructions WHERE recipe_id = ? ORDER BY step_number", (recipe['id'],))
    recipe_dict['instructions'] = [dict(s) for s in cursor.fetchall()]
    
    conn.close()
    return recipe_dict

def get_all_recipes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, slug, title, chef, description, youtube_id, media_url, prep_time, cook_time, calories FROM recipes ORDER BY id DESC")
    recipes = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return recipes

if __name__ == "__main__":
    init_db()
    print("Database updated and initialized successfully.")
