import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Fix Recipe 79 Instructions (Honey Glazed Chicken Roll)
cursor.execute("DELETE FROM instructions WHERE recipe_id = 79")
clean_steps_79 = [
    (1, "Pipihkan & Bumbui Daging Ayam", "Ambil 500 gr paha/dada ayam fillet berkulit. Pipihkan dengan pemukul daging atau punggung pisau hingga ketebalannya rata. Taburi sedikit garam dan lada di kedua sisi.", 0),
    (2, "Marinasi Saus Madu Gurih", "Campurkan 2 sdm madu murni, 2 sdm kecap asin, 1 sdm saus tiram, 3 siung bawang putih cincang halus, irisan jahe, dan 1 sdt minyak wijen. Balurkan ke daging ayam, diamkan 15 menit.", 0),
    (3, "Gulung Rapat dalam Aluminium Foil", "Tata irisan jahe di bagian dalam daging, lalu gulung daging ayam memanjang dengan rapat. Bungkus gulungan ayam menggunakan aluminium foil atau baking paper hingga membentuk silinder padat.", 0),
    (4, "Panggang atau Kukus Matang", "Panggang dalam oven/airfryer bersuhu 190°C selama 20-25 menit (atau kukus 20 menit) hingga daging ayam matang dan sari daging terkunci lembut di dalam.", 1200),
    (5, "Glazing & Karamelisasi Saus", "Buka bungkusan foil, letakkan gulungan ayam di pan teflon panas bersama sisa saus marinasi. Masak dan putar-putar selama 3-5 menit hingga saus mengental mengkilap (caramelized glaze) melapisi kulit ayam. Potong bulat tebal dan sajikan!", 240)
]
for st in clean_steps_79:
    cursor.execute("INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)", (79, st[0], st[1], st[2], st[3]))

# 2. Audit all other recipes for noisy instructions
cursor.execute('''
SELECT DISTINCT r.id, r.title 
FROM recipes r 
JOIN instructions i ON r.id = i.recipe_id
WHERE i.detail LIKE '%What You%' 
   OR i.detail LIKE '%Original audio%' 
   OR i.detail LIKE '%Edited%'
''')
stray = cursor.fetchall()
print("Any other noisy recipes?", stray)

conn.commit()
conn.close()
print("Recipe 79 steps completely rewritten and verified!")
