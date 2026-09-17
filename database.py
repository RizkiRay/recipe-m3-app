import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "recipes.db"

# Master Gold-Standard 22 Recipes Dataset
ALL_22_RECIPES = [
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
    },
    {
        "slug": "velveting-chicken-stir-fry",
        "title": "Classic Velveting Method: Rahasia Ayam & Ikan Stir-Fry Empuk",
        "chef": "@sometimesdancooks",
        "description": "Teknik restoran Tiongkok untuk mengempukkan dada ayam & ikan agar tetap juicy lembut dan saus menempel sempurna tanpa rasa lembek baking soda.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/DcOFmSVT0FF/",
        "servings": "2-3 Porsi Stir Fry",
        "prep_time": "10 menit",
        "cook_time": "1 menit blanching + 5 menit tumis",
        "calories": "Pro Chinese Restaurant Technique",
        "groups": [
            ("Bahan Utama & Velveting Coating", [
                ("Dada Ayam / Fillet Ikan (Iris tipis)", "300", "gr", "Potong seragam"),
                ("Tepung Maizena (Cornstarch)", "1.5", "sdm", "Membentuk lapisan pelindung kelembapan"),
                ("Putih Telur", "1", "butir", "Mengikat sari daging"),
                ("Minyak Sayur Netral", "1", "sdt", "Mencegah daging saling menempel"),
                ("Garam & Lada Putih", "secukupnya", "", "")
            ]),
            ("Pelengkap Tumisan (Stir-Fry)", [
                ("Bawang Putih (Cincang)", "3", "siung", ""),
                ("Saus Tiram & Kecap Asin", "1.5", "sdm", ""),
                ("Sayuran (Brokoli/Paprika/Jamur)", "150", "gr", "")
            ])
        ],
        "steps": [
            (1, "Iris & Lapisi Daging", "Keringkan irisan daging ayam. Masukkan tepung maizena, putih telur, minyak netral, garam, dan lada. Aduk rata hingga seluruh permukaan daging terbalut lapisan tipis mengkilap.", 0),
            (2, "Water Blanching Cepat (30 Detik)", "Didihkan air dalam panci (atau minyak panas di wajan). Masukkan irisan ayam, masak singkat selama 30-45 detik hingga lapisan luar mengeras putih tapi dalam masih juicy. Tiriskan segera.", 45),
            (3, "Tumis Bumbu & Sayuran", "Panaskan wajan wok dengan 1 sdm minyak. Tumis bawang putih cincang dan sayuran pilihan dengan api besar hingga harum dan renyah.", 120),
            (4, "Masukkan Ayam Velvet & Saus", "Masukkan ayam yang sudah diblanching ke dalam wajan. Tuang saus tiram dan kecap asin. Aduk cepat 1-2 menit hingga saus mengental menempel sempurna pada lapisan maizena ayam.", 120),
            (5, "Sajikan Panas", "Angkat dan sajikan ayam stir-fry super lembut dan juicy selagi hangat!", 0)
        ]
    },
    {
        "slug": "grilled-squid-and-peas-mediterranean",
        "title": "Grilled Squid and Peas with Aioli (Mediterranean Style)",
        "chef": "Jesse Jenkins (@adip_food / @octobre_editions)",
        "description": "Cumi bakar mediterania yang segar dengan kacang polong panggang, kentang rebus, mint, dan saus aioli gurih segar.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/Dbuv21JM-T6/",
        "servings": "2 Porsi",
        "prep_time": "15 menit",
        "cook_time": "10 menit memanggang",
        "calories": "Fresh Mediterranean Seafood",
        "groups": [
            ("Bahan Utama Cumi & Sayur", [
                ("Baby Squid / Cumi Segar (Bersihkan)", "400", "gr", "Utuh atau kerat-kerat"),
                ("Kacang Polong Segar (Green Peas / Broad Beans)", "150", "gr", ""),
                ("Baby Potatoes (Rebus matang empuk)", "200", "gr", "Belah dua"),
                ("Daun Mint Segar (Cincang kasar)", "1", "genggam", "Aroma segar Mediterania"),
                ("Cabai Merah Segar (Cincang halus)", "1", "buah", "")
            ]),
            ("Bumbu Perendam & Dressing", [
                ("Extra Virgin Olive Oil", "3-4", "sdm", "Gunakan kualitas terbaik"),
                ("Jeruk Lemon Segar", "1", "buah", "Kupas bulir buahnya + ambil air perasannya"),
                ("Garam Laut (Sea Salt) & Lada Hitam", "secukupnya", "", ""),
                ("Saus Aioli (Mayones Bawang Putih)", "4", "sdm", "Alas dasar piring saji")
            ])
        ],
        "steps": [
            (1, "Bakar Cumi di Atas Api Terbuka", "Panaskan griddle pan sangat panas atau panggangan arang. Panggang baby squid di atas api besar selama 2-3 menit hingga harum gosong manis (smoky char) dan kenyal matang.", 180),
            (2, "Panggang Kacang Polong", "Panggang kacang polong sebentar di wadah grill basket atau pan panas hingga ada bercak kecokelatan.", 120),
            (3, "Bumbui Cumi Langsung Saat Panas", "Saat cumi baru diangkat dari api panas, segera siram dengan banyak minyak zaitun extra virgin, air lemon, dan garam laut agar rasa meresap ke dalam pori-pori panasnya.", 0),
            (4, "Campur Salad Mediterania", "Campurkan cumi bakar dengan kacang polong panggang, kentang rebus, irisan cabai, daun mint cincang, dan bulir lemon kupas.", 0),
            (5, "Plating dengan Aioli", "Oleskan saus aioli lembut di dasar piring saji. Tata cumi panggang dan salad kentang mint di atasnya. Sajikan segera selagi hangat!", 0)
        ]
    },
    {
        "slug": "hainan-chicken-jelly-rd",
        "title": "Hainan Chicken with Natural Aromatic Jelly (R&D Episode)",
        "chef": "@hwoo.lee",
        "description": "Teknik poaching ayam Hainan untuk menghasilkan lapisan jelly kaldu kolagen alami yang dingin, gurih, dan kenyal di bawah kulit ayam.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/Da4cX71JEeN/",
        "servings": "3-4 Porsi",
        "prep_time": "20 menit",
        "cook_time": "40 menit poaching + chilling",
        "calories": "Mastery Hainanese Poached Chicken",
        "groups": [
            ("Bahan Ayam & Kaldu Poaching", [
                ("Ayam Utuh Segar (Kualitas baik)", "1", "ekor (±1.2 kg)", "Bersihkan rongga dalam"),
                ("Jahe Segar (Memarkan)", "50", "gr", ""),
                ("Daun Bawang", "3", "batang", "Ikat simpul"),
                ("Bawang Putih", "6", "siung", "Memarkan"),
                ("Minyak Wijen & Garam", "secukupnya", "", "")
            ]),
            ("Bahan Ice Bath (Pembentuk Jelly)", [
                ("Es Batu Melimpah + Air Dingin", "1", "baskom besar", "Menghentikan pematangan & mengunci kolagen jelly")
            ])
        ],
        "steps": [
            (1, "Siapkan Rongga Ayam & Air Kaldu", "Masukkan jahe, daun bawang, dan bawang putih ke dalam rongga perut ayam. Didihkan air kaldu di panci besar dengan garam.", 0),
            (2, "Submerge & Poach Lembut", "Celupkan ayam 3 kali ke air mendidih agar suhu luar-dalam seimbang, lalu rendam seluruh badan ayam. Masak dengan api sangat kecil (simmering 85°C) selama 35-40 menit hingga matang lembut.", 2400),
            (3, "Kejut Air Es (Thermal Shock)", "Segera angkat ayam panas dan cemplungkan ke dalam baskom air es selama 15 menit. Penurunan suhu drastis ini mengunci kolagen di bawah kulit menjadi lapisan jelly transparan alami.", 900),
            (4, "Oles Minyak Wijen & Potong", "Angkat ayam dingin, olesi kulitnya dengan minyak wijen murni. Potong rapi dan nikmati tekstur kulit kenyal dengan lapisan jelly gurih alami khas Hainan!", 0)
        ]
    },
    {
        "slug": "vietnamese-beef-pho-slow-broth",
        "title": "Vietnamese Beef Pho with Aromatic Spices",
        "chef": "@mbakaleta",
        "description": "Semangkuk mie Pho Vietnam hangat dengan kaldu sapi rempah (kapulaga arab, pekak, kayu manis) yang wangi semerbak.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/Db3IKQ4Bi75/",
        "servings": "4 Porsi",
        "prep_time": "25 menit",
        "cook_time": "60 menit simmer kaldu",
        "calories": "Comforting Vietnamese Noodle Soup",
        "groups": [
            ("Bahan Kuah Kaldu Sapi Rempah", [
                ("Tulang Sapi / Daging Sengkel Sapi", "750", "gr", "Rebus buang buih darah pertama"),
                ("Kapulaga Arab (Green Cardamom)", "5", "butir", "Sangrai"),
                ("Bunga Lawang / Star Anise", "3", "buah", "Sangrai"),
                ("Kayu Manis Batang", "1", "batang", "Sangrai"),
                ("Biji Ketumbar & Cengkih", "1", "sdt", "Sangrai"),
                ("Bawang Bombay & Jahe (Bakar hingga gosong)", "1", "buah", "Kunci kuah bening manis gurih"),
                ("Kecap Ikan (Fish Sauce) & Gula Batu", "secukupnya", "", "")
            ]),
            ("Isian Mie & Pelengkap Pho", [
                ("Mie Pho (Beras Vietnam) / Kwetiau Beras", "400", "gr", "Seduh air panas"),
                ("Daging Sapi Iris Tipis (Sirloin/Tenderloin)", "200", "gr", "Taruh mentah disiram kuah panas"),
                ("Bakso Sapi Urat", "8", "butir", "")
            ])
        ],
        "steps": [
            (1, "Bakar Bombay, Jahe & Sangrai Rempah", "Bakar bawang bombay dan jahe di atas api kompor hingga kulitnya gosong beraroma. Sangrai kapulaga, bunga lawang, kayu manis, dan cengkih di wajan kering hingga harum.", 300),
            (2, "Rebus Kaldu Bening Sapi", "Rebus tulang sapi dalam air mendidih selama 10 menit, buang air kotor pertama. Isi kembali air bersih, masukkan daging sapi, bombay bakar, jahe bakar, dan kantung rempah sangrai. Simmer api kecil selama 1 jam.", 3600),
            (3, "Bumbui Kuah Pho", "Bumbui kuah dengan kecap ikan dan gula batu hingga gurih manis seimbang. Masukkan bakso sapi.", 0),
            (4, "Susun Mangkuk Pho", "Tata mie pho hangat di mangkuk saji, beri irisan daging sapi mentah tipis, bakso sapi, dan tauge segar.", 0),
            (5, "Siram Kuah Mendidih & Nikmati", "Siramkan kuah kaldu sapi panas mendidih langsung ke atas irisan daging sapi hingga matang seketika. Beri perasan jeruk nipis, daun ketumbar, dan irisan cabe rawit segar!", 0)
        ]
    },
    {
        "slug": "wet-brining-dada-ayam-empuk",
        "title": "Teknik Wet Brining Dada Ayam (Anti Kering & Seret)",
        "chef": "@edmareta",
        "description": "Rahasia merendam dada ayam dalam larutan garam cair (wet brine) semalaman agar daging empuk, gurih meresap, dan tidak seret saat digoreng/airfryer.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/Db15nqQSma9/",
        "servings": "Untuk 1.5 kg Daging Ayam",
        "prep_time": "5 menit",
        "cook_time": "Istirahat chiller semalaman",
        "calories": "Juicy Poultry Preparation Technique",
        "groups": [
            ("Bahan Larutan Wet Brining", [
                ("Dada Ayam / Ayam Utuh Potong", "1.5", "kg", "Bebas lemak berlebih"),
                ("Air Matang Hangat", "1.5", "liter", "Untuk melarutkan garam"),
                ("Garam Dapur", "2-3", "sdm (±45 gr)", "Kunci tekanan osmosis protein"),
                ("Gula Pasir", "1.5", "sdm", "Menyeimbangkan rasa asin & melembutkan"),
                ("Bawang Putih Bubuk / Utuh Geprek", "4", "siung", "Pengharum"),
                ("Kaldu Alami / Kaldu Jamur", "1", "sdm", "Ekstra rasa umami")
            ])
        ],
        "steps": [
            (1, "Larutkan Garam & Bumbu Brine", "Campurkan garam, gula pasir, bawang putih, dan kaldu ke dalam air hangat. Aduk hingga seluruh butiran garam dan gula larut sempurna, lalu biarkan air mendingin.", 180),
            (2, "Rendam Daging Ayam", "Masukkan potongan dada ayam ke dalam wadah kedap udara atau toples besar. Tuangkan larutan air garam hingga seluruh bagian ayam terendam sempurna.", 0),
            (3, "Simpan di Chiller Semalaman", "Tutup rapat wadah, simpan di dalam kulkas (chiller) minimal 6-8 jam (atau dari malam hingga pagi). Proses osmosis akan menarik kelembapan dan rasa asin gurih meresap rata ke serat terdalam daging.", 0),
            (4, "Tiriskan & Siap Diolah", "Keluarkan ayam dari kulkas, buang air rendamannya (tidak perlu dicuci garam lagi). Daging ayam kini super empuk dan siap digoreng krispi, dipanggang, dibakar, atau dimasukkan ke airfryer tanpa takut seret!", 0)
        ]
    },
    {
        "slug": "crispy-chicken-cutlet-cornstarch-hack",
        "title": "Crispy Chicken Cutlet: Cornstarch First Layer Method",
        "chef": "@themindfulflavors",
        "description": "Trik pelapis katsu/cutlet ayam agar tepung panir menempel rapat tanpa terlepas saat digoreng: gunakan tepung maizena sebagai lapisan pertama pengunci uap air.",
        "youtube_id": "",
        "media_url": "https://www.instagram.com/reel/DcTm03oR0Gc/",
        "servings": "2 Porsi Cutlet",
        "prep_time": "10 menit",
        "cook_time": "8 menit goreng",
        "calories": "Flawless Japanese/Austrian Cutlet Technique",
        "groups": [
            ("Bahan Utama & Breading System", [
                ("Dada Ayam Fillet (Belah tipis melebar)", "300", "gr", "Keringkan permukaannya dengan tisu"),
                ("Garam, Lada Hitam, Bawang Putih Bubuk", "secukupnya", "", "Bumbu marinasi dasar"),
                ("Tepung Maizena (Lapisan 1)", "3", "sdm", "Menyerap kelembapan permukaan & mengunci uap air"),
                ("Telur Ayam (Lapisan 2)", "1", "butir", "Kocok lepas"),
                ("Tepung Roti Panko / Breadcrumbs (Lapisan 3)", "100", "gr", "Untuk tekstur luar renyah mekar"),
                ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng shallow-fry")
            ])
        ],
        "steps": [
            (1, "Keringkan & Bumbui Dada Ayam", "Keringkan permukaan dada ayam dengan paper towel hingga tidak berair. Taburi garam, lada hitam, dan bawang putih bubuk merata di kedua sisi.", 0),
            (2, "Balur Lapisan 1 (Tepung Maizena)", "Balurkan ayam ke dalam tepung maizena tipis-tipis, tepuk-tepuk sisa tepung berlebih. Maizena akan menyerap kelembapan saat digoreng dan membentuk gel tipis penahan uap air.", 0),
            (3, "Celup Lapisan 2 (Telur Kocok)", "Celupkan ayam berbalut maizena ke dalam mangkuk telur kocok hingga seluruh permukaan basah merata.", 0),
            (4, "Tekan Lapisan 3 (Tepung Panko)", "Pindahkan ayam ke wadah tepung roti panko. Tekan-tekan kuat dengan telapak tangan agar butiran panko tertanam rapat ke lapisan telur.", 0),
            (5, "Goreng hingga Golden Brown", "Panaskan minyak dengan api sedang (170°C). Goreng ayam selama 3-4 menit tiap sisi hingga berwarna cokelat keemasan renyah. Angkat dan tiriskan di atas cooling rack!", 480)
        ]
    },
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
    
    # Ensure all 22 gold recipes exist permanently in DB
    for r_data in ALL_22_RECIPES:
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
            print(f"Verified & Seeded: {r_data['title']}")
            
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
    print("Database SSOT synchronized successfully.")
