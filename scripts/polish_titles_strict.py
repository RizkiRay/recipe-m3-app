import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Clean messy titles in newly ingested recipes
cursor.execute("SELECT id, title, chef, description FROM recipes")
all_recs = cursor.fetchall()

for r_id, title, chef, desc in all_recs:
    t_clean = title
    d_lower = desc.lower()
    
    # Clean titles starting with ingredients or numbers (e.g. "gr daging sapi...")
    if re.match(r'^(gr|gram|kg|\d+|pcs)\s+', t_clean, re.IGNORECASE) or t_clean.startswith('Resep Kreasi') or len(t_clean) > 40:
        if 'ramen' in d_lower:
            t_clean = 'Ramen Kuah Autentik Gurih'
        elif 'bakso' in d_lower or 'baso' in d_lower:
            t_clean = 'Bakso Sapi Rumahan Kenyal Gurih'
        elif 'siomay' in d_lower or 'dimsum' in d_lower:
            t_clean = 'Dimsum Sawi Gulung Ayam Udang'
        elif 'chips' in d_lower or 'kripik' in d_lower or 'keripik' in d_lower:
            t_clean = 'Chicken Breast Crispy Chips'
        elif 'egg drop' in d_lower or 'soup' in d_lower:
            t_clean = 'Seaweed Egg Drop Soup Gurih'
        elif 'sweet potato' in d_lower or 'brownie' in d_lower:
            t_clean = 'High-Protein Sweet Potato Brownie'
        elif 'chicken roll' in d_lower:
            t_clean = 'Honey Glazed Chicken Roll'
        elif 'taichan' in d_lower:
            t_clean = 'Oseng Ayam Bumbu Taichan Pedas Gurih'
        elif 'batokok' in d_lower:
            t_clean = 'Ayam Batokok Rendah Kalori'
        elif 'ikan bakar' in d_lower:
            t_clean = 'Ikan Bakar Bima Bumbu Medok'
        elif 'songkem' in d_lower:
            t_clean = 'Ayam Songkem Kukus Madura'
        elif 'pizza' in d_lower:
            t_clean = 'Pizza Telur Daging Tanpa Tepung'
        elif 'potato rings' in d_lower:
            t_clean = 'Crispy Potato Rings Gurih'
        elif 'chicharron' in d_lower:
            t_clean = 'Crispy Chicken Chicharron'
        elif 'nori' in d_lower:
            t_clean = 'Nori Gulung Udang Crispy'
        elif 'lada hitam' in d_lower:
            t_clean = 'Sapi Lada Hitam Empuk'
        elif 'telur' in d_lower:
            t_clean = 'Telur Kukus Daging Cincang Gurih'
        else:
            # Clean punctuation
            t_clean = re.sub(r'[^\w\s\(\)\-]', '', t_clean).strip()
            t_clean = t_clean[:35]
            
    # Remove emoji & excessive symbols from title
    t_clean = re.sub(r'[^\w\s\(\)\-\:\,\.]', '', t_clean).strip()
    cursor.execute("UPDATE recipes SET title = ? WHERE id = ?", (t_clean.title(), r_id))

# 2. Delete recipe 745 if empty author/title
cursor.execute("DELETE FROM recipes WHERE chef = '@' OR chef = ''")
cursor.execute("DELETE FROM instructions WHERE recipe_id NOT IN (SELECT id FROM recipes)")
cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id NOT IN (SELECT id FROM recipes)")
cursor.execute("DELETE FROM ingredients WHERE group_id NOT IN (SELECT id FROM ingredient_groups)")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM recipes")
print("Total sanitized recipes in DB:", cursor.fetchone()[0])
conn.close()
