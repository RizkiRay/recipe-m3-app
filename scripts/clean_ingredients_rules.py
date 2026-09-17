import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Fix Recipe 244 (Crispy potato rings) specifically
cursor.execute("SELECT id FROM recipes WHERE title LIKE '%potato rings%'")
r_ids = [r[0] for r in cursor.fetchall()]

for rid in r_ids:
    # Get group id
    cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = ?", (rid,))
    g_id = cursor.fetchone()[0]
    
    # Clean ingredients
    cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_id,))
    clean_ings = [
        ("Large Potatoes (Kentang besar)", "3", "buah", "Kupas & potong dadu"),
        ("Tepung Maizena (Cornstarch)", "6-8", "sdm", "Pengikat adonan krispi"),
        ("Tepung Terigu Serbaguna", "2", "sdm", ""),
        ("Susu Cair / Air", "1-2", "sdm", "Gunakan jika adonan terlalu kering"),
        ("Garam Halus", "secukupnya", "", ""),
        ("Chili Flakes (Cabai bubuk kasar)", "1", "sdt", ""),
        ("Kaldu Ayam Bubuk", "1/2", "sdm", ""),
        ("Bawang Putih Bubuk", "1", "sdm", ""),
        ("Lada Hitam Bubuk", "1/2", "sdt", ""),
        ("Peterseli / Parsley Cincang", "1", "sdm", ""),
        ("Minyak Goreng", "secukupnya", "", "Untuk menggoreng deep-fry")
    ]
    for idx, (it, amt, un, nt) in enumerate(clean_ings):
        cursor.execute("INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)", (g_id, it, amt, un, nt, idx))
        
    # Clean instructions
    cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (rid,))
    clean_steps = [
        (1, "Kupas & Rebus Kentang", "Kupas kentang dan potong dadu. Rebus dalam air mendidih bergaram selama 12–15 menit hingga empuk lembut saat ditusuk garpu.", 720),
        (2, "Tiriskan & Haluskan", "Tiriskan kentang hingga uap air menguap kering. Haluskan kentang selagi hangat sampai lembut tanpa gumpalan.", 0),
        (3, "Bumbui & Campur Tepung", "Masukkan garam, kaldu ayam bubuk, chili flakes, bawang putih bubuk, lada hitam, dan peterseli cincang. Tambahkan 2 sdm terigu dan 6-8 sdm maizena (tambahkan 1-2 sdm susu jika terlalu kering). Aduk hingga kalis elastis.", 0),
        (4, "Bentuk Cincin (Ring)", "Ambil sedikit adonan, bulatkan lalu pipihkan tebal. Gunakan spuit/sumpit untuk melubangi bagian tengahnya hingga membentuk cincin rapi.", 0),
        (5, "Dinginkan di Kulkas (30 Menit)", "Tata cincin kentang di atas nampan dan simpan di chiller kulkas selama 30 menit agar kokoh dan tidak hancur saat digoreng.", 1800),
        (6, "Goreng Deep-Fry Crispy", "Panaskan minyak pada suhu 175°C (350°F). Goreng cincin kentang secara bertahap selama 3–4 menit hingga kuning keemasan dan super renyah. Tiriskan dan sajikan hangat dengan saus tomat/sambal!", 240)
    ]
    for st in clean_steps:
        cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (rid, st[0], st[1], st[2], st[3]))

# 2. General Purge for ALL recipes in DB: Delete any ingredient that is actually a step, method header, or hashtag
cursor.execute('''
DELETE FROM ingredients
WHERE item LIKE 'Method%' 
   OR item LIKE 'Cara%' 
   OR item LIKE 'Step%' 
   OR item LIKE 'Langkah%' 
   OR item LIKE '#%' 
   OR item LIKE '%http%' 
   OR item LIKE 'Peel the%'
   OR item LIKE 'Boil them%'
   OR item LIKE 'Heat oil%'
   OR item LIKE 'Fry the%'
   OR item LIKE 'Remove and%'
   OR item LIKE 'Place the%'
   OR item LIKE 'Add % tbsp all-purpose%'
   OR item LIKE 'Mash the potatoes%'
   OR item LIKE 'Take a small portion%'
   OR item LIKE 'Use a nozzle%'
   OR item LIKE 'If the dough%'
''')

# Delete ingredients that duplicate the recipe title
cursor.execute('''
DELETE FROM ingredients
WHERE id IN (
    SELECT i.id FROM ingredients i
    JOIN ingredient_groups ig ON i.group_id = ig.id
    JOIN recipes r ON ig.recipe_id = r.id
    WHERE LOWER(TRIM(i.item)) = LOWER(TRIM(r.title))
)
''')

conn.commit()
conn.close()
print("Cleaned ingredients database successfully!")
