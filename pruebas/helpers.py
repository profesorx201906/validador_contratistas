import time
from playwright.sync_api import sync_playwright
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
def _primero(*c):
    for x in c:
        if x and os.path.exists(x): return x
    return c[0]
# La aplicación: junto a esta carpeta (entrega: pruebas/../index.html) o en ../dist (árbol de desarrollo). Se puede forzar con VC_INDEX.
APP_INDEX = os.path.abspath(os.environ.get('VC_INDEX') or _primero(os.path.join(AQUI, '..', 'index.html'), os.path.join(AQUI, '..', 'dist', 'index.html')))
APP_DIR = os.path.dirname(APP_INDEX)
URL = 'file://' + APP_INDEX
# PDF de muestra (NO se incluyen en la entrega: contienen datos personales). Colóquelos en pruebas/muestras/ o use VC_MUESTRAS.
MUESTRAS = os.path.abspath(os.environ.get('VC_MUESTRAS') or os.path.join(AQUI, 'muestras')) + os.sep
PDF = os.environ.get('VC_PDF_MUESTRA') or MUESTRAS + 'c3_16797358.pdf'   # 8_GF_16797358_5126_SEP_2026.pdf
PD = os.path.join(AQUI, 'pdfs') + os.sep                                  # PDF derivados (los crea make_pdfs.py)
DL = os.path.join(AQUI, 'dl') + os.sep; os.makedirs(DL, exist_ok=True)

def esperar(pg, expr, timeout=30, paso=0.25):
    """Sondea una expresión JS vía evaluate (compatible con la CSP de la página)."""
    t0=time.time(); ult=None
    while time.time()-t0 < timeout:
        try:
            ult = pg.evaluate(expr)
            if ult: return ult
        except Exception as e:
            ult = str(e)
        time.sleep(paso)
    raise TimeoutError('Tiempo agotado esperando: %s (último=%r)' % (expr, ult))

def abrir(p, url=URL, **kw):
    b = p.chromium.launch(**kw.pop('launch', {}))
    ctx = b.new_context(accept_downloads=True, **kw)
    pg = ctx.new_page()
    logs=[]; reqs=[]
    pg.on('console', lambda m: logs.append(m.type+': '+m.text))
    pg.on('pageerror', lambda e: logs.append('PAGEERROR '+str(e)))
    pg.on('request', lambda r: reqs.append(r.url))
    pg.goto(url)
    esperar(pg, '() => !!(window.VC && window.VC.listo === true)', 20)
    return b, ctx, pg, logs, reqs
