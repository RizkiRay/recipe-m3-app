import sqlite3, re

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

# Polish titles that contain full sentences or "Olahan ... Spesial"
cursor.execute("SELECT id, title, chef, description FROM recipes WHERE title LIKE 'Olahan %' OR LENGTH(title) > 40 OR title LIKE '%!%' OR title LIKE '%?%'")
candidates = cursor.fetchall()

for r_id, title, chef, desc in candidates:
    # Heuristic cleaner
    clean = re.sub(r'^Olahan\s+', '', title)
    clean = re.sub(r'\s+Spesial$', '', clean)
    clean = re.sub(r'[^\w\s\(\)\-]', '', clean).strip()
    
    # Check description for better food name
    d_lower = desc.lower()
    if 'bumbu rujak' in d_lower:
        clean = 'Ayam Bakar Bumbu Rujak Medok'
    elif 'pentol' in d_lower:
        clean = 'Pentol Kriwil Sapi High Protein'
    elif 'sweet potato' in d_lower:
        clean = 'Crispy Sweet Potato (Ubi Manis Renyah)'
    elif 'kebab' in d_lower:
        clean = 'Chicken Kebab Rumahan Praktis'
    elif 'dimsum' in d_lower:
        clean = 'Dimsum Goreng Keju Krispi'
    elif 'keripik' in d_lower:
        clean = 'Keripik Renyah Gurih Rumahan'
    elif 'sup ikan' in d_lower:
        clean = 'Sup Ikan Kemangi Kuah Bening Segar'
    elif 'kacang' in d_lower or 'cilok' in d_lower or 'batagor' in d_lower or 'siomay' in d_lower:
        clean = 'Camilan Gurih dengan Saus Kacang Mantap'
    elif len(clean) > 40:
        clean = clean[:40]
        
    if clean:
        cursor.execute("UPDATE recipes SET title = ? WHERE id = ?", (clean.strip().title(), r_id))

conn.commit()
conn.close()
print("Titles polished cleanly!")
