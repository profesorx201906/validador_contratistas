from helpers import *
with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    print('titulo:', pg.title()); print('modo almacenamiento:', pg.inner_text('#store-mode'))
    pg.click('#btn-pruebas')
    esperar(pg, "() => /PASS/.test((document.querySelector('#tests-sum')||{}).textContent||'')", 90)
    print(pg.inner_text('#tests-sum'))
    for r in pg.query_selector_all('.test-row'):
        t = r.inner_text().replace('\n',' | ')
        print(('  ' if 'PASS' == r.get_attribute('data-resultado') else '!!'), t[:220])
    print('--- logs'); print('\n'.join(logs[:30]))
    print('--- requests (no data/blob):', [u for u in reqs if not u.startswith(('data:','blob:'))])
    b.close()
