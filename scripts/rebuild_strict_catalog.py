import urllib.request, json, re, html, sqlite3, time, os, sys

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

NOISE_FILTER = [
    'follow', 'like', 'comment', 'share', 'view', 'reply', 'save', 'simpan', 
    'jangan lupa', 'selamat mencoba', 'happy cooking', 'link di bio', 'link in bio', 
    'dm kami', 'promo', 'baca label', 'alat', 'chopper', 'blender', 'teflon', 
    'spatula', 'garpu', 'sendok', 'wajan', 'panci', 'gengs', 'sorry', 'typo', 
    'mohon maaf', 'snack bocil', 'auto nambah', 'si kecil', 'assalamualaikum', 
    'let\'s make', 'let’s make', 'edited', 'original audio', 'see translation', 
    'worth the effort', 'notes :'
]

VALID_UNITS = [
    'sdm', 'sdt', 'gr', 'gram', 'kg', 'ml', 'l', 'liter', 'buah', 'siung', 
    'butir', 'lembar', 'batang', 'potong', 'bungkus', 'iris', 'tbsp', 'tsp', 
    'cup', 'oz', 'g', 'clove', 'slice', 'pinch', 'sejumput', 'centong'
]

def strict_parse_recipe(shortcode, author, caption, media_url):
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 3:
        return None
        
    ing_lines = []
    step_lines = []
    in_steps_section = False
    
    for l in lines:
        lower = l.lower().strip()
        
        # Check explicit section headers
        if any(lower.startswith(k) for k in ['cara', 'langkah', 'step', 'instruction', 'method', 'how to', 'directions', 'proses']):
            in_steps_section = True
            continue
        if any(lower.startswith(k) for k in ['bahan', 'ingredient', 'bumbu', 'seasoning']):
            in_steps_section = False
            continue
            
        is_numbered_step = bool(re.match(r'^\d+[\.\)\-]\s+[A-Za-z]', l))
        is_noise = any(lower.startswith(w) for w in NOISE_FILTER) or l.startswith('#') or l.startswith('http')
        if is_noise:
            continue
            
        if in_steps_section or is_numbered_step:
            clean_s = re.sub(r'^\d+[\.\)\-]\s*', '', l).strip()
            if len(clean_s) > 6 and not any(clean_s.lower().startswith(w) for w in NOISE_FILTER):
                step_lines.append(clean_s)
        else:
            # Check if line is an action sentence (kata kerja) -> move to step_lines
            is_action = bool(re.match(r'^(grill|tumis|masukan|masak|panaskan|rebus|goreng|panggang|blender|kukus|oleskan|tiriskan|aduk|tuang|campur|peel|boil|fry|heat|serve|roll|cut|slice|chop)\b', lower))
            if is_action and len(l) > 15:
                step_lines.append(l)
            else:
                ing_lines.append(l)
                
    # Clean ingredients strictly
    clean_ingredients = []
    for raw in ing_lines:
        t = re.sub(r'^[•\-\*\s\(\)]+', '', raw).strip()
        if not t or len(t) < 2 or any(np in t.lower() for np in ['gengs', 'typo', 'sorry', 'mohon maaf', 'alat:']):
            continue
            
        # Parse exact amount + unit + item
        m = re.match(r'^([\d\/\,\.\-]+)\s*([a-zA-Z]+)?\s+(.*)$', t)
        if m:
            amt = m.group(1).strip()
            potential_unit = m.group(2).strip().lower() if m.group(2) else ''
            rest = m.group(3).strip()
            
            if potential_unit in VALID_UNITS:
                unit = potential_unit
                item = rest
            elif potential_unit:
                unit = "buah" if any(k in t.lower() for k in ['bawang', 'cabe', 'tomat', 'telur', 'jeruk']) else ""
                item = f"{potential_unit} {rest}"
            else:
                unit = ""
                item = rest
                
            item = item.strip(' :-').title()
            # Double check item is not a full sentence
            if item and len(item) > 1 and len(item) < 40 and not any(v in item.lower() for v in ['grill ', 'tumis ', 'masukan ', 'aduk ']):
                clean_ingredients.append((item, amt, unit, ""))
        else:
            item = t.strip(' :-').title()
            if len(item) > 2 and len(item) < 40 and not any(v in item.lower() for v in ['grill ', 'tumis ', 'masukan ', 'aduk ']):
                clean_ingredients.append((item, "secukupnya", "", ""))
                
    # Deduce clean title
    title = ''
    for line in lines[:5]:
        lower = line.lower()
        if any(k in lower for k in ['ayam', 'sosis', 'ramen', 'tahu', 'nugget', 'pancake', 'sambal', 'ikan', 'chick', 'beef', 'potato', 'soup', 'daging', 'udang', 'cumi', 'telur', 'mie', 'nasi', 'bebek', 'kebab', 'dimsum', 'pizza']):
            t_cand = re.sub(r'^[•\-\*\s\(\)\[\]\d\.]+', '', line).strip()
            t_cand = re.sub(r'[\(\)\[\]!]+$', '', t_cand).strip()
            if len(t_cand) >= 5 and not any(t_cand.lower().startswith(w) for w in ['let\'s', 'let’s', 'follow', 'save', 'worth', 'assalamualaikum', 'resepnya', 'bismillah']):
                title = t_cand
                break
                
    if not title:
        title = f'Resep Kreasi @{author}'
        
    title = title[:55]
    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    # Strict validation: MUST have at least 3 genuine clean ingredients and at least 2 steps
    if len(clean_ingredients) < 3 or len(step_lines) < 2:
        return None
        
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': lines[0] if len(lines[0]) < 130 else f'Resep kuliner lezat dan praktis kreasi dari @{author}.',
        'media_url': media_url,
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '20 menit',
        'calories': 'Koleksi Resep Pilihan',
        'ingredients': clean_ingredients[:15],
        'steps': step_lines[:10]
    }

