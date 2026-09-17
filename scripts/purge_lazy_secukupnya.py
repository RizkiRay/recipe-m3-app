import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Purge all recipes that were automatically batch-scraped with lazy 'secukupnya' amounts
cursor.execute('''
SELECT r.id, r.title, r.chef, COUNT(i.id) as total_ings,
       SUM(CASE WHEN i.amount = 'secukupnya' OR i.amount = '' THEN 1 ELSE 0 END) as secukupnya_count
FROM recipes r
JOIN ingredient_groups ig ON r.id = ig.recipe_id
JOIN ingredients i ON ig.id = i.group_id
GROUP BY r.id
HAVING secukupnya_count >= total_ings - 1
''')
lazy_recipes = cursor.fetchall()
lazy_ids = [r[0] for r in lazy_recipes if r[0] != 542] # keep fixed 542

print('Purging', len(lazy_ids), 'low quality recipes...')

if lazy_ids:
    id_list = ','.join(str(i) for i in lazy_ids)
    cursor.execute(f'DELETE FROM instructions WHERE recipe_id IN ({id_list})')
    cursor.execute(f'DELETE FROM ingredients WHERE group_id IN (SELECT id FROM ingredient_groups WHERE recipe_id IN ({id_list}))')
    cursor.execute(f'DELETE FROM ingredient_groups WHERE recipe_id IN ({id_list})')
    cursor.execute(f'DELETE FROM recipes WHERE id IN ({id_list})')
    conn.commit()

cursor.execute('SELECT COUNT(*) FROM recipes')
print('Remaining Gold-Standard Recipes in DB:', cursor.fetchone()[0])
conn.close()
