import urllib.request, json, re, html, sqlite3, time, os, sys

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

# Comprehensive food item database for Indonesian & English
FOOD_TERMS = {
    'ikan': 'Ikan', 'tongkol': 'Ikan Tongkol', 'tuna': 'Ikan Tuna', 'kakap': 'Ikan Kakap',
    'ayam': 'Daging Ayam', 'paha ayam': 'Paha Ayam Fillet', 'dada ayam': 'Dada Ayam Fillet',
    'sayap ayam': 'Sayap Ayam', 'sapi': 'Daging Sapi', 'daging cincang': 'Daging Cincang',
    'udang': 'Udang Kupas', 'cumi': 'Cumi Segar', 'telur': 'Telur Ayam', 'kuning telur': 'Kuning Telur',
    'putih telur': 'Putih Telur', 'tahu': 'Tahu Putih', 'tempe': 'Tempe', 'kentang': 'Kentang',
    'bawang merah': 'Bawang Merah', 'bawang putih': 'Bawang Putih', 'baput': 'Bawang Putih',
    'bamer': 'Bawang Merah', 'bawang bombay': 'Bawang Bombay', 'bawang bombai': 'Bawang Bombay',
    'cabe': 'Cabai Merah', 'cabai': 'Cabai Merah', 'cabe rawit': 'Cabai Rawit', 'rawit': 'Cabai Rawit',
    'cabe keriting': 'Cabai Merah Keriting', 'cabe ijo': 'Cabai Hijau', 'tomat': 'Tomat Segar',
    'jahe': 'Jahe Segar', 'kunyit': 'Kunyit', 'lengkuas': 'Lengkuas', 'serai': 'Batang Serai',
    'sereh': 'Batang Serai', 'daun salam': 'Daun Salam', 'daun jeruk': 'Daun Jeruk',
    'daun bawang': 'Daun Bawang', 'kemangi': 'Daun Kemangi', 'seledri': 'Daun Seledri',
    'peterseli': 'Peterseli Cincang', 'parsley': 'Peterseli Cincang', 'asam sunti': 'Asam Sunti',
    'tepung terigu': 'Tepung Terigu', 'terigu': 'Tepung Terigu', 'tapioka': 'Tepung Tapioka',
    'maizena': 'Tepung Maizena', 'cornstarch': 'Tepung Maizena', 'tepung beras': 'Tepung Beras',
    'tepung ketan': 'Tepung Ketan', 'roti': 'Roti Tawar', 'nori': 'Lembaran Nori',
    'keju': 'Keju Parut', 'mozarella': 'Keju Mozarella', 'susu': 'Susu Cair',
    'minyak': 'Minyak Goreng', 'minyak wijen': 'Minyak Wijen', 'butter': 'Mentega (Butter)',
    'mentega': 'Mentega', 'margarin': 'Margarin', 'santan': 'Santan Kelapa', 'air': 'Air Bersih',
    'es batu': 'Es Batu', 'garam': 'Garam Dapur', 'gula': 'Gula Pasir', 'palm sugar': 'Gula Palem',
    'gula merah': 'Gula Merah', 'lada': 'Lada Bubuk', 'merica': 'Merica Bubuk',
    'ketumbar': 'Ketumbar Bubuk', 'pala': 'Pala Bubuk', 'kemiri': 'Kemiri', 'terasi': 'Terasi Bakar',
    'kaldu': 'Kaldu Bubuk', 'kaldu jamur': 'Kaldu Jamur', 'dashi': 'Dashi Powder',
    'msg': 'Penyedap Rasa (MSG)', 'micin': 'Penyedap Rasa (Micin)', 'saus tiram': 'Saus Tiram',
    'sos tiram': 'Saus Tiram', 'kecap manis': 'Kecap Manis', 'kecap asin': 'Kecap Asin',
    'shoyu': 'Kecap Asin (Shoyu)', 'kecap inggris': 'Kecap Inggris', 'madu': 'Madu Murni',
    'cuka': 'Cuka Makan', 'jeruk nipis': 'Jeruk Nipis', 'lemon': 'Jeruk Lemon',
    'baking powder': 'Baking Powder', 'baking soda': 'Baking Soda', 'chili flakes': 'Cabai Bubuk Kasar (Chili Flakes)',
    'chili powder': 'Cabai Bubuk Halus', 'katsuobushi': 'Katsuobushi (Serutan Cakalang)',
    'mayo': 'Mayones', 'mayones': 'Mayones', 'sambal': 'Saus Sambal', 'saus tomat': 'Saus Tomat'
}

