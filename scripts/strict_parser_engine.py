import re, html, json

def strict_parse_recipe(shortcode, author, caption, media_url):
    lines = [l.strip() for l in caption.split('\n') if l.strip()]
    if len(lines) < 3:
        return None
        
    # 1. Identify Numbered/Action Steps vs Pure Ingredients
    ing_lines = []
    step_lines = []
    
    in_steps_section = False
    
    for l in lines:
        lower = l.lower().strip()
        
        # Section triggers
        if any(lower.startswith(k) for k in ['cara', 'langkah', 'step', 'instruction', 'method', 'how to', 'directions']):
            in_steps_section = True
            continue
        if any(lower.startswith(k) for k in ['bahan', 'ingredient', 'bumbu', 'seasoning']):
            in_steps_section = False
            continue
            
        # Check if line is numbered step (e.g. "1. Grill di pan...", "2. Tumis...")
        is_numbered_step = bool(re.match(r'^\d+[\.\)\-]\s+[A-Za-z]', l))
        
        # Check if line is social noise / intro
        is_noise = any(lower.startswith(w) for w in [
            'follow', 'like', 'comment', 'share', 'view', 'reply', 'save', 'simpan', 
            'jangan lupa', 'selamat mencoba', 'happy cooking', 'link di bio', 'link in bio', 
            'dm kami', 'promo', 'baca label', 'alat', 'chopper', 'blender', 'teflon', 
            'spatula', 'garpu', 'sendok', 'wajan', 'panci', 'gengs', 'sorry', 'typo', 
            'mohon maaf', 'snack bocil', 'auto nambah', 'si kecil', 'assalamualaikum', 
            'let\'s make', 'let’s make', 'edited', 'original audio', 'see translation', 
            'worth the effort', 'notes :'
        ]) or l.startswith('#') or l.startswith('http')
        
        if is_noise:
            continue
            
        if in_steps_section or is_numbered_step:
            clean_s = re.sub(r'^\d+[\.\)\-]\s*', '', l).strip()
            if len(clean_s) > 6 and not is_noise:
                step_lines.append(clean_s)
        else:
            # Check if line contains food items
            # Must NOT be a sentence with action verbs unless it's an ingredient specification
            is_action_sentence = bool(re.match(r'^(grill|tumis|masukan|masak|panaskan|rebus|goreng|panggang|blender|kukus|oleskan|tiriskan|aduk|tuang|campur|peel|boil|fry|heat|serve|roll|cut|slice|chop)\b', lower))
            if is_action_sentence and len(l) > 20:
                step_lines.append(l)
            else:
                ing_lines.append(l)
                
    # 2. Strict Ingredient Cleaner
    clean_ingredients = []
    for raw in ing_lines:
        t = re.sub(r'^[•\-\*\s\(\)]+', '', raw).strip()
        if not t or len(t) < 2:
            continue
            
        # Parse exact amount + unit + item
        # e.g. "1sdm bubuk dashi" or "1.5sdt garam" or "800ml air" or "5 bawang putih"
        m = re.match(r'^([\d\/\,\.\-]+)\s*([a-zA-Z]+)?\s+(.*)$', t)
        if m:
            amt = m.group(1).strip()
            potential_unit = m.group(2).strip().lower() if m.group(2) else ''
            rest = m.group(3).strip()
            
            # check if potential_unit is a known metric unit
            valid_units = ['sdm', 'sdt', 'gr', 'gram', 'kg', 'ml', 'l', 'liter', 'buah', 'siung', 'butir', 'lembar', 'batang', 'potong', 'bungkus', 'iris', 'tbsp', 'tsp', 'cup', 'oz', 'g', 'clove', 'slice', 'pinch']
            if potential_unit in valid_units:
                unit = potential_unit
                item = rest
            elif potential_unit: # e.g. "5 bawang putih" -> potential_unit is "bawang", rest is "putih"
                unit = "buah" if any(k in t.lower() for k in ['bawang', 'cabe', 'tomat', 'telur']) else ""
                item = f"{potential_unit} {rest}"
            else:
                unit = ""
                item = rest
                
            item = item.strip(' :-').title()
            if item and len(item) > 1:
                clean_ingredients.append((item, amt, unit, ""))
        else:
            # Check trailing number/unit or item without number
            item = t.strip(' :-').title()
            if len(item) > 2:
                clean_ingredients.append((item, "secukupnya", "", ""))
                
    # 3. Clean Title
    title = ''
    for line in lines[:6]:
        lower = line.lower()
        if 'ala' in lower or any(k in lower for k in ['ayam', 'sosis', 'ramen', 'tahu', 'nugget', 'pancake', 'sambal', 'ikan', 'chick', 'beef', 'potato', 'soup']):
            # Clean title
            t_cand = re.sub(r'^[•\-\*\s\(\)\[\]\d\.]+', '', line).strip()
            t_cand = re.sub(r'[\(\)\[\]!]+$', '', t_cand).strip()
            if len(t_cand) > 5 and not any(t_cand.lower().startswith(w) for w in ['let\'s', 'let’s', 'follow', 'save', 'worth', 'assalamualaikum']):
                title = t_cand
                break
                
    if not title:
        title = f'Resep Kuliner @{author}'
        
    title = title[:50]
    slug = f'resep-{author}-{shortcode}'.lower().replace('_', '-').replace('.', '-')
    
    if len(clean_ingredients) < 2 or not step_lines:
        return None
        
    return {
        'slug': slug,
        'title': title,
        'chef': f'@{author}',
        'description': lines[0] if len(lines[0]) < 120 else f'Resep lezat kreasi dari @{author}.',
        'media_url': media_url,
        'servings': '2-3 Porsi',
        'prep_time': '15 menit',
        'cook_time': '20 menit',
        'calories': 'Koleksi Resep Instagram',
        'ingredients': clean_ingredients[:15],
        'steps': step_lines[:10]
    }

# Test with Angela Tjandra's Char Siu Chicken
sample_cap = """Worth the effort! Cocok buat yang laper tengah malem trs bikin ramyun. 🤭 Let's make Char Siu Chicken ala ramen:

1 gulung pake 2 paha fillet skin on

5 bawang putih
6 iris jahe, tebal 0.5 cm 
2 daun bawang
1sdm bubuk dashi (kaldu bubuk lainnya jg oke)
1sdm palm sugar
1.5sdt garam
1sdm dark soy sauce
1/2sdt white pepper
800ml air

1. Grill di pan sampai minyaknya keluar. Pastikan cukup untuk menumis.
2. Tumis perbawangan. Cukup sampai wangi aja.
3. Masukan ayam, bumbu dan air.
4. Masak 20 menit.
5. Ayam sudah matang. Di kondisi ini bisa ditiriskan lalu disimpan difreezer.
6. Grill di pan atau di torch sebelum penyajian.

#charsiuchicken #charsiu #charsiuramen"""

res = strict_parse_recipe("DQMY90JD7FH", "angelatjandra", sample_cap, "https://www.instagram.com/reel/DQMY90JD7FH/")
print("PARSED TEST RESULT:")
print("Title:", res['title'])
print("Ingredients:", res['ingredients'])
print("Steps:", res['steps'])
