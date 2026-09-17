import urllib.request, json, re, html, sqlite3, time, sys

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

# Food keywords that confirm a line is a genuine food ingredient
FOOD_KEYWORDS = [
    'ayam', 'daging', 'sapi', 'ikan', 'udang', 'cumi', 'telur', 'tahu', 'tempe', 'kentang',
    'bawang', 'baput', 'bamer', 'cabe', 'cabai', 'rawit', 'tomat', 'jahe', 'kunyit', 'lengkuas',
    'sereh', 'serai', 'daun salam', 'daun jeruk', 'daun bawang', 'kemangi', 'seledri', 'peterseli',
    'tepung', 'terigu', 'tapioka', 'maizena', 'beras', 'ketan', 'roti', 'nori', 'keju', 'susu',
    'minyak', 'mentega', 'butter', 'margarin', 'santan', 'air', 'es batu', 'garam', 'gula',
    'lada', 'merica', 'ketumbar', 'pala', 'kemiri', 'terasi', 'kaldu', 'msg', 'micin', 'penyedap',
    'saus', 'saos', 'kecap', 'madu', 'cuka', 'jeruk', 'lemon', 'asam', 'pasta', 'mie', 'bihun',
    'kwetiau', 'kulit', 'sosis', 'bakso', 'nugget', 'dimsum', 'mayo', 'mayones', 'sambal',
    'chicken', 'beef', 'pork', 'fish', 'shrimp', 'prawn', 'squid', 'egg', 'tofu', 'potato',
    'garlic', 'shallot', 'onion', 'chili', 'chilli', 'tomato', 'ginger', 'scallion', 'parsley',
    'flour', 'starch', 'cornstarch', 'rice', 'bread', 'cheese', 'milk', 'cream', 'oil',
    'butter', 'water', 'ice', 'salt', 'sugar', 'pepper', 'coriander', 'bouillon', 'sauce',
    'soy sauce', 'honey', 'vinegar', 'lime', 'noodle', 'pasta', 'sausage', 'mayo', 'sesame'
]

# Action verbs to identify cooking instruction lines
STEP_ACTION_VERBS = [
    'rebus', 'goreng', 'tumis', 'panggang', 'kukus', 'bakar', 'potong', 'iris', 'cincang',
    'blender', 'haluskan', 'campur', 'aduk', 'marinasi', 'lumuri', 'balur', 'diamkan',
    'masak', 'didihkan', 'tuang', 'masukkan', 'saring', 'tiriskan', 'angkat', 'sajikan',
    'bentuk', 'bulatkan', 'gulung', 'bungkus', 'panaskan', 'olesi', 'simpan', 'rendam',
    'peel', 'boil', 'heat', 'fry', 'remove', 'place', 'mix', 'add', 'mash', 'take',
    'use', 'slice', 'chop', 'cut', 'stir', 'whisk', 'drain', 'bake', 'roast', 'grill',
    'steam', 'serve', 'roll', 'wrap', 'pour', 'season', 'combine', 'blend', 'cook'
]

NOISE_FILTER = [
    'follow', 'like', 'comment', 'share', 'view', 'reply', 'save', 'simpan', 'jangan lupa',
    'selamat mencoba', 'happy cooking', 'link di bio', 'link in bio', 'dm kami', 'promo',
    'diskon', 'voucher', 'shopee', 'tokopedia', 'baca label', 'alat', 'chopper', 'blender',
    'teflon', 'spatula', 'garpu', 'sendok', 'wajan', 'panci', 'mitochiba', 'idealife',
    'gengs', 'sorry', 'typo', 'mohon maaf', 'snack bocil', 'auto nambah', 'si kecil',
    'edited', 'original audio', 'see translation', 'copyright', 'warning'
]

