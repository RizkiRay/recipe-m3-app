import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# 1. Delete low quality incomplete entries from auto-scrape (e.g. coffee, vague single-action posts)
cursor.execute("DELETE FROM recipes WHERE id IN (736, 739, 746, 756, 766, 767, 770, 772, 778)")
cursor.execute("DELETE FROM instructions WHERE recipe_id NOT IN (SELECT id FROM recipes)")
cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id NOT IN (SELECT id FROM recipes)")
cursor.execute("DELETE FROM ingredients WHERE group_id NOT IN (SELECT id FROM ingredient_groups)")

# 2. Re-sanitize & polish remaining recipes in DB
cursor.execute("SELECT id, title, chef, description FROM recipes")
recipes = cursor.fetchall()

for r_id, title, chef, desc in recipes:
    # Get all ingredients for this recipe
    cursor.execute('''
    SELECT i.id, i.item, i.amount, i.unit 
    FROM ingredients i 
    JOIN ingredient_groups ig ON i.group_id = ig.id 
    WHERE ig.recipe_id = ? 
    ORDER BY i.sort_order ASC
    ''', (r_id,))
    ings = cursor.fetchall()
    
    for i_id, item, amt, unit in ings:
        item_clean = item.strip()
        lower = item_clean.lower()
        
        # Check if item is an action sentence, header, or noise
        is_bad = False
        
        # Check noise / emojis / greetings
        if any(w in lower for w in [
            'resep', 'recipe', 'cara', 'langkah', 'step', 'method', 'tips', 'happy re-cook',
            'edited', 'original audio', 'follow', 'view', 'like', 'reply', 'comment', 'see translation',
            '#', 'http', 'dm kami', 'link di bio', 'baca label', 'alat', 'chopper', 'blender',
            'teflon', 'spatula', 'garpu', 'sendok', 'wajan', 'panci', 'gengs', 'sorry', 'typo',
            'mohon maaf', 'snack bocil', 'auto nambah', 'si kecil', 'assalamualaikum', 'let\'s make',
            'worth the effort', 'notes :', 'mudah banget', 'servings:', 'diamkan hingga', 'sweet stiff starter',
            'dough', 'selamat mencoba'
        ]):
            is_bad = True
            
        # Check if it starts with an action verb (kata kerja)
        if any(lower.startswith(v) for v in [
            'grill ', 'tumis ', 'masukan ', 'rebus ', 'goreng ', 'panggang ', 'kukus ', 'potong ', 
            'blender ', 'campur ', 'aduk ', 'tuang ', 'oleskan ', 'tiriskan ', 'simpan ', 'rendam ', 
            'peel ', 'boil ', 'heat ', 'fry ', 'remove ', 'place ', 'mix ', 'add ', 'mash ', 'take ', 
            'use ', 'slice ', 'chop ', 'cut ', 'stir ', 'whisk ', 'drain ', 'bake ', 'roast ', 'serve '
        ]):
            is_bad = True
            
        # Check if item length is too long (sentence leak) or too short
        if len(item_clean) > 40 or len(item_clean) < 2 or item_clean == title:
            is_bad = True
            
        if is_bad:
            print(f"Purged bad ingredient [{i_id}] from Recipe [{r_id}] {title}: \"{item_clean}\"")
            cursor.execute("DELETE FROM ingredients WHERE id = ?", (i_id,))
            continue
            
        # Clean prefix noise like bullets or numbers
        clean_name = re.sub(r'^[•\-\*\d\.\s\(\)\/:]+', '', item_clean).strip()
        clean_name = re.sub(r'[\(\)]+$', '', clean_name).strip()
        
        # If amount is secukupnya but unit has value, clean it
        if amt == 'secukupnya' and unit:
            unit = ''
            
        if clean_name != item:
            cursor.execute("UPDATE ingredients SET item = ?, amount = ?, unit = ? WHERE id = ?", (clean_name.title(), amt, unit, i_id))

    # Clean instructions
    cursor.execute("SELECT id, detail FROM instructions WHERE recipe_id = ? ORDER BY step_number ASC", (r_id,))
    steps = cursor.fetchall()
    for s_id, detail in steps:
        d_clean = detail.strip()
        d_lower = d_clean.lower()
        if any(w in d_lower for w in ['selamat mencoba', 'happy cooking', 'tips untuk menghidangkan', 'calories & macros', 'original recipe', 'high-protein recipes', 'try it and let me know']):
            cursor.execute("DELETE FROM instructions WHERE id = ?", (s_id,))
            print(f"Purged farewell/tips step [{s_id}] from Recipe [{r_id}] {title}: \"{d_clean[:40]}\"")

conn.commit()

# Delete recipes with fewer than 3 ingredients or 2 steps
cursor.execute('''
DELETE FROM recipes 
WHERE id NOT IN (SELECT DISTINCT recipe_id FROM ingredient_groups WHERE id IN (SELECT DISTINCT group_id FROM ingredients))
   OR (SELECT COUNT(*) FROM ingredients WHERE group_id IN (SELECT id FROM ingredient_groups WHERE recipe_id = recipes.id)) < 3
   OR (SELECT COUNT(*) FROM instructions WHERE recipe_id = recipes.id) < 2
''')
deleted_invalid = cursor.rowcount

conn.commit()
cursor.execute("SELECT COUNT(*) FROM recipes")
print(f"Sanitization complete! Deleted {deleted_invalid} invalid recipes. Total pure recipes: {cursor.fetchone()[0]}")
conn.close()
