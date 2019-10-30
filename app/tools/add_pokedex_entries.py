import requests
import sqlite3
import json

# https://pokeapi.co/api/v2/pokemon-species/3/flavor_text_entries/
pokedb = sqlite3.connect('../app/data/pokedex.db')

def write_entry(no, text):
    pokedb.cursor().execute('update pkmn set pokedex_entry = ? where pokedex_entry is null and pokedex_no = ?', [text, no])
    print(f'Wrote {no}')

priority = ['alpha-sapphire', 'moon', 'sun']

rows = pokedb.cursor().execute('select pokedex_no from pkmn where pokedex_entry is null').fetchall()
for row in rows:
    no, = row
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{no}/')
    if not r.ok:
        print(f'Error for {r.url}: {r.status_code}')
        continue
    dex = r.json()
    entries = {}
    for entry in dex['flavor_text_entries']:
        if entry['language']['name'] == 'en':
            for n, ver in enumerate(priority):
                if entry['version']['name'] == ver:
                    entries[ver] = entry['flavor_text']
                    if n == 0:
                        break
    for ver in priority:
        if ver in entries:
            write_entry(no, entries[ver].replace('\n', ' '))
            break


pokedb.commit()
pokedb.close()
print('Done')