def parse_line_ingredient(text):
    text = re.sub(r'^[•\-\*\d\.\s\(\)]+', '', text).strip()
    
    # Check NUMBER UNIT ITEM (e.g., "500 gr paha ayam", "2 sdm saus tiram")
    m = re.match(r'^([\d\/\,\.\-]+)\s*(gr|gram|kg|sdm|sdt|ml|liter|l|buah|siung|butir|lembar|batang|potong|bungkus|tbsp|tsp|cup|oz|g|clove|slice|pinch|sejumput|secukupnya)?\s*(.*)$', text, re.IGNORECASE)
    if m:
        amt = m.group(1).strip()
        unit = m.group(2).strip() if m.group(2) else ''
        item = m.group(3).strip()
        if not item and unit:
            item = unit
            unit = ''
        if item:
            item = re.sub(r'^[•\-\*\s\(\)\/:]+', '', item).strip()
            return item.title(), amt, unit
            
    # Check ITEM NUMBER UNIT (e.g., "Paha ayam 500 gr", "Bawang putih 3 siung")
    m2 = re.match(r'^(.*?)\s*([\d\/\,\.\-]+)\s*(gr|gram|kg|sdm|sdt|ml|liter|l|buah|siung|butir|lembar|batang|potong|bungkus|tbsp|tsp|cup|oz|g|clove|slice)?$', text, re.IGNORECASE)
    if m2:
        item = m2.group(1).strip()
        amt = m2.group(2).strip()
        unit = m2.group(3).strip() if m2.group(3) else ''
        if item:
            item = re.sub(r'^[•\-\*\s\(\)\/:]+', '', item).strip()
            return item.title(), amt, unit
            
    return text.title(), "secukupnya", ""

def parse_and_clean_recipe(shortcode, og_title, og_desc):
    author = ''
    m_author = re.search(r'-\s*([a-zA-Z0-9_\.]+)\s+(?:on|pada)', og_desc)
    if m_author:
        author = m_author.group(1).strip()
    elif 'di Instagram' in og_title or 'on Instagram' in og_title:
        author = og_title.split('on Instagram')[0].split('di Instagram')[0].strip()
    author = author or 'InstagramChef'
    
    m_cap = re.search(r'\"([^\"]+)\"$', og_desc, re.DOTALL) or re.search(r'\"(.+)\"', og_desc, re.DOTALL)
    caption = html.unescape(m_cap.group(1)) if m_cap else og_desc
    
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 2:
        return None
        
    # Check if caption contains culinary substance
    food_match_count = sum(1 for l in lines if any(k in l.lower() for k in FOOD_KEYWORDS))
    if food_match_count < 2:
        return None
        
    # Extract clean Title
    title = ''
    for line in lines[:5]:
        clean_l = re.sub(r'^[•\-\*\s\(\)\[\]\d\.]+', '', line).strip()
        lower = clean_l.lower()
        if len(clean_l) >= 4 and not any(lower.startswith(x) for x in ['follow', 'original', 'edited', 'http', '#', 'see translation', 'view', 'liked by', 'likes', 'reply', 'save', 'dapet food', 'bismillah']):
            if any(k in lower for k in FOOD_KEYWORDS) or any(v in lower for v in STEP_ACTION_VERBS):
                title = clean_l
                break
                
    if not title:
        for line in lines[:5]:
            clean_l = re.sub(r'^[•\-\*\s\(\)\[\]\d\.]+', '', line).strip()
            if len(clean_l) >= 4 and not any(clean_l.lower().startswith(x) for x in ['follow', 'original', 'edited', 'http', '#', 'see translation']):
                title = clean_l
                break
                
    title = re.sub(r'^[•\-\*\s\(\)\[\]]+', '', title)
    title = re.sub(r'[\(\)\[\]]+$', '', title).strip()
    if len(title) > 60:
        title = title[:60] + '...'
    if not title or len(title) < 3:
        title = f'Resep Kreasi @{author}'

    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    # Parse Ingredients and Steps cleanly
    raw_ings = []
    raw_steps = []
    in_steps = False
    
    for l in lines:
        lower = l.lower().strip()
        
        # Skip pure noise lines
        if any(lower == np or lower.startswith(np + ':') or lower.startswith(np + ' ') for np in NOISE_FILTER) or lower.startswith('#') or lower.startswith('http'):
            continue
            
        # Check section transitions
        if any(lower.startswith(k) for k in ['teknik', 'cara', 'step', 'instruction', 'langkah', 'tutorial', 'method', 'how to', 'directions', 'proses']):
            in_steps = True
            continue
        if any(lower.startswith(k) for k in ['bahan', 'ingredient', 'bumbu', 'seasoning', 'recipe', 'resep']):
            in_steps = False
            continue
            
        if not in_steps:
            # If line is an action instruction, move to steps
            if any(lower.startswith(v) for v in STEP_ACTION_VERBS) and len(l) > 15:
                clean_s = re.sub(r'^[\d\.\-\*\s]+', '', l).strip()
                if len(clean_s) > 10:
                    raw_steps.append(clean_s)
            else:
                # Check if it contains a food keyword
                if any(k in lower for k in FOOD_KEYWORDS):
                    item, amt, unit = parse_line_ingredient(l)
                    # Exclude noise words from ingredient name
                    if not any(np in item.lower() for np in NOISE_FILTER) and len(item) > 1:
                        raw_ings.append((item, amt, unit, ''))
        else:
            clean_s = re.sub(r'^[\d\.\-\*\s]+', '', l).strip()
            if len(clean_s) > 10:
                raw_steps.append(clean_s)
                
    # If no explicit steps in caption, generate proper structured cooking steps from the ingredients
    if not raw_steps and raw_ings:
        main_items = ', '.join([ing[0] for ing in raw_ings[:3]])
        raw_steps = [
            f"Siapkan seluruh takaran bahan {title} ({main_items}) sesuai rincian di atas.",
            "Campurkan bumbu marinasi dan olah bahan utama hingga merata sempurna.",
            "Masak dengan api sedang hingga matang sempurna dan bumbu meresap gurih.",
            "Angkat dan sajikan selagi hangat untuk menu spesial keluarga!"
        ]
        
    if len(raw_ings) < 2:
        return None
        
    desc = lines[0] if len(lines[0]) < 140 else f'Panduan resep kuliner lezat dan bergizi kreasi dari @{author}.'
    
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': desc,
        'youtube_id': '',
        'media_url': f'https://www.instagram.com/reel/{shortcode}/',
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '20 menit',
        'calories': 'Koleksi Resep Instagram',
        'ingredients': raw_ings[:18],
        'steps': raw_steps[:10]
    }