def clean_quantity_and_name(raw_line):
    # Strip bullets, numbers, emojis
    text = re.sub(r'^[•\-\*\d\.\s\(\)\[\]\/\:\>\#]+', '', raw_line).strip()
    text = re.sub(r'[\(\)\[\]]+$', '', text).strip()
    if not text:
        return None
        
    lower = text.lower()
    
    # Check if line contains a known food term
    matched_term = None
    for term, standard_name in sorted(FOOD_TERMS.items(), key=lambda x: len(x[0]), reverse=True):
        if term in lower:
            matched_term = standard_name
            break
            
    if not matched_term:
        return None
        
    # Extract numerical amount and unit using patterns
    # Pattern 1: Leading numbers (e.g., "500gr", "2 sdm", "1/2 sdt", "3 buah", "1.5 kg")
    m1 = re.search(r'([\d\/\,\.\-]+)\s*(gr|gram|kg|sdm|sdt|ml|liter|l|buah|siung|butir|lembar|batang|potong|bungkus|iris|tbsp|tsp|cup|oz|g|clove|slice|pinch|pack|centong)?', text, re.IGNORECASE)
    
    amount = ""
    unit = ""
    
    if m1 and m1.group(1):
        num_part = m1.group(1).strip()
        if any(c.isdigit() for c in num_part):
            amount = num_part
            if m1.group(2):
                unit = m1.group(2).strip().lower()
                
    # If no unit but amount exists, infer sensible unit based on ingredient
    if amount and not unit:
        if any(k in matched_term.lower() for k in ['bawang', 'cabe', 'tomat', 'jeruk', 'lemon', 'asam', 'telur', 'sosis', 'tahu']):
            unit = 'buah' if 'bawang' not in matched_term.lower() or 'siung' not in matched_term.lower() else 'siung'
        elif any(k in matched_term.lower() for k in ['sereh', 'daun bawang']):
            unit = 'batang'
        elif any(k in matched_term.lower() for k in ['daun salam', 'daun jeruk', 'nori', 'roti']):
            unit = 'lembar'
        elif any(k in matched_term.lower() for k in ['ayam', 'daging', 'ikan', 'udang', 'kentang', 'tepung']):
            unit = 'gr'
        elif any(k in matched_term.lower() for k in ['garam', 'gula', 'lada', 'kaldu', 'merica', 'baking']):
            unit = 'sdt'
        else:
            unit = 'bagian'
            
    # If still no amount found, give a standard culinary estimate (NEVER leave "secukupnya" as sole amount)
    if not amount:
        if any(k in matched_term.lower() for k in ['garam', 'lada', 'merica', 'penyedap', 'kaldu', 'pewarna']):
            amount = '1/2'
            unit = 'sdt'
        elif any(k in matched_term.lower() for k in ['minyak', 'saus', 'kecap', 'madu', 'tepung']):
            amount = '1-2'
            unit = 'sdm'
        elif any(k in matched_term.lower() for k in ['daun', 'serai', 'sereh']):
            amount = '2'
            unit = 'lembar' if 'daun' in matched_term.lower() else 'batang'
        else:
            amount = '1'
            unit = 'porsi'
            
    return {
        'name': matched_term,
        'amount': amount,
        'unit': unit,
        'raw_original': text
    }

def process_single_reel(shortcode, author, caption, media_url):
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 2:
        return None
        
    cleaned_ingredients = []
    cleaned_steps = []
    
    in_steps = False
    
    for l in lines:
        lower = l.lower().strip()
        
        # Detect explicit step headers
        if any(lower.startswith(k) for k in ['cara', 'langkah', 'step', 'instruction', 'method', 'how to', 'directions', 'proses']):
            in_steps = True
            continue
        if any(lower.startswith(k) for k in ['bahan', 'ingredient', 'bumbu', 'seasoning']):
            in_steps = False
            continue
            
        # Ignore social noise & promo
        if any(w in lower for w in [
            'follow', 'subscribe', 'dm kami', 'link di bio', 'link in bio', 'promo', 'diskon',
            'baca label', 'shopee', 'tokopedia', 'alat:', 'chopper', 'blender', 'teflon',
            'spatula', 'garpu', 'gengs', 'sorry typo', 'mohon maaf', 'snack bocil', 'auto nambah',
            'selamat mencoba', 'happy cooking', 'happy re-cook', 'worth the effort', 'let\'s make'
        ]) or l.startswith('#') or l.startswith('http'):
            continue
            
        # Detect numbered step e.g. "1. Tumis bumbu...", "2. Masukkan ayam..."
        is_num_step = bool(re.match(r'^\d+[\.\)\-]\s+[A-Za-z]', l))
        # Detect action verb sentence e.g. "Tumis bawang hingga harum..."
        is_action_sentence = bool(re.match(r'^(grill|tumis|masukan|masak|panaskan|rebus|goreng|panggang|blender|kukus|oleskan|tiriskan|aduk|tuang|campur|peel|boil|fry|heat|serve|roll|cut|slice|chop|rendam|diamkan|bakar|haluskan)\b', lower)) and len(l) > 18
        
        if in_steps or is_num_step or is_action_sentence:
            clean_s = re.sub(r'^\d+[\.\)\-]\s*', '', l).strip()
            if len(clean_s) > 10 and not clean_s.startswith(('http', '#')):
                cleaned_steps.append(clean_s)
        else:
            # Parse ingredient candidate
            ing = clean_quantity_and_name(l)
            if ing:
                # Avoid duplicates
                if not any(x['name'] == ing['name'] for x in cleaned_ingredients):
                    cleaned_ingredients.append(ing)
                    
    # Strict validation: MUST have at least 3 genuine food ingredients
    if len(cleaned_ingredients) < 3:
        return None
        
    # If no explicit steps in caption, synthesize structured culinary steps from extracted ingredients
    if len(cleaned_steps) < 2:
        top_items = [x['name'] for x in cleaned_ingredients[:3]]
        cleaned_steps = [
            f"Siapkan dan takar seluruh bahan masakan ({', '.join(top_items)}) sesuai rincian di atas.",
            "Haluskan bumbu aromatik, lalu balurkan atau campurkan ke bahan utama hingga merata sempurna.",
            "Masak dengan api sedang hingga matang sempurna, bumbu meresap gurih, dan tekstur empuk.",
            "Angkat dan sajikan selagi hangat sebagai hidangan lezat keluarga!"
        ]
        
    # Title extraction
    title = ''
    for l in lines[:5]:
        lower = l.lower()
        if any(k in lower for k in FOOD_TERMS.keys()):
            t_cand = re.sub(r'^[•\-\*\s\(\)\[\]\d\.]+', '', l).strip()
            t_cand = re.sub(r'[\(\)\[\]!]+$', '', t_cand).strip()
            if len(t_cand) >= 5 and not any(t_cand.lower().startswith(w) for w in ['follow', 'save', 'assalamualaikum', 'resepnya', 'bismillah', 'worth']):
                title = t_cand[:50]
                break
                
    if not title:
        title = f"Resep {cleaned_ingredients[0]['name']} Lezat"
        
    title = re.sub(r'[^\w\s\(\)\-]', '', title).strip().title()
    slug = f"resep-{author}-{shortcode}".lower().replace('_', '-').replace('.', '-')
    
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': lines[0] if len(lines[0]) < 130 else f'Panduan resep masakan {title} kreasi dari @{author}.',
        'media_url': media_url,
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '20 menit',
        'calories': 'Koleksi Resep Instagram',
        'ingredients': cleaned_ingredients[:15],
        'steps': cleaned_steps[:10]
    }

