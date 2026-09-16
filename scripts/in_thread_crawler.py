import json, asyncio, urllib.request, websockets, sqlite3, re, time

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def clean_title_and_parse(r):
    author = r.get('author', '').strip() or 'InstagramChef'
    caption = r.get('caption', '')
    url = r.get('url', '')
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    
    if not lines or 'this content may have been deleted' in caption.lower() or len(lines) < 3:
        return None
        
    title = ''
    for line in lines:
        if line and len(line) >= 4 and not line.lower().startswith(('follow', 'original', 'edited', 'http', '#', 'see translation', 'view', author.lower(), 'liked by', 'likes', 'reply')):
            title = line
            break
            
    if not title:
        title = f'Resep Masakan @{author}'
        
    title = re.sub(r'^[•\-\*\s]+', '', title)
    if len(title) > 65:
        title = title[:65] + '...'

    # extract shortcode from url
    shortcode = url.rstrip('/').split('/')[-1]
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
        if 'cara' in lower or 'step' in lower or 'instruction' in lower or 'langkah' in lower:
            in_steps = True
            in_ingredients = False
            continue
            
        if in_ingredients:
            if len(l) > 2 and not lower.startswith(('http', '#', 'follow', 'save', 'view', 'reply', 'liked')):
                ingredients.append(l)
        elif in_steps:
            if len(l) > 4 and not lower.startswith(('http', '#', 'follow', 'save', 'view', 'reply', 'liked')):
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

async def in_thread_continuous_crawler():
    req = urllib.request.Request('http://localhost:9222/json/list')
    res = urllib.request.urlopen(req)
    tabs = json.loads(res.read())
    ig_tab = [t for t in tabs if 'instagram.com' in t.get('url', '')][0]
    ws_url = ig_tab['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url, max_size=10**8) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
        
        # Navigate to DM thread
        await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'https://www.instagram.com/direct/t/24798134723122041/'}}))
        await asyncio.sleep(6)
        
        processed_urls = set()
        saved_count = 0
        
        # We loop 200 times: find all unclicked reel thumbnails in viewport, click, read modal, close, then scroll up
        for iteration in range(200):
            # 1. Find all thumbnail elements
            get_thumbnails = '''
            (() => {
                const thumbs = Array.from(document.querySelectorAll('img[src*=\"ig_cache_key\"]'));
                return thumbs.length;
            })()
            '''
            await ws.send(json.dumps({'id': 10, 'method': 'Runtime.evaluate', 'params': {'expression': get_thumbnails, 'returnByValue': True}}))
            thumb_count = 0
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 10:
                    thumb_count = msg.get('result', {}).get('result', {}).get('value', 0)
                    break
                    
            # 2. Iterate through each visible thumbnail in the current DOM
            for idx in range(thumb_count):
                click_js = f'''
                (() => {{
                    const thumbs = Array.from(document.querySelectorAll('img[src*=\"ig_cache_key\"]'));
                    if (thumbs.length > {idx}) {{
                        const target = thumbs[{idx}].closest('div[role=\"button\"], div[tabindex]') || thumbs[{idx}];
                        target.click();
                        return true;
                    }}
                    return false;
                }})()
                '''
                await ws.send(json.dumps({'id': 20, 'method': 'Runtime.evaluate', 'params': {'expression': click_js, 'returnByValue': True}}))
                await ws.recv()
                await asyncio.sleep(2.0)
                
                # Check opened modal
                extract_modal_js = '''
                (() => {
                    const article = document.querySelector('article') || document.querySelector('div[role=\"dialog\"]');
                    const author = article?.querySelector('header a, span._ap3a')?.innerText?.trim() || '';
                    const caption = article?.querySelector('h1, span.x193iq5w.xeuugli.x13faqbe')?.innerText || article?.innerText || '';
                    const url = window.location.href;
                    
                    // Click close button if modal is open
                    const closeBtn = document.querySelector('svg[aria-label=\"Close\"], svg[aria-label=\"Tutup\"]')?.closest('div[role=\"button\"]');
                    if (closeBtn) closeBtn.click();
                    
                    return { url, author, caption };
                })()
                '''
                await ws.send(json.dumps({'id': 30, 'method': 'Runtime.evaluate', 'params': {'expression': extract_modal_js, 'returnByValue': True}}))
                while True:
                    msg = json.loads(await ws.recv())
                    if msg.get('id') == 30:
                        val = msg.get('result', {}).get('result', {}).get('value', {})
                        url = val.get('url', '')
                        if url and url not in processed_urls and '/p/' in url or '/reel/' in url:
                            processed_urls.add(url)
                            parsed = clean_title_and_parse(val)
                            if parsed:
                                ok = insert_to_db(parsed)
                                if ok:
                                    saved_count += 1
                                    print(f"[{saved_count}] Saved from DM Modal: {parsed['title']} ({parsed['chef']})")
                        break
                await asyncio.sleep(0.5)

            # 3. Scroll up in chat container to load earlier messages
            scroll_up = '''
            (() => {
                const scrollables = Array.from(document.querySelectorAll('div')).filter(d => {
                    const s = window.getComputedStyle(d);
                    return (s.overflowY === 'auto' || s.overflowY === 'scroll') && d.clientHeight > 300;
                });
                if (scrollables.length > 0) {
                    scrollables[0].scrollTop = 0;
                    scrollables[0].dispatchEvent(new Event('scroll', { bubbles: true }));
                    scrollables[0].dispatchEvent(new WheelEvent('wheel', { deltaY: -1000, bubbles: true }));
                }
            })()
            '''
            await ws.send(json.dumps({'id': 40, 'method': 'Runtime.evaluate', 'params': {'expression': scroll_up}}))
            await asyncio.sleep(2.5)
            
            if (iteration + 1) % 5 == 0:
                print(f"--- Iteration {iteration+1}/200 complete. Total saved: {saved_count} ---")

if __name__ == "__main__":
    asyncio.run(in_thread_continuous_crawler())