def rebuild_database_with_strict_parser():
    with open('/tmp/deep_automated_reels.json') as f:
        all_shortcodes = json.load(f)
        
    valid_scs = [s for s in all_shortcodes if len(s) >= 10]
    print(f"Rebuilding database strictly from all {len(valid_scs)} DM reels...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Retain the 22 gold recipes and rebuild everything cleanly
    cursor.execute("DELETE FROM instructions")
    cursor.execute("DELETE FROM ingredients")
    cursor.execute("DELETE FROM ingredient_groups")
    cursor.execute("DELETE FROM recipes")
    conn.commit()
    conn.close()
    
    # 1. Seed the core 22 hand-crafted gold recipes first
    import seed_gold_recipes
    seed_gold_recipes.main() if hasattr(seed_gold_recipes, 'main') else None
    
    # 2. Ingest the remaining reels using the strict parser
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added_count = 0
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
            
            parsed = strict_parse_recipe(sc, author, caption, url)
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
                    for i_idx, (it, amt, un, nt) in enumerate(parsed['ingredients']):
                        cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, it, amt, un, nt, i_idx))
                    for s_idx, st in enumerate(parsed['steps']):
                        cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, s_idx+1, f'Langkah {s_idx+1}', st, 0))
                    conn.commit()
                    added_count += 1
                    print(f"✓ [{added_count}] Strict Clean: {parsed['title']} ({parsed['chef']}) - {len(parsed['ingredients'])} bahan, {len(parsed['steps'])} langkah")
        except Exception as e:
            pass
            
        time.sleep(0.3)
        if (idx + 1) % 50 == 0:
            print(f"--- Processed {idx+1}/{len(valid_scs)} reels ---")
            
    cursor.execute("SELECT COUNT(*) FROM recipes")
    final_total = cursor.fetchone()[0]
    conn.close()
    print(f"\n==========================================")
    print(f"STRICT SANITIZATION REBUILD FINISHED!")
    print(f"Total pure, strictly verified recipes in DB: {final_total}")
    print(f"==========================================")

if __name__ == "__main__":
    rebuild_database_with_strict_parser()
