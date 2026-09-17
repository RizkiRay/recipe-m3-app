import sqlite3

conn = sqlite3.connect('/Users/rizkiraynaldy/playground/resep-m3-app/recipes.db')
cursor = conn.cursor()

titles_map = {
    729: 'Ayam Salt-Roasted Crispy (Xương Gà Rang Muối)',
    730: 'Tahu Bulat Kopong Tasikmalaya',
    731: 'Nori Gulung Udang Crispy (Snack Bocil)',
    732: 'Crispy Potato Rings (Cincin Kentang Renyah)',
    734: 'Hambagu Sapi Jepang (Japanese Hamburger Steak)',
    738: 'Chikuro Gurih Keju Renyah',
    741: 'Ayam Tumis Merah Hijau Gurih',
    742: 'Pork Loin Scallion Rice Bowl',
    748: 'Padakjeon (Korean Chicken Scallion Pancake)',
    750: 'Ayam Batokok Lado Mudo Padang',
    752: 'Telur Oseng Bawang Gurih Praktis',
    753: 'Bayam Telur Saus Tiram',
    754: 'Chicken Meal-Prep Strips High Protein',
    755: 'Ikan Bakar Bumbu Kuning Daun Pisang',
    758: 'Sapi Lada Hitam Paprika Gurih',
    759: 'Kaldu Ramen Ayam Kental (Tori Paitan)',
    760: 'Dimsum Sawi Putih Gulung Ayam Udang',
    762: 'Crispy Fried Chicken Drumsticks',
    763: 'Ikan Bakar Khas Bima NTB Gurih Asam Manis',
    764: 'Telur Kukus Daging Cincang Smoky Wijen',
    765: 'Seaweed Chicken Mushroom Egg Drop Soup',
    769: 'Sambal Terubuk Bakar Cobek Sunda',
    771: 'Ayam Rebus Lembut Minyak Wijen (Poached Chicken)',
    773: 'BBQ Fried Chicken Wings Smoked Butter',
    775: 'Ayam Songkem Kukus Bumbu Medok',
    776: 'Nori Udang Panggang Teflon Crispy',
    777: 'Char Siu Chicken Ala Ramen Gurih Karamel'
}

for r_id, title in titles_map.items():
    cursor.execute("UPDATE recipes SET title = ? WHERE id = ?", (title, r_id))

conn.commit()
cursor.execute("SELECT COUNT(*) FROM recipes")
print(f"Polished {len(titles_map)} titles. Total recipes in DB: {cursor.fetchone()[0]}")
conn.close()
