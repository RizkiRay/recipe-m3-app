import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Process all ingredients across all recipes
cursor.execute('''
SELECT i.id, r.id, r.title, i.item, i.notes
FROM ingredients i
JOIN ingredient_groups ig ON i.group_id = ig.id
JOIN recipes r ON ig.recipe_id = r.id
''')
all_items = cursor.fetchall()

def extract_prep_note(item_name, raw_note):
    lower_item = item_name.lower()
    lower_raw = raw_note.lower() if raw_note else ""
    
    # 1. Clean prep notes dictionary (hanya instruksi persiapan fisik bahan yang relevan)
    prep_actions = [
        (r'\b(?:giling|dihaluskan|halus|cincang halus|chopper)\b', 'Giling / cincang halus'),
        (r'\b(?:iris tipis|iris serong|iris halus|rajang|diiris)\b', 'Iris tipis'),
        (r'\b(?:memarkan|geprek|digeprek)\b', 'Memarkan / geprek'),
        (r'\b(?:kupas|dikupas)\b', 'Kupas bersih'),
        (r'\b(?:potong dadu|potong kotak|dadu)\b', 'Potong dadu'),
        (r'\b(?:peras|peras airnya|keringkan)\b', 'Peras airnya hingga kering'),
        (r'\b(?:kocok lepas|kocok)\b', 'Kocok lepas'),
        (r'\b(?:rebus matang|rebus sebentar|rebus)\b', 'Rebus sebentar / empuk'),
        (r'\b(?:sangrai|disangrai)\b', 'Sangrai wangi'),
        (r'\b(?:bakar|panggang)\b', 'Bakar / panggang')
    ]
    
    extracted_prep = ""
    for pattern, clean_prep in prep_actions:
        if re.search(pattern, lower_raw):
            extracted_prep = clean_prep
            break
            
    # Check if raw_note contains quality/flavor tip
    if not extracted_prep and raw_note:
        clean_n = re.sub(r'^[•\-\*\d\.\s\(\)]+', '', raw_note).strip()
        clean_n = re.sub(r'[\(\)]+$', '', clean_n).strip()
        # If it's a short meaningful note and not a duplicate of item name or a full sentence
        if 3 < len(clean_n) < 35 and clean_n.lower() != lower_item and not any(w in clean_n.lower() for w in ['secukupnya', 'gram', 'sdm', 'sdt', 'http', '#', 'resep']):
            extracted_prep = clean_n.capitalize()
            
    return extracted_prep

updated_count = 0
for i_id, r_id, r_title, item_name, raw_note in all_items:
    clean_note = extract_prep_note(item_name, raw_note)
    cursor.execute("UPDATE ingredients SET notes = ? WHERE id = ?", (clean_note, i_id))
    if clean_note:
        updated_count += 1

conn.commit()
print(f"Refined prep notes for all ingredients. Total meaningful notes: {updated_count}")

# Check Recipe 941 (Nugget Ayam) specifically
cursor.execute("SELECT i.item, i.amount, i.unit, i.notes FROM ingredients i JOIN ingredient_groups ig ON i.group_id = ig.id WHERE ig.recipe_id = 941")
print("\nSample Recipe 941 (Nugget Ayam) Ingredients:")
for row in cursor.fetchall():
    print(f" - {row[0]}: {row[1]} {row[2]} ({row[3]})")

conn.close()