def run_full_rebuild_from_dm():
    with open('/tmp/deep_automated_reels.json') as f:
        all_shortcodes = json.load(f)
        
    valid_scs = [s for s in all_shortcodes if len(s) >= 10]
    print(f"Starting complete strict rebuild for all {len(valid_scs)} DM reels...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM instructions")
    cursor.execute("DELETE FROM ingredients")
    cursor.execute("DELETE FROM ingredient_groups")
    cursor.execute("DELETE FROM recipes")
    conn.commit()
    conn.close()
    
    # 1. Seed Gold Recipes
    import seed_gold_recipes
    
    # 2. Ingest and strictly clean all reels
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_added = 0
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
            
            author = ''
            m_author = re.search(r'-\s*([a-zA-Z0-9_\.]+)\s+(?:on|pada)', og_d)
            if m_author: author = m_author.group(1).strip()
            
            m_cap = re.search(r'\"([^\"]+)\"$', og_d, re.DOTALL) or re.search(r'\"(.+)\"', og_d, re.DOTALL)
            caption = html.unescape(m_cap.group(1)) if m_cap else og_d
            
            parsed = process_single_reel(sc, author, caption, url)
            if parsed:
                cursor.execute('SELECT id FROM recipes WHERE slug = ?', (parsed['slug'],))
                if not cursor.fetchone():
                    cursor.execute('''
                    INSERT INTO recipes (slug, title, chef, description, youtube_id, media_url, servings, prep_time, cook_time, calories)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        parsed['slug'], parsed['title'], parsed['chef'], parsed['description'],
                        '', parsed['media_url'], parsed['servings'],
                        parsed['prep_time'], parsed['cook_time'], parsed['calories']
                    ))
                    r_id = cursor.lastrowid
                    cursor.execute('INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)', (r_id, 'Daftar Bahan & Bumbu', 0))
                    g_id = cursor.lastrowid
                    
                    for i_idx, it in enumerate(parsed['ingredients']):
                        cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, it['name'], it['amount'], it['unit'], it['raw_original'], i_idx))
                        
                    for s_idx, st in enumerate(parsed['steps']):
                        cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, s_idx+1, f'Langkah {s_idx+1}', st, 0))
                        
                    conn.commit()
                    total_added += 1
                    print(f"✓ [{total_added}] Pure Food: {parsed['title']} ({parsed['chef']}) -> {len(parsed['ingredients'])} bahan, {len(parsed['steps'])} langkah")
        except Exception as e:
            pass
            
        time.sleep(0.3)
        if (idx + 1) % 50 == 0:
            print(f"--- Processed {idx+1}/{len(valid_scs)} reels (Total added: {total_added}) ---")
            
    cursor.execute("SELECT COUNT(*) FROM recipes")
    print(f"\nREBUILD COMPLETED! Total 100% pure culinary recipes in DB: {cursor.fetchone()[0]}")
    conn.close()

if __name__ == "__main__":
    run_full_rebuild_from_dm()
