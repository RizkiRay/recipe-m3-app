import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Sanitize Recipe 355 (Tahu Bulat)
cursor.execute("SELECT id FROM recipes WHERE title LIKE '%TAHU BULAT%'")
tahu_ids = [r[0] for r in cursor.fetchall()]

for tid in tahu_ids:
    cursor.execute("UPDATE recipes SET title = 'Tahu Bulat Kopong Gurih Renyah', description = 'Resep tahu bulat kopong renyah dan gurih khas tasikmalaya/pasar malam, anti kempis saat digoreng.' WHERE id = ?", (tid,))
    cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = ?", (tid,))
    g_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_id,))
    
    clean_ings = [
        ("Tahu Putih Segar (Peras airnya dengan kain)", "10", "buah (±500 gr)", "Wajib diperas sampai benar-benar kering"),
        ("Kuning Telur", "1", "butir", "Pengikat adonan & melembutkan"),
        ("Bawang Putih Bubuk", "1/2", "sdt", ""),
        ("Merica / Lada Bubuk", "1/2", "sdt", ""),
        ("Baking Powder Double Acting", "1/2", "sdt", "Kunci tahu mengembang kopong"),
        ("Garam Dapur", "1/2", "sdt", ""),
        ("Gula Pasir & Kaldu Bubuk", "1/2", "sdm", ""),
        ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
    ]
    for idx, (it, amt, un, nt) in enumerate(clean_ings):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it, amt, un, nt, idx))
        
    cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (tid,))
    clean_steps = [
        (1, "Peras Air Tahu hingga Kering", "Hancurkan tahu putih, lalu bungkus dengan kain bersih atau serbet tipis. Peras sekuat tenaga hingga air di dalam tahu keluar maksimal dan ampas tahu benar-benar kering.", 0),
        (2, "Bumbui & Uleni Adonan", "Campurkan ampas tahu kering dengan kuning telur, bawang putih bubuk, merica bubuk, garam, gula pasir, kaldu bubuk, dan baking powder. Aduk dan uleni hingga adonan halus kalis.", 0),
        (3, "Bulatkan Tahu", "Ambil sejumput adonan tahu, bulatkan dengan telapak tangan hingga licin dan mulus tanpa retakan (ukuran sebesar bola pingpong).", 0),
        (4, "Simpan di Kulkas (Chiller)", "Tata bola tahu di wadah tertutup, simpan di kulkas minimal 1-2 jam agar adonan set dan baking powder bereaksi sempurna.", 3600),
        (5, "Goreng dari Minyak Hangat", "Masukkan bola tahu ke dalam wajan berisi minyak yang masih hangat (api kecil). Aduk-aduk terus perlahan. Saat tahu mulai mengembang dan mengapung, besarkan ke api sedang. Goreng sambil terus diaduk bolak-balik selama 10-15 menit hingga kulitnya kering garing kecokelatan. Angkat dan tiriskan!", 600)
    ]
    for st in clean_steps:
        cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (tid, st[0], st[1], st[2], st[3]))

# 2. General database-wide cleaning for apologies, typos, seasoning labels, hashtags
cursor.execute('''
DELETE FROM ingredients
WHERE item LIKE '%mohon maaf%'
   OR item LIKE '%sorry%'
   OR item LIKE '%typo%'
   OR item LIKE '%seasoning%'
   OR item LIKE '%bumbu :%'
   OR item LIKE '%bahan :%'
   OR item LIKE '#%'
   OR item LIKE '%✨%'
   OR item LIKE '%dm kami%'
   OR item LIKE '%link di bio%'
   OR item LIKE '%baca label%'
   OR item LIKE '%dapatkan di%'
''')

conn.commit()
conn.close()
print("Cleaned Tahu Bulat and purged all social apologies/hashtags across DB!")
