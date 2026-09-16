import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "recipes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        chef TEXT,
        description TEXT,
        youtube_id TEXT,
        servings TEXT,
        prep_time TEXT,
        cook_time TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredient_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        amount TEXT,
        unit TEXT,
        notes TEXT,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (group_id) REFERENCES ingredient_groups(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        step_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        detail TEXT NOT NULL,
        timer_seconds INTEGER DEFAULT 0,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    # Seed data: Egg Chicken Roll HokBen
    cursor.execute("SELECT id FROM recipes WHERE slug = 'egg-chicken-roll-hokben'")
    existing = cursor.fetchone()
    if not existing:
        cursor.execute("""
        INSERT INTO recipes (slug, title, chef, description, youtube_id, servings, prep_time, cook_time)
        VALUES (
            'egg-chicken-roll-hokben',
            'Egg Chicken Roll ala HokBen',
            'Chef Devina Hermawan',
            'Juicy, gurih, kulit empuk berserat lembut, cocok untuk stok lauk beku (frozen food) keluarga.',
            'ShLeN8usfg8',
            '4-5 Gulung (±25-30 potong)',
            '25 menit',
            '20 menit kukus + 5 menit goreng'
        )
        """)
        recipe_id = cursor.lastrowid
        
        # Groups
        groups_data = [
            ('Bahan Kulit', [
                ('Telur (atau 1 utuh + 2 kuning)', '2', 'butir', 'Gunakan 2 putih telur untuk isian daging'),
                ('Tepung Terigu', '80', 'gr', 'Protein sedang'),
                ('Tepung Maizena', '40', 'gr', ''),
                ('Air', '250-280', 'ml', 'Sesuaikan kekentalan adonan'),
                ('Minyak Goreng', '2', 'sdm', 'Campur ke adonan agar tidak lengket'),
                ('Garam', '1/2', 'sdt', ''),
                ('Kaldu Bubuk', '1/2', 'sdt', ''),
                ('Pewarna Kuning Makanan', 'secukupnya', '', 'Opsional agar warna lebih cantik')
            ]),
            ('Bahan Isian Daging', [
                ('Paha Ayam Fillet', '600', 'gr', 'Keringkan dengan tisu dapur sebelum digiling'),
                ('Putih Telur', '2', 'butir', 'Bikin tekstur kenyal dan juicy'),
                ('Bawang Putih', '5-6', 'siung', 'Cincang halus'),
                ('Bawang Goreng', '2', 'sdm', 'Opsional untuk aroma'),
                ('Minyak Wijen', '1', 'sdm', 'Aroma khas HokBen'),
                ('Bubuk Pala / Ngohiong', '1/2', 'sdt', 'Opsional'),
                ('Garam', '1-2', 'sdt', 'Giling di awal bersama daging'),
                ('Gula Pasir', '1', 'sdm', ''),
                ('Kaldu Bubuk / MSG', '1', 'sdt', ''),
                ('Lada Putih Bubuk', '1/2', 'sdt', ''),
                ('Es Batu / Air Es', '50-70', 'gr', 'Menjaga adonan tetap dingin saat digiling'),
                ('Tepung Maizena', '2-3', 'sdm', ''),
                ('Roti Tawar + Air/Susu 50ml', '2', 'lembar', 'Opsional: melembutkan tekstur daging')
            ]),
            ('Perekat & Pelengkap', [
                ('Campuran Terigu + Air', 'secukupnya', '', 'Lem ujung kulit'),
                ('Minyak Goreng', 'secukupnya', '', 'Untuk menggoreng deep-fry')
            ])
        ]
        
        for g_idx, (g_name, items) in enumerate(groups_data):
            cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, ?, ?)", (recipe_id, g_name, g_idx))
            group_id = cursor.lastrowid
            for i_idx, item_tuple in enumerate(items):
                cursor.execute("""
                INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (group_id, item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], i_idx))
        
        # Steps
        steps_data = [
            (1, 'Buat Adonan Kulit', 'Campur terigu, maizena, telur, air, minyak, garam, kaldu bubuk, dan pewarna kuning. Aduk rata menggunakan whisk hingga licin tanpa gumpalan, lalu saring.', 0),
            (2, 'Dadar Kulit Dadar', 'Panaskan wajan teflon anti-lengket (api kecil-sedang). Tuang 1 centong adonan, putar wajan hingga rata. Masak sampai pinggir kulit terkelupas sendiri. Angkat dan dinginkan. Ulangi sampai adonan habis.', 0),
            (3, 'Giling Daging Pertama', 'Keringkan paha ayam fillet. Masukkan ayam, garam, gula, dan kaldu bubuk ke dalam food processor. Giling 2-3 menit sampai serat protein pecah dan tekstur lengket/bouncy.', 180),
            (4, 'Bumbui Isian', 'Masukkan bawang putih cincang, bawang goreng, lada, bubuk pala, minyak wijen, putih telur, maizena, dan es batu. Giling rata kembali.', 0),
            (5, 'Tambahkan Roti Lembut (Opsional)', 'Rendam 2 lembar roti tawar dengan 50 ml air/susu. Masukkan ke adonan daging dan giling sebentar sampai menyatu lembut.', 0),
            (6, 'Gulung Daging & Kulit', 'Ambil selembar kulit dadar (diameter ±26-28cm). Ratakan adonan ayam memanjang di bagian bawah. Gulung 1 putaran, lipat sisi kiri dan kanan ke dalam, gulung rapat. Oleskan larutan terigu sebagai lem di ujungnya.', 0),
            (7, 'Kukus Roll', 'Siapkan kukusan yang dialasi baking paper/dioles minyak. Kukus Egg Chicken Roll selama 15-20 menit hingga matang. Angkat dan biarkan dingin sempurna agar set & mudah dipotong.', 1200),
            (8, 'Potong & Goreng', 'Potong serong roll yang sudah dingin. Goreng dalam minyak panas dengan api sedang hingga kuning keemasan dan renyah di luar. Sajikan hangat dengan salad dan saus!', 300)
        ]
        
        for step in steps_data:
            cursor.execute("""
            INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds)
            VALUES (?, ?, ?, ?, ?)
            """, (recipe_id, step[0], step[1], step[2], step[3]))
            
    conn.commit()
    conn.close()

def get_recipe_by_slug(slug='egg-chicken-roll-hokben'):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM recipes WHERE slug = ?", (slug,))
    recipe = cursor.fetchone()
    if not recipe:
        conn.close()
        return None
    
    recipe_dict = dict(recipe)
    
    # Get groups and ingredients
    cursor.execute("SELECT * FROM ingredient_groups WHERE recipe_id = ? ORDER BY sort_order", (recipe['id'],))
    groups = cursor.fetchall()
    recipe_dict['ingredient_groups'] = []
    for g in groups:
        g_dict = dict(g)
        cursor.execute("SELECT * FROM ingredients WHERE group_id = ? ORDER BY sort_order", (g['id'],))
        g_dict['items'] = [dict(i) for i in cursor.fetchall()]
        recipe_dict['ingredient_groups'].append(g_dict)
        
    # Get instructions
    cursor.execute("SELECT * FROM instructions WHERE recipe_id = ? ORDER BY step_number", (recipe['id'],))
    recipe_dict['instructions'] = [dict(s) for s in cursor.fetchall()]
    
    conn.close()
    return recipe_dict

def get_all_recipes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, slug, title, chef, description, youtube_id, prep_time, cook_time FROM recipes ORDER BY id DESC")
    recipes = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return recipes

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully with SQLite.")
