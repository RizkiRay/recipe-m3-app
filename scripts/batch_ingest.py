import json, asyncio, urllib.request, websockets, os, sqlite3, re

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def clean_title_and_parse(r):
    author = r.get('author', '').strip()
    caption = r.get('caption', '')
    shortcode = r.get('shortcode', '')
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 3:
        return None
        
    title = lines[0]
    if len(title) > 60 or title.lower().startswith(('follow', 'original', 'audio', author.lower())):
        for line in lines[1:5]:
            if line and not line.lower().startswith(('follow', 'original', 'edited', 'http', '#', 'see translation', 'view')):
                title = line
                break
                
    title = re.sub(r'^[•\-\*\s]+', '', title)
    if len(title) > 65:
        title = title[:65] + '...'
    if not title or len(title) < 3:
        title = f'Resep Spesial @{author}'

    slug = f'resep-{author}-{shortcode}'.lower()
    
    desc = ''
    ingredients = []
    steps = []
    
    in_ingredients = False
    in_steps = False
    
    for l in lines[1:30]:
        lower = l.lower()
        if 'bahan' in lower or 'ingredient' in lower:
            in_ingredients = True
            in_steps = False
            continue
        if 'cara' in lower or 'step' in lower or 'instruction' in lower or 'langkah' in lower:
            in_steps = True
            in_ingredients = False
            continue
            
        if in_ingredients:
            if len(l) > 3 and not lower.startswith(('http', '#', 'follow', 'save')):
                ingredients.append(l)
        elif in_steps:
            if len(l) > 5 and not lower.startswith(('http', '#', 'follow', 'save')):
                steps.append(l)
        else:
            if len(desc) < 180 and not lower.startswith(('http', '#', 'follow', 'see translation', 'view', 'liked by', 'likes', 'reply')):
                desc += ' ' + l
                
    desc = desc.strip() or f'Panduan resep lezat dan praktis kreasi dari @{author}.'
    if not ingredients:
        ingredients = [l for l in lines[2:12] if len(l) > 3 and not l.lower().startswith(('http', '#', 'follow', 'liked', 'reply', 'see', 'view'))]
    if not steps:
        steps = [
            'Siapkan seluruh takaran bahan yang diperlukan sesuai daftar di atas.',
            'Campurkan dan olah bahan sesuai panduan teknik di video original.',
            'Masak hingga matang sempurna dan sajikan selagi hangat!'
        ]
        
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}' if author else '@InstagramChef',
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

async def scrape_and_save_direct(shortcode):
    try:
        req_tab = urllib.request.Request(f'http://localhost:9222/json/new?https://www.instagram.com/reel/{shortcode}/', method='PUT')
        tab = json.loads(urllib.request.urlopen(req_tab).read())
        ws_url = tab['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=10**8) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await asyncio.sleep(2.2)
            
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
                    parsed = clean_title_and_parse({'shortcode': shortcode, **val})
                    if parsed:
                        insert_to_db(parsed)
                        print(f"✓ Saved: {parsed['title']} ({parsed['chef']})")
                    break
    except Exception as e:
        print(f"✗ Err {shortcode}:", e)

async def main():
    with open('/tmp/deep_automated_reels.json') as f:
        shortcodes = json.load(f)
    valid_shortcodes = [s for s in shortcodes if len(s) >= 10]
    
    # Process all from index 50 to end
    tasks = valid_shortcodes[50:]
    print(f"Processing remaining {len(tasks)} shortcodes...")
    
    # Process in chunks of 4 concurrent tabs for speed
    chunk_size = 4
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i:i+chunk_size]
        await asyncio.gather(*(scrape_and_save_direct(sc) for sc in chunk))
        await asyncio.sleep(0.5)

    print("All tasks finished!")

if __name__ == "__main__":
    asyncio.run(main())
