import urllib.request, json, re, html, sqlite3, time, sys

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def parse_og_recipe(shortcode, og_title, og_desc):
    # og_title e.g.: "Sukma Dewi, SE.,M.Ak di Instagram: "PECINTA IKAN..."
    # og_desc e.g.: "14K likes, 259 comments - sukmadewi.official pada October 30, 2023: "CAPTION..."
    
    author = ''
    m_author = re.search(r'-\s*([a-zA-Z0-9_\.]+)\s+(?:on|pada)', og_desc)
    if m_author:
        author = m_author.group(1).strip()
    elif 'di Instagram' in og_title or 'on Instagram' in og_title:
        author = og_title.split('on Instagram')[0].split('di Instagram')[0].strip()
        
    author = author or 'InstagramChef'
    
    # Extract inner caption from quotes
    caption = ''
    m_cap = re.search(r'\"([^\"]+)\"$', og_desc, re.DOTALL) or re.search(r'\"(.+)\"', og_desc, re.DOTALL)
    if m_cap:
        caption = html.unescape(m_cap.group(1))
    else:
        caption = og_desc
        
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 3:
        return None
        
    # Check if lines have genuine culinary keywords
    has_food_keywords = any(any(k in l.lower() for k in ['ikan', 'ayam', 'daging', 'telur', 'bawang', 'cabe', 'garam', 'gula', 'tepung', 'minyak', 'rebus', 'goreng', 'panggang', 'tumis', 'bumbu', 'bahan', 'sdt', 'sdm', 'gr', 'gram', 'ml', 'siung']) for l in lines)
    if not has_food_keywords:
        return None
        
    # Extract title
    title = lines[0]
    if len(title) > 60 or any(title.lower().startswith(x) for x in ['follow', 'original', 'edited', 'http', '#', 'see translation', 'view', 'liked by', 'likes', 'reply']):
        for line in lines[1:6]:
            if line and len(line) >= 4 and not any(line.lower().startswith(x) for x in ['follow', 'original', 'edited', 'http', '#', 'see translation', 'view', 'liked by', 'likes', 'reply']):
                title = line
                break
                
    title = re.sub(r'^[•\-\*\s\(\)]+', '', title)
    title = re.sub(r'[\(\)]+$', '', title).strip()
    if len(title) > 65:
        title = title[:65] + '...'
    if not title or len(title) < 3:
        title = f'Resep Spesial @{author}'

    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    desc = ''
    groups = []
    current_group_name = 'Daftar Bahan & Bumbu'
    current_items = []
    steps = []
    
    in_steps = False
    
    noise_patterns = ['edited', 'what you', 'audio', 'follow', 'reply', 'view', 'like', 'comment', 'see translation', 'http', '#', 'original', 'save', 'recipe', 'resep', 'instagram', 'makanenak', 'masakan']
    
    for l in lines:
        lower = l.lower()
        if any(lower.startswith(k) for k in ['teknik', 'cara', 'step', 'instruction', 'langkah', 'tutorial']):
            if current_items:
                groups.append((current_group_name, current_items))
                current_items = []
            in_steps = True
            continue
            
        if not in_steps and (lower.startswith('(') and lower.endswith(')') and len(l) < 35):
            if current_items:
                groups.append((current_group_name, current_items))
                current_items = []
            current_group_name = l.strip('()')
            continue
            
        if not in_steps:
            if any(lower.startswith(k) for k in ['bahan', 'ingredient']):
                continue
            if len(l) > 2 and not any(lower == np or lower.startswith(np + ':') for np in noise_patterns):
                # Clean item bullet
                clean_item = re.sub(r'^[•\-\*\d\.\s]+', '', l)
                if clean_item and len(clean_item) > 2:
                    current_items.append((clean_item, '', '', ''))
        else:
            if len(l) > 3 and not any(lower.startswith(np) for np in ['http', '#', 'follow', 'save', 'view', 'reply', 'liked']):
                clean_step = re.sub(r'^[\d\.\-\*\s]+', '', l)
                if clean_step and len(clean_step) > 3:
                    steps.append(clean_step)
                    
    if current_items:
        groups.append((current_group_name, current_items))
        
    if not groups:
        return None
        
    if not steps:
        steps = [
            'Siapkan seluruh takaran bahan yang diperlukan sesuai panduan di atas.',
            'Olah dan masak bahan sesuai teknik di video Instagram original.',
            'Sajikan selagi hangat dan nikmati bersama keluarga!'
        ]
        
    desc = lines[0] if len(lines[0]) < 120 else f'Panduan resep lezat dan praktis kreasi dari @{author}.'
    
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': desc,
        'youtube_id': '',
        'media_url': f'https://www.instagram.com/reel/{shortcode}/',
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '15 menit',
        'calories': 'Koleksi Resep Instagram',
        'groups': groups,
        'steps': steps[:10]
    }

def insert_recipe(parsed):
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
        for g_idx, (g_name, items) in enumerate(parsed['groups']):
            cursor.execute('INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)', (r_id, g_name, g_idx))
            g_id = cursor.lastrowid
            for i_idx, it in enumerate(items):
                cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, it[0], it[1], it[2], it[3], i_idx))
        for idx, st in enumerate(parsed['steps']):
            cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, idx+1, f'Langkah {idx+1}', st, 0))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def fetch_and_save(shortcode):
    url = f'https://www.instagram.com/reel/{shortcode}/'
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
        
        parsed = parse_og_recipe(shortcode, og_t, og_d)
        if parsed:
            ok = insert_recipe(parsed)
            if ok:
                print(f"✓ Saved: {parsed['title']} ({parsed['chef']})")
                return True
            else:
                print(f"- Already in DB: {shortcode}")
        else:
            print(f"✗ Skipped non-recipe / no text: {shortcode}")
    except Exception as e:
        print(f"✗ Error {shortcode}:", e)
    return False

def main():
    with open('/tmp/unprocessed_reels.json') as f:
        unprocessed = json.load(f)
        
    print(f"Starting lightweight mobile metadata scrape for {len(unprocessed)} reels...")
    saved_count = 0
    for idx, sc in enumerate(unprocessed):
        ok = fetch_and_save(sc)
        if ok:
            saved_count += 1
        time.sleep(0.4) # Fast and safe
        if (idx + 1) % 25 == 0:
            print(f"--- Progress: {idx+1}/{len(unprocessed)} processed (New recipes saved: {saved_count}) ---")
            
    print(f"Complete! Total newly added recipes: {saved_count}")

if __name__ == "__main__":
    main()
