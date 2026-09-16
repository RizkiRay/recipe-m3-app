import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Update id 46 (Baso Sapi Tanpa Tepung)
cursor.execute('''
UPDATE recipes 
SET title = 'Bakso Sapi Rumahan (Tanpa Tepung / Low Carb)', 
    description = 'Resep bakso sapi kenyal sehat tanpa tepung, cocok untuk MPASI, anak-anak, dan menu diet sehat keluarga.' 
WHERE id = 46
''')

# 2. Update id 79 (Honey Glazed Chicken Roll)
cursor.execute('''
UPDATE recipes 
SET title = 'Honey Glazed Chicken Roll (Ayam Gulung Madu)', 
    description = 'Olahan ayam gulung gurih manis dengan glaze saus madu kental, praktis untuk makan malam keluarga.' 
WHERE id = 79
''')

# 3. Update id 120 (Daging Berselimut)
cursor.execute('''
UPDATE recipes 
SET title = 'Daging Sapi Berselimut Telur & Tepung Renyah', 
    description = 'Olahan daging sapi empuk dibalut telur dan tepung bumbu krispi gurih, nikmat untuk lauk makan atau camilan.' 
WHERE id = 120
''')

# 4. Update id 144 (Sambal Ijo Khas Padang)
cursor.execute('''
UPDATE recipes 
SET title = 'Sambal Ijo Khas Padang Gurih Wangi (Anti Langu & Hitam)', 
    description = 'Rahasia membuat sambal hijau khas rumah makan Padang yang tetap berwarna hijau segar, gurih mantap, dan tidak langu.' 
WHERE id = 144
''')

# 5. Delete low-quality non-recipe posts
cursor.execute('DELETE FROM recipes WHERE id IN (61, 67, 69, 93, 148, 150)')
cursor.execute('DELETE FROM instructions WHERE recipe_id IN (61, 67, 69, 93, 148, 150)')
cursor.execute('DELETE FROM ingredient_groups WHERE recipe_id IN (61, 67, 69, 93, 148, 150)')

conn.commit()
conn.close()
print("Database cleanup & metadata polish completed!")