def save_recipe(parsed):
    if not parsed:
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM recipes WHERE slug = ?', (parsed['slug'],))
    existing = cursor.fetchone()
    
    if existing:
        r_id = existing[0]
        # Update details
        cursor.execute('''
        UPDATE recipes 
        SET title = ?, chef = ?, description = ?, media_url = ?, servings = ?, prep_time = ?, cook_time = ?, calories = ?
        WHERE id = ?
        ''', (
            parsed['title'], parsed['chef'], parsed['description'],
            parsed['media_url'], parsed['servings'],
            parsed['prep_time'], parsed['cook_time'], parsed['calories'], r_id
        ))
        # Clear old groups and steps
        cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = ?", (r_id,))
        for gid in cursor.fetchall():
            cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (gid[0],))
        cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id = ?", (r_id,))
        cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (r_id,))
    else:
        cursor.execute('''
        INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            parsed['slug'], parsed['title'], parsed['chef'], parsed['description'],
            parsed['youtube_id'], parsed['media_url'], parsed['servings'],
            parsed['prep_time'], parsed['cook_time'], parsed['calories']
        ))
        r_id = cursor.lastrowid
        
    # Insert clean ingredients
    cursor.execute('INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)', (r_id, 'Daftar Bahan & Bumbu', 0))
    g_id = cursor.lastrowid
    for idx, (it, amt, un, nt) in enumerate(parsed['ingredients']):
        cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, it, amt, un, nt, idx))
        
    # Insert clean steps
    for idx, st in enumerate(parsed['steps']):
        cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, idx+1, f'Langkah {idx+1}', st, 0))
        
    conn.commit()
    conn.close()
    return True

def run_full_sanitization():
    with open('/tmp/deep_automated_reels.json') as f:
        all_shortcodes = json.load(f)
        
    valid_scs = [s for s in all_shortcodes if len(s) >= 10]
    print(f"Starting thorough sanitization and re-ingest of all {len(valid_scs)} DM reels...")
    
    success = 0
    for idx, sc in enumerate(valid_scs):
        url = f'https://www.instagram.com/reel/{sc}/'
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        )
        try:
            html_text = urllib.request.urlopen(req, timeout=6).read().decode('utf-8')
            m_t = re.search(r'<meta property=\"og:title\" content=\"([^\"]+)\"', html_text)
            m_d = re.search(r'<meta property=\"og:description\" content=\"([^\"]+)\"', html_text)
            og_t = html.unescape(m_t.group(1)) if m_t else ''
            og_d = html.unescape(m_d.group(1)) if m_d else ''
            
            parsed = parse_and_clean_recipe(sc, og_t, og_d)
            if parsed:
                ok = save_recipe(parsed)
                if ok:
                    success += 1
                    print(f"✓ [{success}] Cleaned & Saved: {parsed['title']} ({parsed['chef']}) - {len(parsed['ingredients'])} bahan")
        except Exception as e:
            pass
            
        time.sleep(0.35)
        if (idx + 1) % 50 == 0:
            print(f"--- Processed {idx+1}/{len(valid_scs)} reels (Success: {success}) ---")
            
    print(f"Full sanitization complete! Total valid recipes in DB: {success}")

if __name__ == "__main__":
    run_full_sanitization()
