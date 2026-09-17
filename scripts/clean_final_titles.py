import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Map raw IDs/slugs to elegant verified titles
special_fixes = {
    941: 'Nugget Ayam Wortel Rumahan',
    940: 'Ayam Songkem Madura Pedas Gurih',
    939: 'Keripik Tempe Renyah Gurih',
    938: 'Ayam Bakar Bumbu Rujak Medok',
    937: 'Char Siu Chicken Ramen Gurih Karamel',
    936: 'Pentol & Tahu Kriwil Daging Sapi',
    935: 'Choco Cheese Pancake Lembut Fluffy',
    934: 'Nugget Hati & Paha Ayam Sehat',
    933: 'Pancake Susu Keju Praktis',
    932: 'Chicken Kebab Rumahan Tanpa Minyak',
    931: 'Udang Keju Goreng Renyah Lumer',
    930: 'Pentol Kriwil Sapi High Protein',
    929: 'Udang Goreng Bawang Gurih',
    928: 'Camilan Tahu Aci Saus Kacang',
    927: 'Sup Ikan Kemangi Kuah Segar Bening'
}

for r_id, new_title in special_fixes.items():
    cursor.execute("UPDATE recipes SET title = ? WHERE id = ?", (new_title, r_id))

# Sweep and clean any remaining titles that look like raw sentences
cursor.execute("SELECT id, title, chef, description FROM recipes")
for r_id, title, chef, desc in cursor.fetchall():
    if len(title) > 35 or any(w in title.lower() for w in ['yang', 'udah', 'bisa', 'kapan', 'kalau', 'selain', 'coba', 'inget']):
        cursor.execute("SELECT i.item FROM ingredients i JOIN ingredient_groups ig ON i.group_id = ig.id WHERE ig.recipe_id = ? LIMIT 2", (r_id,))
        sample = [row[0] for row in cursor.fetchall()]
        if sample:
            t_name = f"Olahan {sample[0]}"
            cursor.execute("UPDATE recipes SET title = ? WHERE id = ?", (t_name, r_id))

conn.commit()
conn.close()
print("All catalog titles polished cleanly!")
