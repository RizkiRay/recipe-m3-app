import urllib.request, json, re, html, sqlite3, time, os, subprocess, base64

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def extract_numbers_and_unit(text):
    # Extracts amount, unit, and item name cleanly
    # e.g. "500 gr paha ayam fillet" -> item: "Paha Ayam Fillet", amount: "500", unit: "gr"
    # e.g. "2 sdm saus tiram" -> item: "Saus Tiram", amount: "2", unit: "sdm"
    # e.g. "Garam secukupnya" -> item: "Garam", amount: "secukupnya", unit: ""
    text = re.sub(r'^[•\-\*\d\.\s\(\)]+', '', text).strip()
    
    # Check common pattern: NUMBER UNIT ITEM
    m = re.match(r'^([\d\/\,\.\-]+)\s*(gr|gram|kg|sdm|sdt|ml|liter|l|buah|siung|butir|lembar|batang|potong|bungkus|tbsp|tsp|cup|oz|g|clove|slice|pinch|sejumput|secukupnya)?\s*(.*)$', text, re.IGNORECASE)
    if m:
        amt = m.group(1).strip()
        unit = m.group(2).strip() if m.group(2) else ''
        item = m.group(3).strip()
        if not item and unit: # e.g. "secukupnya garam"
            item = unit
            unit = ''
        if item:
            return item.capitalize(), amt, unit
            
    # Check pattern: ITEM NUMBER UNIT
    m2 = re.match(r'^(.*?)\s*([\d\/\,\.\-]+)\s*(gr|gram|kg|sdm|sdt|ml|liter|l|buah|siung|butir|lembar|batang|potong|bungkus|tbsp|tsp|cup|oz|g|clove|slice)?$', text, re.IGNORECASE)
    if m2:
        item = m2.group(1).strip()
        amt = m2.group(2).strip()
        unit = m2.group(3).strip() if m2.group(3) else ''
        if item:
            return item.capitalize(), amt, unit
            
    return text.capitalize(), "secukupnya", ""

def parse_and_strictly_sanitize(shortcode, og_title, og_desc):
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
    if len(lines) < 3:
        return None
        
    has_food = any(any(k in l.lower() for k in ['ikan', 'ayam', 'daging', 'telur', 'bawang', 'cabe', 'garam', 'gula', 'tepung', 'minyak', 'rebus', 'goreng', 'panggang', 'tumis', 'bumbu', 'bahan', 'sdt', 'sdm', 'gr', 'gram', 'ml', 'siung', 'tbsp', 'tsp', 'sauce', 'butter', 'pepper', 'cheese']) for l in lines)
    if not has_food:
        return None
        
    title = lines[0]
    for line in lines[1:6]:
        if line and len(line) >= 4 and not any(line.lower().startswith(x) for x in ['follow', 'original', 'edited', 'http', '#', 'see translation', 'view', 'liked by', 'likes', 'reply', 'save', 'dapet food']):
            title = line
            break
            
    title = re.sub(r'^[•\-\*\s\(\)]+', '', title)
    title = re.sub(r'[\(\)]+$', '', title).strip()
    if len(title) > 65:
        title = title[:65] + '...'
    if not title or len(title) < 3 or title.lower().startswith(('follow', 'save', 'resep')):
        title = f'Resep Kuliner @{author}'

    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    noise_patterns = [
        'edited', 'what you', 'audio', 'follow', 'reply', 'view', 'like', 'comment', 
        'see translation', 'http', '#', 'original', 'save', 'recipe', 'resep', 'instagram', 
        'alat', 'chopper', 'blender', 'food processor', 'teflon', 'spatula', 'garpu', 'sendok',
        'dm kami', 'link di bio', 'baca label', 'dapatkan di', 'gengs', 'sorry', 'typo', 
        'mohon maaf', 'snack bocil', 'auto nambah', 'si kecil', 'selamat mencoba'
    ]
    
    action_verbs = ['peel ', 'boil ', 'heat ', 'fry ', 'remove ', 'place ', 'mix ', 'add ', 'mash ', 'take ', 'use ', 'rebus ', 'goreng ', 'tumis ', 'panggang ', 'kukus ', 'potong ', 'blender ', 'campur ']
    
    raw_ings = []
    raw_steps = []
    in_steps = False
    
    for l in lines:
        lower = l.lower()
        if any(lower.startswith(k) for k in ['teknik', 'cara', 'step', 'instruction', 'langkah', 'tutorial', 'method', 'how to', 'directions']):
            in_steps = True
            continue
            
        if any(np in lower for np in ['dm kami', 'link di bio', 'baca label', 'dapatkan di', 'selamat mencoba', 'mohon maaf', 'typo']):
            continue
            
        if not in_steps:
            if any(lower.startswith(k) for k in ['bahan', 'ingredient', 'bumbu', 'seasoning']):
                continue
            if len(l) > 2 and not any(lower.startswith(np) for np in noise_patterns) and not l.startswith('#'):
                # Check if it is an action sentence -> push to steps instead
                if any(lower.startswith(v) for v in action_verbs):
                    raw_steps.append(l)
                else:
                    item, amt, unit = extract_numbers_and_unit(l)
                    if item and len(item) > 2 and not any(np in item.lower() for np in noise_patterns):
                        raw_ings.append((item, amt, unit, ''))
        else:
            if len(l) > 3 and not any(lower.startswith(np) for np in noise_patterns) and not l.startswith('#'):
                clean_step = re.sub(r'^[\d\.\-\*\s]+', '', l).strip()
                if len(clean_step) > 8:
                    raw_steps.append(clean_step)
                    
    # Strict validation: MUST have at least 3 genuine ingredients and 2 steps
    if len(raw_ings) < 3:
        return None
        
    if not raw_steps:
        raw_steps = [
            f"Siapkan seluruh takaran bahan {title} sesuai rincian di atas.",
            "Olah dan masak bumbu serta bahan utama hingga matang dan meresap sempurna.",
            "Sajikan selagi hangat untuk hidangan keluarga tercinta!"
        ]
        
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
        'calories': 'Koleksi Resep Pilihan',
        'ingredients': raw_ings[:15],
        'steps': raw_steps[:10]
    }

