import json, asyncio, urllib.request, websockets, sqlite3, re

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def clean_title_and_parse(r):
    author = r.get('author', '').strip() or 'InstagramChef'
    caption = r.get('caption', '')
    shortcode = r.get('shortcode', '')
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    
    # Filter out empty or broken posts
    if not lines or 'this content may have been deleted' in caption.lower():
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
    
    for l in lines:
        lower = l.lower()
        if 'bahan' in lower or 'ingredient' in lower or 'recipe' in lower:
            in_ingredients = True
            in_steps = False
            continue
        if 'cara' in lower or 'step' in lower or 'instruction' in lower or 'langkah' in lower or 'tutorial' in lower:
            in_steps = True
            in_ingredients = False
            continue
            
        if in_ingredients:
            if len(l) > 3 and not lower.startswith(('http', '#', 'follow', 'save', 'view', 'reply', 'liked')):
                ingredients.append(l)
        elif in_steps:
            if len(l) > 5 and not lower.startswith(('http', '#', 'follow', 'save', 'view', 'reply', 'liked')):
                steps.append(l)
        else:
            if len(desc) < 180 and not lower.startswith(('http', '#', 'follow', 'see translation', 'view', 'liked by', 'likes', 'reply', author.lower())):
                desc += ' ' + l
                
    desc = desc.strip() or f'Panduan resep lezat dan praktis kreasi dari @{author}.'
    if not ingredients:
        ingredients = [l for l in lines[1:15] if len(l) > 3 and not l.lower().startswith(('http', '#', 'follow', 'liked', 'reply', 'see', 'view', author.lower()))]
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
        'media_url': f'https://www.instagram.com/reel/{shortcode}/',
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '15 menit',
        'calories': 'Koleksi Resep Instagram',
        'ingredients': ingredients[:15],
        'steps': steps[:10]
    }

def insert_to_db(parsed):
    if not parsed:
        return
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

async def scrape_single_sc(sc):
    try:
        req_tab = urllib.request.Request(f'http://localhost:9222/json/new?https://www.instagram.com/reel/{sc}/', method='PUT')
        tab = json.loads(urllib.request.urlopen(req_tab).read())
        ws_url = tab['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=10**8) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await asyncio.sleep(2.0)
            
            extract_js = '''
            (() => {
                const author = document.querySelector('header a, span._ap3a')?.innerText?.trim() || '';
                const caption = document.querySelector('h1, span.x193iq5w.xeuugli.x13faqbe, article')?.innerText || document.body.innerText;
                const title = document.title;
                return { author, title, caption: caption.slice(0, 2500) };
            })()
            '''
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': extract_js, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 2:
                    val = msg.get('result', {}).get('result', {}).get('value', {})
                    urllib.request.urlopen(urllib.request.Request(f'http://localhost:9222/json/close/{tab["id"]}', method='PUT'))
                    parsed = clean_title_and_parse({'shortcode': sc, **val})
                    if parsed:
                        insert_to_db(parsed)
                        print(f"✓ Saved: {parsed['title']} ({parsed['chef']})")
                    break
    except Exception as e:
        print(f"✗ Err {sc}:", e)

async def main():
    with open('/tmp/missing_shortcodes.json') as f:
        missing = json.load(f)
        
    print(f"Starting ingestion for {len(missing)} remaining missing recipes...")
    chunk_size = 5
    for i in range(0, len(missing), chunk_size):
        chunk = missing[i:i+chunk_size]
        await asyncio.gather(*(scrape_single_sc(sc) for sc in chunk))
        await asyncio.sleep(0.3)
        
    print("All remaining recipes processed!")

if __name__ == "__main__":
    asyncio.run(main())
