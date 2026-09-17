import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Update ID 339: Pizza Telur Tanpa Tepung (High Protein)
cursor.execute('''
UPDATE recipes 
SET title = 'Pizza Telur & Daging Tanpa Tepung (High Protein Low Carb)',
    description = 'Kreasi pizza sehat tanpa tepung terigu berbahan dasar telur dan daging cincang, tinggi protein dan cocok untuk menu diet/meal-prep.'
WHERE id = 339
''')

# 2. Update ID 352: Ayam Goreng Bawang Putih ala MasterChef
cursor.execute('''
UPDATE recipes 
SET title = 'Ayam Goreng Bawang Putih Renyah Gurih',
    description = 'Resep ayam goreng bawang putih utuh khas MasterChef @jonatan.mci13 dengan bumbu marinasi meresap dan aroma bawang harum menggoda.'
WHERE id = 352
''')

# 3. Update ID 356: Sambal Bawang Petis Madura
cursor.execute('''
UPDATE recipes 
SET title = 'Sambal Bawang Petis Madura Pedas Gurih Nendang',
    description = 'Sambal bawang ulek khas Madura yang dipadukan dengan petis hitam gurih, cocok untuk cocolan tahu, tempe, dan ikan goreng.'
WHERE id = 356
''')

# 4. Update ID 364: Ayam Panggang Bumbu Rujak
cursor.execute('''
UPDATE recipes 
SET title = 'Ayam Panggang Bumbu Rujak Pedas Manis Gurih',
    description = 'Resep ayam bakar/panggang dengan bumbu rujak medok bersantan khas Nusantara ala @devyanastasia.'
WHERE id = 364
''')

# 5. Update ID 372: Nori Udang Crispy (Snack Bocil)
cursor.execute('''
UPDATE recipes 
SET title = 'Nori Gulung Udang Crispy (Snack Anak & Keluarga)',
    description = 'Olahan udang cincang gurih berbalut lembaran rumput laut nori renyah, favorit anak-anak dan kaya protein.'
WHERE id = 372
''')

# 6. Delete ambiguous/incomplete recipes (ID 332 coffee, ID 368 1-step, ID 380 undefined)
cursor.execute('DELETE FROM recipes WHERE id IN (332, 368, 380)')
cursor.execute('DELETE FROM instructions WHERE recipe_id IN (332, 368, 380)')
cursor.execute('DELETE FROM ingredient_groups WHERE recipe_id IN (332, 368, 380)')

conn.commit()
conn.close()
print("Cleaned titles and purged incomplete entries successfully!")