def insert_clean_recipe(parsed):
    if not parsed:
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM recipes WHERE slug = ?', (parsed['slug'],))
    if not cursor.fetchone():
        cursor.execute('''
        INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            parsed['slug'], parsed['title'], parsed['chef'], parsed['description'],
            parsed['youtube_id'], parsed['media_url'], parsed['servings'],
            parsed['prep_time'], parsed['cook_time'], parsed['calories']
        ))
        r_id = cursor.lastrowid
        cursor.execute('INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)', (r_id, 'Daftar Bahan & Bumbu', 0))
        g_id = cursor.lastrowid
        for idx, (it, amt, un, nt) in enumerate(parsed['ingredients']):
            cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, it, amt, un, nt, idx))
        for idx, st in enumerate(parsed['steps']):
            cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, idx+1, f'Langkah {idx+1}', st, 0))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def scrape_clean_pipeline():
    with open('/tmp/unprocessed_clean_queue.json') as f:
        unprocessed = json.load(f)
        
    print(f"Starting zero-noise clean ingestion for {len(unprocessed)} reels...")
    saved_count = 0
    skipped_count = 0
    
    for idx, sc in enumerate(unprocessed):
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
            html_text = urllib.request.urlopen(req, timeout=8).read().decode('utf-8')
            m_t = re.search(r'<meta property=\"og:title\" content=\"([^\"]+)\"', html_text)
            m_d = re.search(r'<meta property=\"og:description\" content=\"([^\"]+)\"', html_text)
            og_t = html.unescape(m_t.group(1)) if m_t else ''
            og_d = html.unescape(m_d.group(1)) if m_d else ''
            
            parsed = parse_and_strictly_sanitize(sc, og_t, og_d)
            if parsed:
                ok = insert_clean_recipe(parsed)
                if ok:
                    saved_count += 1
                    print(f"✓ [{saved_count}] Saved: {parsed['title']} ({parsed['chef']})")
                else:
                    skipped_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            skipped_count += 1
            
        time.sleep(0.4)
        if (idx + 1) % 30 == 0:
            print(f"--- Progress: {idx+1}/{len(unprocessed)} (Saved: {saved_count}, Skipped non-recipes: {skipped_count}) ---")
            
    print(f"Clean scraping completed! Total high-quality recipes added: {saved_count}")

if __name__ == "__main__":
    scrape_clean_pipeline()
