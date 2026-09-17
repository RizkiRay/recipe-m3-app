import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Get all recipes and their ingredients to check for intro text / missing numbers
cursor.execute("SELECT id, title, chef FROM recipes")
all_recipes = cursor.fetchall()

for rid, title, chef in all_recipes:
    # 1. Check if first ingredient is a long sentence (intro caption leak)
    cursor.execute("SELECT i.id, i.item FROM ingredients i JOIN ingredient_groups ig ON i.group_id = ig.id WHERE ig.recipe_id = ? ORDER BY i.sort_order ASC", (rid,))
    ings = cursor.fetchall()
    
    for i_id, item_text in ings:
        # If item has more than 50 chars or contains emojis/greetings/captions, delete it
        if len(item_text) > 45 or any(w in item_text.lower() for w in ['enak banget', 'hihi', 'makan enak', 'yuk coba', 'si kecil', 'bocil', 'viral', 'halo']):
            print(f"Purging intro leak from [{rid}] {title}: \"{item_text[:40]}...\"")
            cursor.execute("DELETE FROM ingredients WHERE id = ?", (i_id,))

# 2. Clean trailing farewell words in instructions like "SELAMAT MENCOBAH"
cursor.execute('''
DELETE FROM instructions 
WHERE LOWER(detail) LIKE '%selamat mencoba%' 
   OR LOWER(detail) LIKE '%selamat menikmati%'
   OR LENGTH(detail) < 8
''')

conn.commit()
conn.close()
print("Deep sweep completed!")
