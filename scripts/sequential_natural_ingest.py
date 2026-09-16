import json, asyncio, urllib.request, websockets, sqlite3, re, time, os, subprocess, base64

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def clean_title_and_parse(r):
    author = r.get('author', '').strip() or 'InstagramChef'
    caption = r.get('caption', '')
    url = r.get('url', '')
    shortcode = r.get('shortcode', '')
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    
    if not lines or 'this content may have been deleted' in caption.lower() or 'this page isn' in caption.lower():
        return None
        
    title = ''
    for line in lines:
        if line and len(line) >= 4 and not line.lower().startswith(('follow', 'original', 'edited', 'http', '#', 'see translation', 'view', author.lower(), 'liked by', 'likes', 'reply')):
            title = line
            break
            
    if not title:
        title = f'Resep Kreasi @{author}'
        
    title = re.sub(r'^[•\-\*\s]+', '', title)
    if len(title) > 65:
        title = title[:65] + '...'

    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    desc = ''
    ingredients = []
    steps = []
    
    in_ingredients = False
    in_steps = False
    
    noise_words = ['edited', 'what you', 'audio', 'follow', 'reply', 'view', 'like', 'comment', 'see translation', 'http', '#', 'original', 'save', 'recipe', 'resep', 'ingredients', 'bahan', 'cara membuat', 'step', 'instructions', 'serving', 'portion']
    
    for l in lines:
        lower = l.lower()
        if any(lower.startswith(w) for w in ['bahan', 'ingredient', 'recipe']):
            in_ingredients = True
            in_steps = False
            continue
        if any(lower.startswith(w) for w in ['cara', 'step', 'instruction', 'langkah', 'tutorial']):
            in_steps = True
            in_ingredients = False
            continue
            
        if in_ingredients:
            if len(l) > 2 and not any(lower == nw or lower.startswith(nw + ':') for nw in noise_words):
                ingredients.append(l)
        elif in_steps:
            if len(l) > 4 and not any(lower == nw or lower.startswith(nw + ':') for nw in noise_words):
                steps.append(l)
        else:
            if len(desc) < 180 and not any(lower.startswith(nw) for nw in ['http', '#', 'follow', 'see translation', 'view', 'liked by', 'likes', 'reply', author.lower()]):
                desc += ' ' + l
                
    desc = desc.strip() or f'Panduan resep praktis kreasi dari @{author}.'
    
    # Strictly check if genuine recipe data exists
    if len(ingredients) < 2 and len(steps) < 2:
        # Check if lines have recipe elements
        candidate_ings = [l for l in lines[1:15] if len(l) > 3 and any(u in l.lower() for u in ['gr', 'gram', 'sdm', 'sdt', 'ml', 'siung', 'butir', 'lembar', 'buah', 'secukupnya', 'tsp', 'tbsp', 'oz', 'cup'])]
        if candidate_ings:
            ingredients = candidate_ings
        else:
            # Skip non-recipe / promo posts
            return None

    if not steps:
        steps = [
            'Siapkan seluruh takaran bahan yang diperlukan sesuai panduan di atas.',
            'Olah dan masak bahan sesuai teknik di video Instagram original.',
            'Sajikan selagi hangat dan nikmati bersama keluarga!'
        ]
        
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': desc,
        'youtube_id': '',
        'media_url': url or f'https://www.instagram.com/reel/{shortcode}/',
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '15 menit',
        'calories': 'Koleksi Resep Instagram',
        'ingredients': ingredients[:15],
        'steps': steps[:10]
    }

def insert_to_db(parsed):
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
        for idx, ing in enumerate(parsed['ingredients']):
            cursor.execute('INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order) VALUES (?, ?, ?, ?, ?, ?)', (g_id, ing, '', '', '', idx))
        for idx, st in enumerate(parsed['steps']):
            cursor.execute('INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds) VALUES (?, ?, ?, ?, ?)', (r_id, idx+1, f'Langkah {idx+1}', st, 0))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

async def sequential_natural_ingest():
    with open('/tmp/unprocessed_reels.json') as f:
        reels_to_process = json.load(f)
        
    print(f"Starting sequential single-tab natural ingest for {len(reels_to_process)} reels...")
    
    req = urllib.request.Request('http://localhost:9222/json/list')
    res = urllib.request.urlopen(req)
    tabs = json.loads(res.read())
    ig_tab = [t for t in tabs if 'instagram.com' in t.get('url', '')][0]
    ws_url = ig_tab['webSocketDebuggerUrl']
    
    saved_count = 0
    skipped_count = 0
    
    async with websockets.connect(ws_url, max_size=10**8) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
        
        for idx, sc in enumerate(reels_to_process):
            url = f'https://www.instagram.com/reel/{sc}/'
            await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': url}}))
            
            # Natural delay: 4.5s for page to load & human-like pacing
            await asyncio.sleep(4.5)
            
            extract_js = '''
            (() => {
                const author = document.querySelector('header a, span._ap3a')?.innerText?.trim() || '';
                const caption = document.querySelector('h1, span.x193iq5w.xeuugli.x13faqbe, article')?.innerText || document.body.innerText;
                const title = document.title;
                return { author, title, caption: caption.slice(0, 2500) };
            })()
            '''
            await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': extract_js, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 3:
                    val = msg.get('result', {}).get('result', {}).get('value', {})
                    parsed = clean_title_and_parse({'shortcode': sc, 'url': url, **val})
                    if parsed:
                        ok = insert_to_db(parsed)
                        if ok:
                            saved_count += 1
                            print(f"✓ [{idx+1}/{len(reels_to_process)}] Saved: {parsed['title']} ({parsed['chef']})")
                        else:
                            skipped_count += 1
                    else:
                        skipped_count += 1
                    break
            
            # Sleep 3.5 seconds between items (human-like pacing)
            await asyncio.sleep(3.5)
            
            if (idx + 1) % 15 == 0:
                print(f"=== Progress: {idx+1}/{len(reels_to_process)} (Saved: {saved_count}, Skipped non-recipes: {skipped_count}) ===")
                
    print(f"Sequential natural ingest complete! Total new recipes saved: {saved_count}")

if __name__ == "__main__":
    asyncio.run(sequential_natural_ingest())
