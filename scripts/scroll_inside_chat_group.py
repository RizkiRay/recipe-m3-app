import json, asyncio, urllib.request, websockets, sqlite3, re, time

DB_PATH = '/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db'

def clean_title_and_parse(r):
    author = r.get('author', '').strip() or 'InstagramChef'
    caption = r.get('caption', '')
    url = r.get('url', '')
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    
    if not lines or 'this content may have been deleted' in caption.lower() or len(lines) < 2:
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

    shortcode = url.rstrip('/').split('/')[-1] if url else f'{int(time.time()*1000)}'
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

async def scroll_strictly_inside_dm_group():
    req = urllib.request.Request('http://localhost:9222/json/list')
    res = urllib.request.urlopen(req)
    tabs = json.loads(res.read())
    ig_tab = [t for t in tabs if 'instagram.com' in t.get('url', '')][0]
    ws_url = ig_tab['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url, max_size=10**8) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
        
        # Ensure we are on the specific group thread URL
        await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'https://www.instagram.com/direct/t/24798134723122041/'}}))
        await asyncio.sleep(5)
        
        processed_links = set()
        saved_count = 0
        
        # 150 scroll iterations purely inside the right-hand chat message panel
        for iteration in range(150):
            # Target the chat message container (right pane only, excluding left sidebar)
            scroll_inside_chat_panel = '''
            (() => {
                // Find all containers strictly located on the right message area (left > 350px)
                const chatContainers = Array.from(document.querySelectorAll('div')).filter(d => {
                    const rect = d.getBoundingClientRect();
                    const style = window.getComputedStyle(d);
                    const isScrollable = style.overflowY === 'auto' || style.overflowY === 'scroll';
                    return rect.left > 350 && rect.width > 400 && isScrollable;
                });
                
                if (chatContainers.length > 0) {
                    const panel = chatContainers[0];
                    panel.scrollTop = 0;
                    panel.dispatchEvent(new Event('scroll', { bubbles: true }));
                    panel.dispatchEvent(new WheelEvent('wheel', { deltaY: -800, bubbles: true }));
                    return { found: true, scrollHeight: panel.scrollHeight, scrollTop: panel.scrollTop };
                }
                
                // Fallback: Dispatch wheel on body at right coordinate
                window.dispatchEvent(new WheelEvent('wheel', { clientX: 700, clientY: 300, deltaY: -800, bubbles: true }));
                return { found: false };
            })()
            '''
            await ws.send(json.dumps({'id': 100 + iteration, 'method': 'Runtime.evaluate', 'params': {'expression': scroll_inside_chat_panel, 'returnByValue': True}}))
            await asyncio.sleep(1.8)
            
            # Click any uncollected reel card in the chat pane
            inspect_and_click = '''
            (() => {
                // Find reel cards in chat pane
                const cards = Array.from(document.querySelectorAll('div.x78zum5.xdt5ytf, div[role=\"row\"]')).filter(c => {
                    const r = c.getBoundingClientRect();
                    return r.left > 350; // strictly inside chat panel
                });
                
                for (let i = 0; i < cards.length; i++) {
                    const c = cards[i];
                    const author = c.querySelector('a[href^=\"/\"]')?.innerText?.trim();
                    const img = c.querySelector('img[src*=\"ig_cache_key\"], img');
                    if (author && img && !c.dataset.scraped) {
                        c.dataset.scraped = 'true';
                        img.click();
                        return { clicked: true, author };
                    }
                }
                return { clicked: false };
            })()
            '''
            await ws.send(json.dumps({'id': 200 + iteration, 'method': 'Runtime.evaluate', 'params': {'expression': inspect_and_click, 'returnByValue': True}}))
            clicked_res = {}
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 200 + iteration:
                    clicked_res = msg.get('result', {}).get('result', {}).get('value', {})
                    break
                    
            if clicked_res.get('clicked'):
                await asyncio.sleep(2.5)
                # Read opened article modal
                extract_modal_js = '''
                (() => {
                    const article = document.querySelector('article') || document.querySelector('div[role=\"dialog\"]');
                    const author = article?.querySelector('header a, span._ap3a')?.innerText?.trim() || '';
                    const caption = article?.querySelector('h1, span.x193iq5w.xeuugli.x13faqbe')?.innerText || article?.innerText || '';
                    const url = window.location.href;
                    
                    const closeBtn = document.querySelector('svg[aria-label=\"Close\"], svg[aria-label=\"Tutup\"]')?.closest('div[role=\"button\"]');
                    if (closeBtn) closeBtn.click();
                    
                    return { url, author, caption };
                })()
                '''
                await ws.send(json.dumps({'id': 300 + iteration, 'method': 'Runtime.evaluate', 'params': {'expression': extract_modal_js, 'returnByValue': True}}))
                while True:
                    msg = json.loads(await ws.recv())
                    if msg.get('id') == 300 + iteration:
                        val = msg.get('result', {}).get('result', {}).get('value', {})
                        url = val.get('url', '')
                        if url and url not in processed_links:
                            processed_links.add(url)
                            parsed = clean_title_and_parse(val)
                            if parsed:
                                ok = insert_to_db(parsed)
                                if ok:
                                    saved_count += 1
                                    print(f"[{saved_count}] Saved from Chat Panel: {parsed['title']} ({parsed['chef']})")
                        break
                await asyncio.sleep(1.0)
                
            if (iteration + 1) % 10 == 0:
                print(f"--- Iteration {iteration+1}/150 (Inside DM Group Chat) ---")

if __name__ == "__main__":
    asyncio.run(scroll_strictly_inside_dm_group())
